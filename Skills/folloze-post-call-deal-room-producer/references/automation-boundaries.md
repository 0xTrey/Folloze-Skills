# Post-Call Deal Room Execution Boundaries

Use the most deterministic interface that is currently proven for each step.

## Manual V1 Production Split

| Step | Preferred interface | Why |
| --- | --- | --- |
| Start a run | Manual operator request | No background discovery or Salesforce dependency |
| Read Granola or other call notes | Approved connector or authenticated app | Private source context |
| Find Kaia recording | Browser Control | Authenticated UI search is proven |
| Request Kaia export | Browser Control | The current action lives under Meeting actions |
| Wait for export | Pause and resume the same manual task | No Hermes or cron job |
| Match Outreach email | Gmail connector first | Sender, title, timestamp, and body can be matched structurally |
| Retrieve ZIP | Email download link via authenticated browser | Link is signed and expiring |
| Inspect and prepare media | Included Python helper | Deterministic, local, testable, and credential-free |
| Validate/copy template | Folloze API | Board identity and template flag need readback |
| Update native board config | Folloze API | Existing direct writer is proven |
| Create/update native link items | Folloze API only where the current contract is proven | Avoid unnecessary browser editing |
| Upload MP3/MP4 | Verified Content Upload API when available, Browser Control fallback | Never guess a binary endpoint |
| Publish and metadata readback | Folloze API | Explicit state and response evidence |
| Visual and public playback QA | Browser Control | Layout and playback require rendered verification |

## Disabled Background Paths

Do not use Hermes, cron, LaunchAgents, Salesforce polling, or automatic meeting detection in v1. Existing paused post-intro DSR jobs must remain paused.

## Candidate API Improvement

The largest remaining browser dependency is Folloze binary upload. Before automating it through an API:

1. Capture the live application's upload-init, transfer, finalize, and item-attachment requests using an approved network-inspection method.
2. Confirm whether the contract is stable, authorized, and usable by the existing Folloze OAuth client.
3. Implement behind a feature flag.
4. Validate MIME type, file size, checksum, upload completion, created item ID, category attachment, and board readback.
5. Verify public playback after publish.
6. Retain Browser Control fallback.

Do not infer an upload endpoint from link-item APIs. Do not copy browser tokens into scripts.

## Manual Resume Shape

The operator resumes from the last recorded checkpoint. Do not submit multiple Kaia exports, duplicate a board, or create another recording item simply because the email was delayed.

## V1 Rerun Boundary

Historical rerun reconciliation is out of scope. Within one active manual run, preserve the Kaia recording ID, Folloze board ID, media hash, and content-item ID so a resume does not duplicate work.
