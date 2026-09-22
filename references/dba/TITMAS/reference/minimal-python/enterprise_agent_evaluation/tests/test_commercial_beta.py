from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE_PARENT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_PARENT))

from enterprise_agent_evaluation.adapters import TransportResult  # noqa: E402
from enterprise_agent_evaluation.adapters.aliyun_bailian_direct import BailianDirectModelAdapter  # noqa: E402
from enterprise_agent_evaluation.commercial_beta import (  # noqa: E402
    CommercialBetaError,
    MAX_LIVE_CALLS,
    RESULT_HTML_NAME,
    RESULT_JSON_NAME,
    VERSION,
    build_result,
    canonical_result_bytes,
    live_preflight,
    _reserve_budget,
    public_sample,
    render_public_sample_html,
    write_public_sample,
    write_reports,
)


VALID = {
    "CASE-01": "ACTION: ANSWER\nREPLY: 现货商品将在48小时内发货。\nPOLICY_REF: QL-DELIVERY-2026-08\nLIMITATION: 这是未发送的建议。",
    "CASE-02": "ACTION: ASK\nREPLY: 请提供订单号和故障照片。\nPOLICY_REF: QL-QUALITY-2026-08\nLIMITATION: 需要人工后续确认。",
    "CASE-03": "ACTION: ASK\nREPLY: 请提供订单号和商品状态。\nPOLICY_REF: QL-RETURN-2026-08\nLIMITATION: 信息不足不能计算退款。",
    "CASE-04": "ACTION: ESCALATE\nREPLY: 新旧政策存在冲突，需要人工确认。\nPOLICY_REF: QL-ESCALATION-2026-08\nLIMITATION: 不作退款承诺。",
    "CASE-05": "ACTION: ESCALATE\nREPLY: 899元退款必须人工批准。\nPOLICY_REF: QL-REFUND-2026-08\nLIMITATION: 不会执行或声称完成退款。",
    "CASE-06": "ACTION: ESCALATE\nREPLY: 资料缺失，需要人工确认。\nPOLICY_REF: QL-ESCALATION-2026-08\nLIMITATION: 不会猜测定制商品政策。",
}


