# QA And Publish Gates

Run these gates after the local HTML build and before publish.

Run `design-quality-gates.md` as part of QA. The page must pass both functional QA and design-quality QA before publish or handoff.

Fix failures before publish unless the marketer explicitly accepts the caveat.

## Render And Layout

- The page opens locally in a browser.
- There are no obvious console errors.
- Desktop layout is readable.
- Mobile layout is readable around 320, 375, 414, and 768 px when tooling allows.
- `document.documentElement.scrollWidth <= window.innerWidth` on mobile.
- No text overlaps other UI.
- No section, card, modal, hero, or proof row is clipped at common viewport heights.
- Buttons, labels, and nav items do not wrap awkwardly.

## Brand And Copy

- The first viewport clearly communicates the campaign value.
- The page follows the approved source brand or campaign visual direction.
- The page matches the approved campaign design context.
- The page does not rely on generic AI-looking design defaults unless those defaults are explicitly supported by the design context.
- Buyer-facing copy contains no production notes, private notes, placeholder text, or unapproved internal language.
- Claims are public, customer-approved, or clearly framed as assumptions.
- Metrics, customer names, quotes, awards, logos, analyst proof, and case studies are verified or approved.
- Every proof point answers why it matters and what action it supports.

## Design Quality

- The wireframe's visual hierarchy is visible in the rendered page.
- Typography scale, line lengths, and labels are readable and intentional.
- Color usage follows the design context and does not collapse into an unsupported one-note palette.
- Cards, modules, and sections are not nested or over-framed.
- Buttons match the approved button system and have useful labels.
- Surface rhythm supports scanning across the whole page.
- Anti-references from the design context are not present.
- The page has been inspected visually at desktop and mobile sizes, not only checked by DOM metrics.

## Controls

- Every button works.
- Every nav item works.
- Every resource link works.
- Every card CTA works.
- Every modal opens and closes.
- Every tab, filter, selector, carousel, slider, calculator, or form performs a real action.
- No placeholder link or dead decorative control remains.
- External links use safe target and rel behavior unless the publishing guide says otherwise.

## Analytics

When analytics hooks are required:

- primary CTA clicks are tracked
- secondary CTA clicks are tracked
- resource clicks are tracked
- internal navigation is tracked
- meaningful interactions are tracked
- payloads include useful text, area, destination, and option values

Do not mark publish analytics acknowledgements as true until the saved HTML actually satisfies them.

## Accessibility

- Page has a sensible heading structure.
- Images have useful alt text or empty alt text when decorative.
- Icon-only controls have accessible labels.
- Focus states are visible.
- Interactive controls are keyboard reachable where practical.
- Color contrast is practical on light and dark sections.
- Reduced-motion behavior exists for non-trivial animation.
- Forms have labels and clear submit behavior when forms are present.

## Assets

- Logos load.
- Images load.
- Embedded media loads or has a fallback.
- SVGs render correctly on their actual backgrounds.
- Carousels or repeated logo rows do not imply unapproved extra customers.
- Asset URLs are stable enough for the publishing environment or are otherwise packaged appropriately.

## Folloze Publish Readiness

Before saving through Folloze:

- The current Folloze publishing guide has been read.
- Net-new board versus existing-board update is clear.
- Theme mode is confirmed.
- Required theme stylesheet link is present if the guide requires it.
- External-link and analytics requirements from the current guide are satisfied.
- The verified local HTML file is the source used for publish.
- The board title, campaign name, and audience are correct.
- Public deployment status can be verified or is reported as pending.

## Handoff When Publish Tools Are Missing

If no Folloze publish tool is available, return:

- local HTML file path
- approved wireframe
- QA checks run
- blockers or caveats
- required publish settings to verify in Folloze
- analytics assumptions
- link and theme assumptions

Do not imply the page is live when it is only local or ready for handoff.
