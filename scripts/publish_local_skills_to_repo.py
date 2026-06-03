#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path


DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
DEFAULT_SOURCE_ROOT = DEFAULT_CODEX_HOME / "skills"
DEFAULT_NAMESPACE_DIR = "Troy Folloze Created Skills"


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description=(
            "Copy local Codex skills not yet tracked in the shared repo into a "
            "repo namespace folder and update the manifest."
        ),
    )
    parser.add_argument(
        "--repo-root",
        default=str(repo_root),
        help="Path to the local Folloze-Skills clone.",
    )
    parser.add_argument(
        "--source-root",
        default=str(DEFAULT_SOURCE_ROOT),
        help="Path to the local Codex skills root. Defaults to $CODEX_HOME/skills or ~/.codex/skills.",
    )
    parser.add_argument(
        "--manifest",
        help="Path to the skills manifest. Defaults to <repo-root>/skills-manifest.json.",
    )
    parser.add_argument(
        "--namespace-dir",
        default=DEFAULT_NAMESPACE_DIR,
        help="Subdirectory under Skills/ where published skills should be copied.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Publish only the named local skill. May be passed multiple times.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without modifying the repo.",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def write_manifest(path: Path, manifest: dict, dry_run: bool) -> None:
    content = json.dumps(manifest, indent=2) + "\n"
    if dry_run:
        print(f"update_manifest: {path}")
        return
    path.write_text(content)


def is_repo_managed_skill(path: Path, repo_root: Path) -> bool:
    try:
        target = path.resolve()
    except FileNotFoundError:
        return False
    return repo_root == target or repo_root in target.parents


def discover_local_skills(source_root: Path, repo_root: Path) -> list[tuple[str, Path]]:
    if not source_root.exists():
        return []

    skills: list[tuple[str, Path]] = []
    for child in sorted(source_root.iterdir()):
        if child.name.startswith("."):
            continue
        skill_dir = child
        if child.is_symlink():
            if is_repo_managed_skill(child, repo_root):
                continue
            skill_dir = child.resolve()
        if not skill_dir.is_dir():
            continue
        if not (skill_dir / "SKILL.md").exists():
            continue
        skills.append((child.name, skill_dir))
    return skills


def selected_skills(
    local_skills: list[tuple[str, Path]],
    requested: set[str],
) -> list[tuple[str, Path]]:
    if not requested:
        return local_skills
    found = {name for name, _ in local_skills}
    missing = sorted(requested - found)
    if missing:
        raise SystemExit(f"Requested local skills not found: {', '.join(missing)}")
    return [(name, path) for name, path in local_skills if name in requested]


def copy_skill(source: Path, dest: Path, dry_run: bool) -> None:
    print(f"publish: {source} -> {dest}")
    if dry_run:
        return
    if dest.exists():
        raise SystemExit(f"Destination already exists in repo: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest, symlinks=False)


def manifest_entry(name: str, namespace_dir: str) -> dict:
    return {
        "name": name,
        "path": f"Skills/{namespace_dir}/{name}",
        "enabled": True,
        "requires_restart": True,
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

    manifest = load_manifest(manifest_path)
    existing_names = {skill["name"] for skill in manifest.get("skills", [])}
    local_skills = selected_skills(
        discover_local_skills(source_root, repo_root),
        set(args.skill),
    )

    published: list[str] = []
    for name, skill_path in local_skills:
        if name in existing_names:
            continue
        dest = repo_root / "Skills" / args.namespace_dir / name
        copy_skill(skill_path, dest, args.dry_run)
        manifest["skills"].append(manifest_entry(name, args.namespace_dir))
        existing_names.add(name)
        published.append(name)

    if published:
        manifest["skills"] = sorted(
            manifest["skills"],
            key=lambda item: item["name"].lower(),
        )
        write_manifest(manifest_path, manifest, args.dry_run)
        print(f"published_skills: {', '.join(published)}")
        print(f"published_namespace: Skills/{args.namespace_dir}")
    else:
        print("published_skills: none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
