#!/usr/bin/env python3
"""Fail-closed checks for files considered for a public commit or push."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple


EXCLUDED_PARTS = {
    ".git",
    ".playwright-cli",
    ".pytest_cache",
    "__pycache__",
    "private",
}
EXCLUDED_SUFFIXES = {
    ".docx",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".pyc",
    ".webp",
    ".xlsx",
    ".zip",
}
FORBIDDEN_FILENAMES = {
    ".env",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
}
PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "generic secret assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|password)\s*[:=]\s*['\"](?!\$|\{|<|example|replace|your-)[^'\"\s]{12,}['\"]"
    ),
    "machine-specific home path": re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/"),
}
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
NON_PII_EMAIL_DOMAINS = {"acme.com", "example.com", "example.org", "example.net"}


class Finding(NamedTuple):
    path: Path
    line: int
    kind: str


def candidate_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file():
            files.append(path)
            continue
        if path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file())
    return sorted(set(files))


def should_skip(path: Path) -> bool:
    return bool(set(path.parts) & EXCLUDED_PARTS) or path.suffix.lower() in EXCLUDED_SUFFIXES


def scan_paths(paths: list[Path], display_root: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for path in candidate_files(paths):
        if should_skip(path):
            continue
        if path.name in FORBIDDEN_FILENAMES or path.name.startswith(".env."):
            findings.append(Finding(path, 0, "forbidden sensitive filename"))
            continue
        try:
            text = path.read_text(errors="strict")
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for kind, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append(Finding(path, line_number, kind))
            for email_match in EMAIL_PATTERN.finditer(line):
                if email_match.group(1).lower() not in NON_PII_EMAIL_DOMAINS:
                    findings.append(Finding(path, line_number, "hardcoded email address or PII"))
    return findings


def print_findings(findings: list[Finding], root: Path | None = None) -> None:
    print("Public-release scan failed:")
    for finding in findings:
        try:
            label = finding.path.relative_to(root) if root else finding.path
        except ValueError:
            label = finding.path
        location = f":{finding.line}" if finding.line else ""
        print(f"- {label}{location}: {finding.kind}")


def tracked_files(root: Path, staged: bool) -> list[Path]:
    cmd = ["git", "-C", str(root), "diff", "--cached", "--name-only", "--diff-filter=ACMR"] if staged else [
        "git",
        "-C",
        str(root),
        "ls-files",
    ]
    result = subprocess.run(cmd, check=True, text=True, capture_output=True)
    return [root / line for line in result.stdout.splitlines() if line]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--staged", action="store_true", help="Scan only staged additions and modifications.")
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    paths = [Path(value).expanduser().resolve() for value in args.paths]
    if not paths:
        paths = tracked_files(root, args.staged)
    findings = scan_paths(paths, display_root=root)
    if findings:
        print_findings(findings, root)
        return 1
    print(f"Public-release scan passed ({'staged' if args.staged else 'tracked'} files).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
