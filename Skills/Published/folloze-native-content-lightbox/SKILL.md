---
name: folloze-native-content-lightbox
description: Prepare or reuse Folloze Content items and connect board HTML-section CTAs to the native item lightbox, including optional scroll return. Use for internal Content API and HTML launcher work, not generic external iframes or visitor-resolution rules.
---

# Folloze native Content lightbox

Use this skill to make a custom HTML section launch an item that is already attached to the same Folloze board. The HTML points to the **Folloze item link**, not the original article or video URL. Folloze owns the viewer. The Content API only ingests or updates Content items; it does not publish the HTML section or configure the board's viewer.

## Work boundary

- Resolve the exact tenant, board, creator, and permitted items before a write. Do not reuse a key, host, board ID, or item route from another environment.
- Keep the Content API credential in a server-side secret store or one-time hidden input. Never put it in the skill, HTML, browser JavaScript, URL, Git, command argument, log, or handoff package.
- Prefer an existing board Content item when its source, visibility, and viewer behavior match. An API POST can create a duplicate. A `202` is asynchronous acceptance, not a live item receipt.
- Treat Content ingestion, HTML save/readback, board publish, and hosted viewer QA as separate outcomes. This skill grants no new permission to create items or publish a board.

## Apply the workflow

1. Inspect the target board's Content section and viewer settings. Record the source URL, board item ID, Content Center ID if available, status, gating, new-tab setting, and copied item link. Reuse the item if it is already suitable.
2. If an item is missing and creation is authorized, read [Content API ingestion](references/content-api.md). Build the target-tenant request, send it from a trusted backend, then reconcile and read back the item before another POST or HTML change.
3. Read [HTML lightbox wiring](references/html-lightbox.md). Adapt [the scoped HTML fragment](assets/native-content-cta.fragment.html) or the existing section's code. Use a verified same-board item link and same-tab navigation. The fragment has no API credential.
4. Save the complete HTML fragment to the intended section and read it back. Publish only when the current task authorizes a live release. Test the hosted board by opening the item, checking what Folloze actually renders, closing it, and confirming audience state and page position where relevant.

Dev can run `node --test tests/lightbox-runtime.test.mjs` from this skill folder to check the example's same-board launch and route-based scroll return before adapting it.

Stop on an unknown API outcome, a tenant or board mismatch, a missing item readback, or a viewer that opens a new tab instead of the intended lightbox. Do not automatically retry create, invent an item slug, change unrelated board settings, or substitute an iframe without a separate product decision.
