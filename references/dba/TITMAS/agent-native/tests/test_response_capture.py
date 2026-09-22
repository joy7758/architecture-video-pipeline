import hashlib
import importlib.util
import json
import os
import stat
import sys
import tempfile
import time
import unittest
from pathlib import Path


DBA_ROOT = Path(__file__).resolve().parents[3]
CAPTURE_PATH = (
    DBA_ROOT / "TITMAS" / "agent-native" / "customer-cycle" / "response_capture.py"
)
SCHEMA_PATH = (
    DBA_ROOT
    / "TITMAS"
    / "agent-native"
    / "customer-cycle"
    / "response-capture-envelope.schema.json"
)
HARNESS_PATH = DBA_ROOT / "TITMAS" / "conformance" / "harness.py"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CAPTURE = _load("titmas_response_capture", CAPTURE_PATH)
HARNESS = _load("titmas_conformance_harness_for_capture", HARNESS_PATH)


class ResponseCaptureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.capture_directory = Path(self.temporary.name) / "capture"
        self.capture_directory.mkdir()
        self.request = {
            "model": "qwen3.7-max",
            "messages": [{"role": "user", "content": "synthetic public-only request"}],
            "temperature": 0,
            "stream": False,
        }
        self.contract = {
            "type": "DISCOVERY",
            "required_fields": ["result"],
        }

    def tearDown(self):
        self.temporary.cleanup()

    def capture(self, provider, **kwargs):
        return CAPTURE.capture_response(
            provider="SYNTHETIC_PROVIDER",
            request=self.request,
            request_contract=self.contract,
            required_contract_fields=["result"],
            capture_directory=self.capture_directory,
            schema_path=SCHEMA_PATH,
            transport=provider,
            attempt_id=kwargs.pop("attempt_id", None),
            **kwargs,
        )

    def assert_schema(self, envelope):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        HARNESS.validate_schema(envelope, schema)
        self.assertFalse(envelope["raw_prompt_retained"])
        self.assertFalse(envelope["raw_response_retained"])
        self.assertFalse(envelope["hidden_reasoning_retained"])
        self.assertFalse(envelope["credential_material_retained"])

    def test_rc01_normal_success_response(self):
        provider = CAPTURE.FakeProvider(
            returned_model="qwen3.7-max",
            json_body={
                "model": "qwen3.7-max",
                "result": "PASS",
                "finish_reason": "stop",
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 4,
                    "total_tokens": 14,
                },
            },
        )
        result = self.capture(provider, attempt_id="rc-01")
        self.assertEqual("FINALIZED_SUCCESS", result.envelope["state"])
        self.assertEqual("VALID_RESPONSE", result.envelope["outcome_classification"])
        self.assertEqual("MATCH", result.envelope["model_identity_status"])
        self.assertEqual("PASS", result.envelope["contract_validation_status"])
        self.assertEqual(14, result.envelope["usage_total_tokens"])
        self.assertTrue(result.request_sent)
        self.assertEqual(1, provider.calls)
        self.assertFalse(result.spool_path.exists())
        self.assertEqual(
            stat.S_IMODE(result.envelope_path.stat().st_mode),
            0o600,
        )
        self.assert_schema(result.envelope)

    def test_rc02_empty_body_is_not_abstention(self):
        provider = CAPTURE.FakeProvider(
            returned_model="qwen3.7-max",
            empty_body=True,
        )
        result = self.capture(provider, attempt_id="rc-02")
        self.assertEqual("FAILED_EMPTY_BODY", result.envelope["state"])
        self.assertEqual(0, result.envelope["response_body_length"])
        self.assertEqual(hashlib.sha256(b"").hexdigest(), result.envelope["response_body_sha256"])
        self.assertEqual(CAPTURE.NEW_DECISION_REQUIRED, result.envelope["retry_eligibility"])
        self.assertNotIn("abstention", json.dumps(result.envelope).lower())
        self.assertFalse(result.spool_path.exists())
        self.assert_schema(result.envelope)

    def test_rc03_truncated_json_preserves_hash_and_length(self):
        provider = CAPTURE.FakeProvider(
            returned_model="qwen3.7-max",
            json_body={"model": "qwen3.7-max", "result": "PASS", "padding": "abcdefgh"},
            truncate_body=True,
        )
        expected = provider.response.body
        result = self.capture(provider, attempt_id="rc-03")
        self.assertEqual("FAILED_TRUNCATED_BODY", result.envelope["state"])
        self.assertEqual(len(expected), result.envelope["response_body_length"])
        self.assertEqual(hashlib.sha256(expected).hexdigest(), result.envelope["response_body_sha256"])
        self.assertFalse(result.spool_path.exists())
        self.assert_schema(result.envelope)

    def test_rc04_http_400_response_is_captured(self):
        provider = CAPTURE.FakeProvider(
            status=400,
            request_id="rc-04-request",
            returned_model=None,
            json_body={"error": {"code": "invalid_parameter"}},
        )
        result = self.capture(provider, attempt_id="rc-04")
        self.assertEqual("FAILED_HTTP_RESPONSE_CAPTURED", result.envelope["state"])
        self.assertEqual(
            "PROVIDER_HTTP_FAILURE_WITH_RESPONSE",
            result.envelope["outcome_classification"],
        )
        self.assertEqual("rc-04-request", result.envelope["request_id"])
        self.assertTrue(result.envelope["response_body_sha256"])
        self.assertFalse(result.spool_path.exists())
        self.assert_schema(result.envelope)

    def test_rc05_http_500_response_is_captured(self):
        provider = CAPTURE.FakeProvider(
            status=500,
            request_id="rc-05-request",
            json_body={"error": {"code": "server_error"}},
        )
        result = self.capture(provider, attempt_id="rc-05")
        self.assertEqual("FAILED_HTTP_RESPONSE_CAPTURED", result.envelope["state"])
        self.assertEqual(500, result.envelope["http_status"])
        self.assertEqual(CAPTURE.NEW_DECISION_REQUIRED, result.envelope["retry_eligibility"])
        self.assert_schema(result.envelope)

    def test_rc06_failure_before_dispatch_is_safe_to_reauthorize_only_by_human(self):
        provider = CAPTURE.FakeProvider(
            returned_model="qwen3.7-max",
            json_body={"result": "PASS"},
        )
        result = self.capture(
            provider,
            attempt_id="rc-06",
            fail_before_dispatch=True,
        )
        self.assertEqual("FAILED_BEFORE_DISPATCH", result.envelope["state"])
        self.assertFalse(result.request_sent)
        self.assertEqual(0, provider.calls)
        self.assertEqual(CAPTURE.SAFE_REAUTHORIZE, result.envelope["retry_eligibility"])
        self.assert_schema(result.envelope)

    def test_rc07_post_dispatch_timeout_keeps_execution_unknown(self):
        provider = CAPTURE.FakeProvider(connection_interrupt=True)
        result = self.capture(provider, attempt_id="rc-07")
        self.assertEqual(
            "FAILED_AFTER_DISPATCH_OUTCOME_UNKNOWN",
            result.envelope["state"],
        )
        self.assertEqual(
            "POST_DISPATCH_OUTCOME_UNKNOWN",
            result.envelope["outcome_classification"],
        )
        self.assertEqual("NOT_ASSESSED", result.envelope["model_identity_status"])
        self.assertEqual(CAPTURE.NEW_DECISION_REQUIRED, result.envelope["retry_eligibility"])
        self.assertTrue(result.request_sent)
        self.assertEqual(1, provider.calls)
        self.assertNotIn("PROVIDER_NOT_EXECUTED", json.dumps(result.envelope))
        self.assert_schema(result.envelope)

    def test_rc08_missing_returned_model_fails_closed(self):
        provider = CAPTURE.FakeProvider(
            returned_model=None,
            json_body={"result": "PASS"},
        )
        result = self.capture(provider, attempt_id="rc-08")
        self.assertEqual("FAILED_MODEL_IDENTITY_MISSING", result.envelope["state"])
        self.assertEqual("MISSING", result.envelope["model_identity_status"])
        self.assertEqual(CAPTURE.NEW_DECISION_REQUIRED, result.envelope["retry_eligibility"])
        self.assert_schema(result.envelope)

    def test_rc09_model_mismatch_rejects_silent_fallback(self):
        provider = CAPTURE.FakeProvider(
            returned_model="other-model",
            json_body={"model": "other-model", "result": "PASS"},
        )
        result = self.capture(provider, attempt_id="rc-09")
        self.assertEqual("FAILED_MODEL_IDENTITY_MISMATCH", result.envelope["state"])
        self.assertEqual("MISMATCH", result.envelope["model_identity_status"])
        self.assertEqual(
            "SILENT_MODEL_FALLBACK_PROHIBITED",
            result.envelope["retry_reason"],
        )
        self.assert_schema(result.envelope)

    def test_rc10_atomic_write_failure_prevents_dispatch(self):
        provider = CAPTURE.FakeProvider(
            returned_model="qwen3.7-max",
            json_body={"result": "PASS"},
        )
        writer = CAPTURE.AtomicJSONWriter(fail_stage="replace")
        result = self.capture(
            provider,
            attempt_id="rc-10",
            writer=writer,
        )
        self.assertEqual("FAILED_ATOMIC_WRITE", result.envelope["state"])
        self.assertFalse(result.request_sent)
        self.assertEqual(0, provider.calls)
        self.assertFalse(result.envelope_path.exists())
        self.assertFalse(result.spool_path.exists())

    def test_rc11_crash_after_body_is_recoverable_without_retry(self):
        provider = CAPTURE.FakeProvider(
            returned_model="qwen3.7-max",
            json_body={"model": "qwen3.7-max", "result": "PASS"},
            crash_after_body=True,
        )
        with self.assertRaises(CAPTURE.InjectedProcessCrash) as caught:
            self.capture(provider, attempt_id="rc-11")
        crash = caught.exception
        self.assertTrue(crash.envelope_path.exists())
        self.assertTrue(crash.spool_path.exists())
        self.assertEqual(0o600, stat.S_IMODE(crash.spool_path.stat().st_mode))
        recovered = CAPTURE.recover_interrupted_capture(
            crash.envelope_path,
            crash.spool_path,
        )
        self.assertEqual("FAILED_RECOVERY_REQUIRED", recovered.envelope["state"])
        self.assertTrue(recovered.envelope["response_body_sha256"])
        self.assertGreater(recovered.envelope["response_body_length"], 0)
        self.assertEqual("qwen3.7-max", recovered.envelope["returned_model"])
        self.assertEqual(CAPTURE.NEW_DECISION_REQUIRED, recovered.envelope["retry_eligibility"])
        self.assertTrue(recovered.spool_path.exists())
        self.assert_schema(recovered.envelope)
        CAPTURE.cleanup_spool(recovered.spool_path)
        self.assertFalse(recovered.spool_path.exists())

    def test_rc12_success_cleanup_has_no_secret_or_private_path(self):
        preflight = CAPTURE.request_shape_preflight(
            self.request,
            capture_directory=self.capture_directory,
            schema_path=SCHEMA_PATH,
        )
        self.assertEqual("PASS", preflight["request_shape_preflight"])
        self.assertEqual("PASS", preflight["capture_destination_preflight"])
        self.assertFalse(preflight["network_dispatch_performed"])
        provider = CAPTURE.FakeProvider(
            headers={"x-public-fixture": "rc-12"},
            returned_model="qwen3.7-max",
            json_body={"model": "qwen3.7-max", "result": "PASS"},
        )
        result = self.capture(provider, attempt_id="rc-12")
        self.assertFalse(result.spool_path.exists())
        rendered = result.envelope_path.read_text(encoding="utf-8")
        self.assertNotIn("Authorization", rendered)
        self.assertNotIn("Bearer ", rendered)
        self.assertNotIn("/Users/", rendered)
        self.assertNotIn(str(self.capture_directory), rendered)
        self.assert_schema(result.envelope)
        git_root = Path(self.temporary.name) / "synthetic-repository"
        (git_root / ".git").mkdir(parents=True)
        in_repo_capture = git_root / "capture"
        in_repo_capture.mkdir()
        rejected = CAPTURE.request_shape_preflight(
            self.request,
            capture_directory=in_repo_capture,
            schema_path=SCHEMA_PATH,
        )
        self.assertEqual("FAIL", rejected["capture_destination_preflight"])
        self.assertIn("CAPTURE_DIRECTORY_INSIDE_GIT_WORKTREE", rejected["errors"])

    def test_request_shape_preflight_rejects_unsupported_optional_parameter(self):
        request = dict(self.request)
        request["response_format"] = {"type": "json_object"}
        result = CAPTURE.request_shape_preflight(
            request,
            capture_directory=self.capture_directory,
            schema_path=SCHEMA_PATH,
        )
        self.assertEqual("FAIL", result["request_shape_preflight"])
        self.assertTrue(
            any(item.startswith("UNSUPPORTED_REQUEST_FIELDS") for item in result["errors"])
        )
        self.assertFalse(result["network_dispatch_performed"])

    def test_request_shape_preflight_rejects_malformed_messages(self):
        request = {"model": "qwen3.7-max", "messages": [{"role": "user"}]}
        result = CAPTURE.request_shape_preflight(
            request,
            capture_directory=self.capture_directory,
            schema_path=SCHEMA_PATH,
        )
        self.assertEqual("FAIL", result["request_shape_preflight"])
        self.assertIn("MESSAGE_SHAPE_INVALID", result["errors"])
        self.assertFalse(result["network_dispatch_performed"])

    def test_fake_provider_supports_headers_interrupt_and_delay(self):
        provider = CAPTURE.FakeProvider(
            status=200,
            request_id="headers-only",
            returned_model="qwen3.7-max",
            json_body={"result": "PASS"},
            delay_seconds=0.001,
            interrupt_after_headers=True,
        )
        started = time.monotonic()
        result = self.capture(provider, attempt_id="headers-interrupt")
        self.assertGreaterEqual(time.monotonic() - started, 0.001)
        self.assertEqual("headers-only", result.envelope["request_id"])
        self.assertEqual(
            "FAILED_AFTER_DISPATCH_OUTCOME_UNKNOWN",
            result.envelope["state"],
        )
        self.assert_schema(result.envelope)

    def test_cycle_001_replay_preserves_unknown_after_send(self):
        result = CAPTURE.replay_cycle_001_failure(
            capture_directory=self.capture_directory,
            schema_path=SCHEMA_PATH,
        )
        self.assertEqual(
            "FAILED_AFTER_DISPATCH_OUTCOME_UNKNOWN",
            result.envelope["state"],
        )
        self.assertEqual(
            "POST_DISPATCH_OUTCOME_UNKNOWN",
            result.envelope["outcome_classification"],
        )
        self.assertEqual("NOT_ASSESSED", result.envelope["model_identity_status"])
        self.assertEqual(CAPTURE.NEW_DECISION_REQUIRED, result.envelope["retry_eligibility"])
        rendered = json.dumps(result.envelope)
        for forbidden in (
            "AGENT_DISCOVERY_FAILURE",
            "MODEL_REJECTION",
            "VALID_ABSTENTION",
            "PROVIDER_NOT_EXECUTED",
        ):
            self.assertNotIn(forbidden, rendered)
        self.assert_schema(result.envelope)


if __name__ == "__main__":
    unittest.main()
