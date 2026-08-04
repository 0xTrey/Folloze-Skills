# Recording And Transcript Intake

Use this procedure for every manual internal deal-room run.

## Operator-specific transcript intake

Determine who is running the skill before touching Folloze.

### Trey-run room

1. Search the connected Granola source for the exact meeting using account, date, title, and attendees.
2. Use the matching Granola transcript or sufficiently detailed notes as the primary call source.
3. Materialize a temporary readable local `.txt`, `.md`, `.vtt`, or `.srt` transcript outside the skill repository so the evidence map and media helper have a stable input.
4. Record `transcript_source_mode=granola`, the Granola meeting identifier, meeting-match evidence, and the temporary path.
5. If Granola has no matching or sufficiently complete meeting, stop and request a transcript or an explicitly authorized Kaia fallback.

### Luke-run room

1. Require Luke to supply the exact Kaia download/email package or extracted handoff directory from the call.
2. Inspect only that package/location for a transcript (`.txt`, `.md`, `.vtt`, `.srt`, `.pdf`, or `.docx`) and recording (`.mp3`, `.mp4`, `.m4a`, `.mov`, or `.wav`).
3. If both valid assets match the meeting, set `transcript_source_mode=kaia_package` and `acquisition_mode=local_provided`. Do not open Kaia, inspect email, request another export, or use browser automation.
4. If Luke supplies extracted files instead of an archive, apply the same validation and use `transcript_source_mode=local_file`.
5. If a required asset is absent, use browser/email export only when the invocation explicitly authorizes fallback. If a supplied asset is corrupt, ambiguous, or belongs to the wrong meeting, stop for correction instead of exporting over it.

The transcript is a strategy and editing input, not a buyer-facing deliverable unless Trey explicitly requests upload.

Do not commit the raw transcript. Record only its source mode, local/temporary path, file type, readability check, meeting/account match, and buyer-safe evidence references in the repo-backed processing receipt.

Stop if:

- the transcript is missing or unreadable
- it belongs to the wrong account or meeting
- it is too incomplete to support the value section and clip decision
- multiple transcript candidates exist and cannot be disambiguated safely

## Recording decision tree

Use this exact order:

1. Check the recording path supplied in the invocation.
2. If Luke supplied a Kaia archive or handoff directory, inspect that exact location before any other source. Do not broadly scan Downloads or the home directory.
3. Validate any candidate with `file` and `ffprobe`.
4. If one valid local media file matches the account/meeting, set `acquisition_mode=local_provided` and do not open Kaia, request an export, inspect email, or download a ZIP.
5. If a supplied/found local file is corrupt, incomplete, has the wrong streams, or belongs to the wrong meeting, stop and request correction. Do not silently replace it with a browser export.
6. If no local recording was supplied or found and the invocation explicitly authorizes fallback, set `acquisition_mode=kaia_browser_export` and use the existing authenticated Kaia/Outreach export workflow.
7. If local media is absent and fallback was not authorized, stop and request the missing decision.
8. If more than one plausible local recording exists, stop and ask which one is authoritative.

Supported source formats are MP3, MP4, M4A, MOV, and WAV. Require a non-empty file, a readable duration, and at least one audio stream. For a video deliverable, also require a video stream.

Do not move a user-supplied source into git. Treat it as a local sensitive input. Preserve it unless Trey explicitly authorizes deletion.

## Kaia browser fallback

Use browser automation only when local media validation fails because the recording is absent, not merely because the browser path is familiar.

1. Open the exact call in Outreach Kaia.
2. Request the recording export.
3. Wait for the emailed ZIP export and retrieve that exact export.
4. Extract the MP3 or MP4.
5. Verify the exported media matches the account, meeting date, and expected call duration.
6. After the edited output is verified and uploaded, resolve the exact ZIP created by this export and move only that file to macOS Trash. Never use a broad directory target, glob, or permanent recursive deletion. Record the trashed filename so it can be recovered if needed.

Record export request evidence and the retrieved media filename without exposing email contents or authentication data.

## Determine the clip

Use transcript timestamps when available. Identify:

- source start time
- internal pre-call or front-of-call chatter
- the first customer-relevant moment worth preserving
- any clearly useless internal outro that should be removed

Preserve useful customer introductions and context. Do not apply a fixed number of seconds to every call. If the transcript lacks timestamps, inspect or transcribe the opening minutes and choose the boundary from the actual content.

Create a private cut manifest with:

