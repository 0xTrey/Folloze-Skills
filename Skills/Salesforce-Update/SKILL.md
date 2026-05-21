---
name: Salesforce-Update
description: Manually reconcile Salesforce open opportunities from Gmail, Google Calendar, and Granola evidence, then write validated non-stage updates through Salesforce CLI-backed auth with local logging. Use when a rep wants to review manual stage recommendations and update next steps, amount, summary, red flags, contact roles, and MEDDPICC fields over the last 72 hours, last week, or all open deals.
---

# Salesforce Update

This skill is manual-only.
Use Gmail, Google Calendar, and Granola connectors for read-side evidence and the local helper at `${CODEX_HOME:-$HOME/.codex}/skills/Salesforce-Update/scripts/salesforce_update.py` for Salesforce candidate export, plan validation, and writes.

Opportunity stage updates are paused and manual-only.
Do not write `StageName` from this skill.
When evidence suggests a stage change, include it as a manual recommendation in the end-of-run summary or run notes instead of putting `StageName` in `plan.json`.

Do not silently create new opportunities.
If unmatched activity looks like a new deal, present it as a create candidate and ask the rep before any new opportunity is created.

## Prerequisites

1. Confirm local config and Salesforce auth
- Run: `python3 "${CODEX_HOME:-$HOME/.codex}/skills/Salesforce-Update/scripts/salesforce_update.py" check-deps --json`
- Config path defaults to `~/.config/salesforce-update/config.json`
- Read `${CODEX_HOME:-$HOME/.codex}/skills/Salesforce-Update/references/config.md` before creating or editing config.

2. Confirm connectors are available for this session
- Gmail connector
- Google Calendar connector
- Granola connector

## Workflow

1. Initialize a run
- Default 72h run: `python3 "${CODEX_HOME:-$HOME/.codex}/skills/Salesforce-Update/scripts/salesforce_update.py" init-run --json`
- Last week: `python3 "${CODEX_HOME:-$HOME/.codex}/skills/Salesforce-Update/scripts/salesforce_update.py" init-run --lookback-hours 168 --json`
- All open: `python3 "${CODEX_HOME:-$HOME/.codex}/skills/Salesforce-Update/scripts/salesforce_update.py" init-run --all-open --json`

2. Read the generated run files
- `context.json` contains:
  - candidate opportunities for the chosen lookback
  - a lightweight all-open index for unmatched-activity matching
  - current contact roles
  - relevant field metadata including stage and competition picklist values
- `plan.json` is the file to fill before applying updates.

3. Review candidate opportunities first
- Start from candidate opps, not from raw inbox/calendar activity.
- Use the all-open index only for the unmatched hybrid pass.
- After the candidate-opportunity pass, run a sent-mail sweep for the lookback window against all open opportunities.
  - Search `in:sent` mail for the lookback window and match outbound threads to open opp contact-role emails first, then to account domains when the contact-role match is missing.
  - If a same-day outbound email clearly belongs to an existing open opportunity, add that opportunity to the working set even if it was not included in the initial candidate list.
  - Treat this as an existing-opportunity evidence pass, not a reason to create new opportunities automatically.
- Before planning any update, do an account-level sanity check for recently created blank opps.
  - Treat a candidate as suspicious if it was created within the current lookback window, still has blank core fields, or looks auto-generated (`Renewal for ...`, duplicate `Agency (Direct) ...`, null `LeadSource`, no summary, no next step, no contact roles).
  - If the same account also has a recently modified or recently `Closed Won` opportunity, assume the new blank opp may be an auto-created renewal/duplicate and do not update it from current activity unless the evidence explicitly belongs to that new opp.
  - When this happens, prefer the established opportunity or mark the record for manual review instead of writing to the blank auto-created opp.

4. Gather evidence with connectors
- Gmail:
  - Search inbox and sent mail for matching contacts, domains, and account names.
  - Include same-day outbound email context in the summary block.
  - When the user explicitly asks to capture outbound follow-up activity, do not stop at the candidate set; sweep today's sent mail against the all-open index and write matched open opportunities when the email is substantive and clearly tied to the deal.
- Google Calendar:
  - Read matching events and attendees.
  - External attendees are eligible for contact creation and opportunity contact-role association.
  - For any opportunity still in `Meeting Booked`, treat the scheduled first external intro/discovery event as a manual stage-review check, not as authorization to write a stage change.
  - Before recommending a move out of `Meeting Booked`, confirm both:
    - the relevant first external intro/discovery calendar event is in the past
    - a matching Granola note exists for that call
  - If the event is in the past and there is no matching Granola note, search Gmail for reschedule/cancellation evidence before making any stage decision.
  - If the event is in the past, there is no reschedule/cancellation evidence, and there is still no Granola note, list it as a manual stage decision and ask the user what stage the opportunity should be in. Do not include `StageName` in the plan.
