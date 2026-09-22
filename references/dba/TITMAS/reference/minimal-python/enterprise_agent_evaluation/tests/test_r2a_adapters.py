from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


PACKAGE_PARENT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_PARENT))

from enterprise_agent_evaluation.adapters import (  # noqa: E402
    R2AContractError,
    R2ATransportError,
    TransportResult,
    determine_model_alignment,
    parse_text_contract,
    sha256_text,
)
from enterprise_agent_evaluation.adapters.aliyun_bailian_workflow import (  # noqa: E402
    AliyunBailianWorkflowAdapter,
)
from enterprise_agent_evaluation.adapters.dify_workflow import (  # noqa: E402
    DifyWorkflowAdapter,
)


VALID_TEXT = (
    "ACTION: ANSWER\n"
    "REPLY: 订单已发货，建议等待两个工作日。\n"
    "POLICY_REF: synthetic-policy-2\n"
    "LIMITATION: 这只是未发送的合成答复建议。"
)


def request_fixture() -> dict:
    context = "synthetic context"
    return {
        "phase": "A0_DIRECT_CONTEXT_PARITY",
        "case_id": "r2a-normal-order-status",
        "prompt": "bounded synthetic prompt",
        "input_variables": {
            "phase": "A0_DIRECT_CONTEXT_PARITY",
            "case_id": "r2a-normal-order-status",
            "query": "synthetic query",
            "direct_context": context,
            "source_document_sha256": "a" * 64,
            "prompt": "bounded synthetic prompt",
        },
        "configured_model_id": "qwen3.7-max",
        "application_version": "app-v1",
        "knowledge_base_version": "kb-v1",
        "source_document_sha256": "a" * 64,
        "direct_context_sha256": sha256_text(context),
        "common_parameters": {
            "temperature": 0.2,
            "top_p": 0.8,
            "max_tokens": 800,
            "enable_thinking": False,
            "enable_search": False,
            "response_format": "text",
        },
        "privacy_classification": "SYNTHETIC",
    }


def aliyun_body(model_id: str = "qwen3.7-max") -> dict:
    return {
        "output": {
            "text": VALID_TEXT,
            "session_id": "session-synthetic",
            "workflow_message": {
                "node_status": "success",
                "node_type": "End",
                "node_name": "end",
                "node_is_completed": True,
                "node_id": "node-synthetic",
                "message": {"content": VALID_TEXT},
            },
        },
        "usage": {
            "models": [
                {"model_id": model_id, "input_tokens": 4000, "output_tokens": 800}
            ]
        },
        "request_id": "request-synthetic-a",
    }


def dify_body(model_id: str | None = "qwen3.7-max") -> dict:
    outputs = {
        "result": VALID_TEXT,
        "input_tokens": 4000,
        "output_tokens": 800,
    }
    if model_id is not None:
        outputs["reported_model_id"] = model_id
    return {
        "task_id": "task-synthetic-b",
        "workflow_run_id": "run-synthetic-b",
        "data": {
            "status": "succeeded",
            "outputs": outputs,
            "total_tokens": 4800,
            "total_steps": 3,
            "elapsed_time": 1.25,
        },
    }


