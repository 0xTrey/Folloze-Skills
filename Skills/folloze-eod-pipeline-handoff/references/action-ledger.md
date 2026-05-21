# Daily Action-Item Ledger

Use this reference when turning Granola, Gmail, Slack, Salesforce, and daily-sync evidence into the handoff's `Open customer/team action items` section.

## Window

- Default daily EOD window: today from 00:00 through run time in the reporting timezone.
- Include unresolved carryover from prior days only when it remains open or became relevant today.
- If a weekly mode is requested, use the `weekly-customer-action-items` skill directly.

## Candidate Sources

Granola:

- same-day customer-related action items
- follow-ups, commitments, blockers, and unresolved next steps
- next-call brief content when available
- title-only meetings count as meeting evidence, not action-item proof

Gmail:

- inbound customer asks without a meaningful reply
- sent follow-ups that prove completion
- customer dependencies still waiting
- teammate handoffs that affect customer commitments
- ignore promotional, newsletter, bulk, auto-reply, and calendar-logistics-only mail

Slack:

- DMs and threads with account/customer action terms
- unanswered internal questions that block customer delivery
- in-channel owner handoffs
- thread resolution or explicit done signals

Salesforce:

- next steps
- close-date urgency
- stale opportunities
- customer dependencies or missing owners

Daily-sync or local artifacts:

- extracted tasks
- carryover items
- companies map
- use as candidate evidence only, then verify against live sources when possible

## Ownership

Use the strongest available ownership signal:

1. explicit owner named in notes, Slack, or email
2. person making the commitment
3. person being directly asked
4. owner bucket fallback

Owner values:

- named person, such as `Trey`, `Meghan`, or `Luke`
- `Folloze`
- `Customer`
- `Teammate`
- `Shared`
- `Unclear`

## Statuses

Use consistent statuses:

- `Needs Folloze reply`
- `Waiting on customer`
- `Waiting on teammate`
- `Blocked`
- `Owner unclear`
- `Potentially open - no completion evidence found`
- `Completed`

Exclude completed items from the open list unless the completion is important progress for `Moved forward today`.

## Deduplication

Merge items when they share most of:

- same account
- same owner or owner bucket
- same expected outcome
- same blocker/dependency
- close timeframe
- same or overlapping source evidence

When merging:

- keep the clearest verb-led action wording
- preserve all compact source evidence
- prefer the most recent timestamped status
- prefer explicit ownership over inferred ownership

## Completion Check

Do not surface items as open if there is clear completion evidence after the ask:

- sent recap or deliverable
- sent pricing, deck, resource link, recording, portal access, or next-step ask
- Slack thread resolved
- later Granola note says done
- customer or owner confirms completion

If evidence conflicts, prefer the most recent timestamped signal and note the conflict briefly.
