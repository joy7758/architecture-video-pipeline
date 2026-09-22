import importlib.util
import json
import os
import stat
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


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECKPOINT = _load("titmas_semantic_checkpoint", MODULE_PATH)


class SanitizedSemanticCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.checkpoint_directory = Path(self.temporary.name) / "checkpoints"
        self.checkpoint_directory.mkdir(mode=0o700)
        self.cycle_id = "SYNTHETIC-CYCLE-001"
        self.sequence = 0

    def tearDown(self):
        self.temporary.cleanup()

    @staticmethod
    def plan():
        return {
            "problem_understood": "A bounded synthetic customer contract.",
            "contract_version": "0.1.0",
            "relevance_preassessment": "RELEVANT",
            "selected_operation": "EVALUATE",
            "request_body": {"synthetic_request_id": "SYNTHETIC-001"},
            "expected_public_result_shape": {"result_status": "string"},
            "decision_criteria": ["Contract result is customer visible."],
            "limitations": ["SYNTHETIC_ONLY"],
            "non_claims": ["NOT_PRODUCTION_READY"],
        }

    @staticmethod
    def gateway():
        return {
            "operation": "EVALUATE",
            "http_status": 200,
            "public_reason_code": "SYNTHETIC_CONTRACT_MATCH_WITH_LIMITATIONS",
            "request_body_sha256": "d" * 64,
            "response_body_sha256": "e" * 64,
            "customer_visible_result": {
                "result_status": "CONDITIONALLY_RECOMMENDED"
            },
            "limitations": ["SYNTHETIC_ONLY"],
        }

    @staticmethod
    def assessment():
        return {
            "contract_understood": True,
            "operation_usable": True,
            "result_contract_match": True,
            "recommendation": "CONDITIONALLY_RECOMMEND_SERVICE",
            "recommendation_reason": "The synthetic contract matched.",
            "commercial_blockers": ["No production evidence."],
            "repeat_evaluation_recommended": True,
            "limitations": ["SYNTHETIC_ONLY"],
            "non_claims": ["NOT_CUSTOMER_ADOPTION"],
        }

    @staticmethod
    def review():
        return {
            "verdict": "PASS",
            "customer_result_supported": True,
            "blocking_findings": [],
            "non_blocking_findings": ["Synthetic scope remains limited."],
            "evidence_refs": ["checkpoint:synthetic-assessment"],
            "required_corrections": [],
            "limitations": ["SYNTHETIC_ONLY"],
        }

    def persist(
        self,
        stage,
        structured_result,
        *,
        checkpoint_id=None,
        requested_model="synthetic-model",
        returned_model="synthetic-model",
        model_identity_status="MATCH",
        crash_after_durable_write=False,
    ):
        self.sequence += 1
        identifier = checkpoint_id or f"checkpoint-{self.sequence:02d}"
        return CHECKPOINT.persist_checkpoint(
            checkpoint_directory=self.checkpoint_directory,
            checkpoint_id=identifier,
            cycle_id=self.cycle_id,
            stage=stage,
            source_main="a" * 40,
            gateway_revision="b" * 40,
            attempt_id=f"attempt-{self.sequence:02d}",
            provider="SYNTHETIC_PROVIDER",
            requested_model=requested_model,
            returned_model=returned_model,
            model_identity_status=model_identity_status,
            response_capture_state="FINALIZED_SUCCESS",
            response_envelope_ref=f"captures/attempt-{self.sequence:02d}.json",
            response_body_sha256="c" * 64,
            structured_result=structured_result,
            crash_after_durable_write=crash_after_durable_write,
        )

    def test_scp01_plan_persistence_success(self):
        result = self.persist("CONTRIBUTOR_PLAN", self.plan(), checkpoint_id="plan")
        self.assertEqual("DURABLE", result.checkpoint["checkpoint_state"])
        self.assertTrue(result.checkpoint["downstream_dispatch_authorized"])
        self.assertEqual(0o600, stat.S_IMODE(result.checkpoint_path.stat().st_mode))
        self.assertEqual(0o700, stat.S_IMODE(self.checkpoint_directory.stat().st_mode))
        for field in (
            "raw_prompt_retained",
            "raw_response_retained",
            "hidden_reasoning_retained",
            "credential_material_retained",
        ):
            self.assertFalse(result.checkpoint[field])

    def test_scp02_invalid_plan_does_not_allow_gateway(self):
        invalid = self.plan()
        invalid.pop("contract_version")
        with self.assertRaises(CHECKPOINT.SchemaValidationError):
            self.persist("CONTRIBUTOR_PLAN", invalid)
        gate = CHECKPOINT.CheckpointStageGate(
            self.checkpoint_directory, self.cycle_id
        )
        with self.assertRaises(CHECKPOINT.StageGateError):
            gate.authorize_dispatch("GATEWAY_CUSTOMER_PROJECTION")
        self.assertEqual([], list(self.checkpoint_directory.iterdir()))

    def test_scp03_plan_crash_recovery(self):
        with self.assertRaises(CHECKPOINT.InjectedCheckpointCrash) as caught:
            self.persist(
                "CONTRIBUTOR_PLAN",
                self.plan(),
                checkpoint_id="plan-crash",
                crash_after_durable_write=True,
            )
        recovered = CHECKPOINT.load_checkpoint(caught.exception.checkpoint_path)
        self.assertEqual("DURABLE", recovered["checkpoint_state"])
        gate = CHECKPOINT.CheckpointStageGate(
            self.checkpoint_directory, self.cycle_id
        )
        self.assertTrue(gate.authorize_dispatch("GATEWAY_CUSTOMER_PROJECTION"))

    def test_scp04_gateway_projection_persistence_success(self):
        self.persist("CONTRIBUTOR_PLAN", self.plan(), checkpoint_id="plan")
        gate = CHECKPOINT.CheckpointStageGate(
            self.checkpoint_directory, self.cycle_id
        )
        self.assertTrue(gate.authorize_dispatch("GATEWAY_CUSTOMER_PROJECTION"))
        result = self.persist(
            "GATEWAY_CUSTOMER_PROJECTION", self.gateway(), checkpoint_id="gateway"
        )
        self.assertEqual("DURABLE", result.checkpoint["checkpoint_state"])
        self.assertEqual(
            "gateway-customer-projection.schema.json",
            Path(result.checkpoint["contract_schema"]).name,
        )

    def test_scp05_gateway_private_path_is_rejected(self):
        invalid = self.gateway()
        invalid["customer_visible_result"] = {
            "diagnostic": "/Users/example/private-core.py"
        }
        with self.assertRaises(CHECKPOINT.SanitizationError):
            self.persist("GATEWAY_CUSTOMER_PROJECTION", invalid)
        self.assertEqual([], list(self.checkpoint_directory.iterdir()))

    def test_scp06_gateway_crash_recovery(self):
        with self.assertRaises(CHECKPOINT.InjectedCheckpointCrash) as caught:
            self.persist(
                "GATEWAY_CUSTOMER_PROJECTION",
                self.gateway(),
                checkpoint_id="gateway-crash",
                crash_after_durable_write=True,
            )
        recovered = CHECKPOINT.load_checkpoint(caught.exception.checkpoint_path)
        self.assertEqual(
            "GATEWAY_CUSTOMER_PROJECTION", recovered["stage"]
        )
        self.assertEqual("DURABLE", recovered["checkpoint_state"])

    def test_scp07_assessment_persistence_success(self):
        result = self.persist(
            "CONTRIBUTOR_ASSESSMENT",
            self.assessment(),
            checkpoint_id="assessment",
        )
        self.assertEqual(
            "CONDITIONALLY_RECOMMEND_SERVICE",
            result.checkpoint["structured_result"]["recommendation"],
        )
        self.assertTrue(result.checkpoint["downstream_dispatch_authorized"])

    def test_scp08_assessment_must_be_durable_before_reviewer(self):
        self.persist("CONTRIBUTOR_PLAN", self.plan(), checkpoint_id="plan")
        self.persist(
            "GATEWAY_CUSTOMER_PROJECTION", self.gateway(), checkpoint_id="gateway"
        )
        gate = CHECKPOINT.CheckpointStageGate(
            self.checkpoint_directory, self.cycle_id
        )
        with self.assertRaises(CHECKPOINT.StageGateError):
            gate.authorize_dispatch("INDEPENDENT_REVIEW")
        self.persist(
            "CONTRIBUTOR_ASSESSMENT",
            self.assessment(),
            checkpoint_id="assessment",
        )
        self.assertTrue(gate.authorize_dispatch("INDEPENDENT_REVIEW"))

    def test_scp09_assessment_crash_recovery(self):
        with self.assertRaises(CHECKPOINT.InjectedCheckpointCrash) as caught:
            self.persist(
                "CONTRIBUTOR_ASSESSMENT",
                self.assessment(),
                checkpoint_id="assessment-crash",
                crash_after_durable_write=True,
            )
        recovered = CHECKPOINT.load_checkpoint(caught.exception.checkpoint_path)
        self.assertEqual("CONTRIBUTOR_ASSESSMENT", recovered["stage"])
        self.assertEqual("DURABLE", recovered["checkpoint_state"])

    def test_scp10_reviewer_success_persistence(self):
        result = self.persist(
            "INDEPENDENT_REVIEW", self.review(), checkpoint_id="review"
        )
        self.assertEqual("PASS", result.checkpoint["structured_result"]["verdict"])
        self.assertEqual("DURABLE", result.checkpoint["checkpoint_state"])

    def test_scp11_reviewer_timeout_preserves_first_three_stages(self):
        summary = CHECKPOINT.replay_synthetic_d02(self.checkpoint_directory)
        self.assertTrue(summary["plan_checkpoint_durable"])
        self.assertTrue(summary["gateway_checkpoint_durable"])
        self.assertTrue(summary["assessment_checkpoint_durable"])
        self.assertFalse(summary["review_checkpoint_durable"])
        self.assertEqual(
            "POST_DISPATCH_OUTCOME_UNKNOWN", summary["review_outcome"]
        )
        self.assertFalse(summary["cycle_complete"])

    def test_scp12_reviewer_model_mismatch_fails_closed(self):
        with self.assertRaises(CHECKPOINT.StageGateError):
            self.persist(
                "INDEPENDENT_REVIEW",
                self.review(),
                checkpoint_id="review-mismatch",
                requested_model="kimi-k2.6",
                returned_model="other-model",
                model_identity_status="MISMATCH",
            )
        self.assertFalse(
            (self.checkpoint_directory / "review-mismatch.checkpoint.json").exists()
        )

    def test_scp13_raw_provider_response_cannot_enter_checkpoint(self):
        invalid = self.plan()
        invalid["raw_provider_response"] = {"choices": ["raw"]}
        with self.assertRaises(CHECKPOINT.SchemaValidationError):
            self.persist("CONTRIBUTOR_PLAN", invalid)
        result = self.persist(
            "CONTRIBUTOR_PLAN", self.plan(), checkpoint_id="plan-clean"
        )
        rendered = result.checkpoint_path.read_text(encoding="utf-8")
        self.assertNotIn("raw_provider_response", rendered)
        self.assertNotIn("choices", rendered)

    def test_scp14_secret_and_token_scan(self):
        invalid = self.assessment()
        invalid["recommendation_reason"] = "Authorization: Bearer abcdef123456"
        with self.assertRaises(CHECKPOINT.SanitizationError):
            self.persist("CONTRIBUTOR_ASSESSMENT", invalid)
        self.assertEqual([], list(self.checkpoint_directory.iterdir()))

    def test_scp15_checkpoint_hash_tamper_detection(self):
        result = self.persist(
            "CONTRIBUTOR_PLAN", self.plan(), checkpoint_id="plan-tamper"
        )
        payload = json.loads(result.checkpoint_path.read_text(encoding="utf-8"))
        payload["structured_result"]["problem_understood"] = "Tampered result."
        result.checkpoint_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.chmod(result.checkpoint_path, 0o600)
        with self.assertRaises(CHECKPOINT.IntegrityError):
            CHECKPOINT.load_checkpoint(result.checkpoint_path)

    def test_scp16_audit_summary_requires_no_provider_call(self):
        summary = CHECKPOINT.replay_synthetic_d02(self.checkpoint_directory)
        self.assertTrue(summary["customer_recommendation_available"])
        self.assertEqual(
            "CONDITIONALLY_RECOMMEND_SERVICE",
            summary["customer_recommendation"],
        )
        self.assertEqual(0, summary["real_model_call_count"])
        self.assertEqual(0, summary["real_provider_call_count"])
        self.assertFalse(hasattr(CHECKPOINT, "urllib"))


if __name__ == "__main__":
    unittest.main()