- `source_path`
- `transcript_path`
- `transcript_source_mode`
- `acquisition_mode`
- `source_duration_seconds`
- `keep_start_seconds`
- optional `keep_end_seconds`
- `removed_opening_seconds`
- optional `removed_ending_seconds`
- buyer-safe reason for each cut
- timestamp/source evidence used for the decision

Choose the cut boundary once from timestamped transcript evidence. Run transcript analysis, media capability probing, asset resolution, and Folloze/template preflight concurrently. Do not watch or transcribe the entire recording when the transcript already provides a defensible boundary.

## Perform a real media edit

Prefer the bundled deterministic helper, which selects a verified fast encoding path, rejects a zero-time cut, verifies durations/hashes/streams, records elapsed time and encoder choice, and leaves content review explicitly pending:

```bash
python3 scripts/clip_call_recording.py \
  --input INPUT \
  --output OUTPUT.mp4 \
  --transcript TRANSCRIPT \
  --start START_SECONDS \
  --mode auto \
  --transcript-source-mode kaia_package \
  --acquisition-mode local_provided \
  --receipt PRIVATE_RECEIPT.json
```

Add `--end END_SECONDS` when trimming the end. Run the helper from the skill directory or use its absolute path. It requires MP4 output for video sources and MP3 output for audio-only sources.

Use `--mode auto` for production. It prefers a supported hardware encoder and falls back to portable `libx264 -preset veryfast`. Use `--mode hardware` only after capability probing proves the encoder works, and use `--mode software` when repeatability is more important than the fast target. If hardware acceleration is unavailable and a real cut is required, classify the run `standard_ready` rather than promising sub-five-minute completion.

Use direct `ffmpeg` only when the helper cannot support a valid source/destination requirement, and preserve the same proof contract. Example video command:

```bash
ffmpeg -y -ss START_SECONDS -i INPUT \
  -map 0:v? -map 0:a? \
  -c:v libx264 -preset veryfast -crf 22 \
  -c:a aac -b:a 160k -movflags +faststart \
  OUTPUT.mp4
```

Example audio command:

```bash
ffmpeg -y -ss START_SECONDS -i INPUT \
  -c:a libmp3lame -b:a 192k \
  OUTPUT.mp3
```

Add `-t DURATION_SECONDS` when trimming the end. Adapt codecs only when the source/destination requires it and record the actual command. Never overwrite the source file.

A copy, rename, file-extension change, metadata edit, or remux without the intended time cut is not clipping.

Prepare the board copy/config and independent asset uploads while the media edit runs, but do not publish until the verified edited media is uploaded and linked. Review only the new opening 30–60 seconds and any edited ending during the timed run; a full-call replay is not required.

## Verify the edited output

Do not mark the recording edited until all applicable checks pass:

1. The output exists, is non-empty, and has a different hash from the source.
2. `ffprobe` reads the output without error.
3. The output contains the required audio stream and, for video, the required video stream.
4. Output duration matches the intended keep interval within normal encoding tolerance.
5. When opening chatter was removed, output duration is shorter by approximately the recorded removed interval.
6. Review the first 30 to 60 seconds of the edited output and confirm the internal small talk is gone and the first useful buyer-facing moment remains. Record reviewer identity, review timestamp, and a short buyer-safe description of the new opening.
7. Review the ending when an end cut was applied.
8. Play the local output before upload.
9. After Folloze upload, verify playback, buyer-facing title, correct cover, and the card destination.

If review shows that no removable opening chatter existed, record `clip_required=false`, `recording_clipped=false`, reviewer identity/time, and a short buyer-safe description of the acceptable original opening. Use the validated source without a pointless transcode. Otherwise require a new edited file and a positive removed interval.

The processing receipt must include:

```json
{
  "transcript_source_mode": "granola | kaia_package | local_file | kaia_browser_export",
  "acquisition_mode": "local_provided | kaia_browser_export",
  "transcript_file_readable": true,
  "transcript_meeting_match_validated": true,
  "source_duration_seconds": 0,
  "output_duration_seconds": 0,
  "removed_opening_seconds": 0,
  "removed_ending_seconds": 0,
  "clip_required": true,
  "recording_clipped": true,
  "opening_chatter_clipped": true,
  "source_and_output_hashes_differ": true,
  "streams_verified": true,
  "opening_review": "passed",
  "opening_reviewed_by": "reviewer identity",
  "opening_reviewed_at": "ISO-8601 timestamp",
  "new_opening_description": "buyer-safe description",
  "local_playback": "passed",
  "folloze_playback": "passed"
}
```

Keep the receipt and buyer-safe cut rationale in the deal repo. Do not include raw transcript passages, tokens, cookies, email bodies, or private audio content.
