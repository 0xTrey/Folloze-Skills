---
name: monthly-folloze-adoption-reports
description: Run Folloze monthly customer adoption reporting from the Salesforce account roster, Salesforce active contracts/amendments, Gainsight PX user activity, PDF generation, audit manifests, and Slack customer-channel posting. Use when asked to run, test, troubleshoot, schedule, or maintain monthly adoption reports for matched customers, including license reconciliation and channel delivery.
---

# Monthly Folloze Adoption Reports

## Overview

Use this skill to generate one-page Folloze adoption PDFs for the matched customer roster and post each PDF to the correct customer Slack channel. The workflow reconciles paid license denominators from Salesforce active contracts and amendments, then compares them to active licensed users from Gainsight PX over the previous six full calendar months.

## Source Of Truth

- Roster: Google Sheet tab `Salesforce + Gainsight` at `https://docs.google.com/spreadsheets/d/1wfA_AmSj7Phyhe6HnqfxVSLKgt8rXugTfRX3J4tR3TM`.
- Included accounts: current tab 1 rows with a Gainsight Org ID and a confident Slack mapping.
- Excluded accounts: Box and Infinite Edge Consulting unless the user asks to add them back.
- Paid licenses: Salesforce active Contract records, including active main contracts and active amendments.
- License activity: Gainsight PX user export for the previous six full calendar months before the run date.
- Delivery: nearest matched customer Slack channel, using explicit user mappings and the saved posting manifest.

## Monthly Run

1. Read the current Sheet roster and preserve user-confirmed account/Gainsight matches.
2. Query Salesforce active contracts where `Status = Activated`, `StartDate <= run date`, and `EndDate >= run date`.
3. Include the main contract and all active amendments. Aggregate all non-terminated subscription/license lines on those parent active contracts.
4. Do not trust subscription-line `Active__c` or line-level start/end dates by themselves when the parent Contract is active; line metadata can be stale.
5. Classify product names into Creator, Collaborator/Associate User, and general/unclassified license buckets.
6. For Oracle, use the signed Schedule Ten fee schedule from the 2026-06-30 renewal as source of truth for 44 Creator licenses unless a newer signed contract supersedes it.
7. Pull Gainsight PX users by account/org ID for the previous six full calendar months and count active Creator, Collaborator, and unclassified licensed users.
8. Generate a one-page executive PDF per account showing paid licenses, active licensed users, utilization percentage, contract source notes, and CSM action.
9. Create an audit manifest with generated, skipped, posted, link-posted, failed, mapping-needed, active contracts used, license lines used, and no-license-line accounts.
10. Post each PDF to the mapped Slack customer channel. Verify the channel exists and is not archived before posting.
11. If upload succeeds but the file is not shared to the channel, post the PDF permalink in a channel message and mark the account `link-posted`.
12. Do not post ambiguous channel matches. Return a mapping-needed list for the user.

## Local Scripts

The current implementation lives in `/Users/troysmith/Documents/Playground`:

- `batch_adoption_reports.py`: builds PDFs and `manifest.json` from prepared roster, Salesforce contract/subscription exports, contract-document entitlement extraction, and PX user CSV.
- `create_slack_posting_manifest.py`: maps generated PDFs to Slack channels and writes `slack_posting_manifest.json`.

Environment knobs:

- `RUN_DATE`: ISO date/datetime override for test runs.
- `OUT_DIR`: output folder override.
- `PX_USERS_CSV`: Gainsight PX users CSV path override.
- `RECENT_SKIP_NAMES`: comma-separated account names to skip when avoiding reports generated in the prior 48 hours.

## Slack Mappings

Use the saved channel map in `create_slack_posting_manifest.py` and honor these explicit mappings:

- IFS -> `#ifs-copperleaf` (`C0A2F4KM42Z`)
- Schlumberger -> `#schlumberger` (`C03M2PP3UPM`)
- The Marketing Practice -> `#agency-tmp` (`CTBA9048P`)

## Validation

Before calling a run ready, verify:

- The generated manifest count matches the expected included roster count.
- Box and Infinite Edge Consulting are absent unless re-added.
- `slack_posting_manifest.json` has no unmatched accounts.
- Workday, Autodesk, Oracle, Schoox, Capgemini, TELUS, Descartes, TierPoint, Docusign, HP, and Schlumberger are mapped when present.
- PDF header uses the actual run date, not test-run language.
- The activity window is the previous six full calendar months for the run date.
- Salesforce denominators come from active contracts plus active amendments, not stale line-only flags.
