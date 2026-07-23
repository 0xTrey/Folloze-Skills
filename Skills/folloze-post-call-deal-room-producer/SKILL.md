---
name: folloze-post-call-deal-room-producer
description: Manually produce and publish a Folloze-owned post-call digital deal room from completed meeting context, including Outreach Kaia export, emailed ZIP retrieval, pre-call trimming, native Folloze recording upload, Luke deck collection, customer-logo harvesting, Board 248319 duplication, buyer-safe updates, internal seller review, and customer-share approval. Use when Trey asks to turn a completed demo, discovery, or intro call into a native Folloze resource center with the actual recording.
---

# Folloze Post-Call Deal Room Producer

Use this skill as a manual, seller-initiated production run. Do not attach it to Salesforce, Hermes, cron, Calendar polling, or automatic call detection.

The operator can begin the deal-room draft as soon as the call ends. The production run is not complete until the Kaia recording has been exported, prepared, edited when necessary, uploaded to Folloze, and verified on the published board.

The board should publish automatically after production QA. Publication is not customer delivery. Share the published room only with Luke or another internal seller for review. Never send it to an end customer until the seller explicitly approves external sharing.

## Ownership Boundaries

- This skill owns the complete manual post-call production run.
- `Folloze-Digital-Deal-Room-Internal` owns native board copy, configuration, direct API save, publish, and readback.
- Browser Control is always part of the run for Kaia export, Folloze media handling when required, designer QA, and public playback verification.
- `folloze-brand-kit` supplies Folloze positioning and buyer-safe language.
- `brand-harvester` supplies the official customer logo and light/dark alternatives.
- The local helpers in this skill validate the Kaia ZIP and perform approved recording edits. They never authenticate to Outreach or Folloze.

Do not use Salesforce. Do not hand the run to Hermes. Do not create or resume a background job.

## Fixed V1 Decisions

- Invocation: manual only.
- Universal native template: Board `248319`.
- Draft timing: begin immediately after the call.
- Required completion dependency: edited recording uploaded and playable.
- Deck owner: Luke always creates a new account-specific deck.
- Missing deck: send Luke an automated Slack request and keep the deck checkpoint open.
- Recording preference: MP4 video first; audio only when no usable video exists.
- Transcript: ignore it and never upload it.
- ZIP retention: delete the exact downloaded ZIP after successful media extraction and hash verification.
- Recording title: `[Account Name] + Folloze Demo + [recording date]`.
- Customer logo: always harvest the official logo and choose the light/dark variant that passes contrast QA.
- Publish: automatic after saved-board and designer QA.
- Delivery: internal Luke review only; external sharing requires explicit seller approval.
- Reruns and historical QA migration: out of scope for v1.

## Required Safety Rules

- State the manual working goal before writes: account, meeting, template `248319`, target board intent, recording state, deck state, publish state, and customer-share state.
- Treat Gmail, Granola, Kaia, Calendar, Drive, Slack, ZIPs, raw media, and meeting notes as private inputs.
- Translate call context into buyer-safe messaging. Never expose raw objections, pricing commentary, private notes, internal tasks, or transcript excerpts.
- Never commit recordings, ZIPs, transcripts, signed links, tokens, cookies, or auth headers.
- Do not embed the Kaia viewer, share URL, or emailed download URL.
- Do not upload the ZIP. Upload the final edited MP4 or approved audio fallback.
- Never send a customer-facing email or Slack message from this skill.
- Any internal Slack message sent by the skill must explicitly say it is an automated message from Codex.
- Treat `published`, `internally_shared`, `seller_approved`, and `customer_shared` as separate states.

## Universal Template And Corporate Brand

Use Board `248319`, `[Account Name] - Folloze Resource Center - July 2026 Template`, as the universal template.

Before every copy, confirm through the API that:

- board ID is exactly `248319`
- `is_template` is `true`
- the board is accessible
- the expected published version exists

Read:

- `references/july-2026-template-map.md`
- `references/current-corporate-brand.md`

The template should use Folloze's current corporate system: deep navy surfaces, electric violet accents, white and pale-blue supporting surfaces, Instrument Sans/Inter-style typography, rounded cards, restrained shadows, and official Folloze imagery.

For every copied room:

1. Harvest the account's official public logo.
2. Collect a full-color, dark, and light/white variant when available.
3. Select the variant with sufficient contrast on the active header background.
4. Do not use CSS filters to manufacture a logo variant when an official one exists.
5. Hide the customer-logo slot when no safe official logo can be found.

## Manual Run States

Track these checkpoints:

1. `manual_run_started`
2. `source_pack_ready`
3. `board_draft_saved`
4. `deck_present` or `deck_requested_from_luke`
5. `recording_export_requested`
6. `export_zip_downloaded`
7. `media_prepared`
8. `trim_reviewed`
9. `media_edited`
10. `media_uploaded`
11. `designer_qa_passed`
12. `published`
13. `public_verified`
14. `seller_review_sent`
15. `seller_approved_for_external_share`
16. `customer_shared`

The production run may finish at `seller_review_sent`. The last two states are separate seller-controlled delivery steps.

Store only non-secret run metadata: meeting identity, Kaia recording ID, board ID, deck status, media basename/hash/size/duration, publish state, public URL, verification timestamps, and internal-review status.

## Workflow

### 1. Start The Draft After The Call

Use the exact meeting title, account, date, Granola note, Gmail context, and any promised resources supplied by the seller. Calendar and Drive can clarify the meeting or deck, but no Salesforce lookup is needed.

Separate facts into:

- `buyer_safe`
- `internal_only`
- `missing`

