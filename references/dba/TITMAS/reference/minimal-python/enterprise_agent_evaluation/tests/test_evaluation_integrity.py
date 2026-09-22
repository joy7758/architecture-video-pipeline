from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from enterprise_agent_evaluation.evaluation_integrity import (
    EvaluationIntegrityError,
    evaluate_integrity,
)


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/evaluation_integrity_cases.json"


class EvaluationIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        assert fixture["synthetic_only"] is True
        cls.cases = fixture["cases"]

    def _evaluate(self, case):
        payload = {
            key: value
            for key, value in case.items()
            if key not in {"expected_outcome", "expected_stop_state"}
        }
        return evaluate_integrity(payload)

    def test_required_cases_preserve_multi_dimensional_results(self):
        for case in self.cases:
            result = self._evaluate(case)
            self.assertEqual(case["expected_outcome"], result["derived_outcome"])
            self.assertEqual(case["dimensions"], result["dimensions"])

    def test_correct_answer_with_invalid_trace_is_not_collapsed_to_pass(self):
        result = self._evaluate(self.cases[1])
        self.assertEqual("PASS", result["dimensions"]["answer_correctness"])
        self.assertEqual("FAIL", result["dimensions"]["trace_validity"])
        self.assertEqual("ANSWER_CORRECT_TRACE_INVALID", result["derived_outcome"])

    def test_typed_stop_has_no_score_or_ranking_eligibility(self):
        result = self._evaluate(self.cases[4])
        self.assertEqual("STOPPED", result["evaluation_status"])
        self.assertEqual("EVIDENCE_INSUFFICIENT", result["stop_state"])
        self.assertIsNone(result["numeric_score"])
        self.assertFalse(result["ranking_eligible"])
        self.assertFalse(result["ordinary_execution_failure"])
        self.assertEqual(["artifact_receipt", "trace_binding"], result["missing_evidence"])

    def test_all_typed_stop_states_are_reachable_without_scoring(self):
        base = copy.deepcopy(self.cases[0])
        base.pop("expected_outcome")
        mutations = {
            "SEMANTICS_UNGROUNDED": {"semantic_grounding": False},
            "NON_COMPARABLE": {"comparable": False},
            "NON_IDENTIFIABLE": {"identifiable": False},
            "ABSTAIN": {"abstain_requested": True},
        }
        for expected, mutation in mutations.items():
            with self.subTest(stop_state=expected):
                case = copy.deepcopy(base)
                case.update(mutation)
                case["stop_reason"] = f"Synthetic stop: {expected}"
                result = evaluate_integrity(case)
                self.assertEqual(expected, result["stop_state"])
                self.assertEqual(f"Synthetic stop: {expected}", result["stop_reason"])
                self.assertIsNone(result["numeric_score"])
                self.assertFalse(result["ranking_eligible"])

    def test_unknown_dimension_fails_closed(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_outcome")
        changed["dimensions"]["fluency"] = "PASS"
        with self.assertRaises(EvaluationIntegrityError):
            evaluate_integrity(changed)

    def test_typed_stop_without_auditable_reason_fails_closed(self):
        changed = copy.deepcopy(self.cases[4])
        changed.pop("expected_outcome")
        changed.pop("expected_stop_state")
        changed["stop_reason"] = None
        with self.assertRaises(EvaluationIntegrityError):
            evaluate_integrity(changed)

    def test_unregistered_stop_state_field_fails_closed(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_outcome")
        changed["stop_state"] = "UNKNOWN_STOP"
        with self.assertRaises(EvaluationIntegrityError):
            evaluate_integrity(changed)

    def test_case_label_cannot_choose_the_derived_outcome(self):
        changed = copy.deepcopy(self.cases[1])
        changed.pop("expected_outcome")
        changed["case_id"] = "COMPLETE_FOR_DECLARED_SCOPE"
        result = evaluate_integrity(changed)
        self.assertEqual("ANSWER_CORRECT_TRACE_INVALID", result["derived_outcome"])

    def test_input_is_not_mutated_and_key_order_does_not_change_result(self):
        payload = copy.deepcopy(self.cases[2])
        payload.pop("expected_outcome")
        original = copy.deepcopy(payload)
        reordered = dict(reversed(list(payload.items())))
        first = evaluate_integrity(payload)
        second = evaluate_integrity(reordered)
        self.assertEqual(original, payload)
        self.assertEqual(first, second)

    def test_stop_metadata_without_a_stop_fails_closed(self):
        changed = copy.deepcopy(self.cases[0])
        changed.pop("expected_outcome")
        changed["stop_reason"] = "This reason has no typed stop."
        with self.assertRaises(EvaluationIntegrityError):
            evaluate_integrity(changed)

    def test_result_is_deterministic(self):
        first = self._evaluate(self.cases[3])
        second = self._evaluate(self.cases[3])
        self.assertEqual(first, second)
        self.assertEqual(64, len(first["assessment_digest"]))


if __name__ == "__main__":
    unittest.main()
