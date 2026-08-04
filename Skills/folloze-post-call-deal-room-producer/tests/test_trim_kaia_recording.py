from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "trim_kaia_recording.py"
SPEC = importlib.util.spec_from_file_location("trim_kaia_recording", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load trim_kaia_recording.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class TrimKaiaRecordingTests(unittest.TestCase):
    def test_parses_supported_timestamps(self) -> None:
        self.assertEqual(MODULE.parse_timestamp("12.5"), 12.5)
        self.assertEqual(MODULE.parse_timestamp("01:30"), 90)
        self.assertEqual(MODULE.parse_timestamp("1:02:03.5"), 3723.5)

    def test_rejects_invalid_timestamp_components(self) -> None:
        with self.assertRaises(MODULE.TrimError):
            MODULE.parse_timestamp("01:75")
        with self.assertRaises(MODULE.TrimError):
            MODULE.parse_timestamp("1:60:00")

    def test_builds_required_filename(self) -> None:
        self.assertEqual(
            MODULE.output_filename("Tru Technologies", "2026-07-23"),
            "Tru Technologies - Folloze Demo - 2026-07-23.mp4",
        )

    def test_sanitizes_filename_characters(self) -> None:
        self.assertEqual(
            MODULE.output_filename("ACME / North: America", "2026-07-23"),
            "ACME North America - Folloze Demo - 2026-07-23.mp4",
        )

    def test_rejects_invalid_date(self) -> None:
        with self.assertRaises(MODULE.TrimError):
            MODULE.output_filename("ACME", "07-23-2026")


if __name__ == "__main__":
    unittest.main()
