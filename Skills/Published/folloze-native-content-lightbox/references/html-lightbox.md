# HTML-section lightbox wiring

Folloze's [item-sharing guide](https://help.folloze.com/s/article/Sharing-Content-Items) describes the board Content-tab share link and default lightbox viewer. The [Visibility guide](https://help.folloze.com/s/article/The-Visibility-Tab) identifies the URL item's new-tab setting. Check both on the **target board** before relying on the lightbox. Folloze may show a processed page snapshot, a file viewer, or a source-site player; do not promise that a raw source page will render in an iframe.

## Map the CTA

- Copy the actual item link from the board's Content section after item readback. The source URL in `url_item.url` is **not** the CTA destination.
- In a uniquely scoped HTML fragment, make the resource action a `button type="button"` or a same-tab link. Set its verified Folloze item link as data, call `window.location.assign(itemUrl)`, and do not set `target="_blank"` or `window.open`.
- Keep contact/demo CTAs pointed to their real destination. Only content-resource CTAs should become item-viewer actions.
- Set the board's viewer to Lightbox where that configuration is exposed and keep URL items' `open_in_new_tab` off. Saving HTML alone does not set viewer configuration.
- If the board uses a query-parameter item route or a custom hosting page instead of a `/items/...` path, adapt the route check before using the asset. Do not guess route shapes; copy and test a real target-board item link. The [Website Engager guide](https://help.folloze.com/s/article/Folloze-Website-Engager-Embedding-a-Folloze-Board-on-a-Webpage) documents its own item-link route options.

The [portable HTML fragment](../assets/native-content-cta.fragment.html) has one example tile, a scoped listener that supports more tiles, and one-time scroll return. Replace its `data-board-url` and each `data-item-url` with verified links. Its placeholders deliberately fail closed. Merge it into the existing section rather than nesting a full HTML document. No credential belongs in the fragment.

## Scroll return

Before same-tab item navigation, store the current document offset in tab-scoped `sessionStorage`, keyed by board origin and path. When the viewer closes, restore the offset and clear the key. Folloze can change the route without re-running embedded JavaScript or firing `popstate`, so the example also watches a route change while the section remains mounted. It skips restoration while on an item route and clamps the offset to the current page height. This is local UI state, not identity resolution or tracking.

Test a full hosted round trip at a resource well below the hero. Record before/after position and the selected audience or widget state if the page has one. A local HTML preview or an API `202` cannot establish that Folloze opened its native viewer. If the source is gated, opens a new tab, renders incorrectly, or reloads at the top, diagnose that specific board/item path before release.

For analytics, a scoped CTA can optionally call `flzAnalytic('folloze_content_item_opened', {text, destination}, launcher)` when available. Treat the event call, Folloze analytics readback, and downstream delivery as different receipts.
