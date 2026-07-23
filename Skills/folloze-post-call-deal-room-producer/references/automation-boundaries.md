# Post-Call Deal Room Automation Boundaries

Use the most deterministic interface that is currently proven for each step.

## Current Production Split

| Step | Preferred interface | Why |
| --- | --- | --- |
| Detect completed call and opportunity | Connector or approved API | Structured matching and readback |
| Read Granola or other call notes | Approved connector or authenticated app | Private source context |
| Find Kaia recording | Browser Control | Authenticated UI search is proven |
| Request Kaia export | Browser Control | The current action lives under Meeting actions |
| Wait for export | Resumable runner such as Hermes | The export is asynchronous |
| Match Outreach email | Gmail connector first | Sender, title, timestamp, and body can be matched structurally |
| Retrieve ZIP | Email download link via authenticated browser | Link is signed and expiring |
| Inspect and prepare media | Included Python helper | Deterministic, local, testable, and credential-free |
| Validate/copy template | Folloze API | Board identity and template flag need readback |
| Update native board config | Folloze API | Existing direct writer is proven |
| Create/update native link items | Folloze API only where the current contract is proven | Avoid unnecessary browser editing |
| Upload MP3/MP4 | Browser Control | Binary media API contract is not yet proven |
| Publish and metadata readback | Folloze API | Explicit state and response evidence |
| Visual and public playback QA | Browser Control | Layout and playback require rendered verification |

## Hermes Role

Hermes can own orchestration without owning credentials or media:

- persist the non-secret state machine
- wake after the export-request checkpoint
- poll Gmail with bounded retries
- notify the operator when the ZIP is available or a checkpoint needs input
- launch the deterministic media-preparation step
- hand the prepared local path to the foreground Browser Control upload step
- record board and verification evidence

Hermes should not store browser cookies, signed Outreach links, raw ZIP bytes, recordings, or transcript content.

## Candidate API Improvement

The largest remaining browser dependency is Folloze binary upload. Before automating it through an API:

1. Capture the live application's upload-init, transfer, finalize, and item-attachment requests using an approved network-inspection method.
2. Confirm whether the contract is stable, authorized, and usable by the existing Folloze OAuth client.
3. Implement behind a feature flag.
4. Validate MIME type, file size, checksum, upload completion, created item ID, category attachment, and board readback.
5. Verify public playback after publish.
6. Retain Browser Control fallback.

Do not infer an upload endpoint from link-item APIs. Do not copy browser tokens into scripts.

## Retry Policy Shape

Keep retry numbers configurable until the owner answers the workflow questions. A safe default shape is:

- poll after a short initial delay
- retry with bounded backoff for a fixed total window
- never submit multiple Kaia exports during that window
- escalate with the exact meeting title, recording ID, request timestamp, and current checkpoint
- allow a human to resume without rebuilding the board or requesting a new export

## Idempotency

Use stable identifiers:

- source: Kaia recording ID
- board: Folloze board ID
- media: SHA-256 hash
- item: Folloze content-item ID after upload

On a rerun, compare these identifiers before creating another export, board, item, or publish event. Never duplicate a recording card merely because the run resumed.
