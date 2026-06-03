---
name: folloze-campaign-board-builder
description: Guide marketers from campaign brief to approved wireframe, local editable HTML, automatic QA, and Folloze publish readiness. Use when a marketer wants to build a Folloze board, ABM microsite, campaign landing page, demand generation page, event follow-up experience, resource hub, or account-specific buyer experience.
---

# Folloze Campaign Board Builder

Use this customer-facing skill to help marketers turn a campaign idea into a Folloze-ready buyer experience.

This is a thin-harness, fat-skill workflow:

- The harness is only the available local editor, browser, file system, and Folloze publishing tools.
- The skill owns the campaign strategy, information intake, wireframe choice, build standards, QA gates, and publish-readiness checks.
- Customer research systems are inputs to the brief, not hard-coded dependencies. The customer can bring CRM, MAP, intent, web analytics, content library, DAM, call notes, product docs, spreadsheets, or pasted research.
- Customer brand systems are inputs to the design context, not hard-coded dependencies. The customer can bring a source website, brand guide, design system, screenshot, asset pack, or their own design context file.
- Keep the core skill brand-agnostic. For Folloze-owned example boards, use `folloze-brand-kit` as an optional brand pack; do not make Folloze's palette, voice, or campaign defaults mandatory for customer boards.

## Required Sequence

Run the work in this order:

1. Campaign brief
2. Campaign design context
3. Wireframe recommendation and approval
4. Local HTML build
5. Automatic QA
6. Folloze publish or publish handoff

Do not start the full HTML build until the marketer has approved the wireframe or explicitly asked to proceed with a named wireframe.

## Minimum Inputs

The brief must identify these three inputs before a wireframe is recommended:

- Campaign goal: what the experience should make the audience do, understand, request, register for, evaluate, or buy.
- Audience: segment, account, persona, buying committee, customer group, partner group, or event audience.
- Campaign style: ABM microsite, landing page, demand generation, event follow-up, product launch, nurture hub, customer expansion, partner campaign, or other named campaign type.

If any of these are missing, ask concise questions to fill only the gap. Do not ask a long questionnaire when the marketer has already given enough direction to move forward.

## Phase 1: Campaign Brief

Use `references/campaign-brief-template.md` to convert the marketer's campaign idea into a practical build brief.

The brief should answer:

- What is the campaign trying to accomplish?
- Who is the audience and what do they already know?
- What research or data sources should inform the page?
- Which materials are required or available?
- Which sources are public, private, approved for buyer-facing use, or strategy-only?
- What offer, CTA, event, resource, meeting, demo, trial, or next step should the page drive?
- What brand, source page, screenshot, brand guide, design system, or design context should define the visual system?
- What compliance, legal, accessibility, localization, or review constraints matter?
- What is missing, and can the build proceed with labeled assumptions?

Research and data-source wiring should be captured as customer-provided inputs. If the customer has a connector or MCP tool for a source, use it when available. If not, ask for a pasted packet, exported file, approved claims, or links. Never invent facts to fill a campaign gap.

## Phase 2: Campaign Design Context

Use `references/campaign-design-context.md` to capture the customer's visual and campaign system before recommending a wireframe.

The design context should answer:

- Who is the brand owner?
- What campaign register is this?
- What source design inputs should be followed?
- What audience mood should the page create?
- What typography, color, surface, button, card, media, proof, and motion patterns should guide the build?
- What anti-references should the board avoid?
- What design assumptions are still unresolved?

If the customer has no formal brand guide, inspect the approved source page or screenshot and capture the design facts. If the source is unavailable or blocked, ask for a screenshot, brand page, or short design context before building.

For Folloze-owned boards, use `folloze-brand-kit` and its `references/campaign-board-design-context.md` as the example brand pack. For customer-owned boards, use the customer's brand context instead.

## Phase 3: Wireframe Recommendation

Use `references/wireframe-catalog.md` to choose the best wireframe for the campaign.
Use `references/design-quality-gates.md` to make sure the recommendation includes visual hierarchy and campaign shape, not only section order.

Return a wireframe recommendation before building:

