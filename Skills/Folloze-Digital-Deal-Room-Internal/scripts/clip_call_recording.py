#!/usr/bin/env python3
"""Create and technically verify a real time cut of a call recording.

This helper proves that media was re-encoded with a positive opening and/or
ending cut. It intentionally cannot mark content review or playback complete;
the agent must review the new opening and play both local and Folloze outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def fail(message: str) -> None:
    raise SystemExit(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe(path: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=index,codec_type,codec_name",
            "-of",
            "json",
            str(path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        fail(f"ffprobe could not read {path}: {completed.stderr.strip()}")
    data = json.loads(completed.stdout)
    try:
        data["duration_seconds"] = float(data["format"]["duration"])
    except (KeyError, TypeError, ValueError):
        fail(f"ffprobe did not return a readable duration for {path}")
    return data


def stream_types(probe_data: dict[str, Any]) -> set[str]:
    return {str(stream.get("codec_type")) for stream in probe_data.get("streams", [])}


def available_video_encoders() -> set[str]:
    completed = subprocess.run(
        ["ffmpeg", "-hide_banner", "-encoders"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        fail(f"Could not inspect ffmpeg encoders: {completed.stderr.strip()}")
    known = {"h264_videotoolbox", "h264_nvenc", "h264_qsv", "h264_vaapi", "libx264"}
    return {encoder for encoder in known if encoder in completed.stdout}


def hardware_encoder_candidates(encoders: set[str]) -> list[str]:
    preferred = (
        ["h264_videotoolbox", "h264_nvenc", "h264_qsv", "h264_vaapi"]
        if platform.system() == "Darwin"
        else ["h264_nvenc", "h264_qsv", "h264_vaapi", "h264_videotoolbox"]
    )
    return [encoder for encoder in preferred if encoder in encoders]


def select_video_encoders(mode: str, encoders: set[str]) -> list[str]:
    hardware = hardware_encoder_candidates(encoders)
    if mode == "software":
        if "libx264" not in encoders:
            fail("Software mode requires the libx264 encoder")
        return ["libx264"]
    if mode == "hardware":
        if not hardware:
            fail("Hardware mode requested, but ffmpeg exposes no supported H.264 hardware encoder")
        return [hardware[0]]
    candidates = hardware[:1]
    if "libx264" in encoders:
        candidates.append("libx264")
    if not candidates:
        fail("No supported H.264 encoder is available")
    return candidates


def video_encoder_args(encoder: str) -> list[str]:
    if encoder == "libx264":
        return ["-c:v", encoder, "-preset", "veryfast", "-crf", "22"]
    if encoder == "h264_videotoolbox":
        return ["-c:v", encoder, "-b:v", "5M", "-allow_sw", "1"]
    if encoder == "h264_nvenc":
        return ["-c:v", encoder, "-preset", "p4", "-cq", "22"]
    if encoder == "h264_qsv":
        return ["-c:v", encoder, "-preset", "veryfast", "-global_quality", "22"]
    if encoder == "h264_vaapi":
        return ["-c:v", encoder, "-qp", "22"]
    fail(f"Unsupported encoder selected: {encoder}")


def build_command(
    source: Path,
    output: Path,
    start: float,
    keep_duration: float,
    has_video: bool,
    video_encoder: str | None = None,
) -> list[str]:
    # Input seeking avoids decoding discarded opening chatter and is materially
    # faster on long calls while the subsequent re-encode preserves a clean cut.
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-i", str(source)]
    if keep_duration > 0:
        command.extend(["-t", f"{keep_duration:.3f}"])
    if has_video:
        if output.suffix.lower() != ".mp4":
            fail("Video sources must use an .mp4 output so the verified codecs and Folloze playback contract are deterministic")
        if not video_encoder:
            fail("A video encoder is required for video sources")
        command.extend(["-map", "0:v:0", "-map", "0:a:0"])
        command.extend(video_encoder_args(video_encoder))
        command.extend(["-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart"])
    else:
        if output.suffix.lower() != ".mp3":
            fail("Audio-only sources must use an .mp3 output so the verified codec and Folloze playback contract are deterministic")
        command.extend(["-map", "0:a:0", "-c:a", "libmp3lame", "-b:a", "192k"])
    command.append(str(output))
    return command


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--transcript", required=True, type=Path)
    parser.add_argument("--start", required=True, type=float, help="First retained second from the source")
    parser.add_argument("--end", type=float, help="Last retained source second; omit to keep through the end")
    parser.add_argument(
        "--transcript-source-mode",
        required=True,
        choices=("granola", "kaia_package", "local_file", "kaia_browser_export"),
    )
    parser.add_argument("--acquisition-mode", required=True, choices=("local_provided", "kaia_browser_export"))
    parser.add_argument(
        "--mode",
        choices=("auto", "hardware", "software"),
        default="auto",
        help="Video encoder policy. Auto probes hardware first and falls back to libx264 veryfast.",
    )
    parser.add_argument("--receipt", type=Path, help="Optional private JSON receipt destination")
    args = parser.parse_args()

    source = args.input.expanduser().resolve()
    output = args.output.expanduser().resolve()
    transcript = args.transcript.expanduser().resolve()
    if not source.is_file() or source.stat().st_size == 0:
        fail(f"Source recording is missing or empty: {source}")
    if not transcript.is_file() or transcript.stat().st_size == 0:
        fail(f"Transcript is missing or empty: {transcript}")
    if source == output:
        fail("Output must be a new file; never overwrite the source recording")
    if output.exists():
        fail(f"Output already exists: {output}")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        fail("ffmpeg and ffprobe are required")

    source_probe = probe(source)
    source_duration = source_probe["duration_seconds"]
    source_streams = stream_types(source_probe)
    if "audio" not in source_streams:
        fail("Source recording has no audio stream")
    if args.start < 0 or args.start >= source_duration:
        fail("--start must be at least 0 and before the source duration")
    keep_end = source_duration if args.end is None else args.end
    if keep_end <= args.start or keep_end > source_duration + 0.25:
        fail("--end must be after --start and no later than the source duration")

    removed_opening = args.start
    removed_ending = max(0.0, source_duration - keep_end)
    if removed_opening < 0.25 and removed_ending < 0.25:
        fail("No positive time cut was requested; do not claim the recording was clipped")

    keep_duration = keep_end - args.start
    output.parent.mkdir(parents=True, exist_ok=True)
    has_video = "video" in source_streams
    encoder_probe = available_video_encoders() if has_video else set()
    encoder_candidates = select_video_encoders(args.mode, encoder_probe) if has_video else ["libmp3lame"]
    encoder_attempts: list[dict[str, Any]] = []
    processing_started_at = datetime.now(timezone.utc)
    processing_started = time.monotonic()
    command: list[str] = []
    selected_encoder: str | None = None
    for index, encoder in enumerate(encoder_candidates):
        if output.exists():
            output.unlink()
        command = build_command(source, output, args.start, keep_duration, has_video, encoder if has_video else None)
        attempt_started = time.monotonic()
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        attempt_elapsed = round(time.monotonic() - attempt_started, 3)
        encoder_attempts.append(
            {
                "encoder": encoder,
                "exit_code": completed.returncode,
                "elapsed_seconds": attempt_elapsed,
            }
        )
        if completed.returncode == 0:
            selected_encoder = encoder
            break
        if args.mode != "auto" or index == len(encoder_candidates) - 1:
            fail(f"ffmpeg failed with {encoder}: {completed.stderr.strip()}")
    if not selected_encoder:
        fail("ffmpeg did not produce an output with any selected encoder")
    processing_elapsed = round(time.monotonic() - processing_started, 3)
    processing_completed_at = datetime.now(timezone.utc)

    output_probe = probe(output)
    output_streams = stream_types(output_probe)
    required_streams = {"audio", "video"} if "video" in source_streams else {"audio"}
    streams_verified = required_streams.issubset(output_streams)
    tolerance = 1.5
    duration_verified = abs(output_probe["duration_seconds"] - keep_duration) <= tolerance
    source_hash = sha256(source)
    output_hash = sha256(output)
    hashes_differ = source_hash != output_hash
    technical_passed = streams_verified and duration_verified and hashes_differ
    if not technical_passed:
        fail("Edited output failed stream, duration, or hash verification")

    receipt = {
        "transcript_source_mode": args.transcript_source_mode,
        "acquisition_mode": args.acquisition_mode,
        "transcript_file_readable": True,
        "transcript_identity_validated_by_helper": False,
        "source_path": str(source),
        "output_path": str(output),
        "transcript_path": str(transcript),
        "source_duration_seconds": round(source_duration, 3),
        "output_duration_seconds": round(output_probe["duration_seconds"], 3),
        "keep_start_seconds": round(args.start, 3),
        "keep_end_seconds": round(keep_end, 3),
        "removed_opening_seconds": round(removed_opening, 3),
        "removed_ending_seconds": round(removed_ending, 3),
        "clip_required": True,
        "recording_clipped": True,
        "opening_chatter_clipped": removed_opening >= 0.25,
        "source_sha256": source_hash,
        "output_sha256": output_hash,
        "source_and_output_hashes_differ": hashes_differ,
        "streams_verified": streams_verified,
        "duration_verified": duration_verified,
        "duration_tolerance_seconds": tolerance,
        "technical_edit_verification": "passed",
        "encoding_mode_requested": args.mode,
        "encoder_probe": {
            "available_supported_video_encoders": sorted(encoder_probe),
            "hardware_candidates": hardware_encoder_candidates(encoder_probe),
        },
        "encoder_selected": selected_encoder,
        "encoder_attempts": encoder_attempts,
        "hardware_fallback_used": bool(
            has_video and len(encoder_attempts) > 1 and selected_encoder == "libx264"
        ),
        "software_preset": "veryfast" if selected_encoder == "libx264" else None,
        "processing_started_at": processing_started_at.isoformat(),
        "processing_completed_at": processing_completed_at.isoformat(),
        "processing_elapsed_seconds": processing_elapsed,
        "processing_realtime_factor": round(processing_elapsed / output_probe["duration_seconds"], 4),
        "opening_review": "pending_manual_review",
        "opening_reviewed_by": None,
        "opening_reviewed_at": None,
        "new_opening_description": None,
        "local_playback": "pending_manual_review",
        "folloze_playback": "pending_upload_and_review",
        "ffmpeg_command": command,
    }
    if args.receipt:
        receipt_path = args.receipt.expanduser().resolve()
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
