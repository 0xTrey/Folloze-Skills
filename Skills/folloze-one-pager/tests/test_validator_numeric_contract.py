#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import validate_one_pager as validator  # noqa: E402


class NumericClaimPatternTests(unittest.TestCase):
    def test_ordinary_number_word_prose_is_not_numeric_proof(self) -> None:
        for text in (
            "one workflow",
            "one connected workflow",
            "two coordinated motions",
        ):
            with self.subTest(text=text):
                self.assertIsNone(validator.NUMERIC_CLAIM_PATTERN.search(text))

    def test_metric_shaped_claims_still_require_proof(self) -> None:
        for text in (
            "50% more engagement",
            "$1 million in pipeline",
            "3x conversion",
            "twenty-fold improvement",
            "two accounts",
            "twenty accounts",
            "one percent improvement",
            "from nine to four steps",
            "one in three buyers",
            "double engagement",
        ):
            with self.subTest(text=text):
                self.assertIsNotNone(validator.NUMERIC_CLAIM_PATTERN.search(text))


class StructuralNumberTests(unittest.TestCase):
    def test_path_index_keeps_exemption_under_traced_claim_card(self) -> None:
        parser = validator.PageParser()
        parser.feed(
            '<article data-placement="path_build" data-pillar="Build" '
            'data-claim-id="claim-build" data-source-ids="src-brand">'
            '<span class="path-index" data-non-claim-number>01</span>'
            '<p>one workflow</p>'
            "</article>"
        )

        nodes = {node.text: node for node in parser.visible_nodes}
        self.assertTrue(nodes["01"].non_claim_number)
        self.assertEqual(nodes["01"].claim_id, "claim-build")
        self.assertEqual(nodes["01"].source_ids, ("src-brand",))
        self.assertFalse(nodes["one workflow"].non_claim_number)

    def test_marker_remains_restricted_to_trusted_structural_elements(self) -> None:
        raw_html = (
            '<span class="buyer-copy" data-non-claim-number>'
            "50% more engagement"
            "</span>"
        )
        parser = validator.PageParser()
        parser.feed(raw_html)

        issues = validator.validate_microsite_structure(
            raw_html,
            parser,
            brief=None,
            mode="final",
        )

        self.assertIn("PROOF009", {item.rule_id for item in issues})

    def test_path_index_marker_allows_only_template_sequence_values(self) -> None:
        raw_html = '<span class="path-index" data-non-claim-number>04</span>'
        parser = validator.PageParser()
        parser.feed(raw_html)

        issues = validator.validate_microsite_structure(
            raw_html,
            parser,
            brief=None,
            mode="final",
        )

        self.assertIn("PROOF010", {item.rule_id for item in issues})


if __name__ == "__main__":
    unittest.main()
