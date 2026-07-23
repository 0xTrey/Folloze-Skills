from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "prepare_kaia_export.py"
SPEC = importlib.util.spec_from_file_location("prepare_kaia_export", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load prepare_kaia_export.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class PrepareKaiaExportTests(unittest.TestCase):
    def test_prefers_largest_video_and_ignores_transcript(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "export.zip"
            with ZipFile(archive_path, "w") as archive:
                archive.writestr("transcript.txt", "private transcript")
                archive.writestr("audio/call.mp3", b"a" * 100)
                archive.writestr("video/preview.mp4", b"v" * 200)
                archive.writestr("video/full-call.mp4", b"v" * 400)

            result = MODULE.prepare_export(archive_path, output_dir=root / "prepared")

            self.assertEqual(result.media_kind, "video")
            self.assertEqual(result.archive_member, "video/full-call.mp4")
            self.assertEqual(Path(result.output_path).name, "full-call.mp4")
            self.assertFalse((root / "prepared" / "transcript.txt").exists())

    def test_audio_only_export_uses_audio(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "export.zip"
            with ZipFile(archive_path, "w") as archive:
                archive.writestr("recording/call.m4a", b"a" * 64)

            result = MODULE.prepare_export(archive_path, output_dir=root / "prepared")

            self.assertEqual(result.media_kind, "audio")
            self.assertEqual(result.bytes, 64)
            self.assertEqual(len(result.sha256), 64)

    def test_rejects_path_traversal_before_extraction(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "export.zip"
            with ZipFile(archive_path, "w") as archive:
                archive.writestr("../escape.mp4", b"unsafe")

            with self.assertRaises(MODULE.ExportError):
                MODULE.prepare_export(archive_path, output_dir=root / "prepared")

            self.assertFalse((root / "escape.mp4").exists())

    def test_rejects_oversized_declared_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "export.zip"
            with ZipFile(archive_path, "w") as archive:
                archive.writestr("call.mp4", b"v" * 20)

            with self.assertRaises(MODULE.ExportError):
                MODULE.prepare_export(
                    archive_path,
                    output_dir=root / "prepared",
                    max_uncompressed_bytes=10,
                )

    def test_cli_deletes_only_input_zip_after_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "export.zip"
            unrelated_zip = root / "keep.zip"
            with ZipFile(archive_path, "w") as archive:
                archive.writestr("call.mp4", b"video bytes")
            with ZipFile(unrelated_zip, "w") as archive:
                archive.writestr("other.txt", "keep me")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    str(archive_path),
                    "--output-dir",
                    str(root / "prepared"),
                    "--delete-zip-after-success",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(archive_path.exists())
            self.assertTrue(unrelated_zip.exists())


if __name__ == "__main__":
    unittest.main()
