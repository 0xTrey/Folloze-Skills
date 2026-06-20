# Post-Call Package Contract

Use this contract when a user asks to turn completed-call context into a seller-reviewed package before building or publishing a Folloze deal room.

This reference captures the durable workflow from the post-call deal-room autopilot prototype. It is not a requirement to run that prototype; it is the skill-level contract to preserve when producing equivalent output by hand, with an LLM, or through a local generator.

## Inputs

Treat the full input bundle as private strategy material until classified:

- Zoom AI recap, transcript, seller notes, Granola notes, or pasted call notes
- attendees and roles
- Salesforce account, contact, opportunity, next-step, and stage context
- Gmail thread summary and follow-up state
- Drive or Docs candidate assets
- existing Folloze board id or board URL

Input facts must include source and confidence whenever possible.

## Fact Ledger

Build the fact ledger before composing any buyer-facing artifact.

Each fact must include:

- `id`: stable id such as `F001`
- `fact`: neutral restatement of the fact
- `source`: `call_notes`, `crm_summary`, `email_thread_summary`, `attendees`, `drive_assets`, `salesforce`, or `expected_but_absent`
- `classification`: `buyer_safe`, `internal_only`, or `missing`
- `confidence`: `confirmed`, `likely`, `unclear`, or `missing`
- `reason`: why the classification was chosen

Default-deny rule: a fact stays `internal_only` unless it clearly matches a buyer-safe signal and does not contain internal-only material.

Always classify these as `internal_only`:

- pricing, budget, discount, quote, commercial posture, ACV, ARR
- objections, pushback, competitive comparisons, risk, churn, skepticism, deal-breakers
- legal negotiation, redlines, procurement strategy, package strategy
- CRM summaries, email thread summaries, call intelligence, engagement data, and internal follow-up gaps

Buyer-safe facts usually include:

- stated goals, use cases, success criteria, requested resources, evaluation topics
- agreed next steps, demo/workshop/pilot plans, non-commercial timeline
- workflow context the buyer openly shared
- attendee identity when role assessment is not included

Add missing ledger entries for expected but absent deal facts such as decision timeline, KPIs, agreed next step, economic buyer, required resources, or next meeting.

## Package Artifacts

A completed package has status `DRAFT_PENDING_APPROVAL` and contains five artifacts:

1. Internal deal context brief
2. Buyer-safe deal-room plan
3. Follow-up email draft
4. Human approval checklist
5. Analytics follow-up plan

The internal brief may cite any ledger fact. The deal-room plan and follow-up email may cite only `buyer_safe` fact ids.

## Asset Handling

Classify each candidate asset before including it:

- `yes`: explicitly approved for external sharing
- `pending_approval`: appears shareable but external approval is not confirmed
- `no`: name or type suggests internal material

Assets with pricing, battlecard, strategy, notes, forecast, MEDDPICC, quote, discount, or competitive hints should default to `no`.

Approved Drive assets still need upload or attachment as Folloze content items before a native board is considered complete. Do not expose raw external Drive links in buyer-facing resource cards unless the user explicitly approves that delivery path.

## Leak Check

Before any save path is considered, scan buyer-facing artifacts for:

- non-`buyer_safe` fact ids
- significant fragments from `internal_only` facts
- raw note attribution such as "said", "mentioned", "Zoom recap", "transcript", or "internal note"
- pricing, budget, discount, competitor, objection, battlecard, or internal-only terms
- dead placeholders such as `[DEAL_ROOM_LINK]` in anything being published

If the leak check fails, stop before Folloze save or publish.

## Approval Checklist

Every item starts `pending`. Blocking items must be resolved by a human before an API push or publish:

- A01: review every buyer-safe classification in the fact ledger
- A02: read the deal-room plan as the buyer and confirm no strategy, pricing, objections, or internal tasks leak
- A03: confirm follow-up email recipients and language if an email draft is included
- A04: confirm leak check passed
- A05: approve or remove pending external assets
- A06: resolve missing expected facts when they affect save readiness
- A07: confirm board action: new board, existing-board update, draft-only push, or publish

## Analytics Follow-Up Plan

Include a practical seller follow-up plan:

- first buyer visit within 48 hours
- new stakeholder visit
- repeat views on a specific asset or section
- engagement with next-step or mutual-action-plan content
- no visit within 7 days

Do not claim analytics are already configured or available unless the board implementation actually records the relevant interactions and the user has access to the resulting Folloze analytics.

## Live Action Boundary

The package generator or assistant may create local draft files only. It must not:

- publish a Folloze board
- update an existing live board
- send the follow-up email
- write Salesforce, tracker, or CRM state

Live actions require explicit user intent, current auth, the correct board identity, and a successful readback after the action.
