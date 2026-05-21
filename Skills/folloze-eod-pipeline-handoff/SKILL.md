---
name: folloze-eod-pipeline-handoff
description: Build the daily read-only Folloze end-of-day pipeline handoff for the current Codex user, blending the operating recap, pipeline risk snapshot, and customer/team action-item ledger across calendar, Salesforce, Granola, Gmail, Slack, Google Drive, daily-sync artifacts, and optional legacy deal-index context. Use when a teammate asks for an EOD handoff, pipeline risk snapshot, tomorrow priorities, open customer action items, unresolved follow-ups, or when the Folloze EOD Pipeline Handoff Codex automation runs.
---

# Folloze EOD Pipeline Handoff

Generate one daily Folloze GTM end-of-day handoff for the current authenticated teammate. The handoff is individual, read-only, and delivered in the Codex inbox/thread by the host automation.

## Defaults

- Audience: the current Codex user, not Trey by default.
- Team scope: Folloze GTM teammates who use the shared Codex setup.
- Schedule: local weekday end-of-day run at 11:00 PM, or as soon as Codex can run after the machine wakes.
- Window: today from 00:00 through run time in the teammate's local time zone. Default timezone is `America/Chicago` unless `FOLLOZE_TIMEZONE` or the host context says otherwise.
- Delivery: Codex inbox/thread only.
- Mode: strictly read-only and report-only. Do not write to Salesforce, Gmail, Granola, Drive, Slack, or any customer system.
- Tone: chief of staff: concise, operational, evidence-aware, and action-oriented.
- Final output: no markdown tables.

## Source Expectations

Use live connected sources when available:

1. Folloze work calendar for today's external meetings and tomorrow's constraints.
2. Salesforce for open opportunities owned by the current Salesforce user.
3. Granola for same-day meeting notes, follow-ups, commitments, blockers, and next-call context.
4. Gmail for inbound asks, outbound completion evidence, customer dependencies, and follow-up state.
5. Slack for internal customer-action threads and blockers when available.
6. Google Drive for targeted account artifacts only when needed.
7. Daily-sync or legacy deal-index artifacts only as optional local context when present.

Salesforce is the preferred pipeline source. Legacy deal-index or daily-sync artifacts are fallback/enrichment sources, not the source of truth when Salesforce is available.

If a source is unavailable, say what coverage is incomplete. Do not turn a source failure into a false negative.

## Automation Setup

When this skill is installed or synced for a teammate, create or update the local Codex automation from `AutomationTemplates/folloze-eod-pipeline-handoff-daily/template.json`.

The automation should:

- run locally on weekdays at 11:00 PM in the teammate's local time zone
- deliver to the Codex inbox/thread
- use this skill as the runbook
- run read-only
- continue with caveats when a connector is unavailable

Codex automations can only run when the local environment is available. If the teammate wants the Mac to wake before the run, that is a local OS power setting and should be configured explicitly by the teammate or IT; do not change machine power settings without approval.

## Workflow

### 1. Establish Time Window And User

- Use live system date/time.
- Identify the current teammate from the connected Codex account, calendar account, Gmail account, or Salesforce user profile.
- Resolve the reporting timezone from `FOLLOZE_TIMEZONE`, the host locale, or `America/Chicago`.
- If the run happens before mid-afternoon, label the output as an in-progress operating snapshot.

### 2. Gather Same-Day Operating Evidence

Collect bounded context for today:

- today's Folloze work calendar events and tomorrow's external meetings
- same-day Granola meetings and action items
- Gmail threads tied to today's accounts, meetings, and follow-ups
- Slack threads or DMs tied to customer/account action items when available
- daily-sync markdown/JSON if the teammate has that local artifact
- targeted Drive docs only when they are clearly tied to today's account context

Classify movement as customer/deal movement only when evidence shows a customer, partner, prospect, pipeline, renewal, blocker, or account action changed. Do not treat automation maintenance, source retrieval, or internal setup work as deal progress unless it unblocked customer execution.

### 3. Build The Account List

Merge candidate accounts from:

- today's external meetings
- Granola meeting titles, attendees, and notes
- Gmail sender/recipient domains and subjects
- Slack channel names, mentions, DMs, and threads
- Salesforce opportunity account names
- daily-sync companies map or legacy deal-index names when available

