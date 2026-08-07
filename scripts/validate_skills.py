#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


FORBIDDEN_TEXT_PATTERNS = (
    "/Users/",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def validate_manifest(root: Path, manifest: dict, errors: list[str]) -> list[dict]:
    seen: set[str] = set()
    skills = manifest.get("skills", [])
    if not isinstance(skills, list) or not skills:
        errors.append("skills-manifest.json must contain a non-empty 'skills' list.")
        return []

    if manifest.get("repository_role") != "internal-development-and-learning":
        errors.append("Manifest must declare repository_role=internal-development-and-learning.")
    if not manifest.get("recommended_customer_distribution"):
        errors.append("Manifest must name the recommended customer distribution.")
    if manifest.get("publication_policy") != "publication-allowlist.json":
        errors.append("Manifest must point to publication-allowlist.json.")

    seen_paths: set[str] = set()
    for skill in skills:
        name = skill.get("name")
        rel_path = skill.get("path")
        if not name or not rel_path:
            errors.append(f"Invalid manifest entry: {skill!r}")
            continue
        if name in seen:
            errors.append(f"Duplicate manifest skill name: {name}")
            continue
        seen.add(name)
        if "/" in name or "\\" in name or name in {".", ".."}:
            errors.append(f"Unsafe manifest skill name: {name}")
        rel = Path(rel_path)
        if rel.is_absolute() or ".." in rel.parts or not rel.parts or rel.parts[0] != "Skills":
            errors.append(f"Unsafe manifest path for {name}: {rel_path}")
            continue
        if rel_path in seen_paths:
            errors.append(f"Duplicate manifest path: {rel_path}")
        seen_paths.add(rel_path)
        if skill.get("lifecycle") == "deprecated" and skill.get("enabled", True):
            errors.append(f"Deprecated skill must not be enabled: {name}")

        skill_dir = root / rel_path
        if not skill_dir.exists():
            errors.append(f"Manifest path does not exist for {name}: {skill_dir}")
            continue
        if not (skill_dir / "SKILL.md").exists():
            errors.append(f"Missing SKILL.md for {name}: {skill_dir / 'SKILL.md'}")

    return skills


def validate_publication_allowlist(root: Path, errors: list[str]) -> None:
    path = root / "publication-allowlist.json"
    if not path.exists():
        errors.append("Missing publication-allowlist.json.")
        return
    try:
        policy = load_manifest(path)
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid publication allowlist JSON: {exc}")
        return
    if policy.get("policy") != "fail-closed":
        errors.append("Publication allowlist must use fail-closed policy.")
    entries = policy.get("allowed_skills")
    if not isinstance(entries, list):
        errors.append("Publication allowlist must contain an allowed_skills list.")
        return
    seen: set[str] = set()
    for entry in entries:
        name = entry.get("name")
        destination = entry.get("destination", f"Skills/Published/{name}")
        if not name or entry.get("approved") is not True:
            errors.append(f"Publication entry must be named and explicitly approved: {entry!r}")
            continue
        if name in seen:
            errors.append(f"Duplicate publication allowlist name: {name}")
        seen.add(name)
        if not destination.startswith("Skills/Published/") or ".." in Path(destination).parts:
            errors.append(f"Unsafe publication destination for {name}: {destination}")


def scan_for_forbidden_paths(root: Path, errors: list[str]) -> None:
    for path in root.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue
        if path == Path(__file__).resolve():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".xlsx"}:
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            if pattern in text:
                errors.append(f"Forbidden machine-specific path '{pattern}' found in {path}")


def compile_python(root: Path, errors: list[str]) -> None:
    python_files = sorted(root.rglob("*.py"))
    if not python_files:
        return
    cmd = [sys.executable, "-m", "py_compile", *[str(path) for path in python_files]]
    with tempfile.TemporaryDirectory(prefix="folloze-skills-pyc-") as pycache:
        env = os.environ.copy()
        env["PYTHONPYCACHEPREFIX"] = pycache
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        errors.append(result.stderr.strip() or "Python compilation failed.")


def main() -> int:
    root = repo_root()
    manifest_path = root / "skills-manifest.json"
    errors: list[str] = []

    if not manifest_path.exists():
        errors.append(f"Missing manifest: {manifest_path}")
    else:
        manifest = load_manifest(manifest_path)
        validate_manifest(root, manifest, errors)

    validate_publication_allowlist(root, errors)

    scan_for_forbidden_paths(root, errors)
    compile_python(root, errors)

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
