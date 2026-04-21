---
name: sales-to-cs-internal-handoff-folloze
description: Run the Folloze post-close Sales to Customer Success onboarding workflow for a closed-won customer. Use when the user manually triggers /Sales-to-CS-Internal-Handoff or asks for a sales to CS internal handoff using a deal notes Google Doc link and a Salesforce Opportunity link. Gather context from Salesforce, Granola, Gmail, Google Drive, signed order forms, and linked deal documents; create the internal handoff Google Doc, submit the instance request form, update or create the onboarding kickoff deck, store the final artifacts in the customer Google Drive folder, and share the final links in Slack.
---

# Sales To Cs Internal Handoff Folloze

## Overview

Use this skill for closed-won Folloze customers when Sales is handing the account to Customer Success and onboarding.

Bias toward current signed reality, not the largest sales-cycle vision. Always produce a Google Doc handoff, always submit the Google instance request form, always update or create the onboarding kickoff deck, and always end with a Slack handoff that links the core artifacts.

## Required Inputs

- The canonical deal notes Google Doc link
- The Salesforce Opportunity link

Optional but useful:

- A known onboarding kickoff deck link if one already exists
- A known contract or order form link if the user already has it
- A known customer Slack channel if the team already uses one

## Workflow

### 1. Resolve the opportunity and working window

1. Read the Salesforce Opportunity first. Treat Salesforce as the system of record.
2. Capture at minimum:
   - account name
   - account domain
   - opportunity created date
   - close date / stage
   - signed contract state
   - current signed package / plan
   - creator and collaborator counts if present
3. Set the Gmail lookback window to the age of the opportunity.
   - 180-day-old opportunity -> search the last 180 days of email
   - 60-day-old opportunity -> search the last 60 days of email
4. Normalize the account name and domain before searching other systems.

### 2. Gather the source pack

Treat the canonical deal notes doc as the entrypoint to the rest of the deal context.

Collect from all of these:

1. Salesforce Opportunity
2. Canonical deal notes Google Doc
3. Linked docs inside the deal notes doc
4. Customer Google Drive account folder
5. Granola meetings
6. Gmail threads and attachments
7. Signed order form / contract artifacts

Use these source rules:

- Deal notes doc is the canonical Google doc for the deal.
- Linked docs inside the deal notes doc should be read when they contain relevant scope, onboarding, pricing, legal, security, or use-case context.
- Granola search should include both:
  - account name matches
  - participant email domain matches
- Gmail search should include:
  - any thread containing the customer domain
  - any linked-doc references that appear in the deal notes
  - signed order form / contract emails and attachments
- If the signed order form exists only in Gmail, move or upload it into the customer Drive folder before finishing.

If sources disagree:

1. Signed contract / order form
2. Salesforce Opportunity
3. Most recent email thread with commercial confirmation
4. Granola meeting evidence
5. Earlier planning docs

### 3. Build the normalized account summary

Before writing anything, extract and normalize:

- confirmed champion
- confirmed admin users
- likely collaborators
- signed scope
- excluded scope
- priority use cases
- first priority campaign
- current tech stack
- integrations included in contract
- launch timing
- subdomain needs
- current blockers, dependencies, and open questions
- best-supported upsell or cross-sell ideas

Always separate:

- `Current Signed Scope`
- `Sales-Cycle Expansion Ideas`

Do not blur them together.

### 4. Create the CS handoff Google Doc

Always create a Google Doc in the customer Drive folder.

Use the structure in [references/handoff-doc-template.md](references/handoff-doc-template.md).

Required content:

- internal, operational tone
- current signed scope
- excluded scope
- priority use cases
- first priority campaign
- confirmed users and likely collaborators
- implementation notes
- blockers and dependencies
- integrations in scope
- expansion ideas
- audit log

The audit log must sit at the bottom of the doc and include:

- sources referenced
- artifacts created
- assumptions made
- missing data
- failures or hiccups during execution

