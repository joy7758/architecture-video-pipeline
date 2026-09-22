from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE_PARENT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_PARENT))

from enterprise_agent_evaluation.adapters import TransportResult, sha256_text  # noqa: E402
from enterprise_agent_evaluation.adapters.aliyun_bailian_workflow import (  # noqa: E402
    AliyunBailianWorkflowAdapter,
)
from enterprise_agent_evaluation.adapters.dify_workflow import DifyWorkflowAdapter  # noqa: E402
from enterprise_agent_evaluation.r2a_smoke_runner import (  # noqa: E402
    DBA_ROOT,
    ROUTE_IDS,
    R2ASmokeBlocked,
    SmokeBudget,
    build_request,
    live_preflight,
    load_r2a_cases,
    load_r2a_contract,
    native_rag_differences,
    run_private_smoke,
)


VALID_TEXT = (
    "ACTION: ANSWER\n"
    "REPLY: 这是合成答复建议。\n"
    "POLICY_REF: synthetic-policy\n"
    "LIMITATION: 未经人工批准不得发送。"
)


def rag_config(prefix: str) -> dict:
    return {
        "chunking_strategy": f"{prefix}-native",
        "chunk_size": 500 if prefix == "a" else 600,
        "chunk_overlap": 50,
        "embedding_model": f"{prefix}-embedding",
        "retrieval_top_k": 3,
        "score_threshold": 0.5,
        "reranker": f"{prefix}-reranker",
        "knowledge_base_version": f"{prefix}-kb-v1",
    }


def route_metadata() -> dict:
    return {
        ROUTE_IDS[0]: {
            "application_version": "a-app-v1",
            "knowledge_base_version": "a-kb-v1",
            "rag_configuration": rag_config("a"),
        },
        ROUTE_IDS[1]: {
            "application_version": "b-app-v1",
            "knowledge_base_version": "b-kb-v1",
            "rag_configuration": rag_config("b"),
        },
    }


class CountingTransport:
    def __init__(self, provider: str, *, model_id: str | None = "qwen3.7-max", text: str = VALID_TEXT):
        self.provider = provider
        self.model_id = model_id
        self.text = text
        self.calls = 0

    def __call__(self, url, headers, payload, timeout):
        self.calls += 1
        if self.provider == "aliyun":
            body = {
                "output": {"text": self.text, "workflow_message": {"node_status": "success"}},
                "usage": {"models": [{
                    "model_id": self.model_id,
                    "input_tokens": 4000,
                    "output_tokens": 800,
                }]},
                "request_id": f"a-{self.calls}",
            }
        else:
            outputs = {
                "result": self.text,
                "input_tokens": 4000,
                "output_tokens": 800,
            }
            if self.model_id is not None:
                outputs["reported_model_id"] = self.model_id
            body = {
                "task_id": f"b-task-{self.calls}",
                "workflow_run_id": f"b-run-{self.calls}",
                "data": {
                    "status": "succeeded",
                    "outputs": outputs,
                    "total_tokens": 4800,
                    "elapsed_time": 0.5,
                },
            }
        return TransportResult(200, body)


def adapter_pair(*, model_a: str | None = "qwen3.7-max", model_b: str | None = "qwen3.7-max", text_b: str = VALID_TEXT):
    ta = CountingTransport("aliyun", model_id=model_a)
    tb = CountingTransport("dify", model_id=model_b, text=text_b)
    adapters = {
        ROUTE_IDS[0]: AliyunBailianWorkflowAdapter(
            api_key="secret-a",
            app_id="app-a",
            transport=ta,
        ),
        ROUTE_IDS[1]: DifyWorkflowAdapter(
            api_key="secret-b",
            base_url="https://api.dify.ai/v1",
            transport=tb,
        ),
    }
    return adapters, ta, tb


def ready_environment() -> dict[str, str]:
    environment = {
        "TITMAS_R2A_LIVE_AUTHORIZED": "true",
        "DASHSCOPE_API_KEY": "secret-a",
        "BAILIAN_APP_ID": "app-a",
        "DIFY_WORKFLOW_API_KEY": "secret-b",
        "DIFY_BASE_URL": "https://api.dify.ai/v1",
        "R2A_BAILIAN_APP_VERSION": "a-app-v1",
        "R2A_BAILIAN_KB_VERSION": "a-kb-v1",
        "R2A_DIFY_APP_VERSION": "b-app-v1",
        "R2A_DIFY_KB_VERSION": "b-kb-v1",
        "R2A_DIFY_DSL_SHA256": "d" * 64,
        "R2A_SOURCE_DOCUMENT_SHA256": load_r2a_cases()["source_document"]["sha256"],
        "R2A_BAILIAN_CONFIGURED_MODEL_ID": "qwen3.7-max",
        "R2A_DIFY_CONFIGURED_MODEL_ID": "qwen3.7-max",
        "R2A_COMMON_PARAMETERS_JSON": json.dumps(load_r2a_contract()["common_parameters"]),
        "R2A_ROUTE_A_RAG_CONFIGURATION_JSON": json.dumps(rag_config("a")),
        "R2A_ROUTE_B_RAG_CONFIGURATION_JSON": json.dumps(rag_config("b")),
    }
    for name in (
        "R2A_BAILIAN_WORKFLOW_PUBLISHED",
        "R2A_BAILIAN_SOURCE_HASH_CONFIRMED",
        "R2A_BAILIAN_MODEL_ALIAS_CONFIRMED",
        "R2A_BAILIAN_THINKING_DISABLED",
        "R2A_BAILIAN_SEARCH_DISABLED",
        "R2A_DIFY_SANDBOX_READY",
        "R2A_DIFY_WORKFLOW_PUBLISHED",
        "R2A_DIFY_TONGYI_PLUGIN_INSTALLED",
        "R2A_DIFY_BYOK_CONFIRMED",
        "R2A_DIFY_SOURCE_HASH_CONFIRMED",
        "R2A_DIFY_MODEL_ALIAS_CONFIRMED",
        "R2A_DIFY_THINKING_DISABLED",
        "R2A_DIFY_SEARCH_DISABLED",
        "R2A_PHASE_ROUTING_CONFIRMED",
        "R2A_COMMON_PARAMETER_INTERSECTION_CONFIRMED",
    ):
        environment[name] = "true"
    return environment


