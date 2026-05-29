---
name: folloze-zoom-deal-room
description: Turn Zoom AI meeting recaps, meeting notes, Gmail/Calendar context, and Salesforce opportunity context into buyer-safe Folloze deal-room briefs and, when explicitly requested, Folloze MCP or API deal rooms. Use when a Folloze teammate asks to turn Zoom notes, call notes, meeting assets, meeting recaps, or follow-up tasks into a deal room, sales room, resource hub, proposal follow-up page, or Folloze board.
---

# Folloze Zoom Deal Room

Use this skill to convert Zoom recap notes into a grounded deal-room plan and, when the user asks to build or publish, a Folloze-hosted sales room.

This is an intake and orchestration skill. It should use:

- Gmail or pasted notes for the Zoom recap source.
- Salesforce read-only context for account and opportunity resolution when available.
- `folloze-brand-kit` for Folloze positioning, buyer-facing language, and product capability references.
- `Folloze-MCP-Demo-Builder` for rich custom HTML pages saved through Folloze MCP.
- The existing external board creation API path only for fast template-based boards where custom HTML is not needed.

## Operating Rules

- State the working goal before material edits: source note, account, audience, output path, repo target, save intent, and private-note boundary.
- Start from the real Zoom recap or meeting note. Do not write a generic deal room from memory when a source email, note, or transcript is available.
- Treat Zoom notes, Gmail, Calendar, Granola, Salesforce, Slack, and Drive as private strategy inputs unless the user explicitly approves external use.
- Do not quote meeting notes, expose raw objections, expose budget commentary, or mention internal tasks in buyer-facing page copy.
- If the account identity is unresolved or ambiguous, build the internal brief but stop before Folloze save.
- If the user asks for a Folloze-owned deal room, use Folloze positioning and deal-room structure. If the user asks for a vendor-owned account page, hand off to `Folloze-MCP-Demo-Builder` and keep Folloze invisible.
- Do not save, publish, update a live board, or write tracker rows unless the user explicitly asks for a Folloze save/update/publish or the request is clearly a create-board request.
- When saving through MCP, follow the current MCP guide returned by the tool over this skill's local memory.
- Keep durable HTML source and notes in an obvious git-backed repo before saving through MCP or API.

## Workflow

### 1. Gather The Source

Use the narrowest source path first:

1. If the user points to an email, read that Gmail thread.
2. If the user pasted Zoom notes, use the pasted content as the primary source.
3. If the user gives an account or meeting name only, search Gmail and Calendar for the latest matching Zoom recap or meeting-assets email.
4. If the source is a Zoom meeting-assets email, preserve the recap link as internal evidence only.

Extract only the facts needed for deal-room planning. Do not echo the full transcript or full recap back to the user unless they request it.

### 2. Extract A Deal-Room Intake

Use `references/zoom-recap-schema.md` to build a compact intake object:

- meeting identity and date
- account identity and confidence
- attendees, absent stakeholders, and buyer roles
- current workflow or incumbent tools
- pains, goals, objections, proof needs, and commercial constraints
- promised follow-ups and owners
- required resources, docs, examples, proposal items, and next meeting
- recommended deal-room type and save readiness

Mark each important field with confidence: `confirmed`, `likely`, `unclear`, or `missing`.

### 3. Resolve The Account

For named deals, perform a read-only Salesforce check when available:

- confirm Salesforce auth and current org
- search Account, Contact, and Opportunity records by account name, contact names, email domains, and opportunity clues
- compare Salesforce context to the Zoom note before using it

Do not write Salesforce from this skill. If Salesforce finds weak or conflicting matches, keep the conflict in the internal brief and stop before a live Folloze save.

### 4. Build The Internal Deal-Room Brief

Use `references/source-boundaries.md` before writing the brief.

The brief should include:

- account and opportunity state
- buyer situation
- top goals and objections
- decision path and next meeting
- promised follow-ups
- content/resource plan
- buyer-safe message spine
- save-readiness assessment

This brief is internal. It can mention source evidence and private constraints, but it should label what cannot be used externally.

### 5. Choose The Output Route

Use `references/mcp-api-routing.md`.

Default route: rich MCP HTML deal room.

Choose MCP when the deal room needs any of:

- custom resource hub
- mutual action plan
- stakeholder-specific paths
- proposal/security/MSA module
- event follow-up journey
- interactive tools, tabs, drawers, calculators, or schedulers
- stronger visual/story control

Choose the external board creation API only when the user needs a fast template board and accepts fixed sections.

### 6. Build The Deal Room

For MCP:

1. Read the current Folloze landing-page creation guide.
2. Ask for theme mode if it has not already been authorized for this board or motion.
3. Use `assets/deal-room-template.html` only as a starting shell; replace every placeholder before preview or save.
4. Build a single self-contained HTML file in the relevant git-backed workspace.
5. Run the quality gates from `references/deal-room-structure.md` and the MCP demo-builder quality gates.
6. Save through MCP only after the user asks to save, publish, update, or push.

For API:

1. Select an approved deal-room template.
2. Map the intake to available template fields only.
3. Do not claim the API can add sections, native content items, or custom interactions.
4. Keep secrets out of the skill package and rely on the environment or existing API workflow.

### 7. Final Response

For a scoping/dry run, return:

- matched source note and account confidence
- recommended route
- proposed deal-room sections
- blockers before save
- next build step

For a completed build, return:

- local HTML source path
- verification performed
- board ID and exact returned Folloze URL if saved
- public deployment status, especially when MCP returns only a designer URL
- any tracker logging status if it was in scope

## Save Blockers

Stop before live Folloze save when any of these are true:

- account identity is unclear
- output brand owner is unclear
- user has not authorized theme mode when MCP requires it
- buyer-facing copy contains raw meeting-note phrasing
- promised resources have no real link, document, or in-page content module
- CTAs or clickable controls are placeholders
- analytics acknowledgements would be false
- existing board ID versus net-new board intent is unclear
