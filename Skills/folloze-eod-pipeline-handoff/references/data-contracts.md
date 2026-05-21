# Data Contracts

Use this reference when selecting fields from Salesforce or local fallback artifacts.

## Config

Optional environment variables:

- `FOLLOZE_PRIMARY_USER_EMAIL`
- `FOLLOZE_PRIMARY_USER_NAME`
- `FOLLOZE_TIMEZONE`
- `FOLLOZE_DEAL_INDEX_PATH`
- `FOLLOZE_DAILY_SYNC_DIR`
- `ENABLE_GRANOLA`
- `ENABLE_GMAIL`
- `ENABLE_SLACK`
- `ENABLE_SALESFORCE`
- `WRITE_MODE`

`WRITE_MODE` must be treated as false unless the host explicitly enables it. This skill's default behavior remains read-only.

## Salesforce Opportunity Fields

Minimum useful fields:

- opportunity id
- opportunity name
- owner name and owner email
- account id and account name
- stage
- amount
- close date
- forecast category
- probability
- last activity date
- next step or Folloze custom next-step field when available
- created date and last modified date when useful

Preferred query behavior:

- query open opportunities owned by the current Salesforce user
- group by account for account-level action and risk review
- preserve exact close dates and last activity dates
- do not write opportunity updates from this skill

## Legacy Deal-Index Shape

Legacy local deal-index files may appear as top-level metadata plus a `deals` map.

Each deal record can include:

- `status`
- `name`
- `account`
- `domain`
- `sf_opportunity_id`
- `sf_stage`
- `sf_amount`
- `sf_close_date`
- `sf_last_activity`
- `sf_probability`
- `sf_forecast_category`
- `sf_synced_at`
- `next_step`

Counting rules:

- active deals have `status == "active"` or no closed/lost status marker
- Salesforce-linked deals have `sf_opportunity_id`
- stale sync lowers confidence; it does not prove pipeline risk by itself

## Daily-Sync Shape

Daily-sync JSON can include:

- extracted tasks
- carryover items
- company/account map
- calendar summary
- email summary
- meeting summary

Use it as candidate evidence only. Verify open/completed state against live Gmail, Granola, Slack, or Salesforce when possible.

## Pipeline Risk Signals

High-signal risks:

- close date already past
- close date in next 7 days and activity is stale
- customer meeting today with no captured follow-up
- active opportunity has a Folloze-owned action item open
- Proposal, validation, or Best Case opportunity has stale activity or missing next step
- high-value opportunity has no clear owner, next step, or customer dependency

Lower-confidence risks:

- old gap report says the account is risky
- local deal-index data is stale
- meeting title exists but no notes or email evidence exist

Label lower-confidence risks as directional.
