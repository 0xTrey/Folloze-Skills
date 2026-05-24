---
name: folloze-sales-doc
description: "Use this skill to create or deliver Folloze sales preparation and customer lifecycle documents, including call prep docs, executive packages, account briefs, follow-up summaries, QBR docs, onboarding plans, renewal prep, champion briefs, stakeholder maps, and Google Doc packages for a prospect or customer touchpoint. Trigger when a Folloze teammate asks to prep for a call, build a doc, create an account package, summarize an account, turn meeting/email evidence into a shareable brief, or import/share the result as a native Google Doc. Always use this skill for Folloze account documentation regardless of lifecycle stage."
---

# Folloze Sales & Customer Lifecycle Doc Skill

This skill produces branded, professional account documents for every stage of the Folloze customer lifecycle - from pre-sale discovery prep through post-sale QBRs and renewals. Depending on the request, the output may be a repo-backed Markdown source, a DOCX, a native Google Doc, or a paste-ready follow-up package.

## Quick Reference

| Lifecycle Stage | Doc Type | Key Sections |
|---|---|---|
| Pre-Sale | Discovery Prep | Company snapshot, contacts, pain mapping, pitch angles, discovery Qs |
| Pre-Sale | Champion Brief | Champion profile, org map, internal politics, talking points |
| Active Deal | Stakeholder Map | Buyer roles, influence, objections per person |
| Active Deal | Proposal Summary | Value prop mapped to pain, ROI framing, next steps |
| Post-Sale | Onboarding Plan | Goals, milestones, team contacts, success metrics |
| Post-Sale | QBR / Business Review | Usage stats, wins, gaps, roadmap alignment |
| Post-Sale | Renewal Prep | Health score, risks, expansion opportunities, renewal narrative |
| Any Stage | Account Summary | Snapshot of where the account stands right now |
| Any Stage | Executive Package | Stakeholder-specific brief, meeting follow-up, field/event plan, risks |

---

## Step 1 — Identify the Doc Type and Gather Inputs

Ask the user (or infer from context) the following:

1. **Lifecycle stage** — pre-sale, active deal, or post-sale?
2. **Doc type** — which of the above types fits best?
3. **Account info** — company name, contact names/titles, any call notes or CRM data provided
4. **What do they know?** — any intel already in the conversation (call notes, prior emails, research)

If the user provides call notes or raw information, extract structured content from them. If they provide a company name but no research, use web search to gather company snapshot data before building the doc.

For executive packages or shareable account briefs, infer the stakeholder audiences from the request. Tailor separate sections for the named readers, such as sales, field marketing, events, leadership, customer success, or IT/security, instead of returning one generic meeting recap.

---

## Step 2 — Research (if needed)

For pre-sale docs, always research:
- Company size, funding, stage, revenue signals
- Marketing team structure and key contacts (LinkedIn, Crunchbase, job postings)
- Current martech stack (job descriptions are a goldmine)
- Recent company news or growth signals
- ABM maturity signals (are they hiring ABM? what tools do they mention?)

For post-sale docs, pull from:
- Call notes and CRM data provided by the user
- Any product usage stats shared
- Prior correspondence in the conversation

For executive packages and follow-up briefs, use the real evidence stack before writing:

- Salesforce for account, opportunity, owner, stage, health, renewal, and pipeline context when allowed.
- Granola for meeting notes, attendee context, open questions, and promised follow-ups.
- Gmail for current thread state, sent follow-through, stakeholder asks, and source discrepancies.
- Google Drive for existing deal notes, decks, prior briefs, proposals, security notes, or event plans.
- Public website or web search for company context, current messaging, public proof, news, and martech clues.

If sources disagree, keep the discrepancy visible in the working notes or final caveat. Do not smooth over a customer/account naming conflict before someone sends the package externally.

---

## Step 3 — Build the Document

Use the `docx` npm library. Always follow the **Folloze Design System** defined in `references/design-system.md`.

### Document Structure by Type

#### Discovery / Call Prep Doc
1. Header block (company name, doc type, date, "Selling: Folloze")
2. Company Snapshot (two-col table)
3. Growth Signals / Why Now (dark callout box)
4. Marketing Team & Key Contacts (person cards)
5. Their Situation Today (callout box with current pain/stack)
6. Folloze Pitch Angles (numbered, mapped to their specific pain)
7. Discovery Questions (grouped by theme)
8. Likely Objections & Responses (two-col table)
9. Call Strategy & Goals
10. Quick Reference Cheat Sheet (two-col table)

