#!/usr/bin/env python3
"""Stage 5 semantic checkpoint branch-gate tests."""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


DBA_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    DBA_ROOT
    / "TITMAS"
    / "agent-native"
    / "customer-cycle"
    / "semantic_checkpoint.py"
)
SPEC = importlib.util.spec_from_file_location("stage5_semantic_checkpoint", MODULE_PATH)
assert SPEC and SPEC.loader
CHECKPOINT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKPOINT
SPEC.loader.exec_module(CHECKPOINT)


def standard_contribution() -> dict:
    return {
        "submission_id": "stage5-submission-SYNTHETIC-01",
        "contribution_type": "TEST_VECTOR",
        "submission": {
            "vector_id": "STAGE5-VECTOR-SYNTHETIC",
            "target_specification": "DRAFT-ID-CORE-INTEROP-001"
        },
        "conformance_status": "CONFORMANCE_PASS",
        "reason_codes": ["TITMAS-STAGE5-CONTRIBUTION-CONFORMANT"],
        "agent_recommendation": "PROCEED_TO_HUMAN_REVIEW",
        "human_disposition_required": True,
        "limitations": ["SYNTHETIC_ONLY"],
        "non_claims": ["NOT_STANDARD_ADOPTION"],
    }


def standard_review() -> dict:
    return {
        "review_id": "STAGE5-REVIEW-SYNTHETIC",
        "submission_id": "stage5-submission-SYNTHETIC-01",
        "verdict": "PASS",
        "checks": {
            "grounding": True,
            "schema_correctness": True,
            "developer_value": True,
            "scope": True,
            "compatibility": True,
            "positive_cases": True,
            "negative_cases": True,
            "failure_behavior": True,
            "semantic_elevation": True,
            "authority_boundary": True,
            "commercial_overclaim": True,
        },
        "blocking_findings": [],
        "non_blocking_findings": ["Synthetic scope only."],
        "required_corrections": [],
        "human_disposition_required": True,
        "limitations": ["SYNTHETIC_ONLY"],
    }


class Stage5SemanticCheckpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "checkpoints"
        self.root.mkdir(mode=0o700)
        os.chmod(self.root, 0o700)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def persist(self, stage: str, value: dict, checkpoint_id: str) -> None:
        CHECKPOINT.persist_checkpoint(
            checkpoint_directory=self.root,
            checkpoint_id=checkpoint_id,
            cycle_id="STAGE5-SYNTHETIC",
            stage=stage,
            source_main="a" * 40,
            gateway_revision="b" * 40,
            attempt_id=f"attempt-{checkpoint_id}",
            provider="SYNTHETIC_PROVIDER",
            requested_model="synthetic-model",
            returned_model="synthetic-model",
            model_identity_status="MATCH",
            response_capture_state="FINALIZED_SUCCESS",
            response_envelope_ref=f"captures/{checkpoint_id}.json",
            response_body_sha256="c" * 64,
            structured_result=value,
        )

    def test_standard_contribution_requires_durable_plan(self) -> None:
        gate = CHECKPOINT.CheckpointStageGate(self.root, "STAGE5-SYNTHETIC")
        with self.assertRaises(CHECKPOINT.StageGateError):
            gate.authorize_dispatch("STANDARD_CONTRIBUTION")

    def test_standard_contribution_is_durable(self) -> None:
        self.persist("STANDARD_CONTRIBUTION", standard_contribution(), "contribution")
        record = CHECKPOINT.load_checkpoint(
            self.root / "contribution.checkpoint.json"
        )
        self.assertEqual("DURABLE", record["checkpoint_state"])

    def test_standard_review_requires_durable_contribution(self) -> None:
        gate = CHECKPOINT.CheckpointStageGate(self.root, "STAGE5-SYNTHETIC")
        with self.assertRaises(CHECKPOINT.StageGateError):
            gate.authorize_dispatch("STANDARD_REVIEW")
        self.persist("STANDARD_CONTRIBUTION", standard_contribution(), "contribution")
        self.assertTrue(gate.authorize_dispatch("STANDARD_REVIEW"))

    def test_standard_review_is_durable_before_human_disposition(self) -> None:
        self.persist("STANDARD_REVIEW", standard_review(), "review")
        record = CHECKPOINT.load_checkpoint(self.root / "review.checkpoint.json")
        self.assertTrue(record["downstream_dispatch_authorized"])
        self.assertTrue(record["structured_result"]["human_disposition_required"])


if __name__ == "__main__":
    unittest.main()
