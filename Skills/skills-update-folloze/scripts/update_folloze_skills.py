#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_REPO_URL = os.environ.get(
    "FOLLOZE_SKILLS_REPO_URL",
    "https://github.com/0xTrey/Folloze-Skills.git",
)
DEFAULT_REPO_ROOT = Path(
    os.environ.get(
        "FOLLOZE_SKILLS_REPO_ROOT",
        str(Path.home() / "Projects" / "Folloze-Skills"),
    )
)
DEFAULT_SYNC_REPO_ROOT = Path(
    os.environ.get(
        "FOLLOZE_SKILLS_SYNC_REPO_ROOT",
        str(Path.home() / ".cache" / "folloze-skills" / "Folloze-Skills-sync"),
    )
)
DEFAULT_BRANCH = os.environ.get("FOLLOZE_SKILLS_REPO_BRANCH", "main")
DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
DEFAULT_DEST = DEFAULT_CODEX_HOME / "skills"
MORNING_BRIEF_SKILL = "folloze-morning-brief"
MORNING_BRIEF_AUTOMATION_TEMPLATE = (
    "AutomationTemplates/folloze-morning-brief-daily/template.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap, safely pull, and sync shared Folloze Codex skills.",
    )
    parser.add_argument("--repo-root", default=str(DEFAULT_REPO_ROOT))
    parser.add_argument(
        "--sync-repo-root",
        default=str(DEFAULT_SYNC_REPO_ROOT),
        help=(
            "Dedicated clean clone used when --repo-root is dirty, on another branch, "
            "or ahead/diverged from origin."
        ),
    )
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--dest", default=str(DEFAULT_DEST))
    parser.add_argument(
        "--mode",
        choices=("symlink", "copy"),
        default="copy",
        help="Install mode. Copy is the safe default so installs never point at a development checkout.",
    )
    parser.add_argument("--skill", action="append", default=[])
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def run(
    cmd: list[str],
    *,
    dry_run: bool = False,
) -> subprocess.CompletedProcess[str] | None:
    print(f"$ {' '.join(cmd)}")
    if dry_run:
        return None
    return subprocess.run(cmd, check=True, text=True)


