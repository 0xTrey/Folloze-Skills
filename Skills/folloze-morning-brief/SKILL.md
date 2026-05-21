---
name: folloze-morning-brief
description: Build the daily read-only Folloze GTM chief-of-staff morning brief for the current Codex user from Folloze calendar, Salesforce opportunities/accounts owned by that user, Granola meeting context, Gmail, Google Drive, and optional role-specific MCPs. Use when a teammate asks for their morning brief, daily GTM priorities, meeting prep, pipeline or account overview, open tasks, or when the Folloze Morning Brief Codex automation runs.
---

# Folloze Morning Brief

Generate the daily Folloze GTM morning brief for the current authenticated teammate. The brief is individual, read-only, and delivered in the Codex inbox/thread by the host automation.

## Defaults

- Audience: the current Codex user, not Trey by default.
- Team scope: Folloze GTM teammates who use the shared Codex setup.
- Schedule: local daily run at 7:00 AM, or as soon as Codex can run after the machine wakes.
- Delivery: Codex inbox/thread only.
- Calendar scope: Folloze work calendar only; do not inspect personal calendars.
- Salesforce scope: open opportunities where the current Salesforce user is the opportunity owner. For CSM-style roles, group results at the account level because multiple opportunities may exist for the same account.
- Mode: strictly read-only and report-only. Do not write to Salesforce, Gmail, Granola, Drive, Slack, or any customer system.
- Tone: chief of staff: concise, direct, context-rich, action-oriented, and urgency-aware.
- Final output: no markdown tables.

## Source Expectations

Use the teammate's connected sources in this order:

1. Folloze work calendar for today's schedule.
2. Salesforce for the current user's open opportunities and account context.
3. Granola for follow-up context and recent meeting notes.
4. Gmail for unresolved customer asks, open follow-ups, and recent account signals.
5. Google Drive for targeted account or meeting artifacts when needed.
6. Optional role-specific MCPs, such as Gainwell for CSM workflows, when available.

Granola is a required source for follow-up context when available. If Granola is missing, unavailable, or returns only thin stubs, continue with caveats instead of blocking the brief.

If a source is unavailable, say what coverage is incomplete. Do not turn a source failure into a false negative.

## Automation Setup

When this skill is installed or synced for a teammate, create or update the local Codex automation from `AutomationTemplates/folloze-morning-brief-daily/template.json`.

The automation should:

- run locally every day at 7:00 AM in the teammate's local time zone
- deliver to the Codex inbox/thread
- use this skill as the runbook
- run read-only
- continue with caveats when a connector is unavailable

Codex automations can only run when the local environment is available. If the teammate wants the Mac to wake before the run, that is a local OS power setting and should be configured explicitly by the teammate or IT; do not change machine power settings without approval.

## Workflow

### 1. Establish Today And The User

- Use live system date/time.
- Identify the current teammate from the connected Codex account, calendar account, or Salesforce user profile.
- If the user identity is ambiguous, continue with the authenticated connector user and state the assumption in source notes.

### 2. Read Today's Folloze Calendar

Read today's events from the Folloze work calendar.

Classify events as:

- external customer/prospect/partner/vendor
- internal Folloze
- sales execution block
- admin/personal/OOO/working location

Include external meetings by default. Include internal meetings only when they materially change priorities, deal execution, or customer follow-up.

Filter out:

- working-location entries
- OOO/all-day availability markers
- gym/personal/admin events
- Reclaim/focus/prospecting blocks unless they create a real constraint
- internal-only meetings with no customer/account impact

For each included external meeting, capture:

- local display time
- meeting title
- account or domain when detectable
- external attendees when useful
- why it matters today
- prep angle or likely next step

If calendar retrieval fails, say calendar coverage is unavailable. If retrieval succeeds but no external meetings are visible, say no clear external meetings are visible today.

### 3. Build The Salesforce Account And Pipeline View

Use Salesforce to query open opportunities owned by the current Salesforce user.

Minimum useful fields:

- opportunity id and name
- owner
- account id and account name
- stage
- amount
- close date
- forecast category
- probability
- last activity date
- next step or Folloze custom next-step field when available
- customer success or renewal fields when available

Group opportunities by account. This is required for CSM-style users because one account can have multiple live opportunities.

Prioritize accounts and opportunities by:

1. accounts with external meetings today
2. near-term close dates
3. stale last activity
4. high value or committed/best-case forecast
5. proposal, validation, renewal, onboarding, or blocked stages
6. recent Granola or Gmail activity

Do not use local OpenClaw deal-index files as the primary source. The source of truth for this skill is Salesforce ownership plus live connected evidence.

