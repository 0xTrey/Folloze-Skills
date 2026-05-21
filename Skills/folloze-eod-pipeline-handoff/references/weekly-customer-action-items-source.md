# Weekly Customer Action Items Source Pattern

The `weekly-customer-action-items` skill is the source pattern for the action ledger. This EOD skill uses the same model with a shorter reporting window and generic ownership.

Reusable behavior:

- gather action items from Granola, Gmail, and Slack
- include explicit action items and implied follow-ups or commitments
- include unresolved states: open, unanswered, blocked, waiting on customer, waiting on Folloze, waiting on teammate
- deduplicate repeated items across sources
- group final output by customer account
- label ownership and status
- ignore promotional, newsletter, bulk marketing, auto-reply, and logistics-only messages
- exclude completed items when completion evidence is clear

Differences in the EOD version:

- the default window is today through run time, not Monday-Friday
- the primary teammate is the current authenticated user, not a hardcoded person
- Salesforce opportunity risk is integrated into prioritization
- completed same-day follow-ups can appear under `Moved forward today`
- open action items can influence `Pipeline risk snapshot` and `Tomorrow's priorities`
