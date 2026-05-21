# Legacy Workflow Notes

The original end-of-day handoff ran as a chief-of-staff OpenClaw workflow with an external chat delivery target. The team Codex version keeps the useful operating pattern and removes legacy delivery assumptions.

Legacy behavior:

- daily end-of-day handoff
- separate daily pipeline-risk analysis
- external chat delivery
- local deal-index based pipeline context
- local daily-sync artifacts
- current-day calendar and meeting context

Codex skill migration decisions:

- Skill name is `folloze-eod-pipeline-handoff`.
- Named-persona branding is removed for the team version.
- Delivery is Codex inbox/thread only.
- The handoff is generated for the current teammate.
- Salesforce owned opportunities are preferred for pipeline risk.
- Local deal-index and daily-sync files are optional fallback/enrichment sources.
- The weekly customer action-items method becomes a daily rolling action ledger.
- The skill is read-only and report-only.

Historical pitfalls to avoid:

- producing three separate reports instead of one handoff
- treating internal automation/admin work as customer progress
- listing tasks as open without checking completion evidence
- overstating stale local deal-index context
- using external-chat-specific language or destination IDs
- using user-specific absolute paths
