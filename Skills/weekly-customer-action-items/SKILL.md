---
name: weekly-customer-action-items
description: Build a consolidated Monday-through-Friday America/New_York summary of outstanding or unanswered customer action items across Granola notes, Gmail, and Slack. Use when the user asks for weekly customer follow-ups, unresolved tasks, unanswered asks, open action items, or a by-account summary of what still needs attention. Deduplicate repeated items across sources, ignore promotional or sales email, ignore email threads where meghan@folloze.com is not a participant, and present one grouped summary by customer account with clear ownership.
---

# Weekly Customer Action Items

Use this skill to compile one weekly customer-action summary from Granola, Gmail, and Slack, then return a clean by-account view of what is still open, unanswered, blocked, or waiting on someone.

## Defaults

- Business week means Monday 12:00 AM through Friday 11:59 PM in `America/New_York`.
- If the user does not name a week, use the most recent completed business week.
- Include both explicit action items and implied follow-ups or commitments.
- Include all unresolved states:
  - open but not clearly completed
  - unanswered
  - blocked
  - waiting on customer
  - waiting on Folloze
- Combine duplicates from multiple sources into one canonical action item.
- Group the final summary by customer account.
- Label each item with an owner when possible: `Meghan`, `customer`, `teammate`, `shared`, or `unclear`.
- Ignore promotional, newsletter, and bulk marketing email.
- Ignore any email thread where `meghan@folloze.com` is not in the participant list.

## Output

Return one consolidated weekly summary grouped by customer account.

For each account, include:
- a short account summary
- open action items
- owner for each item
- status for each item
- last meaningful touch date if known
- compact evidence pulled from Granola, Gmail, and Slack

Use this shape:

```markdown
# Weekly Customer Action Items
Week: 2026-04-06 to 2026-04-10 (America/New_York)

## Account: Acme
Summary: Two unresolved items remain. Meghan owes a follow-up recap, and the customer still owes pricing feedback.

- Action item: Send recap with integration answers
  Owner: Meghan
  Status: Unanswered / outbound follow-up still needed
  Last touch: 2026-04-08
  Evidence: Granola notes cited the recap as a next step [[0]](...); Slack DM asked whether it had been sent; no matching sent email found

- Action item: Customer to confirm security review owner
  Owner: Customer
  Status: Waiting on customer
  Last touch: 2026-04-09
  Evidence: Mentioned in meeting notes [[1]](...); customer email acknowledged receipt but gave no owner
```

If an item cannot be tied to an account, place it in `Account: Unmapped` and say what is missing.

## Workflow

### 1. Lock the reporting window

- Convert the requested week into explicit dates in `America/New_York`.
- State the exact Monday and Friday dates in the response.
- If the user says relative dates such as `this week` or `last week`, resolve them explicitly before summarizing.

### 2. Build the candidate account list

Start by identifying which customer accounts were active in the chosen week.

Use these signals:
- Granola meeting titles, attendees, and note content
- Gmail sender domains, recipient domains, and subject lines
- Slack channel names, channel mentions, DM context, and explicit company names

Normalize obvious variants into one account label:
- `Okta`, `okta`, and `okta.com` should collapse into `Okta`
- prefer the customer-facing company name over the raw domain

If two names may refer to the same account, merge them and note the inference.

### 3. Gather evidence in parallel by source

#### Granola

- Prefer `query_granola_meetings` for open-ended weekly action-item discovery.
- Ask specifically for:
  - follow-ups discussed
  - commitments made
  - next steps
  - owners
  - blockers
  - anything still unresolved
- Preserve Granola citation links exactly as returned.
- If needed, narrow with `document_ids` after identifying relevant meetings.

Good query pattern:

```text
For the business week of Monday through Friday in America/New_York, list all customer-related action items, follow-ups, commitments, blockers, and unresolved next steps from these meetings. Include explicit owners when available and preserve citations.
```

#### Gmail

- Search both inbound and sent mail for the chosen week.
- Focus on customer accounts found in Step 2.
- Capture two categories:
  - unreplied inbound asks Meghan owes
  - threads where the next move belongs to the customer or another teammate
- Ignore:
  - promotional or newsletter messages
  - automated marketing mail
  - any thread where `meghan@folloze.com` is not in `from`, `to`, or `cc`

Use Gmail query syntax where helpful, for example:

```text
after:2026-04-06 before:2026-04-12 -category:promotions -category:social
```

Then filter the returned threads manually for customer relevance and outstanding status.

Email heuristics:
- `Unanswered by Meghan`: inbound request with no meaningful reply from Meghan in the thread
- `Waiting on customer`: Meghan replied or sent a follow-up, but the customer has not answered
- `Waiting on teammate`: an internal handoff or request is still pending
- `Closed`: clear completion or explicit confirmation; exclude it

Do not treat calendar logistics, signatures, marketing blasts, or auto-replies as meaningful progress.

#### Slack

- Search public/private channels and DMs for the same week.
- Cover DMs plus customer-relevant channels surfaced by account names or domains.
- Look for:
  - direct asks
  - follow-up promises
  - questions without answers
  - shared next steps
  - blocker discussions
- Read full threads when a search hit looks actionable.
- If direct Slack tools are unavailable, use any connected-source workspace search that can surface Slack results for the same account and date keywords, then inspect the returned snippets or linked artifacts for evidence.

Good search fragments:
- `"follow up" after:YYYY-MM-DD before:YYYY-MM-DD`
- `"next step" after:YYYY-MM-DD before:YYYY-MM-DD`
- `"action item" after:YYYY-MM-DD before:YYYY-MM-DD`
- `"can you" after:YYYY-MM-DD before:YYYY-MM-DD`
- `"will send" after:YYYY-MM-DD before:YYYY-MM-DD`
- `"waiting on" after:YYYY-MM-DD before:YYYY-MM-DD`

If the available Slack tools do not expose starred or favorite channels directly, approximate the requested coverage by searching all accessible Slack content for the week plus DMs, then state that assumption briefly.

Slack heuristics:
- unanswered DM or thread question
- promised follow-up not yet sent
- account task assigned in-channel without completion evidence
- internal blocker that prevents a customer deliverable

### 4. Extract candidate action items

Turn raw evidence into a flat list of candidate items.

Each candidate should include:
- account
- action item summary in plain language
- owner
- current status
- source
- date of latest supporting evidence
- source link or citation

Prefer concise, verb-led summaries such as:
- `Send follow-up recap with pricing answers`
- `Customer to confirm security reviewer`
- `Natalie to share revised deck before Thursday`

### 5. Deduplicate across Granola, Gmail, and Slack

Merge items when they refer to the same underlying work.

Treat items as duplicates when they share most of the following:
- same account
- same owner
- same expected outcome
- matching timeframe
- same blocker or dependency

When merging:
- keep the clearest wording as the canonical action item
- preserve all supporting evidence
- prefer the most recent status signal
- carry forward explicit ownership from any source

### 6. Decide whether an item is still outstanding

Default rule:
- discovery window = the selected business week
- outstanding check = through the end of that week

If the user asks for what is still open now, or if it is cheap to verify, do a light post-week check through the present so you do not surface already-closed work as open.

Exclude items with clear completion evidence such as:
- a sent recap or deliverable matching the promised follow-up
- a Slack thread resolving the ask
- a later Granola note marking the item done
- explicit confirmation from the customer or owner

### 7. Resolve ownership

Use the strongest available ownership signal in this order:
1. explicit owner named in notes, Slack, or email
2. person making the commitment
3. person being directly asked to do the work
4. fallback `unclear`

Use these owner buckets:
- `Meghan`
- `Customer`
- `Teammate`
- `Shared`
- `Unclear`

### 8. Format the final summary by account

Order accounts by urgency:
1. accounts with unresolved Meghan-owned items
2. accounts blocked on customer response
3. accounts waiting on internal teammates
4. unmapped items

Within each account, list the most urgent or stale items first.

Statuses should be short and consistent:
- `Needs Meghan reply`
- `Waiting on customer`
- `Waiting on teammate`
- `Blocked`
- `Owner unclear`

## Guardrails

- Do not invent account names, owners, or completion states.
- Preserve Granola citations exactly.
- Keep email and Slack evidence short; summarize instead of pasting long thread text.
- Ignore non-customer operational chatter unless it blocks a customer action item.
- If an item is ambiguous, include it only when the unresolved work is real; otherwise place it under `Unmapped` or omit it.
- If the evidence conflicts, say so and prefer the most recent timestamped signal.
- When a source suggests an item is still open but another source shows completion, exclude it and mention the completion signal only if the user asks why it was filtered out.
