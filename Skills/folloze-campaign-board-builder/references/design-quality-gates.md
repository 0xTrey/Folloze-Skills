# Design Quality Gates

Use these gates during wireframe review, before local preview, and again during QA.

The goal is to prevent a campaign board from looking like a generic AI-generated landing page. These gates are brand-agnostic and should be applied against the customer's approved campaign design context.

## Brand System Fit

- The board follows the approved campaign design context, source page, brand guide, screenshot, or design system.
- Buttons, cards, labels, surfaces, and CTA hierarchy feel native to the brand owner.
- The page does not invent a new palette, icon style, roundedness, or typography system when brand evidence exists.
- The design uses customer-provided or source-owned assets before generic web images.
- If exact brand assets are unavailable, fallbacks are labeled in the working summary.

## Campaign Shape

- The wireframe defines visual hierarchy, not only section order.
- The first viewport makes the audience, offer, and next action clear.
- The page has one main campaign argument.
- Section order builds momentum instead of repeating the same value claim.
- The strongest proof or resource appears before deep product detail when proof is available.
- The final CTA follows naturally from the campaign journey.

## Anti-Generic Checks

Fix these before build or publish:

- generic SaaS hero that could fit any company after swapping the logo
- purple-blue gradient default that is not supported by the brand source
- cards inside cards
- every section as a floating card
- fake app chrome, fake browser window, fake phone frame, or fake dashboard used as decoration
- rounded-square icon tile above every heading
- three equal feature cards used as the main structure without a campaign reason
- gray text on tinted or colored backgrounds with weak contrast
- placeholder arrows, decorative chevrons, or buttons that do not do real work
- meaningless stats, proof, logos, or badges
- stock-like imagery that does not help the buyer understand the offer
- overused filler such as unlock, seamless, robust, transform, innovative, or game-changing when a specific outcome is available

## Design Passes

Use these named passes as a shared vocabulary with the marketer:

- Shape: improve the page structure, hierarchy, and campaign narrative before code.
- Typeset: fix heading scale, line length, label treatment, wrapping, and type contrast.
- Colorize: align palette, accents, surfaces, and contrast to the design context.
- Layout: fix spacing, grid rhythm, section density, and scan path.
- Clarify: sharpen section copy, CTA labels, proof implications, and resource names.
- Adapt: verify desktop, tablet, and narrow mobile behavior.
- Harden: fix overflow, link behavior, accessibility, analytics, and edge cases.
- Polish: final visual and interaction pass before publish or handoff.

## Wireframe Gate

Before asking the marketer to approve a wireframe, confirm:

- campaign register is selected
- visual hierarchy is described
- first viewport is defined
- section rhythm is defined
- interaction modules are justified
- required proof and materials are named
- anti-references are known or explicitly missing
- QA risks are listed

Do not ask for wireframe approval if the recommendation is only a list of sections.

## Build Gate

Before writing or generating HTML:

- source design inputs have been inspected or the customer has provided a design context
- brand owner is clear
- campaign register is clear
- typography, color, button, card, and surface rules are captured
- required assets are available or assumptions are explicit
- interactions are limited to what can be built and QAed

## Visual QA Gate

Before publish or handoff:

- inspect rendered desktop and mobile views
- compare the rendered page to the campaign design context
- check that text does not clip, overlap, or wrap awkwardly
- check that the page does not collapse into a one-note palette
- check that dark sections set readable light text and light sections set readable dark text
- check that CTA labels are specific and benefit-oriented
- check that every visible interaction changes state, moves the visitor, submits information, opens content, or tracks a meaningful event

If the board fails any design gate, revise the source HTML and re-run QA.
