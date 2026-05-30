# Campaign Design Context

Use this reference after the campaign brief and before wireframe recommendation.

The design context is a portable brand and campaign contract. It tells the local code agent how the board should look, feel, and behave without hardcoding any one company's brand into this skill.

## Purpose

Capture the customer's visual system, campaign register, and anti-references before building.

The goal is not to copy a source page. The goal is to extract enough design facts to make the Folloze board feel like it belongs to the customer's brand and campaign system.

## Required Design Context

Create a short working note with these fields:

```text
Campaign design context:
- Brand owner:
- Campaign register:
- Source design inputs:
- Audience mood:
- Typography:
- Color system:
- Surface rhythm:
- Button system:
- Card and module style:
- Imagery and media:
- Proof and resource style:
- Motion tolerance:
- Interaction expectations:
- Accessibility constraints:
- Anti-references:
- Unknowns or assumptions:
```

## Field Guidance

Brand owner:

- The company or brand the buyer should feel is speaking.
- For partner or co-branded campaigns, state the primary brand and secondary brand roles.

Campaign register:

- Campaign landing page
- ABM microsite
- Demand generation page
- Event follow-up
- Resource hub
- Product launch
- Executive briefing
- Role-based chooser
- Product or workflow workbench

Source design inputs:

- Source website
- Existing landing page
- Brand guide
- Design system
- Screenshot
- Deck
- Asset pack
- Customer-provided design context file

Audience mood:

- Examples: executive, practical, technical, urgent, calm, premium, approachable, operational, educational, category-defining.
- This should match the audience and offer, not the agent's default taste.

Typography:

- Source font names when known.
- Display style, body style, label style, line-height feel, heading density, and casing.
- If exact fonts are unavailable, choose a close system fallback and label it as a fallback.

Color system:

- Primary brand colors, neutrals, accent colors, dark surfaces, light surfaces, and warning or success colors when needed.
- Prefer source-brand colors over generic purple, blue, or gray defaults.

Surface rhythm:

- How sections alternate: white, tinted, dark, image-led, editorial, dense, or spacious.
- Whether the first viewport should reveal the next section.

Button system:

- Primary, secondary, utility, text-link, and card-action styles.
- Include radius, border, fill, text color, hover/focus behavior, icon use, and width behavior.

Card and module style:

- Radius, border, shadow, density, image framing, labels, dividers, and spacing.
- State whether cards are central to the brand or should be used sparingly.

Imagery and media:

- Approved product images, screenshots, photography, icon style, video, illustrations, or no-imagery guidance.
- Do not invent visual proof assets.

Proof and resource style:

- Customer logos, case studies, analyst proof, resource cards, quote treatments, metrics, or proof bands.
- Use only verified or customer-approved proof.

Motion tolerance:

- None, restrained, purposeful, or expressive.
- Every non-trivial motion needs a reduced-motion fallback.

Interaction expectations:

- Selectors, filters, calculators, tabs, forms, modals, carousels, maps, resource paths, or simple static page.
- Every interaction must do real work and be QAed.

Accessibility constraints:

- Contrast needs, focus states, alt text, keyboard behavior, localization, reduced motion, text expansion, and mobile constraints.

Anti-references:

- What the board should not look or sound like.
- Examples: generic SaaS hero, purple-blue gradient, stock-photo hero, fake app chrome, glassmorphism, oversized card stacks, playful copy, technical dashboard, marketing fluff.

Unknowns or assumptions:

- Anything still missing.
- State whether the build can proceed with assumptions or needs customer input first.

## Customer Extension Pattern

Customers can fork this file into their own brand pack.

Good customer extensions:

- approved brand token values
- product screenshot rules
- industry-specific campaign registers
- localization rules
- legal or compliance constraints
- examples of approved campaign pages
- examples of anti-references

Keep the core skill brand-agnostic. Put company-specific brand rules in a brand pack or customer-owned reference file.
