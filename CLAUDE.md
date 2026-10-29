# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is a personal fork (`giaphongbsr-Windy/antigravity-for-claude-code`) of the `antigravity` Claude Code plugin (upstream `yuting0624/antigravity-for-claude-code`). The plugin lets Claude delegate work to the Antigravity CLI (`agy`, Gemini). The fork adds a second plugin, `google-ai/`, plus `.claude/rules/` for the owner's Google AI setup (NotebookLM, Flow). Fork-specific rules live in `.claude/rules/` — read them before changing anything.

## Commands

Run everything from WSL (see `.claude/rules/wsl.md`); the repo lives at `~/antigravity-for-claude-code`.

```bash
bash tests/run-tests.sh                                   # whole suite; stubs agy, no network
shellcheck --severity=error scripts/*.sh tests/*.sh hooks/*.sh   # CI gate (warnings are advisory)
python3 -m py_compile scripts/measure-session.py
python3 -c "import json; [json.load(open(p)) for p in ('.claude-plugin/plugin.json','.claude-plugin/marketplace.json','prices.json','hooks/hooks.json','hooks/policy-context.json','google-ai/.claude-plugin/plugin.json')]"
claude --plugin-dir ~/antigravity-for-claude-code          # load the plugin live from the working tree
scripts/agy-delegate.sh --tier flash "..."                 # call the wrapper directly
scripts/doctor.sh                                          # agy install/auth/platform diagnosis (= agy-doctor)
```

`tests/run-tests.sh` is one large bash file with no single-test runner; to iterate on one area, run it and `grep` the `ok:`/`FAIL:` lines. The `tests/check-*.py` files are standalone checks the suite also calls (CHANGELOG placement, embedded-python quoting, helper order, sandbox claims).

Known baseline on this machine (WSL, bash 5.3, before any fork change): 422 pass, 2 fail — "byte cap clips a multibyte payload too" and "--background with only '-' finished with rc 0". Treat those as pre-existing, not regressions.

## Architecture

- **`bin/` → `scripts/`.** Every `bin/<name>` is a 1-line shim that `exec`s `scripts/<name>.sh`. Shims exist because `$CLAUDE_PLUGIN_ROOT` is not exported to model-run Bash, so commands and skills call bare names (`agy-delegate`, `agy-job`, `agy-handoff`, `agy-media`, `agy-doctor`, `agy-trace`, …) that resolve via the plugin's `bin/` on PATH. Never write `$CLAUDE_PLUGIN_ROOT/scripts/...` in a command or skill.
- **`scripts/agy-delegate.sh` is the core.** Everything else (`agy-job` background jobs, `agy-handoff`, `agy-media`, `cloud-debug`, the slash commands) goes through it. It maps `--tier flash|flash-lo|pro` to an exact `--model`, runs `agy -p` with stdout to a temp file (MCP children hold pipes open — issue #37) under a wall-clock `timeout`, parses `--output-format json` when available, and reports via stderr: `AGY_USAGE {...}` on success, `AGY_SIGNAL {...}` on classified failure. Exit codes: 0 ok · 1 usage · 2 agy failed · 3 empty · 10 quota · 11 auth · 12 timeout (incl. partial reply) · 13 agy missing · 14 model unavailable · 15 permission denied. The authoritative list is the `# Exit codes:` header in that script.
- **Plugin options.** `userConfig` in `.claude-plugin/plugin.json` reaches hooks as `CLAUDE_PLUGIN_OPTION_*`, but NOT Bash subshells; `scripts/lib/plugin-options.sh` re-reads them from `~/.claude/settings.json` → `pluginConfigs["antigravity@…"].options`. Explicit env vars win. Adding an option means touching both `plugin.json` and whatever script consumes it.
- **Policy lives in prose.** `skills/antigravity/SKILL.md` is the plugin's "brain" (when/how to delegate, tiers, guardrails); `hooks/policy-context.json` is the condensed version injected by the `SessionStart` hook (`hooks/inject-policy.sh`, toggle `coding_policy`). `hooks/nudge-delegation.sh` (`UserPromptSubmit`) adds an advisory note for bulk-looking prompts. If behaviour changes, update the skill — don't claim capabilities the code lacks.
- **`agents/antigravity-delegate.md`** has only Bash/Read/Glob and a `PreToolUse` hook (`hooks/validate-delegate-bash.sh`) that denies every Bash command except the bare wrapper names, so file writing happens on Gemini. Changing what the agent may run means changing that validator and its gate tests.
- **`commands/*.md`** are the `/antigravity:*` slash commands; they are prompt instructions that call the bin names.
- **`google-ai/`** (fork only) is a separate plugin in the same marketplace: routing between `agy`, the NotebookLM CLI `nlm`, and Google Flow via browser automation. It has no scripts; it depends on `nlm` installed separately.

## Constraints that CI or the suite enforce

- **Bash 3.2 + BSD userland** (macOS CI job runs `/bin/bash` 3.2): no `declare -A`, `mapfile`/`readarray`, `${v^^}`, or GNU-only `sed`/`date`/`grep` flags. Style: `set -euo pipefail`, quoted expansions, new scripts get `usage()` and a test in `tests/run-tests.sh`.
- No single quotes/apostrophes inside single-quoted `python3 -c '…'` blocks (`tests/check-embedded-python.py`).
- `version` in `skills/antigravity/SKILL.md` frontmatter must equal `.claude-plugin/plugin.json`.
- `CHANGELOG.md` has no "Unreleased" section; a new line goes under a new `## x.y.z` heading (or the newest heading if its version is ahead of the base `plugin.json`). On PRs the suite fails a line added under an already-shipped section.
- Cost figures are estimates from `prices.json`; say so whenever quoting one.
- Treat agy output as a claim to verify, never as proof. `--yolo` grants every tool on the whole machine (not just `--dir`); `--sandbox` does not contain it.