Normalize obvious variants into one account label, such as `okta`, `okta.com`, and `Okta Inc.` becoming `Okta`. Prefer the customer-facing company name over a raw domain.

### 4. Extract And Verify Action Items

Use the account-action method from `weekly-customer-action-items`, but apply it to the daily window plus unresolved carryover.

Read `references/action-ledger.md` when extracting, deduplicating, or status-labeling action items.

Candidate action items can come from:

- explicit Granola action items, commitments, blockers, and next steps
- Gmail customer asks, promised follow-ups, unanswered requests, and sent completion evidence
- Slack customer-action threads, blockers, and owner handoffs
- Salesforce next steps, close-date urgency, or customer dependencies
- daily-sync extracted tasks or carryover items when present

Before listing an item as open, check for completion evidence after the ask:

- sent recap or deliverable
- sent pricing, deck, resource link, recording, or portal access
- Slack thread resolution
- later Granola note marking the item done
- customer or owner confirmation

If completion is uncertain, keep the item cautious: `Potentially open - no completion evidence found`.

### 5. Build Pipeline Risk Snapshot

Use Salesforce open opportunities owned by the current Salesforce user. If Salesforce is unavailable and a local deal-index artifact exists, use it as a fallback and label the lower confidence.

Read `references/data-contracts.md` when selecting source fields or using local fallback files.

For each opportunity or account, assess:

- close date in the past or next 7/14/30 days
- no recent activity
- missing next step
- high-value opportunity with stale activity
- proposal, validation, solution-development, discovery, or meeting-booked stage with no clear next action
- Best Case or Commit forecast with stale activity
- same-day customer meeting with no captured follow-up
- open Folloze-owned action item tied to an active opportunity

Limit the final `Pipeline risk snapshot` to the 3-7 highest-signal risks. Link risks to action items when possible.

If a local legacy deal-index file is present, `scripts/summarize_pipeline_context.py` can produce a compact fallback risk summary. Use the script only as support; do not load large local JSON files directly into the final answer.

### 6. Decide Tomorrow's Priorities

Prioritize tomorrow by:

1. customer-impacting Folloze-owned action items
2. active opportunity close-date risk
3. blockers needing teammate, manager, or executive decision
4. tomorrow external meetings
5. stale internal dependencies that block customer delivery

Limit final priorities to 3 unless a true exception requires more.

### 7. Write The Handoff

Use this section order:

1. Today in one paragraph
2. Moved forward today
3. Pipeline risk snapshot
4. Open customer/team action items
5. Blockers / unresolved items
6. Tomorrow's priorities
7. What `<teammate>` should personally watch

Use `templates/output-template.md` as the shape. Keep it concise enough to read quickly in the Codex inbox.

### 8. Reality Check

Before finalizing, check:

- Calendar claims are supported by retrieved Folloze calendar events.
- Completed items have completion evidence.
- Open items have no clear completion evidence.
- Customer/deal progress is separated from internal automation/admin work.
- Pipeline risks are supported by Salesforce or clearly labeled fallback data.
- Action items are deduped across Granola, Gmail, Slack, and Salesforce.
- Owners are explicit or marked `Unclear`.
- Missing/stale sources are called out as caveats.
- No write action is proposed as already performed.

## Output Rules

- No markdown tables.
- No delivery outside the Codex inbox/thread in v1.
- No raw tool logs.
- No invented meetings, opportunities, tasks, owners, or completion states.
- Use concrete dates and local times.
- Keep private email and Slack evidence compact; summarize instead of pasting long threads.
- Preserve citations or links where the connector provides them.
- Ignore promotional, newsletter, bulk, auto-reply, and pure calendar-logistics messages.
- If nothing material is found, still return the handoff with honest empty-state language.

## Done Criteria

The EOD handoff is acceptable when it:

- uses live date/time and a clear reporting window
- summarizes actual same-day operating movement
- includes a Salesforce-grounded pipeline risk snapshot or a clearly labeled fallback
- includes a deduped action-item ledger grouped by account
- checks completion evidence before listing items as open
- recommends tomorrow's top priorities
- stays read-only
- is suitable for Codex inbox reading
