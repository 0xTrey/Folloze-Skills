---
name: Folloze-Content-Magic-Builder
description: Turn a customer-provided content item or approved content concept into an interactive Folloze experience. Use when the user uploads or links a whitepaper, report, ebook, webinar, blog post, deck, video, checklist, guide, or similar asset, or when they provide an idea for one, and wants it transformed into an interactive buyer journey instead of a static download.
---

# Folloze Content Magic Builder

Use this skill to transform one approved content item into an interactive Folloze-ready experience that helps a buyer explore the idea, self-select a path, and take the next action.

## Fit

Use this when the content item is the center of the page. If the user is asking for a broad campaign page, use `Folloze-Top-Of-Funnel-Campaign-Landing-Page`. If the asset is being tailored to one named account, combine this workflow with `Folloze-One-To-One-Microsite-Builder`.

## Minimum Inputs

Gather only what is missing:

- The source content item: file, URL, pasted text, transcript, deck, video, approved summary, or approved idea-only concept.
- Target audience.
- Desired conversion action.
- Source brand or design direction.
- Whether the full asset should stay gated, ungated, summarized, pending, or used as supporting material.

## Source And Rights Boundaries

- Use only user-provided, public, or approved content.
- Do not reproduce long third-party copyrighted text from an external source. Summarize, excerpt briefly, and link to the source when needed.
- Preserve compliance-sensitive claims exactly only when they are in the approved source. If a claim is unclear, label it for review.
- Keep internal content, notes, or unpublished materials out of buyer-facing copy unless explicitly approved.
- If the input is only a concept for an asset that does not yet exist or cannot be accessed, read `references/idea-only-assets.md` before outlining, writing, linking, or saving.

## Workflow

1. Extract the asset spine: core promise, audience pain, key ideas, proof points, recommended action, and useful visuals.
2. Decide the interactive shape: guided summary, chapter path, assessment, calculator, quiz, checklist, resource hub, video companion, or role-based explorer.
3. Build a page outline that lets the buyer get value before downloading or requesting a meeting.
4. Create one self-contained local HTML file in the active repo.
5. Include real interactions: tabs, accordions, filters, progress path, quiz, checklist, modal, embedded media, resource cards, or CTA anchors.
6. Link to or embed the original asset according to the approved gating/share model. For idea-only assets, render final-asset links as explicitly pending.
7. QA desktop/mobile, interaction behavior, source fidelity, and content-rights boundaries.

## Page Standards

- The page should not look like a wrapper around a PDF. It should turn the asset into a usable journey.
- Lead with the buyer problem and useful takeaway, not the asset title alone.
- Break long content into scan-friendly modules and paths.
- Every interactive element should teach, qualify, route, or advance the buyer.
- Use the source asset's diagrams, concepts, or sections only when they are approved and render well.

## QA Gates

Before final response or publish:

- The source asset is identified and approved for the intended use.
- Long text has been transformed into original summaries or short compliant excerpts.
- Interactions work and are not decorative.
- CTA and original asset access path are clear.
- For idea-only assets, the final response clearly states this is an idea-only build, separates generated preview content from pending full-asset items, and gets explicit confirmation before saving to a live board.
- Mobile reading and interaction states are clean.
- If saved through Folloze MCP, use the available Folloze MCP publishing tools and current Folloze guide. Report local source path, board ID, returned edit URL, and public URL status separately.

## Final Response

Return the local file path, source asset used, interactive shape, CTA, content-rights caveats, QA status, and Folloze save/publish status.