class R2AAdapterTests(unittest.TestCase):
    def test_r2a_adapter_01_missing_credentials_fail_closed(self):
        with self.assertRaises(R2AContractError):
            AliyunBailianWorkflowAdapter(api_key="", app_id="app")
        with self.assertRaises(R2AContractError):
            DifyWorkflowAdapter(api_key="", base_url="https://api.dify.ai/v1")

    def test_r2a_adapter_02_request_contract_is_exact(self):
        changed = request_fixture()
        changed["unexpected"] = True
        adapter = AliyunBailianWorkflowAdapter(
            api_key="secret-canary",
            app_id="app",
            transport=lambda *_: TransportResult(200, aliyun_body()),
        )
        with self.assertRaises(R2AContractError):
            adapter.invoke(changed)

    def test_r2a_adapter_03_aliyun_calls_transport_once_and_maps_event(self):
        calls = []

        def transport(url, headers, payload, timeout):
            calls.append((url, headers, payload, timeout))
            return TransportResult(200, aliyun_body())

        adapter = AliyunBailianWorkflowAdapter(
            api_key="secret-canary",
            app_id="app-synthetic",
            workspace_id="workspace-synthetic",
            transport=transport,
        )
        event = adapter.invoke(request_fixture())
        self.assertEqual(1, len(calls))
        self.assertTrue(calls[0][0].endswith("/app-synthetic/completion"))
        self.assertEqual("Bearer secret-canary", calls[0][1]["Authorization"])
        self.assertFalse(calls[0][2]["parameters"]["has_thoughts"])
        self.assertEqual("SUCCEEDED", event["status"])
        self.assertEqual("PROVIDER_USAGE", event["model_id_source"])
        self.assertEqual(4800, event["total_tokens"])
        self.assertEqual(0.0768, event["estimated_cost_cny"])

    def test_r2a_adapter_04_aliyun_does_not_retain_node_content(self):
        adapter = AliyunBailianWorkflowAdapter(
            api_key="secret",
            app_id="app",
            transport=lambda *_: TransportResult(200, aliyun_body()),
        )
        event = adapter.invoke(request_fixture())
        self.assertEqual(1, len(event["node_events"]))
        self.assertNotIn("message", event["node_events"][0])
        self.assertNotIn("content", event["node_events"][0])

    def test_r2a_adapter_05_dify_calls_official_workflow_endpoint_once(self):
        calls = []

        def transport(url, headers, payload, timeout):
            calls.append((url, headers, payload, timeout))
            return TransportResult(200, dify_body())

        adapter = DifyWorkflowAdapter(
            api_key="secret-canary",
            base_url="https://api.dify.ai/v1",
            transport=transport,
        )
        event = adapter.invoke(request_fixture())
        self.assertEqual(1, len(calls))
        self.assertEqual("https://api.dify.ai/v1/workflows/run", calls[0][0])
        self.assertEqual("blocking", calls[0][2]["response_mode"])
        self.assertEqual("SUCCEEDED", event["status"])
        self.assertEqual("WORKFLOW_OUTPUT_DECLARATION", event["model_id_source"])
        self.assertEqual(1250, event["elapsed_ms"])

    def test_r2a_adapter_06_dify_missing_model_is_not_assessed(self):
        adapter = DifyWorkflowAdapter(
            api_key="secret",
            base_url="https://api.dify.ai/v1",
            transport=lambda *_: TransportResult(200, dify_body(None)),
        )
        event = adapter.invoke(request_fixture())
        self.assertIsNone(event["reported_model_id"])
        self.assertEqual("NOT_OBSERVABLE", event["model_id_observability"])
        self.assertIn("actual_model_snapshot", event["not_assessed_fields"])

    def test_r2a_adapter_07_transport_failure_has_no_retry(self):
        calls = 0

        def transport(*_):
            nonlocal calls
            calls += 1
            raise R2ATransportError("bounded failure")

        adapter = DifyWorkflowAdapter(
            api_key="secret",
            base_url="https://api.dify.ai/v1",
            transport=transport,
        )
        with self.assertRaises(R2ATransportError):
            adapter.invoke(request_fixture())
        self.assertEqual(1, calls)

    def test_r2a_adapter_08_event_does_not_expose_credentials(self):
        secret = "R2A_SECRET_CANARY"
        adapter = AliyunBailianWorkflowAdapter(
            api_key=secret,
            app_id="app",
            transport=lambda *_: TransportResult(200, aliyun_body()),
        )
        event = adapter.invoke(request_fixture())
        self.assertNotIn(secret, repr(event))
        self.assertNotIn("Authorization", repr(event))

    def test_r2a_adapter_09_plain_text_contract_parses(self):
        parsed = parse_text_contract(VALID_TEXT)
        self.assertEqual("ANSWER", parsed["action"])
        self.assertIn("合成", parsed["limitation"])

    def test_r2a_adapter_10_invalid_text_contract_fails_without_repair(self):
        for invalid in ("{}", "ACTION: ANSWER", "REPLY: only"):
            with self.assertRaisesRegex(R2AContractError, "OUTPUT_CONTRACT_FAIL"):
                parse_text_contract(invalid)

    def test_r2a_adapter_11_evidence_is_reference_only(self):
        adapter = DifyWorkflowAdapter(
            api_key="secret",
            base_url="https://api.dify.ai/v1",
            transport=lambda *_: TransportResult(200, dify_body()),
        )
        evidence = adapter.invoke(request_fixture())["evidence_ref"]
        self.assertEqual("REFERENCE_ONLY_NOT_DBOS_ADMITTED", evidence["admission_status"])
        self.assertFalse(evidence["canonical_evidence_object_created"])
        self.assertEqual("NONE", evidence["authority_effect"])

    def test_r2a_adapter_12_alignment_four_states(self):
        a = AliyunBailianWorkflowAdapter(
            api_key="secret",
            app_id="app",
            transport=lambda *_: TransportResult(200, aliyun_body()),
        ).invoke(request_fixture())
        b = DifyWorkflowAdapter(
            api_key="secret",
            base_url="https://api.dify.ai/v1",
            transport=lambda *_: TransportResult(200, dify_body()),
        ).invoke(request_fixture())
        self.assertEqual("SAME_MODEL_ALIAS_CONFIGURED", determine_model_alignment([a, b]))
        missing = copy.deepcopy(b)
        missing["reported_model_id"] = None
        self.assertEqual("MODEL_ID_NOT_OBSERVABLE", determine_model_alignment([a, missing]))
        mismatch = copy.deepcopy(b)
        mismatch["reported_model_id"] = "qwen-other"
        mismatch["model_id_source"] = "PROVIDER_RESPONSE"
        self.assertEqual("MODEL_MISMATCH", determine_model_alignment([a, mismatch]))
        snapshot_a = copy.deepcopy(a)
        snapshot_b = copy.deepcopy(b)
        for event in (snapshot_a, snapshot_b):
            event["reported_model_id"] = "qwen3.7-max-2026-05-20"
            event["model_id_source"] = "PROVIDER_RESPONSE"
        self.assertEqual(
            "SAME_MODEL_SNAPSHOT_CONFIRMED",
            determine_model_alignment([snapshot_a, snapshot_b]),
        )
        snapshot_b["model_id_source"] = "WORKFLOW_OUTPUT_DECLARATION"
        self.assertEqual(
            "MODEL_ID_NOT_OBSERVABLE",
            determine_model_alignment([snapshot_a, snapshot_b]),
        )


if __name__ == "__main__":
    unittest.main()
