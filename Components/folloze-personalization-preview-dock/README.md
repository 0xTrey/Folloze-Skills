# Folloze Personalization Preview Dock

This package is the canonical reusable source for the fixed-bottom **View as** control used to demonstrate dynamic personalization on one Folloze board.

The dock is a board component, not a Folloze Content item. Put the generated markup, CSS, and runtime inside the board's custom HTML section. Articles, videos, and other viewer assets remain separate board Content items and can open through Folloze's native lightbox.

## Product boundary

The dock owns the control surface, two to six manual views, selected state, counter, collapse behavior, context signals, one-URL explanation, keyboard behavior, session selection, viewer scroll return, analytics call, and its change event.

The board owns every audience-specific headline, logo, image, CTA, section, Content item, claim, and source. It listens for `folloze:personalization-preview-change` and applies the matching board variant. The component also emits the original `audience-preview-change` event so existing implementations can migrate without a breaking update.

The event detail includes `key`, `label`, `signals`, `trigger`, `source: manual`, and `componentVersion`.

The component never reads cookies, IP addresses, company matching, 6sense, or visitor profiles. Every change comes from a visible manual selection.

## Package contract

- `component.json` records the component identity, semantic version, entry point, and public events.
- `src/config.schema.json` defines the portable configuration shape.
- `src/index.mjs` validates the view data and renders scoped markup, CSS, and inline runtime.
- `examples/four-view.config.mjs` is a fictional, tenant-free starting configuration.
- `examples/integration.mjs` shows the board-builder integration.
- `tests/personalization-preview-dock.test.mjs` protects the manual-only, accessibility, responsive, analytics, and viewer-return contract.

## Board integration

Use `renderPersonalizationPreviewDock` when the board builder already owns the final `<style>` and `<script>` tags. Use `renderPersonalizationPreviewFragment` when it needs one embeddable output. Pass a unique root class, an ordered view array, a default key, an analytics area, and the dock configuration. Do not load a runtime script or stylesheet from GitHub at page view time.

Each view requires:

- a stable lowercase key;
- a short visible label;
- a context label;
- a plain-language explanation of what changes;
- a list of active context signals.

The board runtime listens on the same scoped root:

```js
root.addEventListener('folloze:personalization-preview-change', event => {
  applyBoardVariant(event.detail.key);
});
```

Place the board listener in the same HTML fragment, immediately after the dock fragment. The component emits the resolved initial selection in a microtask, then emits every manual change, so the dock and the board content stay aligned after a viewer return or page reload.

Mark native viewer links or controls with `data-folloze-content-item`. The dock stores the current scroll position before the viewer changes route and restores it when the visitor returns to the board. A board can also dispatch `folloze:content-item-open` on the root. The prior `audience-preview-item-open` event remains supported for existing builds.

The board-specific adapter has one job: listen for the change event and update the page content. Keep that mapping next to the board content manifest, not inside this component. `examples/integration.mjs` shows both the fragment renderer and the event connection.

## Release workflow

1. Copy or import a pinned component version into the board build workspace.
2. Add a board-specific view configuration beside the board's content manifest.
3. Keep source-brand content outside this package.
4. Generate one self-contained Folloze HTML fragment.
5. Run `node --test tests/*.test.mjs` and render every view at desktop, 390 px, and 320 px.
6. Treat local QA, Folloze save/readback, publish, anonymous QA, and analytics delivery as separate receipts.

Increase the major version for event, configuration, or markup-contract changes. Increase the minor version for backward-compatible capabilities. Do not silently edit copied component code inside one board. Fix the canonical package, add a test, then intentionally update each board.

Move existing live experiences to this package in a separate board-update cycle so repository packaging, Folloze save, publish, and anonymous hosted QA remain distinct receipts.
