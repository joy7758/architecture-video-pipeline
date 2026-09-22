import copy
import json
import os
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PACKAGE_PARENT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_PARENT))

from enterprise_agent_evaluation import (  # noqa: E402
    ContractValidationError,
    EvaluationError,
    load_human_judgments,
    load_profile,
    load_scenario,
    project_recommendation,
    run_route,
    serialize_result,
)
from enterprise_agent_evaluation.profile_loader import document_digest  # noqa: E402


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = PACKAGE_ROOT / "fixtures"
PROFILE_PATH = FIXTURES / "r1_evaluation_profile.json"
SCENARIO_PATH = FIXTURES / "r1_scenario_pack.json"
JUDGMENTS_PATH = FIXTURES / "r1_human_judgments.json"
CORE_MODULES = [
    PACKAGE_ROOT / "profile_loader.py",
    PACKAGE_ROOT / "scenario_loader.py",
    PACKAGE_ROOT / "evaluation_runner.py",
    PACKAGE_ROOT / "recommendation_projector.py",
]


class R1KernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_profile(PROFILE_PATH)
        cls.scenario = load_scenario(SCENARIO_PATH)
        cls.human = load_human_judgments(JUDGMENTS_PATH, cls.scenario)
        cls.run_a = run_route(cls.profile, cls.scenario, "mock_route_a")
        cls.run_b = run_route(cls.profile, cls.scenario, "mock_route_b")
        cls.result_a = project_recommendation(
            cls.profile, cls.scenario, cls.run_a, cls.human
        )
        cls.result_b = project_recommendation(
            cls.profile, cls.scenario, cls.run_b, cls.human
        )

    @staticmethod
    def _write_json(directory: str, name: str, payload: dict) -> Path:
        path = Path(directory) / name
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_r1_01_valid_eep_loads(self):
        self.assertEqual("titmas:r1:synthetic-customer-support", self.profile["profile_id"])
        self.assertTrue(self.profile["schema_ref"].endswith("02_ENTERPRISE_EVALUATION_PROFILE.schema.json"))

    def test_r1_02_invalid_eep_fails_closed(self):
        bad = copy.deepcopy(self.profile["document"])
        del bad["evaluation_weights"]
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_json(directory, "bad-profile.json", bad)
            with self.assertRaises(ContractValidationError):
                load_profile(path)

    def test_r1_03_valid_esp_loads(self):
        self.assertEqual(6, len(self.scenario["document"]["tasks"]))
        self.assertTrue(self.scenario["schema_ref"].endswith("03_ENTERPRISE_SCENARIO_PACK.schema.json"))

    def test_r1_04_invalid_esp_fails_closed(self):
        bad = copy.deepcopy(self.scenario["document"])
        bad["tasks"] = bad["tasks"][:-1]
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_json(directory, "bad-scenario.json", bad)
            with self.assertRaises(ContractValidationError):
                load_scenario(path)

    def test_r1_05_profile_version_changes_result_binding(self):
        changed = copy.deepcopy(self.profile["document"])
        changed["profile_version"] = "0.1.1"
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_json(directory, "profile.json", changed)
            profile = load_profile(path)
            run = run_route(profile, self.scenario, "mock_route_a")
            result = project_recommendation(profile, self.scenario, run, self.human)
        self.assertNotEqual(self.result_a["evaluation_id"], result["evaluation_id"])
        self.assertEqual("0.1.1", result["profile_version"])

    def test_r1_06_scenario_version_changes_result_binding(self):
        changed_scenario = copy.deepcopy(self.scenario["document"])
        changed_scenario["scenario_pack_version"] = "0.1.1"
        with tempfile.TemporaryDirectory() as directory:
            scenario_path = self._write_json(directory, "scenario.json", changed_scenario)
            scenario = load_scenario(scenario_path)
            changed_profile = copy.deepcopy(self.profile["document"])
            changed_profile["validity_conditions"]["scenario_pack_digest"] = scenario["scenario_pack_digest"]
            profile_path = self._write_json(directory, "profile.json", changed_profile)
            profile = load_profile(profile_path)
            run = run_route(profile, scenario, "mock_route_a")
            result = project_recommendation(profile, scenario, run, self.human)
        self.assertNotEqual(self.result_a["evaluation_id"], result["evaluation_id"])
        self.assertEqual("0.1.1", result["scenario_pack_version"])

    def test_r1_07_unobserved_fields_are_not_assessed(self):
        self.assertIn("real_customer_outcomes", self.result_a["not_assessed_fields"])
        self.assertNotIn(0, self.result_a["not_assessed_fields"])
        self.assertNotIn("PASS", self.result_a["not_assessed_fields"])

    def test_r1_08_observed_fact_is_separate_from_human_judgment(self):
        observed = self.result_a["case_results"][0]["observed_fact"]
        judgment = self.result_a["case_results"][0]["human_judgment"]
        self.assertNotIn("business_completed", observed)
        self.assertNotIn("tool_calls", judgment)

    def test_r1_09_provisional_assessment_is_not_final_authority(self):
        for assessment in self.result_a["provisional_assessments"]:
            self.assertEqual("NONE", assessment["final_authority_effect"])
            self.assertTrue(assessment["human_judgment_required"])

    def test_r1_10_recommendation_index_uses_eep_weights(self):
        weights = self.profile["document"]["evaluation_weights"]
        expected = round(
            (
                self.result_a["business_completion_score"] * weights["business_completion"]
                + self.result_a["stability_score"] * weights["continuous_stability"]
                + self.result_a["risk_control_score"] * weights["permission_and_risk_control"]
                + self.result_a["enterprise_value_score"] * weights["enterprise_net_value"]
                + self.result_a["deployment_migration_score"] * weights["deployment_and_migration_difficulty"]
            )
            / 100.0,
            2,
        )
        self.assertEqual(expected, self.result_a["recommendation_index"])

    def test_r1_11_eep_weights_total_one_hundred(self):
        self.assertEqual(100, sum(self.profile["document"]["evaluation_weights"].values()))

    def test_r1_12_red_line_is_not_offset_by_high_score(self):
        self.assertGreater(self.result_b["recommendation_index"], 80)
        self.assertEqual("FAIL", self.result_b["red_line_result"])
        self.assertEqual("L0", self.result_b["deployment_level"])

    def test_r1_13_two_mock_routes_produce_different_results(self):
        self.assertNotEqual(serialize_result(self.result_a), serialize_result(self.result_b))
        self.assertNotEqual(self.result_a["recommendation_index"], self.result_b["recommendation_index"])

    def test_r1_14_route_b_red_line_cannot_receive_l3(self):
        self.assertTrue(self.result_b["red_line_events"])
        self.assertNotEqual("L3", self.result_b["deployment_level"])

    def test_r1_15_evidence_level_is_capped_at_e1(self):
        self.assertEqual({"E1"}, {self.result_a["evidence_level"], self.result_b["evidence_level"]})

    def test_r1_16_evidence_reuses_existing_titmas_reference_binding(self):
        for reference in self.result_a["evidence_refs"]:
            self.assertEqual(
                "TITMAS/reference/minimal-python/titmas_reference.py",
                reference["source_contract_ref"],
            )
            self.assertEqual(
                "REFERENCE_ONLY_NOT_DBOS_ADMITTED",
                reference["evidence_binding"]["admission_status"],
            )
            self.assertFalse(reference["canonical_evidence_object_created"])

    def test_r1_17_repeated_input_is_byte_identical(self):
        second_run = run_route(self.profile, self.scenario, "mock_route_a")
        second = project_recommendation(self.profile, self.scenario, second_run, self.human)
        self.assertEqual(serialize_result(self.result_a), serialize_result(second))

    def test_r1_18_runtime_does_not_open_network_socket(self):
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            run = run_route(self.profile, self.scenario, "mock_route_a")
            project_recommendation(self.profile, self.scenario, run, self.human)

    def test_r1_19_runtime_does_not_read_or_emit_secret_canary(self):
        canary = "R1_SECRET_CANARY_MUST_NOT_APPEAR"
        with mock.patch.dict(os.environ, {"R1_SECRET_CANARY": canary}, clear=False):
            serialized = serialize_result(self.result_a).decode("utf-8")
        self.assertNotIn(canary, serialized)
        source = "\n".join(path.read_text(encoding="utf-8") for path in CORE_MODULES)
        self.assertNotIn("os.environ", source)
        self.assertNotIn("getenv(", source)

    def test_r1_20_runtime_creates_no_database(self):
        source = "\n".join(path.read_text(encoding="utf-8") for path in CORE_MODULES)
        for marker in ("sqlite3", "sqlalchemy", "psycopg", "CREATE TABLE"):
            self.assertNotIn(marker, source)

    def test_r1_21_result_creates_no_authority_chain(self):
        serialized = serialize_result(self.result_a).decode("utf-8")
        for marker in ("permission_grant", "authorization_decision", "execution_permission"):
            self.assertNotIn(marker, serialized)
        self.assertEqual("RECOMMENDATION_ONLY", self.result_a["decision_effect"])

    def test_r1_22_recommendation_card_uses_same_fact_object(self):
        card = self.result_a["recommendation_card"]
        self.assertEqual(self.result_a["evaluation_id"], card["source_evaluation_id"])
        self.assertEqual(self.result_a["fact_digest"], card["source_fact_digest"])

    def test_r1_23_deleting_projection_does_not_change_fact_digest(self):
        result = copy.deepcopy(self.result_a)
        fact_digest = result["fact_digest"]
        del result["recommendation_card"]
        self.assertEqual(fact_digest, result["fact_digest"])

    def test_r1_24_six_cases_and_two_routes_are_exact(self):
        self.assertEqual(6, len(self.result_a["case_results"]))
        self.assertEqual({"mock_route_a", "mock_route_b"}, {self.result_a["tested_route_id"], self.result_b["tested_route_id"]})

    def test_r1_25_scenario_digest_mismatch_fails_closed(self):
        changed = copy.deepcopy(self.profile)
        changed["document"]["validity_conditions"]["scenario_pack_digest"] = "0" * 64
        with self.assertRaises(EvaluationError):
            run_route(changed, self.scenario, "mock_route_a")

    def test_r1_26_manifest_tamper_fails_closed(self):
        changed = copy.deepcopy(self.scenario["document"])
        changed["tasks"][0]["instruction"] = "tampered"
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_json(directory, "scenario.json", changed)
            with self.assertRaises(ContractValidationError):
                load_scenario(path)

    def test_r1_27_human_fixture_is_explicitly_non_authoritative(self):
        self.assertEqual("SYNTHETIC_TEST_ONLY", self.human["fixture_scope"])
        self.assertEqual("NONE", self.human["human_authority_effect"])

    def test_r1_28_missing_human_judgment_fails_closed(self):
        changed = copy.deepcopy(self.human)
        changed["judgments"] = changed["judgments"][1:]
        with self.assertRaises(EvaluationError):
            project_recommendation(self.profile, self.scenario, self.run_a, changed)

    def test_r1_29_esp_red_lines_must_be_covered_by_eep(self):
        changed = copy.deepcopy(self.profile)
        changed["document"]["red_line_rules"] = [
            item
            for item in changed["document"]["red_line_rules"]
            if item["rule_id"] != "unauthorized_refund"
        ]
        with self.assertRaises(EvaluationError):
            run_route(changed, self.scenario, "mock_route_b")

    def test_r1_30_output_contains_no_real_vendor_brand(self):
        serialized = serialize_result(self.result_a).decode("utf-8").lower()
        for brand in ("openai", "anthropic", "alibaba", "tencent", "baidu", "volcengine"):
            self.assertNotIn(brand, serialized)


if __name__ == "__main__":
    unittest.main()
