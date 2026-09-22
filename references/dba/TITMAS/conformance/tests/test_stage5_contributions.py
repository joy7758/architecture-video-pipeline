#!/usr/bin/env python3
"""Deterministic Stage 5 contribution contract tests."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "stage5_contributions.py"
SPEC = importlib.util.spec_from_file_location("stage5_contributions_tested", MODULE_PATH)
assert SPEC and SPEC.loader
STAGE5 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = STAGE5
SPEC.loader.exec_module(STAGE5)


def disclosure() -> dict:
    return {
        "assisted": False,
        "provider": "NONE",
        "model": "NONE",
        "scope": "DETERMINISTIC_FIXTURE",
        "human_accountability": "REQUIRED",
    }


def proposal() -> dict:
    return {
        "proposal_id": "STAGE5-PROP-IDENTITY-HANDOFF",
        "title": "Bounded identity handoff failure code",
        "problem": "Developers need one interoperable failure code when identity handoff provenance is missing.",
        "developer_value": "A stable failure classification reduces framework-specific ambiguity without granting authority.",
        "scope": ["Define one failure code and its fail-closed behavior."],
        "non_goals": ["Do not create identity or permission."],
        "affected_objects": ["IDENTITY_OBJECT"],
        "proposed_change": {
            "summary": "Add a bounded MISSING_IDENTITY_PROVENANCE reason code to the interoperability profile.",
            "field_changes": ["Add reason_code enum value without changing identity ownership."],
        },
        "compatibility": "BACKWARD_COMPATIBLE",
        "positive_cases": ["Complete provenance continues through the handoff."],
        "negative_cases": ["Missing provenance fails closed with the new reason code."],
        "failure_behavior": "Return NOT_ASSESSED and require Human review; do not infer identity.",
        "source_refs": ["TITMAS/specifications/registry.yaml"],
        "ai_assistance_disclosure": disclosure(),
        "human_decisions_required": ["Human Maintainer decides candidate inclusion."],
    }


def adapter() -> dict:
    return {
        "adapter_id": "STAGE5-ADAPTER-SYNTHETIC-TRACE",
        "source_system": "SyntheticTrace",
        "source_version": "1.0",
        "source_license": "Synthetic fixture only",
        "source_semantics": ["trace_id identifies a synthetic observation, not Evidence Truth."],
        "titmas_bindings": [{
            "source_field": "trace_id",
            "titmas_object": "EXECUTION_OBJECT",
            "titmas_field": "observation_reference",
            "mapping_rule": "Map as an observation reference only.",
        }],
        "unsupported_fields": ["raw_payload"],
        "conflicts": ["Observation must not be elevated to Evidence Truth."],
        "positive_cases": ["A trace identifier maps to an observation reference."],
        "negative_cases": ["A trace identifier cannot authorize an execution."],
        "limitations": ["SYNTHETIC_MAPPING_ONLY"],
        "ai_assistance_disclosure": disclosure(),
    }


def vector() -> dict:
    return {
        "vector_id": "STAGE5-VECTOR-MISSING-PROVENANCE",
        "target_specification": "DRAFT-ID-CORE-INTEROP-001",
        "input": {"identity_provenance": None},
        "expected_result": {"status": "NOT_ASSESSED"},
        "expected_reason_code": "TITMAS-MISSING-IDENTITY-PROVENANCE",
        "positive_or_negative": "NEGATIVE",
        "failure_classification": "BOUNDARY",
        "source_refs": ["TITMAS/specifications/registry.yaml"],
        "limitations": ["SYNTHETIC_TEST_VECTOR_ONLY"],
    }


class Stage5ContributionTests(unittest.TestCase):
    def test_valid_proposal(self) -> None:
        result = STAGE5.validate_contribution("SPECIFICATION_PROPOSAL", proposal())
        self.assertEqual("CONFORMANCE_PASS", result["conformance_status"])
        self.assertTrue(result["human_disposition_required"])

    def test_valid_adapter(self) -> None:
        result = STAGE5.validate_contribution("ADAPTER_MAPPING", adapter())
        self.assertEqual("CONFORMANCE_PASS", result["conformance_status"])

    def test_valid_negative_vector(self) -> None:
        result = STAGE5.validate_contribution("TEST_VECTOR", vector())
        self.assertEqual("CONFORMANCE_PASS", result["conformance_status"])

    def test_negative_vector_without_failure_class_fails(self) -> None:
        payload = vector()
        payload["failure_classification"] = "NONE"
        result = STAGE5.validate_contribution("TEST_VECTOR", payload)
        self.assertEqual("CONFORMANCE_FAIL", result["conformance_status"])

    def test_extra_field_fails(self) -> None:
        payload = proposal()
        payload["standard_status"] = "STABLE"
        result = STAGE5.validate_contribution("SPECIFICATION_PROPOSAL", payload)
        self.assertEqual("CONFORMANCE_FAIL", result["conformance_status"])

    def test_private_path_fails(self) -> None:
        payload = adapter()
        payload["source_system"] = "/Users/example/private"
        result = STAGE5.validate_contribution("ADAPTER_MAPPING", payload)
        self.assertEqual("CONFORMANCE_FAIL", result["conformance_status"])

    def test_secret_marker_fails(self) -> None:
        payload = proposal()
        payload["problem"] = (
            "Authorization:" + " Bearer "
            + "synthetic-but-prohibited-token must never enter a contribution."
        )
        result = STAGE5.validate_contribution("SPECIFICATION_PROPOSAL", payload)
        self.assertEqual("CONFORMANCE_FAIL", result["conformance_status"])

    def test_unknown_type_fails(self) -> None:
        result = STAGE5.validate_contribution("UNKNOWN", proposal())
        self.assertEqual("CONFORMANCE_FAIL", result["conformance_status"])


if __name__ == "__main__":
    unittest.main()