### 4. Add Granola Meeting Context

Use Granola for follow-up context around:

- yesterday's meetings
- today's accounts and meetings
- recently discussed blockers
- promised follow-ups and next steps
- recurring customer themes

If Granola exposes a next-call brief for an event or account, elevate it into the external-meetings, risks, or recommended-actions sections. Label it as Granola-derived context.

Do not overstate title-only, note-only, or stub results. If Granola has no usable content for a relevant meeting, say so only when it materially affects confidence.

### 5. Pull Gmail And Drive Signals

Use Gmail to find unresolved or unanswered customer/account items relevant to today. Always search both inbound and sent/outbound mail before classifying a follow-up as open.

Look for:

- inbound customer asks without a meaningful reply
- promised Folloze follow-ups not visibly completed
- customer dependencies still waiting
- teammate blockers that affect customer commitments
- meeting logistics only when they change timing or readiness
- sent messages by the teammate or a Folloze teammate that satisfy a Granola/Gmail follow-up

Use Google Drive only for targeted account or meeting artifacts. Avoid broad Drive archaeology. Prefer current docs, handoff notes, QBRs, renewal docs, and account plans when they are clearly relevant.

### 6. Optional CSM Or Account MCPs

If the teammate has role-specific MCPs such as Gainwell, use them only as read-side enrichment for account health, customer success risk, renewal context, or implementation blockers.

Label optional-source signals clearly and do not fail the run if the optional source is unavailable.

### 7. Identify Candidate Tasks And Verify Completion

Create candidate tasks from Granola and Gmail first, then optional sources. Before anything appears in the final task list, verify whether it was already completed.

Read `references/task-verification.md` when candidate tasks come from yesterday's meetings, prior-day follow-ups, or email commitments.

Treat a candidate as completed when there is matching outbound evidence after the task was created, including:

- the teammate sent the promised follow-up
- another Folloze teammate sent it and the current teammate was cc'd
- the sent message includes the promised artifact, pricing, recording, recap, resource link, or next-step ask
- the recipient list matches the relevant customer/prospect/account thread

Examples:

- If Granola says Luke should send Aprio pricing, and Gmail shows Luke sent the Aprio pricing email while cc'ing the teammate, do not list it as an open task.
- If Granola says the teammate should send Power Digital/G&A partner resources, and Gmail shows the teammate sent the partner portal, deck, recording, and contracting-route note, do not list it as an open task.

Include only tasks that are:

- explicitly assigned to the teammate
- implied by a customer ask or Folloze commitment
- unresolved or not clearly completed
- relevant to today's meetings, owned accounts, pipeline movement, renewal risk, or follow-up hygiene

Exclude tasks with clear completion evidence. When useful, mention completed-but-important follow-ups under `Signals, risks, and blockers` as "completed; now waiting on customer/next step" rather than listing them as tasks.

For each task, include:

- short action
- account or meeting when known
- owner if not the teammate
- source
- due date or urgency when available
- completion check status if evidence was thin or ambiguous

### 8. Write The Brief

Use this section order:

1. Priorities
2. External meetings
3. Overview
4. Pipeline
5. Signals, risks, and blockers
6. Recommended next-step actions
7. Task list

Use `templates/output-template.md` as the shape. Keep the brief concise enough to scan quickly. Prefer a few sharp bullets over long inventories.

### 9. Reality Check

Before finalizing, check:

- Calendar claims are supported by retrieved Folloze calendar events.
- External meetings are not polluted with personal/admin/internal-only events.
- Pipeline claims are grounded in Salesforce owned-opportunity/account data.
- CSM account grouping is used when multiple opportunities share an account.
- Granola claims come from substantive notes or next-call brief content, not stubs.
- Gmail and Granola task candidates were checked against sent/outbound messages before being listed as open.
- Completed follow-ups are not listed as open tasks just because they were mentioned in yesterday's meeting notes.
- Any missing source is called out as a caveat.
- No write action is proposed as already performed.

## Output Rules

- No markdown tables.
- No delivery outside the Codex inbox/thread in v1.
- No raw tool logs.
- No invented meetings, opportunities, tasks, owners, or next steps.
- Use concrete dates and local times.
- Keep source caveats short and grouped at the end only when needed.
- If nothing material is found, still return the brief with honest empty-state language.

## Done Criteria

The morning brief is acceptable when it:

- uses live date/time
- covers Folloze calendar
- covers Salesforce owned opportunities grouped by account
- uses Granola follow-up context or states the caveat
- checks Gmail for unresolved customer tasks
- includes the seven required sections
- recommends concrete next actions
- stays read-only
- is suitable for Codex inbox reading
