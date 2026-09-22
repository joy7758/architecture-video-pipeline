import copy
import importlib.util
import json
import unittest
from pathlib import Path

HARNESS_PATH = Path(__file__).resolve().parents[1] / "harness.py"
SPEC = importlib.util.spec_from_file_location("titmas_harness", HARNESS_PATH)
assert SPEC and SPEC.loader
HARNESS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HARNESS)


class HarnessTests(unittest.TestCase):
    def test_full_harness_passes(self):
        report = HARNESS.run_all(write_report=False)
        self.assertEqual("PASS", report["status"], report)

    def test_all_required_negative_cases_are_rejected(self):
        path = HARNESS.TITMAS_ROOT / "conformance" / "fixtures" / "negative" / "semantic-elevation-cases.json"
        cases = json.loads(path.read_text(encoding="utf-8"))["cases"]
        self.assertEqual(8, len(cases))
        for case in cases:
            self.assertIn(case["expected_error"], HARNESS.semantic_errors(case["payload"]))

    def test_community_status_schema_fails_closed(self):
        status_path = HARNESS.TITMAS_ROOT / "community" / "community-status.json"
        status = json.loads(status_path.read_text(encoding="utf-8"))
        schema = HARNESS.load_json(
            HARNESS.TITMAS_ROOT
            / "conformance"
            / "schemas"
            / "community-status.schema.json"
        )
        unsafe = copy.deepcopy(status)
        unsafe["community_established"] = True
        with self.assertRaises(HARNESS.ConformanceError):
            HARNESS.validate_schema(unsafe, schema)
        HARNESS.validate_schema(status, schema)

    def test_merge_admission_boundary_passes(self):
        details = HARNESS.check_merge_admission_boundary()
        self.assertEqual(15, details["stage_consistency_checks"])
        self.assertEqual(4, details["active_titmas_issue_template_count"])
        self.assertEqual(1, details["active_titmas_pull_request_template_count"])
        self.assertEqual(5, details["dormant_template_hashes_checked"])

    def test_merge_admission_negative_fixtures_fail_closed(self):
        fixture = HARNESS.load_json(
            HARNESS.TITMAS_ROOT
            / "conformance"
            / "fixtures"
            / "merge-admission"
            / "negative.json"
        )
        positive = HARNESS.load_json(
            HARNESS.TITMAS_ROOT
            / "conformance"
            / "fixtures"
            / "merge-admission"
            / "positive.json"
        )
        base = positive["cases"][0]["payload"]
        self.assertEqual(8, len(fixture["cases"]))
        for case in fixture["cases"]:
            errors = HARNESS.merge_admission_errors(
                HARNESS.deep_merge(base, case["patch"])
            )
            self.assertIn(case["expected_error"], errors, case["id"])

    def test_private_boundary_disables_public_operation_and_preserves_history(self):
        status = HARNESS.load_json(
            HARNESS.TITMAS_ROOT / "community" / "community-status.json"
        )
        surface = status["public_contribution_surface"]
        self.assertEqual(
            "PRIVATE_COMMERCIALIZATION_BOUNDARY", status["state"]
        )
        self.assertTrue(surface["templates_developed"])
        self.assertTrue(surface["templates_installed"])
        self.assertFalse(surface["active"])
        self.assertFalse(surface["authorized"])
        self.assertTrue(surface["activation_pr_merged"])
        self.assertFalse(surface["issue_submission_active"])
        self.assertFalse(surface["pull_request_submission_active"])
        self.assertFalse(surface["specification_proposal_active"])
        self.assertFalse(surface["adapter_integration_request_active"])
        self.assertTrue(status["activation_pr"]["merged"])
        self.assertTrue(status["public_contribution_activation"]["executed"])
        self.assertTrue(status["welcome_issue"]["created"])
        self.assertFalse(status["security"]["transport_active"])
        self.assertFalse(status["security"]["transport_verified"])
        self.assertFalse(status["public_launch"]["active"])
        self.assertFalse(status["public_launch"]["authorized"])
        self.assertTrue(status["historical_public_phase"]["limited_public_preview_was_active"])
        self.assertFalse(status["community_established"])

    def test_security_transport_reactivation_fails_closed(self):
        status = HARNESS.load_json(
            HARNESS.TITMAS_ROOT / "community" / "community-status.json"
        )
        schema = HARNESS.load_json(
            HARNESS.TITMAS_ROOT
            / "conformance"
            / "schemas"
            / "community-status.schema.json"
        )
        unsafe = copy.deepcopy(status)
        unsafe["security"]["transport_active"] = True
        with self.assertRaises(HARNESS.ConformanceError):
            HARNESS.validate_schema(unsafe, schema)

    def test_schema_depth_fails_closed(self):
        schema = {"type": "object", "properties": {}}
        instance = {}
        cursor_schema = schema
        cursor_instance = instance
        for index in range(HARNESS.MAX_SCHEMA_DEPTH + 2):
            cursor_schema["properties"] = {"nested": {"type": "object", "properties": {}}}
            cursor_schema = cursor_schema["properties"]["nested"]
            cursor_instance["nested"] = {}
            cursor_instance = cursor_instance["nested"]
        with self.assertRaises(HARNESS.ConformanceError):
            HARNESS.validate_schema(instance, schema)

    def test_json_path_escape_fails_closed(self):
        with self.assertRaises(HARNESS.ConformanceError):
            HARNESS.load_json(Path("/tmp/not-a-titmas-input.json"))

    def test_number_schema_rejects_boolean(self):
        with self.assertRaises(HARNESS.ConformanceError):
            HARNESS.validate_schema(True, {"type": "number"})

    def test_agent_native_surfaces_pass(self):
        details = HARNESS.check_agent_native_surfaces()
        self.assertGreaterEqual(details["agent_tasks_checked"], 1)
        self.assertEqual(1, details["canonical_machine_entries"])

    def test_canonical_contribution_example_has_no_legacy_pilot_identity(self):
        path = (
            HARNESS.TITMAS_ROOT
            / "agent-native"
            / "contributions"
            / "example-contribution-package.json"
        )
        value = json.loads(path.read_text(encoding="utf-8"))
        serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("PILOT-", serialized)

    def test_agent_native_adversarial_coverage(self):
        details = HARNESS.check_agent_native_adversarial()
        self.assertEqual(22, details["adversarial_cases_rejected"])
        self.assertEqual(22, details["adversarial_cases_executed"])

    def test_public_entry_consistency_passes_all_ten_checks(self):
        details = HARNESS.check_public_entry_consistency()
        self.assertEqual(10, details["public_entry_consistency_tests_passed"])
        self.assertEqual(
            [f"PE-{index:02d}" for index in range(1, 11)],
            details["checks"],
        )
        self.assertFalse(details["live_github_truth"])

    def test_integration_reviews_preserve_independent_lineages(self):
        details = HARNESS.check_internal_reviews()
        self.assertEqual(4, details["review_sessions_checked"])
        self.assertEqual(4, details["independent_lineages_checked"])


if __name__ == "__main__":
    unittest.main()
