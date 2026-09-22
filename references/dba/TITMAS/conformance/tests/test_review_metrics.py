#!/usr/bin/env python3
"""Deterministic Review Catch measurement corrections."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


DBA_ROOT = Path(__file__).resolve().parents[3]
GROUNDING_ROOT = (
    DBA_ROOT
    / "TITMAS"
    / "conformance"
    / "grounding"
)
sys.path.insert(0, str(GROUNDING_ROOT))
SPEC = importlib.util.spec_from_file_location(
    "candidate_preflight", GROUNDING_ROOT / "candidate_preflight.py"
)
PREFLIGHT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(PREFLIGHT)


class ReviewMetricTests(unittest.TestCase):
    def test_reviewer_miss_is_not_no_opportunity(self):
        result = PREFLIGHT.compute_review_catch_metrics(
            [
                {
                    "review_stage_reached": True,
                    "preflight_caught": False,
                    "reviewer_opportunity": True,
                    "reviewer_caught": False,
                }
            ]
        )
        self.assertEqual(1, result["review_opportunity_count"])
        self.assertEqual(1, result["review_miss_count"])
        self.assertEqual(0.0, result["review_catch_rate"])

    def test_preflight_catch_is_not_reviewer_opportunity(self):
        result = PREFLIGHT.compute_review_catch_metrics(
            [
                {
                    "review_stage_reached": False,
                    "preflight_caught": True,
                    "reviewer_opportunity": False,
                    "reviewer_caught": False,
                }
            ]
        )
        self.assertEqual(1, result["preflight_catch_count"])
        self.assertEqual(0, result["review_opportunity_count"])

    def test_independent_reviewer_catch_is_counted(self):
        result = PREFLIGHT.compute_review_catch_metrics(
            [
                {
                    "review_stage_reached": True,
                    "preflight_caught": False,
                    "reviewer_opportunity": True,
                    "reviewer_caught": True,
                }
            ]
        )
        self.assertEqual(1, result["review_catch_count"])
        self.assertEqual(1.0, result["review_catch_rate"])

    def test_no_reviewer_stage_is_not_applicable(self):
        result = PREFLIGHT.compute_review_catch_metrics(
            [
                {
                    "review_stage_reached": False,
                    "preflight_caught": False,
                    "reviewer_opportunity": False,
                    "reviewer_caught": False,
                }
            ]
        )
        self.assertEqual("NOT_APPLICABLE", result["review_catch_rate"])
        self.assertEqual(
            "NOT_APPLICABLE_REVIEW_STAGE_NOT_REACHED",
            result["measurement_status"],
        )

    def test_instrumentation_defect_is_explicit(self):
        result = PREFLIGHT.compute_review_catch_metrics(
            [], instrumentation_complete=False
        )
        self.assertEqual(
            "NOT_ASSESSED_INSTRUMENTATION_DEFECT",
            result["review_catch_rate"],
        )

    def test_review_pass_count_does_not_replace_effectiveness(self):
        result = PREFLIGHT.compute_review_catch_metrics(
            [
                {
                    "review_stage_reached": True,
                    "review_pass": True,
                    "preflight_caught": False,
                    "reviewer_opportunity": True,
                    "reviewer_caught": False,
                }
            ]
        )
        self.assertEqual(0.0, result["review_catch_rate"])
        self.assertEqual(1, result["review_miss_count"])


if __name__ == "__main__":
    unittest.main()
