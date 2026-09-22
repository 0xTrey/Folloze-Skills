# Folloze Skills

Public source for Folloze internal skill development, operator workflows, and reusable learning material.

This broad repository is **not the recommended customer or Etai install**. Customer, partner, Claude, Codex, campaign, webinar, and 1:1 board-building agents should use the portable [Folloze MCP Customer Skills](https://github.com/0xTrey/folloze-mcp-customer-skills) pack. That pack owns the customer routing layer, ABM Strategist, mandatory Brand Harvester gate, and motion-specific builders without inheriting private operational assumptions.

## Repository Roles

| Repository | Recommended use |
| --- | --- |
| `folloze-mcp-customer-skills` | Etai, customers, partners, Claude/Codex board agents, and general board creation. |
| `Folloze-Skills` (this repo) | Internal development, reusable Folloze brand material, authorized demo-instance operations, and reviewed internal workflows. |

General requests such as “build a Folloze board,” “make a 1:1,” “build a campaign landing page,” or “promote a webinar” should route to the customer pack. `Folloze-MCP-Demo-Builder` is intentionally narrower: it is only for an authorized internal operator working in a named demo instance or updating a known internal demo board.

## Safe Internal Install

Clone a clean copy and install only skills enabled in `skills-manifest.json`:

```bash
git clone https://github.com/0xTrey/Folloze-Skills.git ~/Projects/Folloze-Skills
cd ~/Projects/Folloze-Skills
python3 scripts/sync_codex_skills.py --client codex --mode copy
```

Claude and dual-client installs are also supported for authorized internal users:

```bash
python3 scripts/sync_codex_skills.py --client claude --mode copy
python3 scripts/sync_codex_skills.py --client both --mode copy
```

Copy mode is preferred because the active agent never points at a dirty development checkout. The installer refuses to overwrite an existing user-owned skill directory. It only replaces a repo-managed symlink or a copy carrying the Folloze management marker.

## Safe Updates

`skills-update-folloze` is pull/install-only. It does not inspect local skill directories, publish local work, commit, or push.

If the preferred development checkout is dirty, ahead/diverged, detached, or on another branch, the updater preserves it exactly and uses a dedicated clean sync clone configured by `FOLLOZE_SKILLS_SYNC_REPO_ROOT`. The default clean clone lives under the current user's cache directory.

```bash
python3 Skills/skills-update-folloze/scripts/update_folloze_skills.py --dry-run
python3 Skills/skills-update-folloze/scripts/update_folloze_skills.py
```

The weekly pull/install-only automation is defined in `AutomationTemplates/folloze-skills-weekly-update/template.json`.

## Publication Is Explicit And PR-Only

There is no automatic local-skill discovery or publish-before-sync step.

`scripts/publish_local_skills_to_repo.py` requires all of the following:

- a clean, non-main PR branch;
- one or more explicit `--skill` names;
- matching approvals in `publication-allowlist.json`;
- a real source directory rather than a symlink;
- a passing secret, PII, local-path, and exclusion scan;
- a destination under `Skills/Published/`.

The helper stages a review candidate in the worktree and manifest only. It never commits or pushes. An empty publication allowlist means no skill is approved for staging.

## Public-Release Gates

Enable the versioned local hooks once per clone:

```bash
git config core.hooksPath .githooks
```

The pre-commit hook scans staged content and validates the manifest. The pre-push hook scans all tracked public content and validates again. CI runs both gates on every pull request and `main` push.

Manual equivalents:

```bash
python3 scripts/validate_skills.py
python3 scripts/scan_public_release.py
python3 -m unittest discover -s tests -v
```

Generated artifacts, browser state, QA output, research bundles, environment files, caches, archives, and private material are excluded from new commits. Existing historical artifacts are not deleted by this cleanup.

## Board Builder Lifecycle

- `folloze-campaign-board-builder` is deprecated and disabled in the manifest. Its files remain as historical learning material; customer builds should use the customer pack router.
- `Folloze-MCP-Demo-Builder` remains enabled for explicit internal demo-instance work only. It contains no default person, tracker, spreadsheet, tab, row, or profile ID.
- The old `skills-updater` alias is deprecated in favor of the pull/install-only `skills-update-folloze`. Existing local files are never deleted automatically.

## Structure

- `Skills/`: internal and reusable skill sources.
- `Skills/support/`: CS and support troubleshooting skills.
- `skills-manifest.json`: explicit install allowlist and lifecycle metadata.
- `publication-allowlist.json`: fail-closed list of reviewed public publication candidates.
- `scripts/`: install, update, validation, publication, and security helpers.
- `AutomationTemplates/`: managed Codex automation templates.
- `.githooks/` and `.github/workflows/`: local and CI public-release gates.

Keep restricted deal material, credentials, tokens, cookies, private policies, operator-specific identifiers, and customer data out of this public repository. Use pointers to access-controlled sources where internal context is required.
