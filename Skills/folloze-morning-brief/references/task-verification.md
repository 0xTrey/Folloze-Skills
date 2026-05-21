# Task Verification

Use this reference when the morning brief surfaces follow-up tasks from Granola, Gmail, Salesforce next steps, or optional account MCPs.

## Principle

Treat every follow-up as a candidate until it has been checked against completion evidence. Do not list yesterday's promised work as open just because it appears in meeting notes.

## Completion Evidence

Search outbound/sent mail after the candidate task timestamp and through the current run time.

Accept completion when the evidence shows one of these:

- the current teammate sent the promised follow-up
- another Folloze teammate sent the promised follow-up and the current teammate was cc'd
- the outbound message includes the promised artifact, pricing, recap, recording, resource link, deck, portal, or next-step ask
- a later thread message confirms the deliverable was received or the task moved to the customer

Use a teammate-cc'd message as completion when the original task was owned by another Folloze teammate. Example: if Luke owed Aprio pricing and Luke sent the pricing email with the current teammate cc'd, mark the task completed and do not list it as open for the current teammate.

## Open Task Evidence

Keep the candidate open when:

- no outbound message is found after the commitment timestamp
- an outbound message exists but does not satisfy the promised deliverable
- the message asks for internal input and the customer-facing follow-up still has not happened
- the latest customer reply creates a new unanswered ask
- completion evidence is ambiguous and the follow-up has meaningful customer or revenue risk

## Status After Completion

Completed follow-ups can still matter. If a completed follow-up creates a waiting state, move it out of `Task list` and into `Signals, risks, and blockers`.

Use wording like:

- `Completed: Luke sent Aprio pricing; now waiting on scoping-call acceptance.`
- `Completed: partner resources sent to Power Digital/G&A; now waiting for Katie's Friday sync with Cindy.`

## Search Pattern

For each candidate task:

1. Identify account, contacts, expected artifact, owner, and task timestamp.
2. Search sent/outbound Gmail from the task timestamp through now.
3. Search thread participants and account/domain names, not just exact task wording.
4. Read the best matching sent messages.
5. Decide `open`, `completed`, `waiting_on_customer`, `waiting_on_teammate`, or `ambiguous`.

Prefer exact thread evidence over broad keyword matches. Avoid treating automated meeting summaries, calendar notifications, and access-confirmation emails as task completion unless they directly prove the promised deliverable was sent.
