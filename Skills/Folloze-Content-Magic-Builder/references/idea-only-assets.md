# Idea-Only Assets

Use this reference when the input is a concept for a content item rather than the item itself: a topic, title, rough premise, or request such as "we want a guide on X" with no finished PDF, recording, deck, published URL, or accessible asset behind it. The asset does not exist or is not accessible at build time.

## Governing Principle

Follow the same rule that governs every other missing asset: never fabricate the thing itself or a destination for it.

- Do not invent statistics, quotes, findings, page counts, named sources, publish dates, download links, watch links, or embedded media.
- Do not present the experience as if it wraps a finished or published asset.
- The build must read as a genuine preview, not a counterfeit of a completed asset.

## Safe Fallback

1. Treat the idea as the approved content spine.
   The concept is the sanctioned scope and the only material to build from. Use it as the outline for the experience: section structure, key points, intended argument, and intended buyer value. Stay strictly inside it; do not add invented data or claims to make the idea look more complete.

2. Build an interactive summary, not a stand-in for the full asset.
   Produce a useful preview of what the finished item will deliver: an overview, core takeaways, a "what's inside" outline, and relevant CTAs. This preview is the deliverable. It should stand on its own as an engaging summary experience, not as a shell pretending the full asset is one click away.

3. Mark the final full-asset URL or file as explicitly pending.
   Any element that would point to the real guide, report, video, or asset must be rendered as a clear pending state. Use a disabled button or visibly non-live treatment such as `[Full asset pending - link to be added]`, plus an inline markup comment near the element. Never wire it to a guessed URL, a placeholder that looks live, or a broken or empty embed dressed up as working.

## Do Not

- Fabricate supporting numbers, named sources, or verbatim quotes for the asset.
- Imply a publish date, "available now" status, or completed-asset status.
- Insert a countdown or gated download against a file that does not exist yet.
- Use a fake, broken, guessed, or empty final-asset link.

## Before Publish

Before saving to a live board, surface a single summary stating that this is an idea-only build. List what was generated from the idea, what is still pending, including the full asset, its URL, and any real data, and require explicit user confirmation before saving.
