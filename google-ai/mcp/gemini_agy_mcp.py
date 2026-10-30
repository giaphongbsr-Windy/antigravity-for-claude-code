"""gemini-agy — a stdio MCP server that lets Claude Desktop / Cowork on Windows ask Gemini.

Cowork runs in an isolated VM and cannot reach WSL, but MCP servers declared in
claude_desktop_config.json run on the Windows host. This server forwards each call to
the antigravity plugin's agy-delegate inside WSL (headless agy hangs on native Windows),
so tiers, exit codes and AGY_USAGE / AGY_SIGNAL lines behave as in Claude Code.

Standard library only, so it needs no pip install. Register it as:
  "gemini-agy": {"command": "C:\\Python314\\python.exe",
                 "args": ["\\\\wsl.localhost\\Ubuntu\\home\\phongdg\\antigravity-for-claude-code\\google-ai\\mcp\\gemini_agy_mcp.py"]}
Env overrides: AGY_WSL_DISTRO (default Ubuntu), AGY_WSL_REPO (default ~/antigravity-for-claude-code).
"""

import json
import os
import subprocess
import sys

SERVER = {"name": "gemini-agy", "version": "0.3.0"}
DISTRO = os.environ.get("AGY_WSL_DISTRO", "Ubuntu")
REPO = os.environ.get("AGY_WSL_REPO", "~/antigravity-for-claude-code")

# Arguments arrive in WSL as positional parameters, never spliced into the script text.
# --exec skips WSL's own shell; -i puts ~/.local/bin (agy) on PATH.
WSL_SCRIPT = 'repo=$1; cmd=$2; shift 2; cd ~ && exec "${repo/#\\~/$HOME}/bin/$cmd" "$@"'

EXIT_MEANING = {
    1: "usage error in the call",
    2: "agy failed",
    3: "Gemini returned an empty answer",
    10: "the weekly agy quota of Google AI Plus is spent; do the work without Gemini and tell the user",
    11: "agy is not signed in; the user must run `agy` once inside WSL to log in",
    12: "timed out; output above may be partial; retry with a larger timeout_minutes or a narrower prompt",
    13: "agy is not installed in WSL",
    14: "the model for this tier is not available on the user's plan",
    15: "Gemini asked for a tool permission it was not given; put the content in the prompt, or set web_search for research",
}

NO_TOOLS = ("\n\n(Answer only from the content in this prompt. Do not run commands, "
            "read files or use any other tool.)")

TOOLS = [
    {
        "name": "gemini_ask",
        "description": (
            "Ask Google Gemini (via the user's Google AI Plus agy quota, which is limited and weekly). "
            "Use for a second opinion from another model, Google/web search research, or bulky reading "
            "you want summarised outside Claude's context. Put all needed content IN the prompt: Gemini "
            "cannot see the user's files. Prefer NotebookLM for questions about the user's own documents. "
            "Gemini output is a claim: verify load-bearing facts before presenting them."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The full task, including any text Gemini needs."},
                "tier": {"type": "string", "enum": ["flash", "flash-lo", "pro"], "default": "flash",
                         "description": "flash = default; flash-lo = trivial tasks; pro = hardest only."},
                "web_search": {"type": "boolean", "default": False,
                               "description": "Allow Google search and URL reads. Grants Gemini full tool access "
                                              "inside WSL, so use only for read-only research prompts."},
                "digest": {"type": "boolean", "default": False,
                           "description": "Ask for a compact digest instead of a long answer."},
                "timeout_minutes": {"type": "integer", "minimum": 1, "maximum": 20, "default": 9},
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "gemini_doctor",
        "description": "Check that WSL, agy and its Google sign-in are ready. Run when gemini_ask fails.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def run_wsl(cmd, args, stdin_text, timeout_s):
    argv = ["wsl.exe", "-d", DISTRO, "--exec", "bash", "-lic", WSL_SCRIPT, "gemini-agy", REPO, cmd] + args
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        p = subprocess.run(argv, input=(stdin_text or "").encode("utf-8"), capture_output=True,
                           timeout=timeout_s, creationflags=flags)
    except subprocess.TimeoutExpired:
        return 12, "", "gemini-agy: WSL call did not return in time"
    except FileNotFoundError:
        return 13, "", "gemini-agy: wsl.exe not found"
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def summarise(rc, out, err):
    lines = [l for l in err.splitlines() if l.strip()]
    signals = [l for l in lines if l.startswith(("AGY_USAGE", "AGY_SIGNAL"))]
    # bash -i without a terminal prints job-control noise; keep only the wrapper's own lines.
    noise = ("bash: cannot set terminal process group", "bash: no job control")
    other = [l for l in lines if l not in signals and not l.startswith(noise)]
    parts = [out.strip() or "(no output)"]
    if rc != 0:
        parts.append("\n[exit %d: %s]" % (rc, EXIT_MEANING.get(rc, "unexpected error")))
        parts.extend(other[-8:])
    parts.extend(signals)
    return "\n".join(parts)


def call_tool(name, a):
    if name == "gemini_doctor":
        rc, out, err = run_wsl("agy-doctor", [], "", 180)
        return summarise(rc, out, err), rc != 0
    if name != "gemini_ask":
        raise ValueError("unknown tool: %s" % name)
    prompt = (a.get("prompt") or "").strip()
    if not prompt:
        return "prompt is empty", True
    tier = a.get("tier") or "flash"
    if tier not in ("flash", "flash-lo", "pro"):
        return "tier must be flash, flash-lo or pro", True
    minutes = max(1, min(20, int(a.get("timeout_minutes") or 9)))
    args = ["--tier", tier, "--timeout", "%dm" % minutes]
    if a.get("digest"):
        args.append("--digest")
    if a.get("web_search"):
        args.append("--yolo")
    else:
        prompt += NO_TOOLS
    rc, out, err = run_wsl("agy-delegate", args + ["-"], prompt, minutes * 60 + 90)
    return summarise(rc, out, err), rc != 0


def send(msg):
    sys.stdout.buffer.write((json.dumps(msg, ensure_ascii=False) + "\n").encode("utf-8"))
    sys.stdout.buffer.flush()


def handle(req):
    method, rid = req.get("method"), req.get("id")
    if rid is None:  # notification (e.g. notifications/initialized)
        return
    if method == "initialize":
        version = (req.get("params") or {}).get("protocolVersion", "2025-06-18")
        result = {"protocolVersion": version, "capabilities": {"tools": {}}, "serverInfo": SERVER}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        p = req.get("params") or {}
        try:
            text, is_error = call_tool(p.get("name"), p.get("arguments") or {})
        except Exception as e:  # report to the model instead of killing the server
            text, is_error = "gemini-agy error: %s" % e, True
        result = {"content": [{"type": "text", "text": text}], "isError": is_error}
    else:
        send({"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "method not found: %s" % method}})
        return
    send({"jsonrpc": "2.0", "id": rid, "result": result})


def main():
    for raw in sys.stdin.buffer:
        raw = raw.strip()
        if not raw:
            continue
        try:
            req = json.loads(raw.decode("utf-8"))
        except ValueError:
            send({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}})
            continue
        handle(req)


if __name__ == "__main__":
    main()
