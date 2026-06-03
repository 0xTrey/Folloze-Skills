---
name: Folloze-Customer-Watchlist
description: Identify Folloze customers with recently signed contracts and upcoming renewals from Salesforce. Use when a recurring weekly review should find accounts signed within the last 120 days and accounts renewing within the next 30 days.
---

# Folloze Customer Watchlist

Use the local helper at `scripts/folloze_customer_watchlist.py` to build a concise customer brief from Salesforce customer accounts.

## Prerequisites

1. Confirm Salesforce CLI access
- Run: `sf org list --json`
- Default org alias is `folloze-prod`

## Workflow

1. Run the helper
- Default weekly run:
  `python3 scripts/folloze_customer_watchlist.py --org folloze-prod`
- JSON output if needed:
  `python3 scripts/folloze_customer_watchlist.py --org folloze-prod --json`

2. When the task includes writing to Google Sheets
- Prefer the wrapper:
  `python3 scripts/generate_watchlist_sheet_payload.py --org folloze-prod`
- The wrapper emits exact artifacts for the sheet write:
  - `runs/history_append.tsv` for rows to append into `Weekly History`
  - `runs/snapshot.tsv` for the full replacement contents of `Current Snapshot`
  - `runs/watchlist_rows.json` for structured inspection if needed
- Use those generated files as the only source for the sheet write.
- Append `history_append.tsv` to `Weekly History`.
- Replace `Current Snapshot` completely with `snapshot.tsv`.
- After writing, read back the first rows of `Current Snapshot` and the most recent rows of `Weekly History` to verify the update landed.

3. Interpret the two sections
- `Signed in last 120 days` uses Salesforce `Account.Contract_Start_Date__c`, but only when that date matches the account's first-ever contract start date with Folloze.
- `Renewing in next 30 days` uses Salesforce `Account.Contract_Renewal_Date__c`.

4. Return a brief that is easy to scan
- Keep the response short.
- Group the output into the two requested sections.
- Include account name, relevant date, day offset, type, and CSM when present.

## Guardrails

- Treat the Salesforce account report fields as the source of truth for both sections.
- Exclude accounts from the recent-start section when the account start date is not the first contract start date found for that account in Salesforce.
- Do not infer dates from opportunity pipeline or signature fields.
- If writing to Sheets, do not stop after generating the payload files. The run is incomplete until the sheet write and verification reads succeed.
- If Salesforce auth fails or the query errors, report the blocker clearly.
