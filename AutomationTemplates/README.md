# Automation Templates

Recommended recurring automations for teams using the shared Folloze skill catalog.

These templates are the approved automation definitions the team should create in Codex after installing the skills. The updater skill can point Codex at install-triggered templates, but raw repo sync alone does not create automations.

For Codex automations, each template should define:

- `id`
- `name`
- `summary`
- `runner`
- `kind`
- `schedule`
- `execution_environment`
- `model`
- `reasoning_effort`
- `cwd_hint`
- `prompt`

The current recommended default for skill distribution is `folloze-skills-weekly-update`.

Skill-specific install-triggered templates:

- `folloze-morning-brief-daily`
- `folloze-eod-pipeline-handoff-daily`
