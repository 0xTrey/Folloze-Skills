---
name: folloze-post-call-deal-room-producer
description: Produce a Folloze-owned post-call digital deal room from completed meeting context, including Outreach Kaia recording export, emailed ZIP retrieval, safe local MP3 or MP4 preparation, native Folloze media upload, template duplication, buyer-safe content updates, QA, publish, and public verification. Use when a Folloze seller asks to turn a completed demo, discovery, or intro call into a native Folloze resource center or deal room with the actual call recording.
---

# Folloze Post-Call Deal Room Producer

Use this skill for the full post-call production flow when a native Folloze deal room must include the actual Outreach Kaia recording as a Folloze content item.

This skill is the orchestration layer. It coordinates:

- completed-call discovery and buyer-safe source synthesis
- the asynchronous Kaia recording export and Outreach email handoff
- safe, local ZIP processing into an MP3 or MP4 upload artifact
- the existing `Folloze-Digital-Deal-Room-Internal` native board writer
- Browser Control for current Folloze binary media upload
- explicit QA, publish, public verification, and cleanup checkpoints

Do not embed the Kaia recording page, viewer URL, share URL, or emailed download URL. Download the export, prepare its media file locally, and upload that media as a native Folloze content item.

## Ownership Boundaries

- This skill owns the completed-call-to-live-room production state machine.
- `folloze-post-intro-dsr-automation` may detect and qualify the event, then hand off here.
- `Folloze-Digital-Deal-Room-Internal` owns native board copy, component configuration, API writeback, publish, and public readback.
- `folloze-zoom-deal-room` remains the Zoom-recap intake path when Kaia is not the recording system.
- `folloze-brand-kit` supplies current Folloze positioning and buyer-safe language.
- The helper script in this skill owns deterministic ZIP inspection and media preparation only. It never authenticates to Outreach or Folloze.

Do not collapse these responsibilities into one opaque browser macro. Each checkpoint must be independently observable and resumable.

## Required Safety Rules

- State the working goal before material writes: account, completed meeting, source systems, Folloze template, target board or new-board intent, recording state, publish authorization, and private-data boundary.
- Treat Gmail, Granola, Kaia, Calendar, Salesforce, Slack, raw transcripts, ZIP exports, and local media as private inputs.
- Translate call context into buyer-safe messaging. Never paste raw objections, private notes, pricing commentary, internal tasks, or unapproved transcript excerpts into the room.
- Never commit a ZIP, recording, transcript, token, cookie, signed download URL, or auth header to Git.
- Use the Outreach email's signed link only to retrieve the export. Never surface it in board content, logs, manifests, or handoff notes.
- Do not upload the ZIP itself. Upload a prepared video or audio file.
- Do not upload or expose a transcript unless the user explicitly authorizes it.
- Prefer MP4 or another supported video export when available so the buyer retains the demo screen share. Use MP3, M4A, or another supported audio file only as fallback.
- Stop before publish unless publish is explicitly authorized by the request or the approved automation policy.
- Never infer public verification from a successful save or publish response. Verify the anonymous public page and media playback separately.

## Default July 2026 Template

The current default native template candidate is:

- board ID: `248319`
- public vanity path: `folloze-deal-room-template-july-2026`
- expected designer title: `[Account Name] - Folloze Resource Center - July 2026 Template`

Before copying it, use the current Folloze template-list or board-read API to confirm that board `248319` exists, is accessible, and is marked as a template. A title or public vanity URL containing the word “template” is not sufficient proof.

If direct API authentication is stale, refresh through the approved Folloze OAuth path. Browser inspection may confirm the visual structure, but do not scrape browser cookies or tokens to bypass the supported authentication flow.

If `248319` is missing or is not marked as a template, stop before creating a board and report the exact failed preflight.

Read `references/july-2026-template-map.md` before editing a board copied from this template.

## Resumable State Machine

Track the run with these ordered statuses:

