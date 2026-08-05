# Production Fast Path

Use this contract for every timed internal deal-room build. It preserves the skill's content and verification rules while preventing production runs from turning into open-ended browser or endpoint investigations.

## Runtime objective

- `fast_ready`: all inputs/auth/assets/media capabilities are ready; stretch target `<=300` seconds.
- `standard_ready`: the path is complete but needs a software encode or ordinary external wait; target `<=480` seconds.
- `blocked`: a required preflight gate is missing; emit the exact blocker before mutation, normally inside `60` seconds.
- Accepted production target: less than `600` seconds.
- Hard timeout: `600` seconds from invocation to `review_notified` or a truthful nonterminal result.
- Sub-five-minute completion is possible only when the media job, asset uploads, and editor invitation stay on their verified fast paths. Do not promise it before preflight.

Start the clock when the explicit invocation and referenced inputs are accessible. Stop it when the Slack handoff is verified or when the run emits its highest verified nonterminal state and blocker.

At `480` seconds, start no new discovery. At `540` seconds, start no new retry. At `600` seconds, emit the machine result immediately. External waits remain part of total wall-clock time.

## Preflight before any Folloze write

Complete these checks concurrently where possible:

1. Invocation names the operator, account, meeting, and supplied package or source.
2. The exact input package contains one readable transcript and one valid matching recording, or the authorized acquisition fallback is explicit.
3. The deck is available or its allowed pending behavior is recorded.
4. The Salesforce Opportunity ID resolves uniquely, or `prototype_override=true` is explicit.
5. Board `248623` resolves by ID and exact name, is still a template, and contains the expected widgets.
6. Warm the selected Folloze MCP profile with its refresh-capable `auth_login(force=false)` path, then require the resulting Experience API access token to pass one compact authenticated read. Short-lived access-token expiry is expected; a valid stored refresh token should rotate it without manual login. Use interactive authentication only when the refresh grant fails.
7. The current editor-invite transport is known, an authenticated app session or supported API path is available, and Luke Rafferty's stable organization user/invite ID resolves with normalized email `luke@folloze.com` and display name `Luke Rafferty`. The email is Trey's confirmed lookup identity, but email or search eligibility alone is not invitation proof.
8. The canonical tracker metadata/header and only the candidate account rows are readable.
9. The shared Drive tile folder and only the required tile files are readable; write access is confirmed when a local tile must be uploaded.
10. Brand logo and accent sources are resolved from first-party material.
11. `ffmpeg`, `ffprobe`, the media helper, and required runtimes are available.
12. Slack can resolve the intended recipient before the board is built.
13. The output receipt location is inside the selected git-backed deal repository and raw media/transcripts remain outside git.

The preflight result must be compact JSON with `fast_ready`, `standard_ready`, or `blocked`, pass/fail for each gate, and elapsed milliseconds. Never include credentials or raw source contents.

If a required preflight gate fails, stop before board copy. Spend no more than 60 seconds confirming the failure. Return the failed gate, the exact safe next action, and `board_mutation_started=false`.

## Parallel execution lanes

After preflight passes, use these lanes:

- **Evidence lane:** parse the transcript once and produce the buyer-safe brief, hero line, value-card evidence map, AI signal decision, and cut manifest.
- **Asset lane:** prepare the deck, correct covers, tracker-backed examples, Drive tiles, logo, and upload manifests.
- **Media lane:** apply the transcript-supported cut, validate streams/duration/hash, and prepare the edited asset for upload.
- **Board lane:** duplicate the verified template, then apply the already-prepared metadata/config/item changes.

Evidence, asset, and media work may run concurrently. The board lane may start only after account/template/auth identity is safe, and it must not publish until all required assets and evidence are ready.

## Media fast path

- Use transcript timestamps to select the cut without manually browsing the entire recording.
- Skip transcoding only when a documented opening review proves `clip_required=false`.
- When clipping is required, prefer the bundled helper's fast production mode and record its actual encoder. Fall back to a portable fast software encode only when hardware acceleration is unavailable.
- Review only the new opening 30–60 seconds and any edited ending; do not replay the entire meeting during the production clock.
- Upload immediately after technical verification and run one Folloze playback check during final verification.

## Board write path

Use one structured, account-neutral run specification that contains only resolved values and content. The writer should:

1. Audit and copy the template.
2. Upload independent files concurrently when the API permits it.
3. Apply metadata, logo, hero, Essentials, value text, and example items from the prepared spec.
4. Assert the ROI widget is unchanged and the value-widget HTML diff is allowlisted.
5. Save once with a real hash, publish once, set the vanity slug, and re-read once.
6. Invite and verify the preflight-resolved Luke Rafferty stable identity through the preflighted editor path.

Do not create account-specific scripts, discover payload shapes, or test speculative endpoints inside a production run.

## One bounded verifier

The verifier gets one normal attempt and one targeted retry only when a read is transient. It checks:

- selected metadata and publication fields
- saved/published hashes and required personalized markers
- ROI byte identity and value-widget diff allowlist
- required board items, buyer-facing titles, covers, and destinations
- editor membership from the board Editors readback
- one authenticated desktop screenshot and one mobile value-section screenshot
- local and Folloze media playback/endpoint health
- selected tracker rows and Drive tile identities
- tracker update readback and Slack message readback

Do not fetch or print the full organization, complete sheet, full DOM, app bundle, or source map. Store hashes and selected fields instead of raw large payloads.

## Exception policy

The following are separate diagnostic tasks, not production work:

- OAuth repair or reauthentication
- browser extension recovery
- CAPTCHA or editor-invite endpoint discovery
- current-app bundle or source-map inspection
- undocumented payload-shape research
- broad Drive, Gmail, Downloads, or sheet searches
- visual redesign outside the approved template rules

After 60 seconds on any such exception, emit the highest verified state and stop. At 600 total seconds, stop regardless of stage. An explicit draft-only override may stop at `published_internal`; it must record `editor_pending` and suppress Slack completion.

## Performance receipt

Include this object in the machine result:

```json
{
  "performance": {
    "runtime_profile": "fast_ready",
    "run_id": "stable run identifier",
    "started_at": "ISO-8601 timestamp",
    "finished_at": "ISO-8601 timestamp",
    "warmed_fast_path": true,
    "target_runtime_seconds": 480,
    "hard_timeout_seconds": 600,
    "total_elapsed_seconds": 0,
    "timed_out": false,
    "external_wait_seconds": 0,
    "api_call_count": 0,
    "browser_call_count": 0,
    "retry_count": 0,
    "browser_fallback_seconds": 0,
    "stages": {
      "preflight": {"elapsed_seconds": 0, "budget_seconds": 45, "passed": true},
      "evidence_and_assets": {"elapsed_seconds": 0, "budget_seconds": 75, "passed": true},
      "media": {"elapsed_seconds": 0, "budget_seconds": 120, "passed": true},
      "board_write_and_publish": {"elapsed_seconds": 0, "budget_seconds": 120, "passed": true},
      "verification_and_handoff": {"elapsed_seconds": 0, "budget_seconds": 90, "passed": true}
    }
  },
  "usage": {
    "token_usage_available": false,
    "input_tokens": null,
    "cached_input_tokens": null,
    "output_tokens": null,
    "cost_estimate_usd": null,
    "cost_basis": "runtime did not expose token usage or model pricing"
  }
}
```

Stage elapsed times may overlap because independent work runs concurrently. Therefore, do not add stage durations to derive total elapsed time; measure total wall-clock time separately.