def git_output(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def is_git_repo(path: Path) -> bool:
    if not path.exists():
        return False
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
        text=True,
        capture_output=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def clone_repo(repo_root: Path, repo_url: str, branch: str, dry_run: bool) -> None:
    run(
        ["git", "clone", "--branch", branch, "--single-branch", repo_url, str(repo_root)],
        dry_run=dry_run,
    )


def prepare_existing_repo(repo_root: Path, branch: str, dry_run: bool) -> None:
    run(["git", "-C", str(repo_root), "fetch", "origin", branch], dry_run=dry_run)


def repo_requires_clean_clone(repo_root: Path, branch: str) -> tuple[bool, str]:
    status = git_output(repo_root, "status", "--porcelain")
    if status:
        return True, "working tree has local changes"

    current_branch = git_output(repo_root, "branch", "--show-current")
    if current_branch != branch:
        return True, f"checked out branch is {current_branch or '(detached HEAD)'}, not {branch}"

    result = subprocess.run(
        [
            "git",
            "-C",
            str(repo_root),
            "rev-list",
            "--left-right",
            "--count",
            f"HEAD...origin/{branch}",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    ahead, _behind = (int(value) for value in result.stdout.split())
    if ahead:
        return True, f"local branch is {ahead} commit(s) ahead or diverged"
    return False, "clean fast-forwardable clone"


def prepare_clean_sync_clone(
    sync_root: Path,
    repo_url: str,
    branch: str,
    dry_run: bool,
) -> bool:
    if not sync_root.exists():
        clone_repo(sync_root, repo_url, branch, dry_run)
        return True
    if not is_git_repo(sync_root):
        raise SystemExit(f"Clean sync path exists but is not a git repo: {sync_root}")
    configured_remote = git_output(sync_root, "remote", "get-url", "origin")
    if configured_remote.rstrip("/") != repo_url.rstrip("/"):
        raise SystemExit(
            f"Dedicated sync clone origin does not match the configured repository URL: {sync_root}"
        )
    if git_output(sync_root, "status", "--porcelain"):
        raise SystemExit(
            f"Dedicated sync clone has local changes: {sync_root}. "
            "Move those changes to a development checkout or choose another --sync-repo-root."
        )
    prepare_existing_repo(sync_root, branch, dry_run)
    if not dry_run:
        current_branch = git_output(sync_root, "branch", "--show-current")
        if current_branch != branch:
            run(["git", "-C", str(sync_root), "checkout", branch])
        run(["git", "-C", str(sync_root), "pull", "--ff-only", "origin", branch])
    return False


def select_sync_repo(
    repo_root: Path,
    sync_root: Path,
    repo_url: str,
    branch: str,
    dry_run: bool,
) -> tuple[Path, bool]:
    if not repo_root.exists():
        clone_repo(repo_root, repo_url, branch, dry_run)
        return repo_root, True
    if not is_git_repo(repo_root):
        raise SystemExit(f"Existing path is not a git repo: {repo_root}")

    prepare_existing_repo(repo_root, branch, dry_run)
    if dry_run:
        dirty = bool(git_output(repo_root, "status", "--porcelain"))
        branch_name = git_output(repo_root, "branch", "--show-current")
        if dirty or branch_name != branch:
            reason = "working tree has local changes" if dirty else f"checked out branch is {branch_name}"
            print(f"primary_repo_not_used: {reason}")
            print(f"clean_sync_repo: {sync_root}")
            return sync_root, not sync_root.exists()
        return repo_root, False

    use_clean, reason = repo_requires_clean_clone(repo_root, branch)
    if use_clean:
        print(f"primary_repo_preserved: {repo_root} ({reason})")
        cloned = prepare_clean_sync_clone(sync_root, repo_url, branch, dry_run=False)
        print(f"sync_repo: {sync_root}")
        return sync_root, cloned

    run(["git", "-C", str(repo_root), "pull", "--ff-only", "origin", branch])
    return repo_root, False


def changed_files(repo_root: Path, old_head: str | None, new_head: str) -> list[str]:
    if old_head is None:
        return []
    output = git_output(repo_root, "diff", "--name-only", f"{old_head}..{new_head}")
    return [line for line in output.splitlines() if line]


def load_manifest(repo_root: Path) -> dict:
    return json.loads((repo_root / "skills-manifest.json").read_text())


def enabled_skills(manifest: dict) -> set[str]:
    return {skill["name"] for skill in manifest["skills"] if skill.get("enabled", True)}


def changed_skill_names(files: list[str], manifest: dict) -> set[str]:
    changed: set[str] = set()
    for skill in manifest["skills"]:
        prefix = Path(skill["path"])
        if any(Path(rel_path) == prefix or prefix in Path(rel_path).parents for rel_path in files):
            changed.add(skill["name"])
    return changed


def missing_installed_skills(dest: Path, enabled_names: set[str]) -> set[str]:
    return {name for name in enabled_names if not (dest / name).exists()}


def sync_skills(
    repo_root: Path,
    dest: Path,
    mode: str,
    skill_names: list[str] | None,
    prune: bool,
    dry_run: bool,
) -> None:
    cmd = [
        sys.executable,
        str(repo_root / "scripts" / "sync_codex_skills.py"),
        "--repo-root",
        str(repo_root),
        "--dest",
        str(dest),
        "--mode",
        mode,
        "--overwrite",
    ]
    if prune:
        cmd.append("--prune")
    if dry_run:
        cmd.append("--dry-run")
    for skill_name in skill_names or []:
        cmd.extend(["--skill", skill_name])
    run(cmd)


def print_install_triggered_automation_notice(repo_root: Path, dest: Path) -> None:
    template = repo_root / MORNING_BRIEF_AUTOMATION_TEMPLATE
    if (dest / MORNING_BRIEF_SKILL).exists() and template.exists():
        print("install_triggered_automation: Folloze Morning Brief")
        print(f"automation_template: {template}")


def main() -> int:
    args = parse_args()
    requested_repo = Path(args.repo_root).expanduser().resolve()
    clean_sync_repo = Path(args.sync_repo_root).expanduser().resolve()
    dest = Path(args.dest).expanduser().resolve()
    requested = set(args.skill)

    old_head = None
    if is_git_repo(requested_repo):
        old_head = git_output(requested_repo, "rev-parse", "HEAD")

    repo_root, cloned = select_sync_repo(
        requested_repo,
        clean_sync_repo,
        args.repo_url,
        args.branch,
        args.dry_run,
    )
    if args.dry_run and not repo_root.exists():
        print("Dry run: a clean clone and full sync would be performed.")
        return 0

    if args.dry_run and repo_root == requested_repo:
        new_head = git_output(repo_root, "rev-parse", f"origin/{args.branch}")
    else:
        new_head = git_output(repo_root, "rev-parse", "HEAD")
    if repo_root != requested_repo or cloned:
        old_head = None

    manifest = load_manifest(repo_root)
    enabled = enabled_skills(manifest)
    files = changed_files(repo_root, old_head, new_head)
    changed = changed_skill_names(files, manifest)
    missing = missing_installed_skills(dest, enabled)

    print(f"repo_used: {repo_root}")
    print(f"old_head: {old_head or '(clean clone)'}")
    print(f"new_head: {new_head}")

    if args.dry_run:
        if files:
            print("changed_files:")
            for path in files:
                print(f"- {path}")
        if missing:
            print(f"missing_installed_skills: {', '.join(sorted(missing))}")
        return 0

    manifest_changed = "skills-manifest.json" in files
    sync_all = cloned or repo_root != requested_repo or args.all or (not requested and manifest_changed)
    if requested:
        selected = sorted(requested)
    elif sync_all:
        selected = []
    else:
        selected = sorted(changed | missing)

    if not sync_all and not selected:
        print("Repo already up to date. No skill changes to sync.")
        return 0

    sync_skills(repo_root, dest, args.mode, selected or None, sync_all, False)
    print_install_triggered_automation_notice(repo_root, dest)
    print("Restart Codex to reload updated skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