1. `source_pack_ready`
2. `recording_export_requested`
3. `awaiting_export_email`
4. `export_zip_downloaded`
5. `media_prepared`
6. `board_draft_saved`
7. `media_uploaded`
8. `designer_qa_passed`
9. `published`
10. `public_verified`

Store only buyer-safe, non-secret run metadata in the durable run record:

- account and meeting title
- meeting date and stable Kaia recording ID
- requested export timestamp and recipient address
- status and last successful checkpoint
- Folloze template and target board IDs
- prepared media basename, MIME type, byte size, SHA-256 hash, and optional duration
- publish state, designer URL, public URL, and verification timestamps
- blocker, retry count, and next action

Do not store the signed email link, local absolute file path, transcript text, ZIP contents, or raw media in the durable record.

## Workflow

### 1. Resolve The Completed Call

Use the narrowest source path first:

1. Start from the exact meeting title, account, and date supplied by the user.
2. Read the matching Granola note or other approved meeting note.
3. Resolve supporting Gmail, Calendar, Salesforce, Drive, Slack, and deck context only as needed.
4. Separate findings into `buyer_safe`, `internal_only`, and `missing` fields.
5. Record promised resources, demo examples, recording need, owners, next step, and unresolved approvals.

When resolving Kaia, match on more than account name. Require the best available combination of exact meeting title, meeting date, account, attendees, duration, and stable recording ID. If two recordings remain plausible, stop and ask for the right one.

### 2. Request The Kaia Export With Browser Control

Use the authenticated Outreach Web App because the export is currently a UI-led asynchronous workflow:

1. Open `https://web.outreach.io/kaia/recordings?smart_view=0`.
2. Search for the resolved meeting title.
3. Open the matching recording and re-check date, account, attendees, and duration.
4. Open **Meeting actions** and choose **Download**.
5. Read the confirmation modal and record the recipient, request time, and stated expiry window.
6. Dismiss the modal after the confirmation has been captured.
7. Set `recording_export_requested`, then `awaiting_export_email`.

Do not repeatedly click Download while waiting. A retry is appropriate only after the chosen timeout or after evidence that the first request failed.

### 3. Resume From The Outreach Email

Prefer the Gmail connector for structured search and message reading. Use Browser Control only when the connector cannot expose the needed link or current session context.

Match the email using:

- sender: Outreach Kaia or `no-reply@outreach.io`
- exact meeting title
- received after `recording_export_requested`
- body stating that the meeting is available to download
- a download-link expiry date

The email's **Download** link points to a ZIP export. Download it to the user's normal download location or an approved temporary location, then set `export_zip_downloaded`.

A live July 23, 2026 export contained `info.json`, `transcript.txt`, and `meeting.mp4`. The package was roughly 868 MiB for a 69-minute recording, so download time, local disk space, Folloze upload limits, and any approved compression policy must be treated as real workflow concerns. Do not hard-code this package shape; validate every archive.

If the email has not arrived, keep the run at `awaiting_export_email`. A scheduled runner such as Hermes may resume the run and check again. Do not keep a browser session blocked indefinitely.

### 4. Prepare The Media Safely

Run:

```bash
python3 Skills/folloze-post-call-deal-room-producer/scripts/prepare_kaia_export.py ~/Downloads/<export>.zip
```

The helper:

- validates the ZIP before extraction
- rejects traversal paths, symlinks, encrypted members, and oversized archives
- chooses video first, then audio
- extracts only the selected media file
- writes a private temporary manifest with the media hash and metadata
- leaves transcripts and unrelated files inside the ZIP

Review the JSON output. Confirm the selected MIME type and file size are supported by the current Folloze upload UI. If `ffprobe` is available, also confirm duration, codecs, and video dimensions.

Set `media_prepared` only after a valid audio or video candidate exists. Do not place the prepared media inside the skill repo.

### 5. Build The Native Board

Hand the source pack to `Folloze-Digital-Deal-Room-Internal` and use board `248319` only after the template preflight passes.

The writer should:

