#!/usr/bin/env python3
"""Build a deterministic, cache-free ZIP of this skill for teammate handoff."""

from __future__ import annotations

import argparse
import hashlib
import stat
import zipfile
from pathlib import Path


ARCHIVE_ROOT = "folloze-digital-deal-room-internal"
EXCLUDED_NAMES = {".DS_Store", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
ZIP_TIMESTAMP = (2026, 8, 4, 0, 0, 0)


def included_files(skill_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in skill_root.rglob("*"):
        relative = path.relative_to(skill_root)
        if any(part in EXCLUDED_NAMES for part in relative.parts):
            continue
        if path.is_file() and path.suffix not in EXCLUDED_SUFFIXES:
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(skill_root).as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(skill_root: Path, output: Path) -> dict[str, object]:
    skill_root = skill_root.resolve()
    output = output.resolve()
    if not (skill_root / "SKILL.md").is_file():
        raise SystemExit(f"Skill root has no SKILL.md: {skill_root}")
    if output.exists():
        raise SystemExit(f"Refusing to overwrite existing package: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)

    files = included_files(skill_root)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in files:
            relative = source.relative_to(skill_root).as_posix()
            info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{relative}", date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            permissions = 0o755 if source.stat().st_mode & stat.S_IXUSR else 0o644
            info.external_attr = (stat.S_IFREG | permissions) << 16
            archive.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    return {
        "package": str(output),
        "sha256": sha256(output),
        "file_count": len(files),
        "archive_root": ARCHIVE_ROOT,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Defaults to the skill directory containing this script.",
    )
    args = parser.parse_args()
    receipt = build(args.skill_root, args.output)
    print(f"package={receipt['package']}")
    print(f"sha256={receipt['sha256']}")
    print(f"file_count={receipt['file_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
