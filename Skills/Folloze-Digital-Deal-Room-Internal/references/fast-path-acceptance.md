# Fast-Path Acceptance Matrix

Run deterministic dry tests before packaging the skill, then benchmark warmed live replays without weakening any existing content or verification gate.

## Required dry cases

1. `happy_local_no_cut`: valid transcript/recording package, deck, tracker rows, tiles, auth descriptors, and no required cut. Expect `fast_ready`, no browser acquisition, no transcode, and no board mutation in dry mode.
2. `happy_local_cut`: timestamped transcript and a valid positive cut. Expect hardware auto-selection when available or `standard_ready` software fallback, plus duration/hash/stream/timing evidence.
3. `corrupt_local`: supplied corrupt media. Expect a preflight blocker inside 60 seconds, no Kaia fallback, and no board mutation.
4. `missing_asset`: missing deck, selected tracker row, tile, or connector access. Expect blocked preflight unless explicit draft-only mode is allowed.
5. `editor_alias`: Luke Rafferty resolves under a noncanonical email alias. Expect selection by stable organization user/invite ID, never by a hardcoded email alone.
6. `editor_captcha_race`: the actual invite fails after preflight. Expect one targeted retry at most, `published_internal` plus `editor_pending`, no Slack completion, and no endpoint discovery.
7. `endpoint_drift`: a known endpoint returns an unexpected response. Expect one targeted retry, then `maintenance_required` by the hard deadline; no app-bundle or source-map inspection.
8. `structural_regression`: modify ROI bytes, value-widget structure, or a baseline example. Expect the bounded verifier to reject publish or completion.
9. `compact_io`: assert exact Sheet ranges and selected API fields; full config, organization, DOM, and source-map payloads must not reach stdout/model context.
10. `hard_ceiling`: inject a slow external operation. Expect no discovery after 480 seconds, no retry after 540 seconds, and a truthful result by 600 seconds.
11. `idempotent_resume`: supply a prior receipt and board ID. Expect reuse of verified assets/state and no duplicate board or content creation.
12. `usage_schema`: unavailable token or pricing data must be null with a reason; never fabricated.

## Live performance acceptance

Measure at least five warmed `fast_ready` replays before claiming the SLA is demonstrated in production. Record total wall-clock time and stage timings, including external waits.

- p50 target: `<=300` seconds
- p95 target: `<=480` seconds
- all runs, including exceptions: truthful result `<=600` seconds

Do not report only successful fast samples. Until this benchmark passes, describe five minutes as a stretch target and 5–8 minutes as the designed operating range.
