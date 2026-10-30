---
name: google-ai-router
description: Pick the right Google AI tool for a task and apply Google AI Plus quota rules. Use when the user wants to use Google AI from Claude — NotebookLM / Gemini Notebook (notebooks, sources, cited answers, Audio/Video Overview, slides, quizzes, mind maps), Gemini (web/Google search, deep research, audio/video understanding, cross-model review, bulk coding via agy), or Google Flow (Veo video, Nano Banana images) — or asks "which Google tool should I use", "hỏi NotebookLM", "dùng Gemini", "tạo video Flow".
---

# Google AI router

The user (anh Phong) is on **Google AI Plus**. Each Google service has a different cost profile on that plan, so route by task, not by habit.

## Routing

| Task | Tool | Where it works |
|---|---|---|
| Answer from the user's own documents with citations; synthesize many sources; generate Audio/Video Overview, slide deck, report, quiz, flashcards, mind map; download artifacts | **NotebookLM via `nlm`** (CLI or its MCP server). Follow the NotebookLM skill that `nlm skill install` set up; run `nlm --help` if no skill is loaded. | Claude Code, Claude Desktop, Cowork |
| Live web/Google search, deep research, transcribe/understand audio-video-images, second-model code review, bulk scaffolding/tests | **antigravity plugin** — `/antigravity:research`, `/antigravity:media`, `/antigravity:review`, `/antigravity:delegate` (bare `agy-delegate`) | Claude Code in WSL; Claude Code on Windows through `agy-wsl` (below) — not Cowork |
| Generate video (Veo) or images (Nano Banana) | **Google Flow in the browser** — skill `google-flow` | Anywhere with Claude in Chrome |

If the needed tool is missing (`nlm: command not found`, `agy` exit 13, no browser), say which tool and how to install it rather than substituting a different one silently.

## Gemini from Claude Code on Windows

The user wants Claude to stay the conductor in a normal Windows session and never run agy by hand. Headless `agy` hangs on native Windows, so this plugin ships `agy-wsl`, which runs the antigravity commands inside WSL (Ubuntu, fork checkout at `~/antigravity-for-claude-code`):

- `agy-wsl agy-doctor` — health check; run it first when agy has not been used this session.
- `agy-wsl agy-delegate [options] "prompt"` — same options, tiers, exit codes and `AGY_USAGE` / `AGY_SIGNAL` stderr lines as `agy-delegate` in the antigravity plugin; its `commands/*.md` say when and how to delegate.
- `agy-wsl agy-media <file> ...`, `agy-wsl agy-job ...` — as their WSL counterparts.

Rules on Windows:

- **Send content through stdin**, e.g. `cat report.md | agy-wsl agy-delegate --tier flash --digest -`, and say "do not use any tools" when the answer is in the prompt. Gemini Flash headless otherwise tries to run commands and gets `PERMISSION_DENIED`, and `--dir` with a `/mnt/d/...` path is slow.
- Windows paths mean nothing inside WSL: convert with `wsl.exe -d Ubuntu wslpath -a 'D:\path'` only when agy itself must open the file (e.g. `agy-media`).
- Web search and URL reads need `--yolo`, which grants agy full access inside WSL. Use it only for read-only research prompts; never with a prompt that asks agy to change files.
- Translate the stderr signals for the user in plain words (quota spent, needs `agy` login in WSL, timeout) rather than pasting them.

## Google AI Plus limits

- **agy:** limited, weekly refresh, no top-up. Delegate only above the break-even; default tier `flash`. Exit 10 (`QUOTA_EXHAUSTED`) → do the work on Claude and tell the user the weekly agy quota is spent; don't retry in a loop.
- **Flow:** ~200 credits/month. Before every generation, state the model and expected credit cost and wait for the user's yes.
- **NotebookLM:** the most generous of the three → prefer it for reading and summarizing documents over spending agy quota.

## Ask first

Uploading company/internal documents to NotebookLM, making a notebook public or sharing it, spending Flow credits, and publishing anything generated — each needs the user's explicit confirmation. Sign-in (`nlm login`, `agy` first run, Google login in the browser) is always done by the user.

## Verify

Gemini and NotebookLM output is a claim: check load-bearing numbers, names and quotes against the cited source before presenting them as fact, and say which parts were checked.
