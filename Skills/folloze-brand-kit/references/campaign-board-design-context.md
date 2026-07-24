# Folloze Campaign Board Design Context

Use this reference when Folloze is the brand owner for a campaign board, ABM microsite, demand generation page, resource hub, event follow-up page, or product/workbench experience.

This is an example brand pack for the customer-facing `folloze-campaign-board-builder` skill. Customers should fork the pattern for their own brand rather than hardcoding Folloze's palette, voice, or campaign style into the core builder skill.

## Campaign Design Context

```text
Campaign design context:
- Brand owner: Folloze
- Campaign register: B2B marketing campaign, ABM microsite, resource hub, event follow-up, product/workbench page, or executive briefing
- Source design inputs: Folloze brand kit, Folloze website, approved campaign assets, approved product screenshots, and current Folloze messaging references
- Audience mood: crisp, practical, enterprise-ready, modern, revenue-focused, confident without hype
- Typography: clean sans-serif system fallback unless an approved Folloze web font is available; large clear display headlines; compact labels; readable body copy
- Color system: Folloze white and soft-gray canvases, dark navy foundations, violet actions, and the approved extended campaign/event palette in `visual-identity.md`
- Surface rhythm: mostly white or `#FAFAFB` surfaces, `#F4F4FB` alternating bands, and bounded dark navy panels for orchestration, proof, or system views
- Button system: clear filled primary CTA, bordered secondary CTA, precise labels, no decorative arrows unless source design supports them
- Card and module style: crisp bordered cards, 8px or smaller radius, restrained shadow, no cards inside cards
- Imagery and media: approved Folloze logos, product screenshots, campaign visuals, or simple workflow diagrams; avoid generic stock imagery
- Proof and resource style: proof must be approved; use qualitative proof when numeric proof is not verified
- Motion tolerance: restrained and purposeful; use hover, state change, and subtle transitions; always include reduced-motion fallback
- Interaction expectations: selectors, tabs, calculators, resource paths, or workbench modules must change state and emit useful analytics
- Accessibility constraints: strong contrast, clear focus states, mobile line-break checks, no horizontal overflow, readable dark-section text
- Anti-references: generic SaaS hero, purple-heavy gradient page, glassmorphism, fake dashboard chrome, decorative icon tiles, hollow AI hype
- Unknowns or assumptions: CTA destination, proof permission, product screenshots, and campaign offer should be verified per board
```

## Folloze Visual Defaults

Use `references/visual-identity.md` for the canonical logo and color source.

Core board palette:

- `#FFFFFF` white
- `#FAFAFB` soft canvas
- `#F4F4FB` tinted section band
- `#F4F4FF` pale violet hero surface
- `#2C3D59` slate
- `#1C293F` navy
- `#071428` deep navy
- `#0A1230` action navy
- `#5B5BFF` primary violet accent
- `#11D175` green accent

Approved extended campaign backgrounds:

- dark bands: `#0C1330` to `#070B1F`
- CTA/proof bands: `#0C1740` to `#070B22`
- cyber navy: `#070B1E`
- orbit light: `#FBFBFE`
- editorial cream: `#F4EEE1`
- sunset: `#FF8A5C` to `#FF5C7A` to `#C8398F`
- terminal black: `#0A0A12`
- cobalt: `#1560FF` to `#0A2ECC` to `#061C8F`

Use accent colors for emphasis, state, and wayfinding. Use expressive themes to create one coherent campaign world or to distinguish examples in a deliberate sequence. Do not scatter the full palette across an ordinary page or default to a one-note blue or purple gradient.

## Folloze Campaign Registers

### Demand Generation

Best for broad mid-market or segment campaigns.

Design direction:

- offer-led first viewport
- clear pain and urgency
- Build / Activate / Signal value path
- resource cards or product overview
- meeting, workshop, demo, or product-tour CTA

### ABM Microsite

Best for one named account or one-to-few account clusters.

Design direction:

- account context in the first viewport when buyer-safe
- account-specific tension or opportunity
- role-specific value
- proof and resources selected for the buying group
- workshop or account review CTA

### Resource Hub

Best for nurture and sales follow-up.

Design direction:

- audience-specific promise
- featured resource
- browsable paths by topic, persona, stage, or use case
- clear recommendation for the next asset
- engagement analytics on every resource

### Product Or Workbench

Best when the visitor needs to understand how Folloze changes the work.

Design direction:

- outcome-led first viewport
- interactive workflow, scenario selector, journey map, or signal map
- short product explanation tied to the workflow
- proof and implementation path
- CTA to plan the campaign or see the platform

### Executive Briefing

Best for senior marketing and revenue leaders.

Design direction:

- crisp strategic thesis
- market or operating pressure
- risk of generic buyer journeys
- value of personalization, governance, and first-party signal
- executive workshop CTA

## Messaging Defaults

Use `references/brand-foundation.md`, `references/messaging-library.md`, and `references/product-capabilities-customer-ready.md`.

Preferred external frame:

- Folloze helps teams target and convert key accounts.
- Your AI creates content. Folloze deploys it, hosts it, governs it, personalizes it, and captures the signal that drives the next move.
- Build. Activate. Signal.

Use plain language:

- personalized buyer experiences
- campaign destinations
- ABM microsites
- first-party engagement signals
- sales-ready follow-up
- governed campaign execution

Avoid external lead language:

- activation layer
- campaign agent
- insight agent
- AI orchestration platform
- fully autonomous campaign execution
- AI replaces marketers

## Folloze-Specific Design Gates

Before publish or handoff, check:

- Folloze logo renders clearly on the chosen background.
- The first viewport states a specific buyer or campaign outcome.
- Build / Activate / Signal appears only when it advances the story.
- AI is framed as acceleration with human review and governance.
- Any named proof or numeric claim comes from approved proof guidance.
- CTA labels are concrete, such as `Book a campaign workshop`, `See how Folloze works`, `Plan your account experience`, or `Explore the product tour`.
- No visible copy says or implies that the page was generated, templated, or internally staged.
- Every selector, tab, calculator, resource card, and CTA emits useful analytics when the publishing path supports it.
