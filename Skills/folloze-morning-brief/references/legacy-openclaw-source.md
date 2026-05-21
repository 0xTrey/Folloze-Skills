# Legacy OpenClaw Migration Notes

The original morning brief ran as a chief-of-staff workflow in OpenClaw and later Hermes.

Legacy behavior:

- daily run at 8:00 AM Central
- named persona branding
- Trey-specific operating context
- external chat delivery
- local deal-index based pipeline context
- broad calendar and pipeline discovery

Codex skill migration decisions:

- Skill name is `folloze-morning-brief`.
- Named-persona branding is removed for the team version.
- Delivery is Codex inbox/thread only.
- The brief is generated for the current teammate, not Trey.
- The pipeline source changes from local deal-index files to Salesforce open opportunities owned by the current user.
- Customer-success users receive an account-level view, grouping multiple opportunities under the same account.
- Granola remains a required follow-up source when available.
- Missing sources produce caveats, not false negatives.
- The skill is read-only and report-only.

Historical pitfalls to avoid:

- including every calendar event instead of filtering for external and deal-relevant meetings
- treating personal/admin events as GTM execution priorities
- overstating stale pipeline context
- blending content generation with delivery failures
- using external-chat-specific language or destination IDs
- using user-specific absolute paths
