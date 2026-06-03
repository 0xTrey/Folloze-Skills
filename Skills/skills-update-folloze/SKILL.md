---
name: skills-update-folloze
description: Update the shared Folloze Codex skills from the central GitHub repository into the local ~/.codex/skills installation, create the standard weekly Codex automation that keeps those skills current, and create install-triggered automations such as Folloze Morning Brief. Use when someone says "update my skills", "sync the Folloze skills", "pull the latest shared skills", "refresh our Codex skills", installs a shared Folloze skill, or asks Codex to set up the recurring team updater or morning brief automation.
---

# Skills Update Folloze

Use this skill to refresh the locally installed Folloze skills from the central GitHub repo.

This skill is the user-facing entrypoint for the shared-skill distribution flow:

- it can publish newly created local Codex skills into the shared repo under `Skills/Troy Folloze Created Skills/`
- it ensures the team repo exists locally
- it fast-forwards the repo from GitHub
- it detects which `Skills/<name>/` folders changed
- it syncs those changes into `${CODEX_HOME:-$HOME/.codex}/skills`
- it compares local and repo skill trees so the newer copy wins during transfers

By default it assumes the local clone lives at `~/Projects/Folloze-Skills`. Override that with `FOLLOZE_SKILLS_REPO_ROOT` if needed.

## When To Use

Use this skill when the user wants any of the following:

- update shared Folloze skills
- sync newly added skills from the repo
- pull the latest skill changes from GitHub
- refresh the local Codex skill installation after another teammate updated a skill
- create the standard recurring Codex automation for team skill updates
- create the local daily Folloze Morning Brief automation after `folloze-morning-brief` is installed

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
- if `folloze-morning-brief` is installed, create a Codex cron automation named `Folloze Morning Brief`
- schedule the morning brief for every day at 7:00 AM in the teammate's local time zone

Prefer the Codex automation route over a raw `launchd` job when the user wants a managed summary after each run.

## Default Command

Run the helper script shipped with this skill:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/publish_local_skills_to_repo.py"
python3 "${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py"
```

The helper will:

- scan `${CODEX_HOME:-$HOME/.codex}/skills` for local skills that are not yet in the shared repo manifest
- refresh an already tracked repo skill when the local copy is newer
- copy those new local skills into `Skills/Troy Folloze Created Skills/<name>/`
- add them to `skills-manifest.json` with the nested repo path
- clone `Folloze-Skills` into `~/Projects/Folloze-Skills` if it does not exist
- fetch and fast-forward `main`
- sync only changed skills when possible
- fall back to a full sync when the manifest changes or on first install
- keep a newer local installed skill instead of overwriting it with an older repo copy
- print a follow-up notice when the morning brief automation should be created

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
Use the shared Folloze skills repo as the source of truth. Prefer FOLLOZE_SKILLS_REPO_ROOT if it is set; otherwise use ~/Projects/Folloze-Skills. Prefer FOLLOZE_SKILLS_REPO_URL if it is set; otherwise use https://github.com/0xTrey/Folloze-Skills.git. Track the main branch. Before pulling from GitHub, inspect ${CODEX_HOME:-$HOME/.codex}/skills for user-created skills that are not already tracked in the repo manifest and are not system or plugin-managed skills. Copy any such new local skills into Skills/Troy Folloze Created Skills/<name>/ in the repo, add them to skills-manifest.json as enabled skills, and report which skills were newly staged for GitHub. For skills that already exist in both places, compare the local and repo skill trees and keep whichever copy is newer based on recursive file modification times. If the local repo clone does not exist, clone it. If it does exist, verify it is a git repo and use that clone. Do not overwrite, repair, or clean a dirty repo; if the local clone has uncommitted changes, use a clean sync clone for repo-to-local refresh work, but still report the dirty working repo because it may contain unpublished local skills. Update the clean sync repo from origin/main with a fast-forward pull. Sync Codex skills from the repo into ${CODEX_HOME:-$HOME/.codex}/skills. When a skill exists in both the repo and the local Codex install, keep the newer copy instead of blindly overwriting. Prefer using the installed helper at ${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py when available. During migration from older installs, ${CODEX_HOME:-$HOME/.codex}/skills/skills-updater/scripts/update_folloze_skills.py is also acceptable. If neither installed helper is available yet, run the repo helper with equivalent behavior. Make sure the sync includes both changed existing skills and newly added skills from the repo manifest. If the manifest changed or a new skill was added, do a full refresh so new skills are installed automatically, including folloze-morning-brief and weekly-customer-action-items when present. If GitHub auth is available and the repo has newly staged or refreshed local skills, commit and push those manifest and skill-folder changes to origin/main; if GitHub auth is blocked, report that explicitly. After syncing, if folloze-morning-brief is installed, ensure a local Codex automation named Folloze Morning Brief exists using AutomationTemplates/folloze-morning-brief-daily/template.json. Return a short inbox summary stating whether the repo was updated or already current, which skills were refreshed, which local or repo copies were kept because they were newer, which new skills were installed, which install-triggered automations were created or already present, and whether Codex should be restarted. Only touch the shared Folloze skills repo, the local Codex skills install, and the Folloze Morning Brief automation.
```

## Create The Morning Brief Automation

If `folloze-morning-brief` is installed or the user asks to set up the morning brief, create or update a recurring Codex automation from `AutomationTemplates/folloze-morning-brief-daily/template.json`.

Use this behavior:

- name: `Folloze Morning Brief`
- schedule: every day at 7:00 AM in the user's local time zone
- workspace root: the user's home directory
- delivery: Codex inbox/thread
- scope: read-only Folloze GTM brief for the current authenticated teammate
- no delivery outside the Codex inbox/thread in v1

If the automation tool is unavailable in the current Codex session, report that the skill was installed and the morning-brief automation still needs to be created from the repo template.

## Guardrails

- If the local repo clone has uncommitted changes, stop and tell the user to use a clean clone for updates
- Do not edit `~/.codex/skills` by hand as part of normal updates; use the helper script
- Do not create unrelated automations when setting up the morning brief
- After a successful update, tell the user whether Codex should be restarted

## Expected Response

Return a short summary:

- repo updated or already current
- which new local skills were staged into `Skills/Troy Folloze Created Skills/`
- which skills were refreshed
- which new skills were installed
- whether the Folloze Morning Brief automation was created, updated, already present, or still needs setup
- whether a Codex restart is needed
