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
| Live web/Google search, deep research, transcribe/understand audio-video-images, second-model code review, bulk scaffolding/tests | **antigravity plugin** — `/antigravity:research`, `/antigravity:media`, `/antigravity:review`, `/antigravity:delegate` (bare `agy-delegate`) | Claude Code in WSL only — not Cowork |
| Generate video (Veo) or images (Nano Banana) | **Google Flow in the browser** — skill `google-flow` | Anywhere with Claude in Chrome |

If the needed tool is missing (`nlm: command not found`, `agy` exit 13, no browser), say which tool and how to install it rather than substituting a different one silently.

## Google AI Plus limits

- **agy:** limited, weekly refresh, no top-up. Delegate only above the break-even; default tier `flash`. Exit 10 (`QUOTA_EXHAUSTED`) → do the work on Claude and tell the user the weekly agy quota is spent; don't retry in a loop.
- **Flow:** ~200 credits/month. Before every generation, state the model and expected credit cost and wait for the user's yes.
- **NotebookLM:** the most generous of the three → prefer it for reading and summarizing documents over spending agy quota.

## Ask first

Uploading company/internal documents to NotebookLM, making a notebook public or sharing it, spending Flow credits, and publishing anything generated — each needs the user's explicit confirmation. Sign-in (`nlm login`, `agy` first run, Google login in the browser) is always done by the user.

## Verify

Gemini and NotebookLM output is a claim: check load-bearing numbers, names and quotes against the cited source before presenting them as fact, and say which parts were checked.