class R2ASmokeProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load_r2a_contract()
        cls.cases = load_r2a_cases()

    def test_r2a_protocol_01_contract_freezes_limits_and_no_publication(self):
        self.assertEqual(16, self.contract["limits"]["max_real_model_calls"])
        self.assertEqual(0, self.contract["limits"]["automatic_retries"])
        self.assertEqual(5.0, self.contract["limits"]["cash_cap_cny"])
        self.assertFalse(self.contract["publication_allowed"])
        self.assertEqual("E1", self.contract["evidence_level_cap"])

    def test_r2a_protocol_02_cases_are_exactly_two_a0_and_six_a1(self):
        a0 = [case for case in self.cases["cases"] if "A0_DIRECT_CONTEXT_PARITY" in case["phases"]]
        a1 = [case for case in self.cases["cases"] if "A1_NATIVE_RAG_SMOKE" in case["phases"]]
        self.assertEqual(2, len(a0))
        self.assertEqual(6, len(a1))

    def test_r2a_protocol_03_source_document_digest_and_size_match(self):
        source = self.cases["source_document"]
        self.assertEqual(source["sha256"], sha256_text(source["content"]))
        self.assertEqual(source["size_bytes"], len(source["content"].encode("utf-8")))

    def test_r2a_protocol_04_a0_route_neutral_input_is_byte_identical(self):
        case = self.cases["cases"][0]
        a = build_request(
            contract=self.contract,
            cases_fixture=self.cases,
            case=case,
            phase="A0_DIRECT_CONTEXT_PARITY",
            application_version="a-v1",
            knowledge_base_version="a-kb",
        )
        b = build_request(
            contract=self.contract,
            cases_fixture=self.cases,
            case=case,
            phase="A0_DIRECT_CONTEXT_PARITY",
            application_version="b-v1",
            knowledge_base_version="b-kb",
        )
        self.assertEqual(a["prompt"], b["prompt"])
        self.assertEqual(a["input_variables"], b["input_variables"])
        self.assertEqual(a["direct_context_sha256"], b["direct_context_sha256"])

    def test_r2a_protocol_05_a1_does_not_inject_direct_context(self):
        request = build_request(
            contract=self.contract,
            cases_fixture=self.cases,
            case=self.cases["cases"][0],
            phase="A1_NATIVE_RAG_SMOKE",
            application_version="a-v1",
            knowledge_base_version="a-kb",
        )
        self.assertEqual("", request["input_variables"]["direct_context"])
        self.assertNotIn(self.cases["source_document"]["content"], request["prompt"])

    def test_r2a_protocol_06_common_output_is_text_only(self):
        parameters = self.contract["common_parameters"]
        self.assertEqual("text", parameters["response_format"])
        self.assertFalse(parameters["enable_thinking"])
        self.assertFalse(parameters["enable_search"])
        self.assertNotIn("seed", parameters)

    def test_r2a_protocol_07_call_cap_fails_closed(self):
        budget = SmokeBudget(max_calls=1, per_route_max=1)
        budget.reserve(ROUTE_IDS[0])
        with self.assertRaisesRegex(R2ASmokeBlocked, "real model call cap"):
            budget.reserve(ROUTE_IDS[1])

    def test_r2a_protocol_08_per_route_cap_fails_closed(self):
        budget = SmokeBudget(max_calls=16, per_route_max=1)
        budget.reserve(ROUTE_IDS[0])
        with self.assertRaises(R2ASmokeBlocked):
            budget.reserve(ROUTE_IDS[0])

    def test_r2a_protocol_09_cash_cap_fails_closed(self):
        budget = SmokeBudget(cash_cap_cny=0.1)
        with self.assertRaisesRegex(R2ASmokeBlocked, "cash cap"):
            budget.add_cost(0.11)

    def test_r2a_protocol_10_unknown_cost_fails_closed(self):
        budget = SmokeBudget()
        with self.assertRaisesRegex(R2ASmokeBlocked, "could not be observed"):
            budget.add_cost(None)

    def test_r2a_protocol_11_native_rag_differences_are_retained(self):
        result = native_rag_differences(route_metadata())
        self.assertEqual("NATIVE_RAG_CONFIGURATION_DIFFERENCE", result["status"])
        self.assertEqual("COMPLETE_DEPLOYMENT_ROUTE", result["comparison_object"])
        self.assertIn("embedding_model", result["differences"])

    def test_r2a_protocol_12_live_preflight_defaults_closed(self):
        result = live_preflight({})
        self.assertEqual("R2A_BLOCKED_ACCOUNT_OR_APP_CONFIGURATION", result["status"])
        self.assertFalse(result["live_authorized"])
        self.assertEqual("MISSING", result["credential_presence"]["DASHSCOPE_API_KEY"])

    def test_r2a_protocol_13_live_preflight_accepts_only_complete_attestation(self):
        result = live_preflight(ready_environment())
        self.assertEqual("READY", result["status"])
        self.assertEqual("PRESENT", result["credential_presence"]["DIFY_WORKFLOW_API_KEY"])
        self.assertNotIn("secret-b", repr(result))

    def test_r2a_protocol_14_complete_offline_transport_smoke_is_4_plus_12(self):
        adapters, ta, tb = adapter_pair()
        with tempfile.TemporaryDirectory() as directory:
            result = run_private_smoke(
                adapters=adapters,
                route_metadata=route_metadata(),
                contract=self.contract,
                cases_fixture=self.cases,
                output_dir=Path(directory),
            )
            self.assertEqual(4, result["a0_direct_context_calls"])
            self.assertEqual(12, result["a1_native_rag_calls"])
            self.assertEqual(16, result["total_real_model_calls"])
            self.assertTrue((Path(directory) / "summary.json").is_file())
            self.assertEqual(17, len(list(Path(directory).glob("*.json"))))
        self.assertEqual(8, ta.calls)
        self.assertEqual(8, tb.calls)

    def test_r2a_protocol_15_result_separates_fact_assessment_and_judgment(self):
        adapters, _, _ = adapter_pair()
        with tempfile.TemporaryDirectory() as directory:
            result = run_private_smoke(
                adapters=adapters,
                route_metadata=route_metadata(),
                output_dir=Path(directory),
            )
        self.assertEqual(16, len(result["observed_facts"]))
        self.assertEqual(16, len(result["provisional_assessments"]))
        self.assertEqual([], result["human_judgments"])
        self.assertEqual("NOT_ASSESSED", result["human_judgment_status"])
        self.assertFalse(result["recommendation_index_calculated"])

    def test_r2a_protocol_16_model_mismatch_stops_before_a1(self):
        adapters, ta, tb = adapter_pair(model_b="qwen-other")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(R2ASmokeBlocked, "model identifiers differ"):
                run_private_smoke(
                    adapters=adapters,
                    route_metadata=route_metadata(),
                    output_dir=Path(directory),
                )
        self.assertEqual(1, ta.calls)
        self.assertEqual(1, tb.calls)

    def test_r2a_protocol_17_output_contract_failure_does_not_repair_or_retry(self):
        adapters, ta, tb = adapter_pair(text_b="invalid output")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(Exception, "OUTPUT_CONTRACT_FAIL"):
                run_private_smoke(
                    adapters=adapters,
                    route_metadata=route_metadata(),
                    output_dir=Path(directory),
                )
        self.assertEqual(1, ta.calls)
        self.assertEqual(1, tb.calls)

    def test_r2a_protocol_18_repository_output_path_is_rejected(self):
        adapters, _, _ = adapter_pair()
        with self.assertRaisesRegex(R2ASmokeBlocked, "inside repository"):
            run_private_smoke(
                adapters=adapters,
                route_metadata=route_metadata(),
                output_dir=DBA_ROOT / "forbidden-r2a-output",
            )

    def test_r2a_protocol_19_no_database_retry_or_authority_implementation(self):
        sources = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                PACKAGE_PARENT / "enterprise_agent_evaluation" / "r2a_smoke_runner.py",
                PACKAGE_PARENT / "enterprise_agent_evaluation" / "adapters" / "aliyun_bailian_workflow.py",
                PACKAGE_PARENT / "enterprise_agent_evaluation" / "adapters" / "dify_workflow.py",
            )
        )
        for marker in ("sqlite3", "sqlalchemy", "psycopg", "CREATE TABLE", "permission_grant"):
            self.assertNotIn(marker, sources)
        self.assertNotIn("time.sleep", sources)
        self.assertNotIn("for attempt in", sources)

    def test_r2a_protocol_20_environment_does_not_need_or_emit_publication(self):
        environment = ready_environment()
        environment["PUBLICATION_ALLOWED"] = "true"
        result = live_preflight(environment)
        self.assertEqual("READY", result["status"])
        self.assertNotIn("PUBLICATION_ALLOWED", result)
        self.assertFalse(self.contract["publication_allowed"])


if __name__ == "__main__":
    unittest.main()
