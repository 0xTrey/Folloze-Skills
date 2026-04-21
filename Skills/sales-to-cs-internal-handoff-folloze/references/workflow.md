# Workflow

## Core flow

1. Read Salesforce first.
2. Read the canonical deal notes Google Doc.
3. Open the linked documents inside the deal notes doc when they are relevant.
4. Find the customer account folder in Google Drive.
5. Gather Granola context using both:
   - account name
   - participant email domain
6. Gather Gmail context using the customer domain and the opportunity-age lookback window.
7. Locate the signed order form or contract. If it only exists in Gmail, move or upload it into the customer Drive folder.
8. Normalize the account summary.
9. Create the CS handoff Google Doc in the customer Drive folder.
10. Update or create the onboarding kickoff deck in the customer Drive folder.
11. Submit the instance request form.
12. Post the final artifact bundle in Slack.

## Source precedence

Use this order when sources disagree:

1. Signed order form or contract
2. Salesforce Opportunity
3. Most recent commercial confirmation thread
4. Granola evidence
5. Earlier planning docs

## Artifact checklist

The final artifact bundle should include links to:

- canonical deal notes Google Doc
- Salesforce Opportunity
- signed contract or order form
- CS handoff Google Doc
- onboarding kickoff deck

## Required extracted fields

Extract these before writing:

- customer name
- customer domain
- opportunity age window
- champion
- confirmed admin users
- likely collaborators
- signed plan / package
- creator count
- collaborator count
- launch date or best-supported working date
- custom subdomain need
- exact subdomain if known
- integrations in scope
- tech stack
- priority use cases
- first priority campaign
- blockers
- onboarding dependencies
- upsell / cross-sell ideas

## Practical defaults

- If the plan is unclear, default to `Professional` for the instance form.
- If collaborator count is unclear, default to `0`.
- If subdomain is not explicit, assume `Yes` and set the value to `TBD` unless that would be misleading.
- If launch date is not explicit, infer a best-supported working date from recent calls or emails.
- If the signed scope excludes integrations, do not check integration boxes in the form.

## Write discipline

Always keep customer-facing artifacts and internal artifacts in the customer Drive folder.

Always keep the CS handoff document strictly internal and operational.

Always separate:

- current signed scope
- expansion ideas from the sales cycle

Never present future expansion as current entitlement.
