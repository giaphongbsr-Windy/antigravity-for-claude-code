---
name: google-flow
description: Generate video (Veo) or images (Nano Banana) in Google Flow through browser automation, on a limited Google AI Plus credit budget. Use when the user asks to create, regenerate, or download a Flow video/image or scene. For the full render → export → concat → QA pipeline, also use the google-flow-video-production-qa skill if it is available.
---

# Google Flow (browser, credit-limited)

Flow has no public API; this drives the Flow web app (`https://flow.google.com`) with Claude in Chrome in the user's own signed-in browser. Credits are limited, so every generation is a spending decision. Measured 2026-11-04: balance 250, shown in the account avatar menu with its reset date (22 Nov).

## Credit gate — before each generation

**The gate is your question to the user, and it comes before you click Start generation.** Flow is not the gate: on 2026-11-04, with Agent settings → Confirm before generating on **Always**, a Nano Banana 2 Lite image generated straight away with no approval card. It cost 0 credits, which may be why no card showed; whether paid models show one is unverified.

1. Read the balance from the avatar menu.
2. Tell the user: model, number of outputs, expected cost, balance after. If the cost is unknown, say "cost unknown" and do not guess. Wait for an explicit yes.
3. Only then send the prompt. If an approval card appears, click **Approve** — never **Always approve** — and only if its cost matches what the user agreed; otherwise stop and ask.
4. Keep Confirm before generating on **Always**; never switch it to Never.
5. Prefer a cheap test first: Nano Banana 2 Lite at x1 in Agent settings (the `Settings` button in the composer; Save afterwards), or the lowest-cost video model, before a full-quality video.
6. Re-read the balance afterwards and log the real spend (date, scene, model, credits) in the project's log file, so the budget is trackable.

## Automation rules that are known to matter

These come from the user's production playbook (`google-flow-video-production-qa`); when that skill is available, read it for the details and code. Flow's UI has since moved to an agent chat panel (a new project opens a "What's new" dialog first; dismiss **Get started**), and only the composer and `Start generation` steps were re-checked on 2026-11-04, so confirm the others against the live page.

- Select elements by `aria-label`/text and call `.click()` via JS; do not click by screenshot coordinates on the Flow page (scaled coordinates miss).
- Fill the prompt with `execCommand('insertText')` on the `[contenteditable].ProseMirror` composer, wait ~1s, then click `button[aria-label="Start generation"]`.
- Old approval cards stay in the DOM — approve only the one inside the viewport.
- Regenerate a scene with that tile's **Reuse prompt** button and compare the prefilled prompt to the source prompt before submitting.
- Download with `aria-label="Download scene"` (not the `Download` menu button), one scene at a time, confirming the new file in Downloads before the next.
- The Storyboard Studio iframe cannot be driven; ask the user to do those steps.
- Quality checks (audio present, frames correct) are done on the downloaded file with ffprobe/ffmpeg, never by watching the in-browser player.

## Never

Upload or publish to YouTube or any public platform — stop and hand that click to the user.
