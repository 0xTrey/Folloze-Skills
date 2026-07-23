#!/usr/bin/env python3
"""Safely select and extract one media file from an Outreach Kaia ZIP export."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import shutil
import stat
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile, ZipInfo


VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".m4v"}
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".wav", ".aac"}
DEFAULT_MAX_UNCOMPRESSED_BYTES = 8 * 1024 * 1024 * 1024


class ExportError(RuntimeError):
    """Raised when a Kaia export cannot be prepared safely."""


@dataclass(frozen=True)
class PreparedMedia:
    source_zip: str
    archive_member: str
    output_path: str
    media_kind: str
    mime_type: str
    bytes: int
    sha256: str
    ffprobe: dict | None
    manifest_path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path", type=Path, help="Downloaded Kaia ZIP export")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Private extraction directory; defaults to a new temporary directory",
    )
    parser.add_argument(
        "--prefer",
        choices=("auto", "video", "audio"),
        default="auto",
        help="Preferred media type; auto and video fall back to audio",
    )
    parser.add_argument(
        "--max-uncompressed-bytes",
        type=int,
        default=DEFAULT_MAX_UNCOMPRESSED_BYTES,
        help="Reject archives whose declared uncompressed size exceeds this limit",
    )
    return parser.parse_args()


def _is_symlink(info: ZipInfo) -> bool:
    mode = info.external_attr >> 16
    return stat.S_ISLNK(mode)


def _validate_member(info: ZipInfo) -> None:
    path = PurePosixPath(info.filename.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        raise ExportError(f"Unsafe archive member path: {info.filename!r}")
    if _is_symlink(info):
        raise ExportError(f"Symlink archive member is not allowed: {info.filename!r}")
    if info.flag_bits & 0x1:
        raise ExportError(f"Encrypted archive member is not allowed: {info.filename!r}")


def _media_kind(info: ZipInfo) -> str | None:
    suffix = Path(info.filename).suffix.lower()
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    if suffix in AUDIO_EXTENSIONS:
        return "audio"
    return None


def choose_media(infos: list[ZipInfo], prefer: str) -> tuple[ZipInfo, str]:
    candidates: list[tuple[ZipInfo, str]] = []
    for info in infos:
        if info.is_dir():
            continue
        kind = _media_kind(info)
        if kind:
            candidates.append((info, kind))

    if not candidates:
        raise ExportError("No supported video or audio file was found in the export")

    if prefer == "audio":
        order = ("audio", "video")
    else:
        order = ("video", "audio")

    for kind in order:
        matches = [candidate for candidate in candidates if candidate[1] == kind]
        if matches:
            return max(matches, key=lambda candidate: candidate[0].file_size)

    raise ExportError("No media candidate matched the requested preference")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe_media(path: Path) -> dict | None:
    executable = shutil.which("ffprobe")
    if not executable:
        return None
    command = [
        executable,
        "-v",
        "error",
        "-show_entries",
        "format=duration,format_name:stream=index,codec_type,codec_name,width,height",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return {"error": result.stderr.strip() or "ffprobe failed"}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "ffprobe returned invalid JSON"}


def _deduplicated_output_path(output_dir: Path, member: str) -> Path:
    filename = Path(PurePosixPath(member).name).name
    if not filename:
        raise ExportError(f"Archive member has no safe basename: {member!r}")
    candidate = output_dir / filename
    index = 2
    while candidate.exists():
        candidate = output_dir / f"{Path(filename).stem}-{index}{Path(filename).suffix}"
        index += 1
    return candidate


def prepare_export(
    zip_path: Path,
    output_dir: Path | None = None,
    prefer: str = "auto",
    max_uncompressed_bytes: int = DEFAULT_MAX_UNCOMPRESSED_BYTES,
) -> PreparedMedia:
    zip_path = zip_path.expanduser().resolve()
    if not zip_path.is_file():
        raise ExportError(f"ZIP export does not exist: {zip_path}")
    if max_uncompressed_bytes <= 0:
        raise ExportError("Maximum uncompressed size must be positive")

    try:
        with ZipFile(zip_path) as archive:
            infos = archive.infolist()
            for info in infos:
                _validate_member(info)
            total_size = sum(info.file_size for info in infos)
            if total_size > max_uncompressed_bytes:
                raise ExportError(
                    f"Archive declares {total_size} uncompressed bytes, above the "
                    f"{max_uncompressed_bytes} byte limit"
                )

            selected, kind = choose_media(infos, prefer)
            if output_dir is None:
                destination_dir = Path(tempfile.mkdtemp(prefix="folloze-kaia-"))
            else:
                destination_dir = output_dir.expanduser().resolve()
                destination_dir.mkdir(parents=True, exist_ok=True)

            destination = _deduplicated_output_path(destination_dir, selected.filename)
            with archive.open(selected) as source, destination.open("xb") as target:
                shutil.copyfileobj(source, target, length=1024 * 1024)
    except BadZipFile as exc:
        raise ExportError(f"Invalid ZIP export: {zip_path}") from exc

    mime_type = mimetypes.guess_type(destination.name)[0] or "application/octet-stream"
    digest = sha256_file(destination)
    manifest_path = destination_dir / "prepared-media.json"
    result = PreparedMedia(
        source_zip=zip_path.name,
        archive_member=selected.filename,
        output_path=str(destination),
        media_kind=kind,
        mime_type=mime_type,
        bytes=destination.stat().st_size,
        sha256=digest,
        ffprobe=probe_media(destination),
        manifest_path=str(manifest_path),
    )
    manifest_path.write_text(json.dumps(asdict(result), indent=2) + "\n")
    return result


def main() -> int:
    args = parse_args()
    try:
        result = prepare_export(
            args.zip_path,
            output_dir=args.output_dir,
            prefer=args.prefer,
            max_uncompressed_bytes=args.max_uncompressed_bytes,
        )
    except ExportError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 1

    print(json.dumps({"status": "prepared", **asdict(result)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