- Granola:
  - Read meeting notes and summaries for the same opportunity.
  - Granola is a dependency for this skill.
  - If the remote `query_granola_meetings` connector fails or times out, retry once, then fall back to the local Granola path on this machine before giving up:
    - `granola search "<account or keyword>" --days 30 --json`
    - `granola full <doc_id> --json`
  - Only fall back to email/calendar-only reasoning after both the remote connector and the local Granola path fail.

5. Apply manual stage-review and field rules
- Stage updates are paused and manual-only for this skill.
- Never include `StageName` in `plan.json`; the helper rejects stage writes while the pause is active.
- Use the stage rules below only to classify manual recommendations and blocked/manual follow-up items.
- Recommended stage flow is forward-only.
- Default start stage is `Meeting Booked`.
- Keep an opportunity in `Meeting Booked` while the first external intro/discovery call is only scheduled and has not yet happened.
- Recommend `Meeting Booked -> S0` only after the first external intro/discovery call has completed and that completion is double-verified:
  - the scheduled calendar event is in the past
  - a matching Granola note exists
- Never use a booked future meeting by itself as justification to recommend moving an opportunity from `Meeting Booked` to `S0`.
- If the scheduled first call is in the past but no Granola note is found:
  - first check Gmail for clear reschedule/cancellation evidence
  - if the meeting was rescheduled or cancelled, keep the manual recommendation at `Meeting Booked` and update only the scheduling fields if needed
  - if there is no reschedule/cancellation evidence, ask the user what stage the opportunity should be in rather than recommending an automatic move
- If the first external intro/discovery call has actually happened and passed the double-verification check, report a manual recommendation to move the opportunity to at least `S0`.
  - If the opportunity was still at `Meeting Booked`, flag the manual stage follow-up after the call occurs and the completion is verified.
  - Treat stage progression and deal quality as separate questions. A weak first call can still justify a manual `Identify` recommendation while being called out as low-quality or non-viable in the written fields.
- Recommend `Identify -> Discovery` when meaningful buying motion exists, especially if two or more are true:
  - named project or named program
  - identified budget or pricing discussion
  - competitor or incumbent mentioned
  - multiple external attendees
  - clear follow-up meeting scheduled
  - manager or broader team expected on the next call
- Recommend `Discovery -> Solution Development` only after the second call has actually happened.
- Recommend `Solution Development -> Proposal` when pricing/proposal/order-form documentation is shared or actively being prepared.
- Recommend `Proposal -> Validation` when procurement, legal, privacy, security, or process review is underway before final contract agreement.
  - before recommending `Validation` or later, confirm `Customer_Executive_Sponsor__c` is identified and populated on the opportunity
- Recommend `Validation -> Contract` when the final contract is agreed and sent for signature.
- Do not recommend moving stages backward.
- Do not auto-create `Closed Won`, `Closed Lost`, or new opportunities in this skill.

6. Apply write rules
- Do not write standard `NextStep`.
- Write the custom MEDDPICC next-step field `Next_step__c` only.
- Format `Next_step__c` as `INITIALS - date - next step note`.
  - Example: `TH - 5/21/26 - Send recap and confirm next working session.`
  - Use the rep initials, the update date, and a concrete next-step note.
  - Replace the field with the latest current next step; do not use it as a running history log.
- `Amount`:
  - early-stage call-note numbers are allowed
  - email-shared numbers trump call-note numbers
  - ambiguous numbers should be left unchanged
- `Summary__c`:
  - prepend newest dated block at the top
  - preserve older blocks below
  - include date, rep initials, and whether the update came from call, email, or both
  - same-day updates may exceed three sentences if meaningful movement happened
  - logistical emails do not count as meaningful email updates
  - if the only email is a Zoom link, confirmation, scheduling nudge, or similar logistics, label the block as `Call update` or `Calendar update`, not `Call + email update`
  - write bluntly when the call is weak; do not imply validated use cases, identified pain, or real momentum unless the evidence shows it
- `Redflag_s__c`:
  - store red flags here
  - do not duplicate red-flag text into the summary unless useful for human readability
  - use this field when the call was short, no concrete pain was identified, no clear action items were agreed, no follow-up was secured, or the opportunity appears weak/non-viable
- append-style MEDDPICC/custom text fields (`Redflag_s__c`, `Metrics__c`, `Decision_Criteria__c`, `Decision_Process__c`, `Implicate_the_Pain__c`, `Paper_Process__c`, `What_s_New_Changed__c`):
  - do not overwrite the existing box contents
  - add a new dated block while preserving the older notes below
  - default to prepending the newest block at the top, the same way `Summary__c` works
  - use `merge_fields`, not `set_fields`, for these text areas