1. Copy the template into a new native board or resolve the explicitly named existing target board.
2. Set the account title, description, theme, owner, and vanity path.
3. Replace every template placeholder and customer-specific residue.
4. Populate the essentials, account-specific value propositions, demo examples, integration guides, case studies, and CTA from real call context.
5. Preserve the template's native layout unless the user requests a structural change.
6. Save and read back the board before media upload.

Set `board_draft_saved` only after API readback confirms the target board ID and saved configuration.

### 6. Upload The Recording As A Native Folloze Item

Binary media upload is not currently a proven public direct-API contract in this workflow. Use Browser Control for the upload until the live Folloze request sequence has been captured and validated.

In the authenticated Folloze designer:

1. Open the target board by exact board ID.
2. Navigate to the recording resource in **Resources From Our Calls**.
3. Replace the template placeholder named **Folloze Demo Call Recording**, or create one native video/audio item if the placeholder is absent.
4. Upload the prepared MP4 or MP3/M4A file, not the ZIP.
5. Give it a buyer-safe title such as `[Account] + Folloze Demo Recording`.
6. Add a concise description and approved thumbnail when the UI supports them.
7. Confirm the item is attached to the intended section/category and visible in the designer.
8. Save, refresh, and open the item to verify playback.

If the upload fails due to file size or encoding, stop and report the actual limit or error. Do not silently transcode or reduce quality without an approved media policy.

Set `media_uploaded` only after native item readback or designer playback succeeds.

### 7. Designer QA

Check desktop and narrow layouts. At minimum verify:

- no template placeholder or prior-customer residue remains
- logo pairing is legible on the active background
- the header and CTA match the target account
- the recording card is native, visible, and playable
- promised slides and all approved demo-example URLs are present
- content titles and links are correct
- account priorities use buyer-safe wording
- cards, dashboard visuals, and media are aligned rather than tilted, clipped, or crowded
- no internal notes, signed links, file-system paths, or production labels are exposed

Set `designer_qa_passed` only after the saved designer state is re-opened and checked.

### 8. Publish And Verify

Publish only with authorization. After the publish response:

1. Read back board metadata and published state.
2. Open the public vanity URL in an anonymous or unauthenticated context.
3. Verify the correct board, account branding, final vanity path, resource links, and native recording item.
4. Play enough of the recording to confirm that the public media asset loads.
5. Record `published` and `public_verified` as separate timestamps.

If the board publishes but public playback fails, the run is not complete.

### 9. Cleanup And Handoff

After public media verification:

- delete the temporary extracted media and temporary manifest unless the user selected a retention policy
- move or delete the downloaded ZIP according to the approved retention policy
- keep only the basename, hash, MIME type, size, and verification evidence in the durable run record
- report the target board ID, designer URL, public vanity URL, media status, source-document status, and any remaining buyer-safe follow-up

Treat Salesforce update, tracker update, Slack delivery, and follow-up email as separately authorized actions.

## Automation Boundaries

Read `references/automation-boundaries.md` before proposing a new API shortcut.

The default split is:

- Hermes or a scheduled runner: resume state, poll for export email, enforce retries, and notify
- Browser Control: Kaia export request and current Folloze binary upload
- Gmail connector: email matching and message inspection
- deterministic local helper: ZIP validation, media selection, hash, and metadata
- Folloze API: template validation, board copy, metadata/configuration, native link-item management where proven, publish, and readback

Do not guess a Folloze media endpoint. A future API uploader must be based on an observed supported request contract and must retain Browser Control fallback.

## Completion Contract

A run is complete only when the response separately reports:

- exact source meeting and recording ID
- Outreach export status and expiry, without exposing the signed URL
- ZIP download and media-preparation status
- prepared media type, size, hash, and duration when available
- template preflight result
- target board ID and saved-board readback
- native media upload and playback verification
- designer QA result
- published state
- anonymous public verification result
- cleanup/retention state
- remaining slide, content, or approval gaps

Never summarize an intermediate state as “done.”
