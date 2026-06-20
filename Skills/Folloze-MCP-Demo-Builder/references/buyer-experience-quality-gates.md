# Buyer Experience Quality Gates

Run these gates before local preview and again before saving through Folloze MCP. Fix failures before save unless the user explicitly accepts the caveat.

## Brand And Copy

- The first viewport clearly shows the vendor and, for 1:1 pages, the target-account context when public evidence supports it.
- For cross-sell, upsell, decision-stage, or existing-customer pages, the first viewport and first proof section make the expansion thesis clear: what the customer already proved, what should scale next, and why that matters now.
- Buyer-facing copy avoids internal production terms, including demo, example, proof of concept, microsite, board, template, conversation assets, first meeting, fit, stack, pilot, scorecard, and technical architecture unless the user explicitly asked for them.
- Buyer-facing copy also avoids internal section scaffolding such as existing customer proof, expansion workbench, proof for the expansion case, stakeholder mapping, decision team, resources, evaluation hub, or demo example unless those phrases are explicitly buyer-facing in the source brand.
- The page has one holistic buyer goal, and every visible sentence supports that goal as a decision path, proof point, role-specific value, or useful next action.
- No buyer-facing copy explains why the page, section, resource, or card was created, selected, arranged, or included. Replace demo-explainer copy with buyer outcomes or remove it.
- Major section subheads and subheaders are absent by default. If the user explicitly requests one or the source brand requires one, it must be buyer-facing proof, decision, or action copy, not a section description.
- Leadership, persona, team-value, or "leaders" sections describe selection support for each role: what they need to evaluate, what proof they get, what risk is reduced, and how the vendor helps them move forward.
- All claims come from public vendor messaging, public target-account evidence, user-approved copy, or clearly labeled planning assumptions.
- No invented metrics, logos, customer names, awards, analyst quotes, case studies, or testimonials.
- Private notes shape strategy only; they are not quoted or paraphrased into visible buyer-facing claims.
- Every major section adds a new reason to believe, decision input, proof point, or useful next action. Delete sections that only explain the page's purpose or repeat the same claim in different words.

## Structure

- The page does not default to generic hero, three equal feature cards, final CTA, and footer unless the source brand clearly uses that rhythm.
- No UI cards inside other cards.
- No page sections styled as floating cards unless they are genuine repeated cards, modals, or framed tools.
- No fake browser chrome, fake phone frames, fake IDE frames, or decorative UI shells.
- Hero, proof rows, calculators, and section transitions are not clipped at common desktop or mobile viewport heights.
- Situation/Solution content stays compact and scannable.
- Major ABM narrative sections use full-rail headlines when the headline carries the argument. Decorative eyebrows, category labels, and right-side subheads are removed when they only expose internal page structure.
- Major narrative headers are headline-led. If the header needs a subhead to make sense, rewrite the headline or the next component instead of adding explanatory text.

## Controls And Analytics

- Every visible button, nav item, card CTA, arrow, resource action, "Read more" control, tab, slider, modal opener, and calculator control does real work.
- No `href="#"`, placeholder URL, `javascript:void(0)`, or dead decorative arrow remains.
- Folloze-hosted in-page section navigation does not use raw hash links such as `href="#workflow"`. Use `<button type="button" data-scroll-target="section-id">`, stable target IDs, `scroll-margin-top`, `scrollIntoView()`, and `anchor_click` analytics so the hosted shell does not route visitors to content unavailable.
- Every external URL is real, source-owned or vendor-owned when possible, and uses `target="_blank" rel="noopener"`.
- Primary CTAs and resource CTAs call `flzAnalytic('cta_click', ...)` with useful `text`, `area`, and `url`.
- Meaningful interactions call descriptive analytics events with useful payloads: modal opens/closes, tab changes, scenario selectors, FAQ expands, anchor clicks, sliders, calculators, and model updates.
- MCP analytics acknowledgements stay false until the actual saved HTML satisfies the guide.

## Mobile And Accessibility

- Render at desktop and at mobile widths near 320, 375, 414, and 768 px when tooling allows.
- `document.documentElement.scrollWidth <= window.innerWidth` on mobile.
- `html` and `body` use horizontal clipping when needed to prevent overflow without breaking sticky positioning.
- Button, tab, nav, footer, breadcrumb, and CTA labels do not wrap to two lines.
- Display headings have `min-width: 0` and long-word wrapping where needed.
- Dark sections explicitly set readable light text colors; light sections explicitly set readable dark text colors.
- Button text, focus rings, muted text, card text, and dark-section text pass practical contrast checks.
- Focus-visible, hover, active, disabled, and reduced-motion states exist for interactive controls where applicable.

## Tokens, Motion, And CSS

- Brand colors, neutrals, accents, fonts, radius, shadows, and spacing are centralized as named tokens or clearly grouped custom properties.
- The typography map matches the vendor source or user-provided screenshot: computed font family, heading/body weights, line height, and letter spacing are checked on hero H1, section H2s, nav, buttons, and body copy.
- Avoid one-off color and font improvisation outside the token block unless the value is a verified source-brand asset requirement.
- No `transition: all`; transition only the properties that change.
- Animate transform and opacity where possible, not layout properties such as width, height, top, left, margin, or padding.
- Every keyframe or non-trivial motion has a `prefers-reduced-motion` fallback.
- Accent color is used for emphasis, not large decorative floods, unless the source brand clearly uses that treatment.

## Assets And Proof

- Every referenced logo, image, SVG, and carousel asset loads in local preview.
- Logo assets are source-owned when possible; generic image search is a fallback only when the source site lacks usable assets.
- Logo carousels duplicate content only for animation continuity, not to imply additional customers.
- Auto-moving content pauses on hover/focus or is slow enough not to distract.
- Official SVGs are inspected before use; do not rely on misleading filenames such as `logo-white.svg`.
- Vendor and target-account logos render as clean official marks without boxes, pills, borders, or card containers unless the source brand uses that treatment.
- Public case studies for the exact target account are treated as proof assets: links, embeds, or redirects are verified, CTA labels match the real action, and the proof appears where it strengthens the expansion argument.

## Save Readiness

- The current Folloze landing-page creation guide has been read for this save.
- The chosen theme mode has been authorized by the user or established by prior same-board context.
- The required theme stylesheet link is present exactly as the guide requires.
- The local HTML file is the source of truth when one exists.
- Existing board ID is preserved for updates unless the user explicitly asked for a new board.
- Save only after local preview/review mode is complete and the user has asked to save, publish, update, or push to Folloze.
- When the user provides a specific sheet URL, that sheet is inspected and used for the requested logging task instead of the default tracker unless the user asks for both.
- The holistic buyer-goal pass has removed subheaders and demo-explainer leftovers, and leadership/persona value sections are role-specific selection support rather than internal mapping.
