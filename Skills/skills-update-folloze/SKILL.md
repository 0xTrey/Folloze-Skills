---
name: skills-update-folloze
description: Pull and install the reviewed Folloze internal skills manifest into a local Codex environment without publishing local skills. Use for one-off Folloze skill refreshes or the managed weekly updater. Customer and partner board-building agents should install the portable customer pack instead.
---

# Skills Update Folloze

This is a pull/install-only updater for the broad Folloze internal development and learning repository.

For Etai, customers, partners, Claude users, and general board-building agents, use the portable customer distribution instead:

`https://github.com/0xTrey/folloze-mcp-customer-skills`

That customer pack is the recommended route for ABM strategy, mandatory brand harvesting, and motion-specific customer board builders. This broad repo may contain internal operator workflows, deprecated learning sources, and skills that require private systems.

## Safety Contract

- Never inspect or auto-discover untracked local skills before an update.
- Never copy local skills into this repository as part of an update.
- Never commit or push from the updater.
- Preserve a dirty, ahead, diverged, or differently checked-out development clone exactly as found.
- When the development clone is unsuitable for a fast-forward pull, use the dedicated clean sync clone.
- Install from the explicit enabled entries in `skills-manifest.json` only.
- Copy installs are the safe default; they do not point the active agent at a dirty development checkout.
- Do not overwrite an unowned local skill directory. The sync helper only replaces repo-managed symlinks or directories carrying its management marker.

## Default Update

Run the helper shipped inside this skill:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py"
```

The updater uses these portable overrides when set:

- `FOLLOZE_SKILLS_REPO_ROOT`: preferred development clone.
- `FOLLOZE_SKILLS_SYNC_REPO_ROOT`: dedicated clean sync clone.
- `FOLLOZE_SKILLS_REPO_URL`: remote repository URL.
- `FOLLOZE_SKILLS_REPO_BRANCH`: reviewed branch, normally `main`.
- `CODEX_HOME`: Codex data root.

If the preferred clone is dirty, ahead/diverged, detached, or on another branch, the updater reports the reason and syncs from the clean clone without cleaning, resetting, switching, or committing the development checkout.

Useful variants:

```bash
# Preview the selected source and planned refresh.
python3 "${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py" --dry-run

# Refresh all enabled internal skills.
python3 "${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py" --all

# Refresh one enabled skill.
python3 "${CODEX_HOME:-$HOME/.codex}/skills/skills-update-folloze/scripts/update_folloze_skills.py" \
  --skill folloze-brand-kit
```

## Direct Repo Install

The repo-level installer supports both agent clients:

```bash
python3 scripts/sync_codex_skills.py --client codex --mode copy
python3 scripts/sync_codex_skills.py --client claude --mode copy
python3 scripts/sync_codex_skills.py --client both --mode copy
```

This broad install is for authorized internal users. Customer-facing agents should follow the customer repo installer rather than installing every internal skill.

## Explicit Publication Is Separate

Publishing is never part of update or sync. A maintainer may stage a reviewed candidate only from a clean non-main PR branch by:

1. Adding its exact name and destination to `publication-allowlist.json` through review.
2. Placing a real, non-symlinked source directory under an explicitly selected source root.
3. Running the repo-level helper with `--skill <exact-name>`.
4. Running validation and the public-release scanner.
5. Reviewing the diff and opening a PR.

```bash
python3 scripts/publish_local_skills_to_repo.py \
  --source-root /path/to/reviewed/skills \
  --skill exact-approved-name
python3 scripts/validate_skills.py
python3 scripts/scan_public_release.py
```

The publisher refuses automatic discovery, external symlinks, dirty/main-branch worktrees, non-allowlisted names, secrets, hardcoded personal email addresses, and machine-specific home paths. It never commits or pushes.

## Weekly Automation

Use `AutomationTemplates/folloze-skills-weekly-update/template.json`. The automation is pull/install-only and uses this helper. It must not publish, commit, push, prune user-owned directories, or repair the development checkout.

## Expected Response

Report:

- development clone status and whether it was preserved;
- exact sync clone used;
- old and new commit IDs;
- skills refreshed or already current;
- any unmanaged destination that requires the operator to move or back up;
- whether Codex should be restarted.
