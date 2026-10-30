---
name: google-flow
description: Generate video (Veo) or images (Nano Banana) in Google Flow through browser automation, on a Google AI Plus credit budget (~200 credits/month). Use when the user asks to create, regenerate, or download a Flow video/image or scene. For the full render → export → concat → QA pipeline, also use the google-flow-video-production-qa skill if it is available.
---

# Google Flow (browser, credit-limited)

Flow has no public API; this drives the Flow web app with Claude in Chrome in the user's own signed-in browser. Google AI Plus gives roughly **200 Flow credits per month**, so every generation is a spending decision.

## Credit gate — before each generation

1. Read the current credit balance shown in Flow (if visible) and the cost Flow's approval card shows.
2. Tell the user: model, number of outputs, expected credit cost, balance after. Wait for an explicit yes.
3. On approval click **Approve** — never **Always approve**.
4. Prefer a cheap test first: an image or the lowest-cost video model to validate the prompt before a full-quality video.
5. Log each spend (date, scene, model, credits) in the project's log file so the monthly budget is trackable.

## Automation rules that are known to matter

These come from the user's production playbook (`google-flow-video-production-qa`); when that skill is available, read it for the details and code.

- Select elements by `aria-label`/text and call `.click()` via JS; do not click by screenshot coordinates on the Flow page (scaled coordinates miss).
- Fill the prompt with `execCommand('insertText')` on the `[contenteditable].ProseMirror` composer, wait ~1s, then click `button[aria-label="Start generation"]`.
- Old approval cards stay in the DOM — approve only the one inside the viewport.
- Regenerate a scene with that tile's **Reuse prompt** button and compare the prefilled prompt to the source prompt before submitting.
- Download with `aria-label="Download scene"` (not the `Download` menu button), one scene at a time, confirming the new file in Downloads before the next.
- The Storyboard Studio iframe cannot be driven; ask the user to do those steps.
- Quality checks (audio present, frames correct) are done on the downloaded file with ffprobe/ffmpeg, never by watching the in-browser player.

## Never

Upload or publish to YouTube or any public platform — stop and hand that click to the user.
