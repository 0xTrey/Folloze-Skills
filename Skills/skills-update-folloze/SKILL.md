---
name: skills-update-folloze
description: Update the shared Folloze Codex skills from the central GitHub repository into the local ~/.codex/skills installation, or create the standard weekly Codex automation that keeps those skills current for the GTM team. Use when someone says "update my skills", "sync the Folloze skills", "pull the latest shared skills", "refresh our Codex skills", or asks Codex to set up the recurring team updater automation.
---

# Skills Update Folloze

Use this skill to refresh the locally installed Folloze skills from the central GitHub repo.

This skill is the user-facing entrypoint for the shared-skill distribution flow:

- it ensures the team repo exists locally
- it fast-forwards the repo from GitHub
- it detects which `Skills/<name>/` folders changed
- it syncs those changes into `${CODEX_HOME:-$HOME/.codex}/skills`

By default it assumes the local clone lives at `~/Projects/Folloze-Skills`. Override that with `FOLLOZE_SKILLS_REPO_ROOT` if needed.

## When To Use

Use this skill when the user wants any of the following:

- update shared Folloze skills
- sync newly added skills from the repo
- pull the latest skill changes from GitHub
- refresh the local Codex skill installation after another teammate updated a skill
- create the standard recurring Codex automation for team skill updates

## One-Time Assumptions

- Each teammate should have one clean local clone of the shared repo
- That clone should be used for syncing, not for ad hoc edits
- If the repo is private, the machine must already have GitHub access configured

## Recommended Team Pattern

For the GTM team, the recommended automation pattern is:

- clone the repo once to a stable local path
- sync the skills into `~/.codex/skills`
- create a Codex cron automation named `Folloze Skills Weekly Update`
- schedule it for every Wednesday at 12:00 PM in the teammate's local time zone

Prefer the Codex automation route over a raw `launchd` job when the user wants a managed summary after each run.

## Default Command

Run the helper script shipped with this skill:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py"
```

The helper will:

- clone `Folloze-Skills` into `~/Projects/Folloze-Skills` if it does not exist
- fetch and fast-forward `main`
- sync only changed skills when possible
- fall back to a full sync when the manifest changes or on first install

## Useful Variants

Dry run:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py" --dry-run
```

Force a full refresh:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py" --all
```

Refresh only specific skills:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py" \
  --skill account-org-chart \
  --skill Salesforce-Update
```

## Create The Standard Automation

If the user asks for ongoing team updates, create a recurring Codex automation with this spec:

- name: `Folloze Skills Weekly Update`
- schedule: every Wednesday at 12:00 PM in the user's local time zone
- workspace root: the user's home directory
- scope: only the shared Folloze skills repo and the local Codex skills install

Use this task prompt:

```text
Use the shared Folloze skills repo as the source of truth. Prefer FOLLOZE_SKILLS_REPO_ROOT if it is set; otherwise use ~/Projects/Folloze-Skills. Prefer FOLLOZE_SKILLS_REPO_URL if it is set; otherwise use https://github.com/0xTrey/Folloze-Skills.git. Track the main branch. If the local repo clone does not exist, clone it. If it does exist, verify it is a git repo and use that clone. Do not overwrite, repair, or clean a dirty repo; if the local clone has uncommitted changes, stop and report that a clean clone is required. Update the repo from origin/main with a fast-forward pull. Sync Codex skills from the repo into ${CODEX_HOME:-$HOME/.codex}/skills. Prefer using the installed helper at ${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py when available. During migration from older installs, ${CODEX_HOME:-$HOME/.codex}/skills/skills-updater/scripts/update_folloze_skills.py is also acceptable. If neither installed helper is available yet, run the repo helper with equivalent behavior. Make sure the sync includes both changed existing skills and newly added skills from the repo manifest. If the manifest changed or a new skill was added, do a full refresh so new skills are installed automatically, including weekly-customer-action-items if it is present and not already installed. Return a short inbox summary stating whether the repo was updated or already current, which skills were refreshed, which new skills were installed, and whether Codex should be restarted. Only touch the shared Folloze skills repo and the local Codex skills install.
```

## Guardrails

- If the local repo clone has uncommitted changes, stop and tell the user to use a clean clone for updates
- Do not edit `~/.codex/skills` by hand as part of normal updates; use the helper script
- After a successful update, tell the user whether Codex should be restarted

## Expected Response

Return a short summary:

- repo updated or already current
- which skills were refreshed
- which new skills were installed
- whether a Codex restart is needed
