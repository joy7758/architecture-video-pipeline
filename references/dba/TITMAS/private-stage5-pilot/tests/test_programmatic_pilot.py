#!/usr/bin/env python3

import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
PILOT_ROOT = PROJECT_ROOT / "TITMAS" / "private-stage5-pilot"
sys.path.insert(0, str(PILOT_ROOT))

import programmatic_pilot


class ProgrammaticPilotTests(unittest.TestCase):
    def test_exact_five_scenarios_pass_with_expected_counts(self):
        with tempfile.TemporaryDirectory(prefix="titmas-stage5-p01-test-") as raw:
            output = Path(raw)
            report = programmatic_pilot.run_programmatic_pilot(
                PROJECT_ROOT, output
            )
            self.assertTrue(report["programmatic_pilot_pass"])
            self.assertEqual(report["scenario_count"], 5)
            self.assertEqual(report["scenario_pass_count"], 5)
            self.assertEqual(report["valid_submission_count"], 2)
            self.assertEqual(report["expected_rejection_count"], 3)
            self.assertEqual(report["core_access_count"], 0)
            self.assertEqual(report["real_model_call_count"], 0)
            self.assertEqual(report["automatic_retry_count"], 0)

    def test_registry_has_only_bounded_fields(self):
        allowed = {
            "submission_id",
            "type",
            "source",
            "contributor_kind",
            "conformance_status",
            "review_status",
            "human_disposition",
            "pilot_status",
            "hashes",
            "limitations",
        }
        with tempfile.TemporaryDirectory(prefix="titmas-stage5-p01-test-") as raw:
            output = Path(raw)
            programmatic_pilot.run_programmatic_pilot(PROJECT_ROOT, output)
            registry = json.loads(
                (output / "pilot-contribution-registry.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(len(registry["entries"]), 3)
            for entry in registry["entries"]:
                self.assertEqual(set(entry), allowed)
                self.assertNotIn(
                    entry["pilot_status"], {"ADOPTED", "STABLE", "CERTIFIED"}
                )

    def test_persisted_results_have_no_sandbox_key(self):
        with tempfile.TemporaryDirectory(prefix="titmas-stage5-p01-test-") as raw:
            output = Path(raw)
            programmatic_pilot.run_programmatic_pilot(PROJECT_ROOT, output)
            text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in sorted(output.glob("*.json"))
            )
            self.assertNotIn("Bearer ", text)
            self.assertNotIn("token_hash_prefix", text)
            self.assertNotIn('"token"', text)


if __name__ == "__main__":
    unittest.main()
