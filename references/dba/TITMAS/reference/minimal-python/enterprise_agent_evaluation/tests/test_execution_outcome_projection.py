from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from enterprise_agent_evaluation.execution_outcome_projection import (
    ExecutionOutcomeProjectionError,
    evaluate_execution_outcome_projection,
)


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/execution_outcome_cases.json"


class ExecutionOutcomeProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        assert fixture["synthetic_only"] is True
        cls.cases = fixture["cases"]

    def _evaluate(self, case):
        payload = {
            key: value for key, value in case.items() if key != "expected_projection_status"
        }
        return evaluate_execution_outcome_projection(payload)

    def test_all_declared_cases_are_valid_projections(self):
        for case in self.cases:
            with self.subTest(case_id=case["case_id"]):
                result = self._evaluate(case)
                self.assertEqual(case["expected_projection_status"], result["projection_status"])
                self.assertEqual([], result["issues"])
                self.assertFalse(result["eeoap_core_schema_modified"])
                self.assertFalse(result["canonical_evidence_created"])

    def test_execution_completion_does_not_imply_observed_effect(self):
        result = self._evaluate(self.cases[4])
        self.assertEqual("VERIFIED", result["layers"]["execution_completed"]["state"])
        self.assertEqual("NOT_OBSERVED", result["layers"]["observed_effect"]["state"])
        self.assertEqual("UNVERIFIED", result["layers"]["settled_outcome"]["state"])
        self.assertFalse(result["global_success_proven"])

    def test_report_success_can_be_contradicted_by_reality(self):
        result = self._evaluate(self.cases[1])
        self.assertEqual("VERIFIED", result["layers"]["reported_state"]["state"])
        self.assertEqual("CONTRADICTED", result["layers"]["observed_effect"]["state"])
        self.assertEqual("CONTRADICTED", result["layers"]["settled_outcome"]["state"])

    def test_transient_effect_is_not_a_settled_outcome(self):
        result = self._evaluate(self.cases[2])
        self.assertEqual("VERIFIED", result["layers"]["observed_effect"]["state"])
        self.assertEqual("CONTRADICTED", result["layers"]["settled_outcome"]["state"])

    def test_shared_dependency_is_not_independent_verification(self):
        result = self._evaluate(self.cases[3])
        self.assertEqual([], result["independent_reality_sources"])
        self.assertFalse(result["independence_sufficient_for_settlement"])
        self.assertEqual("UNVERIFIED", result["layers"]["settled_outcome"]["state"])

    def test_legacy_success_maps_to_one_pre_effect_layer_only(self):
        result = self._evaluate(self.cases[0])
        self.assertEqual("reported_state", result["legacy_success_mapping"])
        self.assertFalse(result["legacy_success_claims_global_outcome"])
        self.assertIsNone(result["numeric_score"])

        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        changed["legacy_success_maps_to"] = "settled_outcome"
        invalid = evaluate_execution_outcome_projection(changed)
        self.assertEqual("INVALID", invalid["projection_status"])
        self.assertIn("LEGACY_SUCCESS_MUST_MAP_TO_ONE_PRE_EFFECT_LAYER", invalid["issues"])

    def test_unscoped_aggregate_evidence_is_rejected(self):
        for scope in ("AGGREGATE", ""):
            with self.subTest(claim_scope=scope):
                changed = copy.deepcopy(self.cases[0])
                changed.pop("expected_projection_status")
                changed["evidence_sources"][0]["claim_scope"] = scope
                with self.assertRaises(ExecutionOutcomeProjectionError):
                    evaluate_execution_outcome_projection(changed)

    def test_scope_mismatch_is_invalid_not_silently_reused(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        changed["evidence_sources"][0]["claim_scope"] = "execution_completed"
        result = evaluate_execution_outcome_projection(changed)
        self.assertEqual("INVALID", result["projection_status"])
        self.assertIn("EVIDENCE_SCOPE_MISMATCH:A-command", result["issues"])

    def test_contradicted_completion_and_verified_report_remain_independent(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        changed["layers"]["execution_completed"]["state"] = "CONTRADICTED"
        result = evaluate_execution_outcome_projection(changed)
        self.assertEqual("VALID", result["projection_status"])
        self.assertEqual("CONTRADICTED", result["layers"]["execution_completed"]["state"])
        self.assertEqual("VERIFIED", result["layers"]["reported_state"]["state"])

    def test_observed_effect_without_an_observer_is_invalid(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        changed["layers"]["observed_effect"]["evidence_refs"] = []
        changed["evidence_sources"] = [
            item for item in changed["evidence_sources"] if item["evidence_ref"] != "A-observed"
        ]
        result = evaluate_execution_outcome_projection(changed)
        self.assertEqual("INVALID", result["projection_status"])
        self.assertIn("EVIDENCE_REQUIRED:observed_effect", result["issues"])

    def test_settled_success_requires_an_observation_window_and_delay(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        settled = next(
            item for item in changed["evidence_sources"] if item["evidence_ref"] == "A-settled"
        )
        settled["observation_window"] = None
        settled["settlement_delay_ms"] = 0
        result = evaluate_execution_outcome_projection(changed)
        self.assertEqual("INVALID", result["projection_status"])
        self.assertIn(
            "INDEPENDENT_SETTLEMENT_WITNESS_REQUIRED:settled_outcome",
            result["issues"],
        )

    def test_independent_claim_with_shared_dependency_is_rejected(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        observed = next(
            item for item in changed["evidence_sources"] if item["evidence_ref"] == "A-observed"
        )
        observed["shared_dependency"] = "synthetic-state-db-a"
        with self.assertRaises(ExecutionOutcomeProjectionError):
            evaluate_execution_outcome_projection(changed)

    def test_system_reporter_cannot_also_be_an_independent_observer(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        observed = next(
            item for item in changed["evidence_sources"] if item["evidence_ref"] == "A-observed"
        )
        observed["observer_id"] = "synthetic-service"
        result = evaluate_execution_outcome_projection(changed)
        self.assertEqual("INVALID", result["projection_status"])
        self.assertIn("SELF_REPORT_NOT_INDEPENDENT:A-observed", result["issues"])

    def test_one_independent_camera_can_observe_effect_and_settlement(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        settled = next(
            item for item in changed["evidence_sources"] if item["evidence_ref"] == "A-settled"
        )
        settled["observer_id"] = "synthetic-observer-a"
        result = evaluate_execution_outcome_projection(changed)
        self.assertEqual("VALID", result["projection_status"])
        self.assertEqual(["synthetic-observer-a"], result["independent_observers"])
        self.assertEqual(1, result["independent_observer_count"])
        self.assertEqual(["A-observed", "A-settled"], result["independent_reality_sources"])
        self.assertTrue(result["independence_sufficient_for_settlement"])

    def test_system_reporter_remains_non_independent_across_effect_layers(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        for source in changed["evidence_sources"]:
            if source["evidence_ref"] in {"A-observed", "A-settled"}:
                source["observer_id"] = "synthetic-service"
        result = evaluate_execution_outcome_projection(changed)
        self.assertEqual("INVALID", result["projection_status"])
        self.assertEqual([], result["independent_observers"])
        self.assertEqual(0, result["independent_observer_count"])
        self.assertFalse(result["independence_sufficient_for_settlement"])

    def test_shared_dependency_observer_is_not_independent_across_layers(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        for source in changed["evidence_sources"]:
            if source["evidence_ref"] in {"A-observed", "A-settled"}:
                source["observer_id"] = "synthetic-shared-camera"
                source["verifier_independence"] = "SHARED_DEPENDENCY"
                source["shared_dependency"] = "synthetic-state-db-a"
        result = evaluate_execution_outcome_projection(changed)
        self.assertEqual("INVALID", result["projection_status"])
        self.assertEqual([], result["independent_observers"])
        self.assertEqual(0, result["independent_observer_count"])
        self.assertFalse(result["independence_sufficient_for_settlement"])

    def test_evidence_reference_order_does_not_change_result_or_digest(self):
        original = self._evaluate(self.cases[3])
        changed = copy.deepcopy(self.cases[3])
        changed["layers"]["observed_effect"]["evidence_refs"].reverse()
        reordered = self._evaluate(changed)
        self.assertEqual(original, reordered)
        self.assertEqual(original["projection_digest"], reordered["projection_digest"])

    def test_unverified_effect_cannot_generate_settled_success(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        changed["layers"]["observed_effect"]["state"] = "UNVERIFIED"
        result = evaluate_execution_outcome_projection(changed)
        self.assertEqual("INVALID", result["projection_status"])
        self.assertIn("SETTLEMENT_REQUIRES_VERIFIED_OBSERVED_EFFECT", result["issues"])

    def test_legacy_success_must_match_the_mapped_layer_state(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_projection_status")
        changed["layers"]["reported_state"]["state"] = "CONTRADICTED"
        result = evaluate_execution_outcome_projection(changed)
        self.assertEqual("INVALID", result["projection_status"])
        self.assertIn("LEGACY_SUCCESS_MAPPING_NOT_VERIFIED", result["issues"])

    def test_unknown_layer_state_and_missing_source_id_fail_closed(self):
        unknown = copy.deepcopy(self.cases[0])
        unknown.pop("expected_projection_status")
        unknown["layers"]["reported_state"]["state"] = "SUCCESS"
        with self.assertRaises(ExecutionOutcomeProjectionError):
            evaluate_execution_outcome_projection(unknown)
        missing_source = copy.deepcopy(self.cases[0])
        missing_source.pop("expected_projection_status")
        missing_source["source_statement_id"] = ""
        with self.assertRaises(ExecutionOutcomeProjectionError):
            evaluate_execution_outcome_projection(missing_source)

    def test_projection_does_not_claim_causality_or_mutate_input(self):
        payload = copy.deepcopy(self.cases[0])
        payload.pop("expected_projection_status")
        original = copy.deepcopy(payload)
        result = evaluate_execution_outcome_projection(payload)
        reordered = copy.deepcopy(payload)
        reordered["evidence_sources"] = list(reversed(reordered["evidence_sources"]))
        reordered_result = evaluate_execution_outcome_projection(reordered)
        self.assertEqual(original, payload)
        self.assertEqual(result, reordered_result)
        self.assertFalse(result["causal_attribution_proven"])
        self.assertFalse(result["canonical_evidence_created"])

    def test_result_is_deterministic(self):
        first = self._evaluate(self.cases[0])
        second = self._evaluate(self.cases[0])
        self.assertEqual(first, second)
        self.assertEqual(64, len(first["projection_digest"]))


if __name__ == "__main__":
    unittest.main()