- recommended wireframe name
- why it fits the campaign goal, audience, and style
- alternate wireframes considered
- section-by-section structure
- visual hierarchy and section rhythm
- first-viewport message and CTA
- required content, proof, resources, and data inputs
- interactive modules, if any
- analytics events to track
- anti-references and design assumptions
- QA risks to watch

Then stop and ask the marketer to approve, revise, or choose a different wireframe. Keep the approval request short.

## Phase 4: Local HTML Build

After wireframe approval, create a single local `.html` file that the marketer can edit in their local code agent before publishing.

Use `references/build-standards.md`.
Use `references/design-quality-gates.md` before and after the first render.

Build requirements:

- Create one self-contained HTML file unless the customer explicitly wants a multi-file app.
- Put the source file in the active project workspace. If there is no active workspace and a durable file is needed, ask where the customer wants it created.
- Treat the approved brief, campaign design context, and wireframe as the source of truth.
- Use customer-approved claims, public evidence, and approved brand/material links.
- Keep private or internal data out of buyer-facing copy unless the customer explicitly approves its use.
- Use the campaign design context to set colors, type, buttons, cards, imagery, surface rhythm, proof treatment, and motion.
- Use real links, resources, anchors, modals, tabs, sliders, filters, forms, and CTA destinations. No placeholder controls.
- Include analytics hooks for CTAs and meaningful interactions when the Folloze publishing path supports them.
- Make the page responsive before QA begins.

Buyer-facing copy should sound like a campaign asset, not a production note. Avoid visible language such as `generated by`, `template`, `placeholder`, `internal brief`, `test`, `wireframe`, `draft`, or `QA` unless the marketer explicitly wants those words on the page.

## Phase 5: Automatic QA

Run QA immediately after the local HTML build is complete. Do not wait for the marketer to ask for QA.

Use `references/qa-publish-gates.md`.
Use `references/design-quality-gates.md` for visual and anti-generic review.

At minimum, verify:

- page renders locally
- no obvious console errors
- desktop and mobile layouts are readable
- no horizontal mobile overflow
- buttons and navigation work
- external links are real and safe
- modals, tabs, sliders, filters, calculators, and forms perform real actions
- images, logos, and embedded assets load
- buyer-facing copy contains no private-source leakage or production language
- rendered page matches the campaign design context
- generic AI-looking design patterns have been removed or justified by the source brand
- CTAs and key interactions emit analytics hooks when required
- accessibility basics are present: semantic structure, alt text, focus states, keyboard access, practical contrast, reduced-motion behavior

Fix QA failures before publish unless the marketer explicitly accepts a documented caveat.

## Phase 6: Folloze Publish Or Handoff

Publishing depends on the customer's available Folloze tools.

If Folloze MCP or another Folloze publish tool is available:

1. Read the current Folloze landing-page or board publishing guide before saving.
2. Confirm whether this is a net-new board or an existing-board update.
3. Confirm theme mode, theme stylesheet requirements, analytics requirements, and external-link requirements from the current guide.
4. Save from the verified local HTML file.
5. Return the board ID, exact returned Folloze URL, and public deployment status.

If no Folloze publish tool is available, return a handoff package:

- local HTML file path
- campaign brief summary
- campaign design context summary
- approved wireframe name
- QA status and any caveats
- publish checklist
- required theme, analytics, and link assumptions to verify inside Folloze

Do not claim a page is published, live, or publicly deployed unless the publish tool or a live verification step confirms it.

## Customer Extension Points

This skill is intended to be forked and customized by customers.

Recommended extension points:

- add customer-specific research-source instructions to the brief template
- add a customer-specific campaign design context file or brand pack
- add approved campaign styles or wireframes to the wireframe catalog
- add brand, compliance, localization, or legal gates to QA
- add design anti-references that reflect the customer's brand
- add company-specific analytics event names and payload requirements
- add publishing instructions for the customer's Folloze environment
- add examples of approved briefs, approved wireframes, and passed QA reports

Keep extensions declarative where possible. The skill should describe what a good campaign experience needs; the customer's local tools should provide the data and publishing mechanics.

## Final Response Shape

For a brief or wireframe step, return:

- brief completeness
- recommended wireframe
- missing inputs or assumptions
- the approval question

For a completed build, return:

- local HTML file path
- QA result
- publish status or handoff status
- unresolved caveats

Keep the response marketer-readable and operational.
