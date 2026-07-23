#!/usr/bin/env python3
"""Trim a prepared Kaia recording and apply the Folloze deal-room filename."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


class TrimError(RuntimeError):
    """Raised when a recording cannot be trimmed safely."""


@dataclass(frozen=True)
class EditedMedia:
    input_basename: str
    output_path: str
    account: str
    recording_date: str
    trim_start_seconds: float
    trim_end_seconds: float | None
    original_duration_seconds: float
    output_duration_seconds: float
    input_bytes: int
    output_bytes: int
    input_sha256: str
    output_sha256: str
    codec_mode: str
    manifest_path: str


def parse_timestamp(value: str) -> float:
    text = value.strip()
    if not text:
        raise TrimError("Timestamp cannot be empty")
    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        return float(text)

    parts = text.split(":")
    if len(parts) not in (2, 3):
        raise TrimError(f"Unsupported timestamp: {value!r}")
    try:
        numbers = [float(part) for part in parts]
    except ValueError as exc:
        raise TrimError(f"Unsupported timestamp: {value!r}") from exc

    if any(number < 0 for number in numbers):
        raise TrimError("Timestamp components cannot be negative")
    if len(numbers) == 2:
        minutes, seconds = numbers
        if seconds >= 60:
            raise TrimError("Seconds must be less than 60")
        return minutes * 60 + seconds

    hours, minutes, seconds = numbers
    if minutes >= 60 or seconds >= 60:
        raise TrimError("Minutes and seconds must be less than 60")
    return hours * 3600 + minutes * 60 + seconds


def validate_recording_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise TrimError("Recording date must use YYYY-MM-DD") from exc
    return parsed.isoformat()


def safe_account_name(value: str) -> str:
    normalized = re.sub(r"[\\/:*?\"<>|]+", " ", value).strip()
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = normalized.strip(". ")
    if not normalized:
        raise TrimError("Account name must contain filename-safe characters")
    return normalized


def output_filename(account: str, recording_date: str) -> str:
    return f"{safe_account_name(account)} - Folloze Demo - {validate_recording_date(recording_date)}.mp4"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ffprobe_duration(path: Path) -> float:
    executable = shutil.which("ffprobe")
    if not executable:
        raise TrimError("ffprobe is required but was not found")
    result = subprocess.run(
        [
            executable,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise TrimError(result.stderr.strip() or "ffprobe failed")
    try:
        return float(result.stdout.strip())
    except ValueError as exc:
        raise TrimError("ffprobe returned an invalid duration") from exc


def build_ffmpeg_command(
    input_path: Path,
    output_path: Path,
    start_seconds: float,
    end_seconds: float | None,
    copy_codecs: bool,
    overwrite: bool,
) -> list[str]:
    executable = shutil.which("ffmpeg")
    if not executable:
        raise TrimError("ffmpeg is required but was not found")

    command = [executable, "-hide_banner", "-loglevel", "warning"]
    command.append("-y" if overwrite else "-n")
    command.extend(["-ss", f"{start_seconds:.3f}", "-i", str(input_path)])
    if end_seconds is not None:
        command.extend(["-t", f"{end_seconds - start_seconds:.3f}"])

    if copy_codecs:
        command.extend(["-c", "copy"])
    else:
        command.extend(
            [
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "21",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
            ]
        )
    command.extend(["-movflags", "+faststart", str(output_path)])
    return command


def edit_recording(
    input_path: Path,
    account: str,
    recording_date: str,
    start: str,
    end: str | None = None,
    output_dir: Path | None = None,
    copy_codecs: bool = False,
    overwrite: bool = False,
    dry_run: bool = False,
) -> EditedMedia | dict:
    input_path = input_path.expanduser().resolve()
    if not input_path.is_file():
        raise TrimError(f"Input recording does not exist: {input_path}")
    if input_path.suffix.lower() != ".mp4":
        raise TrimError("The v1 editor expects a prepared MP4 recording")

    start_seconds = parse_timestamp(start)
    end_seconds = parse_timestamp(end) if end else None
    original_duration = ffprobe_duration(input_path)
    if start_seconds >= original_duration:
        raise TrimError("Trim start must be before the recording ends")
    if end_seconds is not None:
        if end_seconds <= start_seconds:
            raise TrimError("Trim end must be after trim start")
        if end_seconds > original_duration + 0.5:
            raise TrimError("Trim end cannot exceed the recording duration")

    destination_dir = (output_dir or input_path.parent).expanduser().resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / output_filename(account, recording_date)
    if destination.exists() and not overwrite:
        raise TrimError(f"Output already exists: {destination}")

    command = build_ffmpeg_command(
        input_path,
        destination,
        start_seconds,
        end_seconds,
        copy_codecs,
        overwrite,
    )
    if dry_run:
        return {
            "status": "dry_run",
            "output_path": str(destination),
            "command": command,
        }

    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise TrimError(result.stderr.strip() or "ffmpeg failed")
    if not destination.is_file() or destination.stat().st_size == 0:
        raise TrimError("ffmpeg did not create a valid output file")

    output_duration = ffprobe_duration(destination)
    expected_duration = (end_seconds or original_duration) - start_seconds
    if abs(output_duration - expected_duration) > 2.0:
        raise TrimError(
            f"Edited duration {output_duration:.3f}s differs from expected "
            f"{expected_duration:.3f}s"
        )

    manifest_path = destination.with_suffix(".json")
    edited = EditedMedia(
        input_basename=input_path.name,
        output_path=str(destination),
        account=safe_account_name(account),
        recording_date=validate_recording_date(recording_date),
        trim_start_seconds=start_seconds,
        trim_end_seconds=end_seconds,
        original_duration_seconds=original_duration,
        output_duration_seconds=output_duration,
        input_bytes=input_path.stat().st_size,
        output_bytes=destination.stat().st_size,
        input_sha256=sha256_file(input_path),
        output_sha256=sha256_file(destination),
        codec_mode="copy" if copy_codecs else "h264_aac_exact",
        manifest_path=str(manifest_path),
    )
    manifest_path.write_text(json.dumps(asdict(edited), indent=2) + "\n")
    return edited


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--account", required=True)
    parser.add_argument("--recording-date", required=True)
    parser.add_argument("--start", default="0")
    parser.add_argument("--end")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--copy-codecs", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = edit_recording(
            args.input_path,
            account=args.account,
            recording_date=args.recording_date,
            start=args.start,
            end=args.end,
            output_dir=args.output_dir,
            copy_codecs=args.copy_codecs,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
        )
    except TrimError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 1

    payload = asdict(result) if isinstance(result, EditedMedia) else result
    print(json.dumps({"status": "edited", **payload}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
