# Default Templates

The default deliverable is a responsive short-scroll microsite. The printable template is optional.

## Responsive Microsite

Start from `assets/one-pager-microsite-template.html`.

Use when:

- the one-pager will be reviewed or shared as HTML
- Folloze MCP may be used after approval
- mobile viewing matters
- the page needs a buyer-facing Promise, Proof, Path narrative
- the page should feel like a concise digital white paper rather than a feature-heavy campaign page

Required structure:

1. sticky header with Folloze and prospect identity
2. `#promise` Hero with one account-specific argument and the role-specific primary CTA
3. Desired outcome treatment with exactly one buyer challenge and one desired outcome
4. `#proof` with approved numeric evidence when available or an approved qualitative reason to believe
5. `#path` with only the relevant Build, Activate, and Signal capabilities
6. `#next-step` CTA with the same approved action

These are the standard buyer-facing modules: Hero, Desired outcome, Folloze capabilities, Proof, and CTA. Preserve `Promise -> Proof -> Path` as the underlying argument.

Use `references/microsite-content-contract.md` for the safe renderer workflow, token mapping, content limits, and claim rules.

## Printable/PDF Template

Use `assets/one-pager-pdf-template.html` only when the user explicitly requests:

- a fixed one-screen leave-behind
- a landscape PDF
- an email attachment

Do not use the fixed layout as the default MCP source. Do not overload it when the approved story needs more room.

## Visual System

Folloze is the default brand owner.

Provisional current public-site tokens:

- deep navy: `#071428`
- slate: `#2C3D59`
- indigo: `#5B5BFF`
- strong indigo: `#3B3BE0`
- muted blue-gray: `#6B7E9D`
- white and pale tinted surfaces
- Instrument Sans when available
- restrained editorial surfaces
- filled and outline pill CTAs

Keep these as CSS variables. The current official Folloze site and bundled `folloze-brand-kit` are the shared authority. Do not make Figma access a prerequisite for using or maintaining the template.

Use only the exact source-backed account accent approved in the intake. Otherwise retain the approved Folloze default.

Favor a simple white-paper feel: short scroll, generous whitespace, readable type, restrained borders, and minimal decorative treatment.

## Template Rules

- Start from `references/render-values-template.json` and use `scripts/render_one_pager.py --brief <approved-intake.json>`; do not perform raw token replacement or bypass the approval gate.
- Select every optional module explicitly so the renderer removes unused content and linked controls.
- Use real official logos or a text fallback.
- Keep source URLs and proof provenance in the intake sidecar.
- Attach one explicit proof-or-claim evidence kind and opaque ID to each proof card.
- Bind every visible proof and Folloze claim string to the exact approved display-content registry entry for that ID.
- Trace buyer-visible account claims with opaque source IDs.
- Do not use external scripts.
- Do not use raw in-page hash links.
- Do not leave dead arrows, buttons, or links.
- Keep custom CSS and JavaScript inline.
- Add the exact MCP-returned theme link only during an authorized save flow.

## QA

Microsite QA:

- 1440 x 900
- 1024 x 768
- 768 x 1024
- 414 x 896
- 390 x 844
- 320 x 568
- no horizontal overflow
- correct scroll-control behavior
- CTA and resource-click analytics plus compatibility with Folloze native analytics
- keyboard focus
- reduced-motion behavior

PDF QA:

- 1536 x 864 source viewport
- one landscape page
- no clipped cards or overlays
- readable logos and text
- rendered PDF or PNG inspection, not metadata alone