#### Champion Brief
1. Header block
2. Champion Profile (person card with background, tenure, priorities)
3. Their Internal Goals & KPIs
4. Organizational Map (who they report to, who influences them)
5. Internal Dynamics (allies, skeptics, budget holders)
6. How to Arm Them (talking points, materials to share)
7. Risk Factors
8. Recommended Next Actions

#### Stakeholder Map
1. Header block
2. Account Overview
3. Stakeholder Cards (one per key contact — role, influence level, stance on Folloze, key concern)
4. Decision-Making Process
5. Engagement Strategy per Stakeholder
6. Risk & Mitigation

#### Onboarding Plan
1. Header block
2. Account Goals (what success looks like for them)
3. Folloze Team Contacts
4. Customer Team Contacts
5. Onboarding Milestones (30/60/90 day table)
6. Success Metrics
7. Known Risks & Mitigation
8. Next Scheduled Touchpoints

#### QBR / Business Review
1. Header block
2. Executive Summary
3. Usage & Engagement Highlights (key stats in callout box)
4. Wins Since Last Review
5. Gaps / Areas to Improve
6. Roadmap Alignment (what's coming that matters to them)
7. Mutual Action Plan
8. Next Steps

#### Renewal Prep
1. Header block
2. Account Health Snapshot (two-col table: green/amber/red signals)
3. Usage Trends
4. Relationship Map (champion strength, exec access)
5. Risks & Mitigation
6. Expansion Opportunities
7. Renewal Narrative (the story to tell)
8. Competitive Threats
9. Recommended Actions & Timeline

#### Executive Package / Account Brief
1. Executive summary with the business objective and near-term decision.
2. Audience-specific sections for each named stakeholder group.
3. Account and opportunity context from Salesforce or deal notes.
4. Meeting and email evidence translated into action, not raw transcript.
5. Field/event plan, sales plan, or follow-up plan when relevant.
6. Risks, naming/source discrepancies, and open questions.
7. Next actions with owners and suggested sequence.

---

## Step 4 — Code Pattern

For durable docs, first verify the active project is inside a git work tree. Keep the source artifact in the relevant repo, usually under `research/`, `docs/`, or another existing project-specific folder. Do not leave the only durable copy in a temp folder or conversation transcript.

When a DOCX is required, use the `docx` npm library and follow the **Folloze Design System** defined in `references/design-system.md`.

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
        LevelFormat } = require('docx');
const fs = require('fs');
```

Read `references/design-system.md` for the full set of reusable component functions (header block, callout box, person card, two-col table, h1, h2, bullet, etc.) — copy them into the script verbatim. Do not reinvent the design components.

File naming convention:
```
[Company]_[DocType]_Folloze.docx
e.g. Tailscale_DiscoveryPrep_Folloze.docx
     Okta_RenewalPrep_Folloze.docx
     Salesforce_QBR_Folloze.docx
```

When the user asks to share, deliver, or put the package in Google Docs:

1. Generate a clean local source and, when needed, a DOCX export.
2. Import or create a native Google Doc through the available Google Workspace, Drive, or Documents tooling.
3. Verify the imported text with connector readback.
4. If permissions matter, share the Google Doc through the available Drive path and verify the final permissions list.
5. Return the Google Doc link and any caveat, such as a naming discrepancy or incomplete source.

---

## Step 5 — Validate and Present

After generating:
1. Run the file and confirm it writes successfully
2. Verify the final artifact in the surface the user asked for: DOCX file, Google Doc, or paste-ready text
3. Give a 2-3 sentence summary of what's inside and what needs confirmation before the call, meeting, or external send

---

## Critical Rules

- **Always use the design system** from `references/design-system.md` — never invent new color schemes or layouts
- **Never make up contacts** — if you can't find a person's name, use a placeholder like `[ABM Manager — confirm name]`
- **Flag assumptions** — if you assumed something (e.g. their stack, their team size), note it in the doc with `[Verify: ...]`
- **Tailor pitch angles to their actual pain** — generic Folloze value props are not enough; map each angle to something specific from research or call notes
- **Keep cheat sheets truly concise** — the quick reference table at the end should be scannable in 30 seconds
- **Keep source boundaries clear** — separate confirmed live evidence from likely or historical public-stack guesses
- **Do not send externally without approval** — when the task is a package or follow-up draft, produce the artifact and approval-ready summary unless the user explicitly asks to send or share with a named recipient