### 5. Submit the instance request form

The form is always part of this workflow for customer creation.

Use [references/instance-request-form.md](references/instance-request-form.md) and prefer the helper script at [scripts/submit_instance_request.py](scripts/submit_instance_request.py).

Rules:

- Fuzzy-match the plan to starter / professional / premium.
- If you cannot tell, default to `Professional`.
- Use only confirmed admin users.
- Default collaborator count to `0` unless the signed contract says otherwise.
- Select integration fields only if integrations are included in the signed contract.
- If integrations are included, select every matching integration box that appears in the company tech stack from the deal notes.
- Subdomain should generally be `Yes`.
- Exact subdomain value will often be `TBD` unless explicitly confirmed in email or calls.

If the form itself is ambiguous or a required form-specific field cannot be supported with a best guess, stop and ask only those form questions.

### 6. Update or create the onboarding kickoff deck

Always update or create the onboarding kickoff presentation and store it in the customer Drive folder.

Use this order:

1. If the user provided a deck link, update that deck.
2. Otherwise, search the customer Drive folder for an existing onboarding kickoff deck.
3. Otherwise, discover the standard template.
4. If the template still cannot be found, create a clean internal kickoff deck and note the gap in the audit log.

Use [references/kickoff-deck-guidance.md](references/kickoff-deck-guidance.md).

Always include:

- customer overview
- current signed scope
- priority use cases
- first priority campaign
- confirmed onboarding team / customer team
- launch assumptions
- dependencies and open questions

### 7. Post the artifact bundle in Slack

At the end of the workflow, ensure there is a customer Slack channel if your available Slack tools support channel discovery and creation.

If channel tooling exists:

1. Check whether a customer Slack channel already exists.
2. Create one if needed.
3. Post a concise internal handoff message with links.

Always include links to:

- deal notes
- Salesforce Opportunity
- contract / signed order form
- CS handoff Google Doc
- onboarding kickoff deck

If Slack channel creation is unavailable in the current environment:

- note the limitation in the audit log
- still return the exact artifact bundle and a Slack-ready summary in the final response

### 8. Done definition

This skill is done only when all of these are true:

1. The instance request form has been submitted.
2. The CS handoff Google Doc exists in Google Drive.
3. The onboarding kickoff deck exists or has been updated in Google Drive.
4. The final Google Drive links are available.
5. The artifact bundle has been shared in Slack, or a clear Slack-tooling limitation has been documented.

## Decision Rules

- Bias toward current signed reality over broad strategy decks.
- Always list at least one upsell or cross-sell idea when there is enough evidence to support it.
- Present best-supported ideas directly; do not label confidence unless the user asks.
- Infer a best guess when that is operationally safe.
- Leave fields blank when guessing would be misleading.
- Use Codex connectors first.
- Use CLI fallbacks when connectors are missing, blocked, or insufficient.
- Support Google CLI, raw HTTP form submission, local scripts, Salesforce CLI, and other APIs when needed.
- Web search is optional and should only be used for missing external context, never to override source-of-truth deal artifacts.

## Remaining Human Questions

Only stop to ask questions when one of these is true:

- the instance request form needs a value that cannot be safely inferred
- the Salesforce Opportunity cannot be read
- the customer Drive folder cannot be found
- the signed order form cannot be located
- the kickoff deck template cannot be found and no acceptable fallback can be created

Do not stop just because the handoff doc or kickoff deck requires reasonable synthesis.

## Resources

- Workflow details: [references/workflow.md](references/workflow.md)
- Handoff doc structure: [references/handoff-doc-template.md](references/handoff-doc-template.md)
- Instance request form mapping: [references/instance-request-form.md](references/instance-request-form.md)
- Kickoff deck guidance: [references/kickoff-deck-guidance.md](references/kickoff-deck-guidance.md)
- Form submission helper: [scripts/submit_instance_request.py](scripts/submit_instance_request.py)