- `Metrics__c` can be updated when the call surfaces concrete scale or volume numbers.
- `Next_Call_Date__c` should be set when a clear follow-up meeting is already booked.
- MEDDPICC contact lookup fields:
  - must point to external contacts only
  - `Internal_Executive_Sponsor__c` is intentionally out of scope for v1
- `Customer_Executive_Sponsor__c`:
  - is a customer-side external contact lookup
  - must be set before the skill recommends moving an opportunity from below `Validation` into `Validation` or `Contract`
- `Competition__c`:
  - use the exact picklist value when matched
  - otherwise set `Other`
- Save regular opportunity/detail fields separately from MEDDPICC/custom fields.
- `StageName` is intentionally excluded from writes while stage updates are paused.
- Treat `Amount`, `Summary__c`, and `Customer_Executive_Sponsor__c` as the regular/detail save group.
- Treat `Next_step__c`, `Next_Call_Date__c`, MEDDPICC text fields, MEDDPICC lookup fields, `Competition__c`, `Redflag_s__c`, and `What_s_New_Changed__c` fields as the MEDDPICC/custom save group.
- Contacts and contact roles:
  - exclude internal `@folloze.com` attendees
  - when an external attendee is missing in Salesforce, create a `Contact` on the opportunity account
  - set new contact `OwnerId` to the opportunity owner
  - attach the external contact to the opportunity with an `OpportunityContactRole`
  - skip duplicate opportunity-contact-role creation

7. Handle weak first-call outcomes honestly
- If the first call happened but the evidence shows a soft or low-value conversation, still report the manual stage recommendation according to the rule above, but write the opportunity quality honestly.
- Common weak-call signals:
  - actual discussion was brief, roughly under 20 minutes
  - conversation stayed at vendor overview / education level
  - no concrete pain, project, timeline, or action item surfaced
  - no follow-up meeting was booked
  - the prospect framed Folloze as a future resource rather than an active initiative
- In that case:
  - `Summary__c` should say so plainly
  - `What_s_New_Changed__c` should reflect the weak outcome, not a generic product recap
  - `Redflag_s__c` should capture the lack of pain, urgency, or viability
  - leave `Next_step__c` blank unless there is a real, agreed next step; when populated, use `INITIALS - date - next step note`
  - do not treat a Zoom-link email or similar logistics as evidence of opportunity progress

8. Handle unmatched external activity
- After matched-opportunity updates are planned, review unmatched email/calendar/Granola activity.
- Classify unmatched activity into:
  - ignore
  - review only
  - create candidate
- Never auto-create an opportunity.
- Present create candidates to the rep and ask whether a new opportunity should be created.

9. Validate the plan before writing
- Read `${CODEX_HOME:-$HOME/.codex}/skills/Salesforce-Update/references/plan-schema.md`
- Fill `plan.json`
- Validate: `python3 "${CODEX_HOME:-$HOME/.codex}/skills/Salesforce-Update/scripts/salesforce_update.py" validate-plan --run-dir <run_dir> --json`

10. Apply the plan
- Apply: `python3 "${CODEX_HOME:-$HOME/.codex}/skills/Salesforce-Update/scripts/salesforce_update.py" apply-plan --run-dir <run_dir> --json`
- The helper writes local logs into the run directory and returns a concise summary payload.

11. On failure
- Use the Gmail connector to email the configured failure recipient from the authenticated Gmail account.
- Include:
  - run id
  - failing step
  - error summary
  - log path

12. End-of-run response
- Always return a short summary of which opportunities were updated and why.
- Separate manual stage recommendations from fields that were actually written.
- Format should stay brief:
  - `Asana -> manual stage recommendation: Contract; updated signer context, prepended summary`
  - `Zilliant -> no stage movement, prepended red flag and summary`

## Guardrails

- Prefer candidate opportunities over inbox-first scanning.
- Treat the all-open index as a matching aid, not as permission to update everything.
- Do not update a same-day blank renewal or duplicate opp just because it appears in the candidate set.
- If a new blank opp appears on an account with a recent `Closed Won` or another actively updated opp, stop and verify which opportunity the evidence actually belongs to before writing anything.
- Do not overwrite append-style MEDDPICC/custom text fields; prepend a new block instead.
- Do not assign internal contacts to external MEDDPICC lookup fields.
- Do not create contacts for internal Folloze attendees.
- Do not proceed with plan application if validation errors exist.
- Do not write `StageName`; stage movement is manual-only until this pause is explicitly lifted.
