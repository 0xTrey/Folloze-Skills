#!/usr/bin/env python3
"""Stage an explicitly approved local skill for public-repo review.

This helper never discovers or publishes skills automatically. A skill must be named
on the command line and pre-approved in publication-allowlist.json.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path


DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
DEFAULT_SOURCE_ROOT = DEFAULT_CODEX_HOME / "skills"


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Stage explicitly allowlisted local skills for public-repo review.",
    )
    parser.add_argument("--repo-root", default=str(repo_root))
    parser.add_argument("--source-root", default=str(DEFAULT_SOURCE_ROOT))
    parser.add_argument("--manifest")
    parser.add_argument("--allowlist")
    parser.add_argument(
        "--skill",
        action="append",
        required=True,
        help="Exact allowlisted skill name. May be passed multiple times.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def load_scanner(repo_root: Path):
    scanner_path = repo_root / "scripts" / "scan_public_release.py"
    spec = importlib.util.spec_from_file_location("scan_public_release", scanner_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load public-release scanner: {scanner_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def approved_entries(allowlist: dict) -> dict[str, dict]:
    entries: dict[str, dict] = {}
    for entry in allowlist.get("allowed_skills", []):
        if entry.get("approved") is True and entry.get("name"):
            entries[entry["name"]] = entry
    return entries


def validate_source(name: str, source_root: Path) -> Path:
    if Path(name).name != name or name in {".", ".."}:
        raise SystemExit(f"Unsafe publication skill name: {name}")
    source = source_root / name
    if source.is_symlink():
        raise SystemExit(
            f"Publication denied for symlinked skill {name}; copy it into a reviewed source "
            "directory and approve that exact source instead."
        )
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        raise SystemExit(f"Requested local skill is missing SKILL.md: {source}")
    try:
        source.resolve().relative_to(source_root.resolve())
    except ValueError as exc:
        raise SystemExit(f"Publication source escapes the selected source root: {source}") from exc
    return source


def require_pr_branch(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "branch", "--show-current"],
        check=True,
        text=True,
        capture_output=True,
    )
    branch = result.stdout.strip()
    if not branch or branch in {"main", "master"}:
        raise SystemExit("Publication candidates may only be staged on a non-main PR branch.")
    status = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--porcelain"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    if status:
        raise SystemExit("Publication requires a clean PR-branch worktree before staging.")
    return branch


def copy_skill(source: Path, dest: Path, dry_run: bool) -> None:
    print(f"stage_publication: {source} -> {dest}")
    if dry_run:
        return
    if dest.exists():
        raise SystemExit(f"Destination already exists in repo: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        dest,
        symlinks=False,
        ignore=shutil.ignore_patterns(
            ".git",
            ".env",
            ".env.*",
            "__pycache__",
            "*.pyc",
            ".pytest_cache",
            ".playwright-cli",
            ".folloze-managed.json",
            "artifacts",
            "output",
            "test-results",
        ),
    )


def manifest_entry(name: str, path: str) -> dict:
    return {
        "name": name,
        "path": path,
        "enabled": False,
        "requires_restart": True,
        "lifecycle": "candidate",
        "audience": "review-required",
    }


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    source_root = Path(args.source_root).expanduser().resolve()
    manifest_path = (
        Path(args.manifest).expanduser().resolve()
        if args.manifest
        else repo_root / "skills-manifest.json"
    )
    allowlist_path = (
        Path(args.allowlist).expanduser().resolve()
        if args.allowlist
        else repo_root / "publication-allowlist.json"
    )

    branch = require_pr_branch(repo_root)
    print(f"publication_branch: {branch}")

    manifest = load_json(manifest_path)
    allowlist = load_json(allowlist_path)
    approved = approved_entries(allowlist)
    requested = list(dict.fromkeys(args.skill))
    blocked = sorted(set(requested) - set(approved))
    if blocked:
        raise SystemExit(
            "Publication denied; skill is not explicitly approved in publication-allowlist.json: "
            + ", ".join(blocked)
        )

    existing_names = {skill["name"] for skill in manifest.get("skills", [])}
    duplicate = sorted(set(requested) & existing_names)
    if duplicate:
        raise SystemExit("Skill is already tracked by the manifest: " + ", ".join(duplicate))

    scanner = load_scanner(repo_root)
    plans: list[tuple[str, Path, str]] = []
    for name in requested:
        entry = approved[name]
        source = validate_source(name, source_root)
        findings = scanner.scan_paths([source], display_root=source_root)
        if findings:
            scanner.print_findings(findings)
            raise SystemExit(f"Public-release scan failed for {name}; nothing was copied.")

        rel_path = entry.get("destination", f"Skills/Published/{name}")
        if not rel_path.startswith("Skills/Published/") or ".." in Path(rel_path).parts:
            raise SystemExit(f"Unsafe publication destination for {name}: {rel_path}")
        if (repo_root / rel_path).exists():
            raise SystemExit(f"Destination already exists in repo: {repo_root / rel_path}")
        plans.append((name, source, rel_path))

    staged: list[str] = []
    for name, source, rel_path in plans:
        copy_skill(source, repo_root / rel_path, args.dry_run)
        manifest["skills"].append(manifest_entry(name, rel_path))
        staged.append(name)

    manifest["skills"] = sorted(manifest["skills"], key=lambda item: item["name"].lower())
    if not args.dry_run:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"publication_candidates_staged: {', '.join(staged)}")
    print("next_step: review the candidate, run validation and public-release scanning, then open a PR")
    print("automatic_commit_or_push: disabled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
