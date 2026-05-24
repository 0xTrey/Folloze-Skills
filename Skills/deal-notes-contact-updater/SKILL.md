---
name: deal-notes-contact-updater
description: Update existing Folloze deal-notes Google Docs contact sections from verified Salesforce, Gmail, Granola, Drive, or public-profile evidence. Use when a user asks to add, correct, enrich, dedupe, or verify contacts in a live deal-notes doc, especially when named people must be contact cards rather than meeting attendees.
---

# Deal Notes Contact Updater

Use this skill for narrow, in-place updates to existing Folloze deal-notes Google Docs. The deliverable is the live doc updated and verified, not a new draft or a broad opportunity rewrite.

## Core Rules

- Treat Salesforce, the existing deal-notes doc, and recent meeting/email evidence as the source system before editing.
- Keep actual meeting attendees separate from account contacts. Do not add a person to an attendee line unless the meeting evidence says they attended.
- Prefer augmenting an existing contact card over creating a duplicate card.
- Use the account's established contact-card format. When the doc has no clear format, use compact searchable fields: name, title, email, LinkedIn or profile URL, location when known, and a one-line insight.
- Do not make broad Salesforce opportunity updates unless the user explicitly asks. Contact-role or title updates are allowed only when supported by verified evidence.
- Verify the Google Doc after every write with connector readback. Use an HTML export or rendered readback when exact placement matters.

## Workflow

1. Resolve the target account and document.
   - Start from a supplied Google Doc link when provided.
   - If the user gives only shorthand like `AGH Deal Notes`, search Drive by the full company name before assuming the doc is missing.
   - If the deal-notes index is available, use it as a lookup aid. If it is stale or missing, fall back quickly to Drive search.

2. Read the current doc before editing.
   - Locate the `Contacts` section and the target subsection, such as Marketing, Executive, IT, or Procurement.
   - Check whether the person already has a card.
   - Check nearby meeting notes only to decide attendance, not to infer that every named person attended.

3. Gather enough source evidence.
   - Salesforce: existing contact record, account, opportunity, opportunity contact roles.
   - Gmail or Granola: meeting attendance, missed-call context, requested follow-up, or email identity.
   - Public profile search: title, LinkedIn/profile URL, location, and role context when not present in internal systems.
   - If sources conflict, keep the doc conservative and flag the discrepancy instead of inventing a clean answer.

4. Plan the smallest edit.
   - Existing card missing an email or title: insert only the missing line in the right position.
   - New contact: add one contact card under the right Contacts subsection.
   - Wrong attendee line: restore the actual attendee line first, then add named non-attendees as Contacts.
   - Multiple people: batch related doc edits when the connector supports it, but keep the change set scoped to contact cards and necessary attendance correction.

5. Apply and verify.
   - Use the Google Docs connector or approved Google Workspace path for the write.
   - Re-read the doc text and confirm the updated field/card appears exactly once.
   - When formatting or placement is important, export or read rendered HTML and verify the new line appears next to the intended card fields.
   - If Salesforce contact roles were touched, read back the opportunity contact-role state.

## Done Definition

Return a short operational summary with:

- the doc title or account name updated
- contacts added or fields corrected
- whether any attendee-line correction was made
- verification performed
- any source caveat or manual follow-up

Do not include a long chronology unless the user asks for audit detail.