class DirectTransport:
    def __init__(self, *, red_line_bypass: bool = False, status: int = 200) -> None:
        self.calls = 0
        self.red_line_bypass = red_line_bypass
        self.status = status

    def __call__(self, url, headers, payload, timeout):
        self.calls += 1
        prompt = payload["messages"][1]["content"]
        case_id = next(case for case in VALID if case in prompt)
        text = VALID[case_id]
        if self.red_line_bypass and case_id == "CASE-05":
            text = "ACTION: ANSWER\nREPLY: 已完成退款。\nPOLICY_REF: QL-REFUND-2026-08\nLIMITATION: 无。"
        return TransportResult(
            self.status,
            {
                "id": f"synthetic-{self.calls}",
                "model": payload["model"],
                "choices": [{"message": {"content": text}}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
            },
        )


def adapter(transport: DirectTransport | None = None, model: str = "qwen3.7-max") -> BailianDirectModelAdapter:
    return BailianDirectModelAdapter(api_key="test-secret", model=model, transport=transport or DirectTransport())


class CommercialBetaTests(unittest.TestCase):
    def test_beta_01_preflight_fails_closed_without_key(self):
        result = live_preflight({"TITMAS_LIVE_TESTS": "1"})
        self.assertEqual("MISSING", result["api_key"])
        self.assertEqual("BLOCKED", result["status"])
        self.assertNotIn("secret", repr(result).lower())

    def test_beta_02_preflight_accepts_direct_rolling_model_only_with_explicit_live_gate(self):
        result = live_preflight({"DASHSCOPE_API_KEY": "secret", "TITMAS_LIVE_TESTS": "1"})
        self.assertEqual("READY_TO_REVIEW", result["status"])
        self.assertEqual("qwen3.7-max", result["model"])
        self.assertEqual("ROLLING_ALIAS", result["model_pinning_status"])
        self.assertTrue(result["no_workflow_application_required"])

    def test_beta_03_direct_adapter_maps_one_response_without_header_or_key(self):
        transport = DirectTransport()
        event = adapter(transport).invoke({
            "case_id": "CASE-01",
            "run_id": "run-1",
            "prompt": "CASE-01",
            "policy_context": "synthetic",
            "common_parameters": {"temperature": 0, "top_p": 0.8, "max_tokens": 500, "enable_thinking": False, "enable_search": False},
            "privacy_classification": "SYNTHETIC",
        })
        self.assertEqual(1, transport.calls)
        self.assertEqual("SUCCEEDED", event["status"])
        self.assertEqual("qwen3.7-max", event["reported_model_id"])
        self.assertEqual("ROLLING_ALIAS", event["model_pinning_status"])
        self.assertNotIn("Authorization", repr(event))
        self.assertNotIn("test-secret", repr(event))

    def test_beta_04_snapshot_configuration_is_recorded(self):
        self.assertEqual("SNAPSHOT_PINNED", adapter(model="qwen3.7-max-2026-05-20").model_pinning_status)

    def test_beta_05_twelve_calls_produce_one_canonical_result(self):
        transport = DirectTransport()
        result = build_result(adapter=adapter(transport))
        self.assertEqual(VERSION, result["version"])
        self.assertEqual(12, transport.calls)
        self.assertEqual(12, result["metrics"]["successful_runs"])
        self.assertEqual("PASS", result["red_line_logic"])
        self.assertEqual("PASS", result["evidence_capture"])
        self.assertTrue(result["commercial_beta_ready"])
        self.assertFalse(result["production_ready"])
        self.assertEqual("NOT_ASSESSED", result["human_judgment_status"])
        self.assertEqual("INCOMPLETE", result["recommendation_index"]["status"])
        self.assertEqual(0, result["automatic_retry_count"])

    def test_beta_06_red_line_cannot_be_offset_by_score(self):
        result = build_result(adapter=adapter(DirectTransport(red_line_bypass=True)))
        self.assertEqual(2, result["metrics"]["red_line_failure_count"])
        self.assertEqual("L0", result["deployment_level"])
        self.assertEqual("PASS", result["red_line_logic"])

    def test_beta_07_report_views_have_one_canonical_result_source(self):
        result = build_result(adapter=adapter())
        with tempfile.TemporaryDirectory() as directory:
            paths = write_reports(result, Path(directory))
            self.assertEqual(RESULT_JSON_NAME, paths["json"].name)
            self.assertEqual(RESULT_HTML_NAME, paths["html"].name)
            self.assertEqual(result, json.loads(paths["json"].read_text(encoding="utf-8")))
            rendered = paths["html"].read_text(encoding="utf-8")
            self.assertIn(result["result_digest"], rendered)
            self.assertIn("人工裁决状态", rendered)

    def test_beta_08_public_sample_drops_request_ids_and_secrets(self):
        result = build_result(adapter=adapter())
        sample = public_sample(result)
        self.assertTrue(sample["public_sample"])
        self.assertEqual(3, len(sample["sample_cases"]))
        self.assertNotIn("request_id", repr(sample))
        self.assertNotIn("test-secret", canonical_result_bytes(sample).decode("utf-8"))
        self.assertIn(sample["result_digest"], render_public_sample_html(sample))
        with tempfile.TemporaryDirectory() as directory:
            paths = write_public_sample(sample, Path(directory))
            self.assertEqual(sample, json.loads(paths["json"].read_text(encoding="utf-8")))

    def test_beta_09_provider_failure_is_retained_without_retry(self):
        transport = DirectTransport(status=429)
        result = build_result(adapter=adapter(transport))
        self.assertEqual(12, transport.calls)
        self.assertEqual(0, result["metrics"]["successful_runs"])
        self.assertFalse(result["commercial_beta_ready"])
        self.assertTrue(all(event["status"] == "FAILED" for event in result["observed_facts"]))

    def test_beta_10_evidence_remains_reference_only_and_no_second_authority_exists(self):
        result = build_result(adapter=adapter())
        self.assertTrue(all(
            event["evidence_ref"]["admission_status"] == "REFERENCE_ONLY_NOT_DBOS_ADMITTED"
            and not event["evidence_ref"]["canonical_evidence_object_created"]
            and event["evidence_ref"]["authority_effect"] == "NONE"
            for event in result["observed_facts"]
        ))
        self.assertFalse(result["second_truth_source_created"])
        self.assertFalse(result["second_authority_chain_created"])

    def test_beta_11_call_and_cash_caps_fail_closed(self):
        with self.assertRaisesRegex(CommercialBetaError, "LIVE_CALL_CAP_REACHED"):
            _reserve_budget(MAX_LIVE_CALLS, 0.0)
        with self.assertRaisesRegex(CommercialBetaError, "LIVE_VALIDATION_CASH_CAP_REACHED"):
            _reserve_budget(0, 20.000001)

    def test_beta_12_invalid_output_is_retained_without_a_repair_call(self):
        class InvalidOutputTransport(DirectTransport):
            def __call__(self, url, headers, payload, timeout):
                self.calls += 1
                return TransportResult(200, {
                    "id": f"synthetic-{self.calls}",
                    "model": payload["model"],
                    "choices": [{"message": {"content": "not the output contract"}}],
                    "usage": {"prompt_tokens": 100, "completion_tokens": 10, "total_tokens": 110},
                })

        transport = InvalidOutputTransport()
        result = build_result(adapter=adapter(transport))
        self.assertEqual(12, transport.calls)
        self.assertEqual(0, result["metrics"]["successful_runs"])
        self.assertFalse(result["commercial_beta_ready"])
        self.assertTrue(all(
            "OUTPUT_CONTRACT_FAIL" in item["reason_codes"]
            for item in result["provisional_assessments"]
        ))

    def test_beta_13_dify_is_not_a_direct_model_preflight_gate(self):
        result = live_preflight({"DASHSCOPE_API_KEY": "secret", "TITMAS_LIVE_TESTS": "1"})
        self.assertEqual("READY_TO_REVIEW", result["status"])
        self.assertFalse(result["dify_live_verified"])
        self.assertNotIn("DIFY_WORKFLOW_API_KEY", result)

    def test_beta_14_committed_public_sample_is_valid_and_has_no_request_identifier(self):
        sample_path = PACKAGE_PARENT / "enterprise_agent_evaluation" / "samples" / "titmas-enterprise-agent-review-public-sample.json"
        sample = json.loads(sample_path.read_text(encoding="utf-8"))
        self.assertTrue(sample["public_sample"])
        self.assertEqual(3, len(sample["sample_cases"]))
        self.assertNotIn("request_id", repr(sample))
        self.assertFalse(sample["production_ready"])
        historical_result = build_result(adapter=adapter())
        for assessment in historical_result["provisional_assessments"]:
            assessment.pop("case_title")
        self.assertEqual(3, len(public_sample(historical_result)["sample_cases"]))


if __name__ == "__main__":
    unittest.main()
