# Source Contracts

## Salesforce

Use Salesforce as the source of truth for pipeline and account context.

Default query shape:

- current Salesforce user
- open opportunities where `OwnerId` or owner email matches the current user
- account fields for grouping
- stage, amount, close date, forecast category, probability, last activity date, and next-step fields when available

For customer-success users, group by account first and then list the most relevant opportunities under that account. Multiple opportunities on one account should not create duplicate account priorities.

Do not write to Salesforce from this skill.

## Folloze Calendar

Use the teammate's Folloze work calendar only.

External event signals:

- non-Folloze attendees
- customer/prospect/partner/vendor domains
- titles with demo, intro, discovery, renewal, QBR, onboarding, security, legal, procurement, executive sync, or walkthrough intent

Low-priority or filtered event signals:

- working location
- OOO
- all-day availability
- Reclaim/focus blocks
- prospecting blocks without a named account
- internal-only meetings unless they affect a customer commitment

## Granola

Use Granola for meeting follow-up and recent-account context.

Prioritize:

- action items
- promised follow-ups
- blockers
- customer commitments
- next steps
- next-call brief content, if exposed by the connector or MCP

If a Granola result contains only a title or a stub, treat it as weak directional evidence.

## Gmail

Use Gmail to find unresolved customer/account follow-ups and to verify whether candidate follow-ups have already been completed.

Relevant email signals:

- unanswered inbound customer asks
- promised Folloze deliverables
- customer dependencies
- internal teammate asks that block a customer action
- scheduling changes that affect today's readiness
- sent/outbound messages from the current teammate after the commitment timestamp
- sent/outbound messages from a Folloze teammate where the current teammate was cc'd
- later customer replies that move the next step from Folloze to the customer

Ignore newsletters, promotions, automated mail, signatures, and purely logistical threads unless they change a meeting or deadline.

Before listing a Granola-derived or meeting-derived follow-up as open, search sent mail and the relevant thread. If the promised email, pricing, recording, deck, resource portal, or recap was already sent, do not list the item as an open task. If it is still strategically relevant, call it out as completed and waiting on the next party.

## Google Drive

Use Google Drive only for targeted context.

Relevant Drive artifacts:

- account plans
- QBR or renewal docs
- onboarding or implementation notes
- handoff docs
- mutual action plans
- customer-facing decks or docs tied to today's meetings

Avoid broad searches when calendar, Salesforce, Granola, and Gmail already provide enough context.

## Optional Role-Specific MCPs

CSM teammates may have additional MCPs such as Gainwell. Use those sources only for read-side account health, renewal, onboarding, or implementation context. Label any optional-source signal and keep the brief useful if the source is unavailable.