Build the draft immediately from Board `248319`. The recording and deck can remain open checkpoints while copy, account priorities, examples, integrations, and case studies are prepared.

### 2. Resolve Luke's Account-Specific Deck

Search Drive and Gmail for a newly created deck matching the account and call. Do not treat the template presentation as the final deck.

If the deck is missing, send Luke this internal Slack message through the approved Slack connector:

```text
Automated message from Codex: Hi Luke — the [Account] Folloze deal-room draft is in progress. Please share the new account-specific presentation deck when it is ready so I can add it before the room is sent for your review.
```

Record `deck_requested_from_luke`. Continue the rest of the draft, but do not mark the deck checkpoint complete until the real deck is attached and opens correctly.

### 3. Request The Kaia Export

Use Browser Control in the authenticated Outreach Web App:

1. Open `https://web.outreach.io/kaia/recordings?smart_view=0`.
2. Search by exact meeting title.
3. Confirm date, account, attendees, duration, and stable recording ID.
4. Choose **Meeting actions** → **Download**.
5. Record the recipient, request time, and expiry window.
6. Dismiss the confirmation modal.

Do not click Download repeatedly. This remains a foreground manual run; pause and resume the same task when the email arrives.

### 4. Download And Prepare The ZIP

Match the Outreach Kaia email by sender, exact meeting title, received time, availability language, and expiry date. The signed link is private.

Run:

```bash
python3 Skills/folloze-post-call-deal-room-producer/scripts/prepare_kaia_export.py \
  ~/Downloads/<export>.zip \
  --delete-zip-after-success
```

The helper validates the archive, rejects unsafe members, selects video before audio, extracts only the selected media, hashes it, probes it with `ffprobe` when available, ignores the transcript, and deletes only the exact input ZIP after success when the flag is present.

Never use `transcript.txt` in the workflow.

### 5. Review And Edit The Recording

Review the opening minutes in a local video player. Remove:

- pre-call chatter between Folloze employees
- setup time with no customer value
- long, useless internal conversation before the buyer joins

Do not remove substantive buyer conversation, customer questions, product context, or promised demo content.

Record the timestamp where the useful customer-facing conversation begins. Then run:

```bash
python3 Skills/folloze-post-call-deal-room-producer/scripts/trim_kaia_recording.py \
  <prepared-video>.mp4 \
  --account "<Account Name>" \
  --recording-date YYYY-MM-DD \
  --start HH:MM:SS
```

The default exact-cut path re-encodes to H.264/AAC with fast-start metadata. This also generally reduces the very large Kaia export. Use `--copy-codecs` only when speed matters more than frame-exact trimming.

Review the edited beginning and confirm audio/video sync. Set `media_edited` only after that playback check.

The final filename must follow:

```text
[Account Name] - Folloze Demo - YYYY-MM-DD.mp4
```

### 6. Finish The Native Board

Delegate native configuration to `Folloze-Digital-Deal-Room-Internal`:

1. Confirm Board `248319` is still a template.
2. Copy it into a new non-template board.
3. Set the account name, buyer-safe description, official customer logo, and vanity path.
4. Replace every placeholder and prior-account residue.
5. Add Luke's real deck.
6. Add the approved demo-example URLs.
7. Select only relevant integration guides and case studies.
8. Save and read back the native config.

### 7. Upload The Final Recording

Prefer the verified Folloze Content Upload or Content8Upload API when it is available and supports the final file. Do not invent an endpoint or reuse link-item APIs for binary media.

Browser Control is always required:

- use it as the upload fallback when the binary API is unavailable
- open the exact target board after any API upload
- confirm the item exists in **Resources From Our Calls**
- confirm the title matches the naming convention
- save and play the uploaded recording in the designer

Do not consider an API response alone sufficient proof of upload.

### 8. QA, Publish, And Internal Handoff

Before publishing, verify:

- official Folloze and customer logos are crisp and readable
- no template, Tru Technologies, ModoMind, pharma, or biotech residue remains
- the account deck opens
- every approved demo-example URL works
- the final edited recording plays from the intended card
- the recording starts at a useful customer-facing moment
- cards, dashboards, media, and headings are level and unclipped
- no transcript, signed URL, file path, or internal production note is exposed

Publish automatically after QA. Then verify the public vanity URL and recording playback in a public/anonymous context.

Send Luke an internal Slack message:

```text
Automated message from Codex: The [Account] Folloze deal room is published and ready for your review: [URL]. The account deck and edited demo recording are included. It has not been shared with the customer. Please approve or send edits before external delivery.
```

Set `seller_review_sent`. Do not contact the customer.

## Execution Boundaries

Read `references/automation-boundaries.md` for the v1 interface split.

- Manual operator: starts and resumes the run.
- Browser Control: Kaia, Folloze media fallback, designer QA, and public playback.
- Gmail/Drive/Slack connectors: email matching, deck retrieval, and internal Luke messages.
- Local Python helpers: ZIP and video processing.
- Folloze API: template validation, board copy, config, proven item operations, publish, and readback.
- Hermes, cron, Salesforce, and automatic meeting detection: disabled for v1.

## Completion Contract

Report separately:

- source meeting and recording ID
- deck status and Luke request status
- ZIP download and deletion status
- original and edited media metadata
- trim start and playback verification
- template preflight
- customer-logo source and selected contrast variant
- target board ID and saved-board readback
- native media upload/playback
- published state and public verification
- internal Luke review message
- seller external-share approval
- customer-share status

Never call the production run complete before the edited recording is uploaded and verified. Never imply the customer received the room merely because it was published.
