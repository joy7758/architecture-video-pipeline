#!/usr/bin/env python3
"""EG-01 through EG-16 for the local private evaluation gateway."""

from __future__ import annotations

import json
import socket
import sys
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path


GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(GATEWAY_ROOT))

import fake_customer  # noqa: E402
import service  # noqa: E402
import workspace  # noqa: E402


FORBIDDEN_RESPONSE_MARKERS = (
    "/Users/",
    "/private/tmp/",
    "Traceback",
    "RuntimeError",
    "_dispatch",
    "_force_internal_failure",
    "Authorization",
    "Bearer ",
    "DASHSCOPE",
    "QIANFAN",
    "OPENAI_API_KEY",
)


class PrivateEvaluationGatewayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.gateway = service.GatewayService(PROJECT_ROOT)
        self.endpoint = self.gateway.start()

    def tearDown(self) -> None:
        self.gateway.stop()

    def request(
        self,
        path: str,
        *,
        payload: dict | None = None,
        raw_body: bytes | None = None,
        token: str | None = "VALID",
        method: str | None = None,
        content_length: int | None = None,
    ) -> tuple[int, dict, str]:
        if token == "VALID":
            token = self.gateway.customer_token
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        data = raw_body
        if payload is not None:
            data = json.dumps(payload, sort_keys=True).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if content_length is not None:
            headers["Content-Length"] = str(content_length)
        request = urllib.request.Request(
            f"{self.endpoint}{path}",
            data=data,
            headers=headers,
            method=method or ("POST" if data is not None else "GET"),
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                rendered = response.read().decode("utf-8")
                return response.status, json.loads(rendered), rendered
        except urllib.error.HTTPError as exc:
            try:
                rendered = exc.read().decode("utf-8")
                return exc.code, json.loads(rendered), rendered
            finally:
                exc.close()

    def assert_sanitized(self, rendered: str) -> None:
        for marker in FORBIDDEN_RESPONSE_MARKERS:
            self.assertNotIn(marker, rendered)

    def valid_evaluation(self) -> dict:
        return {
            "synthetic_request_id": "EG-SYNTHETIC-001",
            "declared_object": {"kind": "synthetic-agent-candidate"},
            "declared_profile": service.SYNTHETIC_PROFILE,
            "contract_version": service.CONTRACT_VERSION,
            "options": {"include_limitations": True},
        }

    def test_eg01_health(self) -> None:
        status, payload, rendered = self.request("/health")
        self.assertEqual(200, status)
        self.assertEqual(
            {
                "status": "ready",
                "mode": "private-evaluation",
                "maturity": "development",
            },
            payload,
        )
        self.assert_sanitized(rendered)

    def test_eg02_capabilities(self) -> None:
        status, payload, rendered = self.request("/v1/capabilities")
        self.assertEqual(200, status)
        self.assertEqual(list(service.CAPABILITIES), payload["capabilities"])
        self.assertEqual({"contract_version", "capabilities"}, set(payload))
        error_contract = json.loads(
            (
                self.gateway.workspaces.customer_bundle / "error-codes.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(set(service.ERRORS.values()), set(error_contract["errors"]))
        self.assert_sanitized(rendered)

    def test_eg03_valid_synthetic_evaluation(self) -> None:
        result = fake_customer.run_fake_customer(
            token=self.gateway.customer_token,
            customer_workspace=self.gateway.workspaces.customer_root,
        )
        self.assertEqual("PASS", result["FAKE_CUSTOMER_DISCOVERY"])
        self.assertEqual("PASS", result["FAKE_CUSTOMER_VALID_CALL"])
        self.assertEqual("PASS", result["FAKE_CUSTOMER_INVALID_CALL_HANDLED"])
        self.assertFalse(result["FAKE_CUSTOMER_CORE_ACCESS"])
        status, payload, _ = self.request(
            "/v1/verify",
            payload={
                "verification_object": {"contract_conformant": True},
                "expected_contract_version": service.CONTRACT_VERSION,
            },
        )
        self.assertEqual(200, status)
        self.assertEqual("PASS", payload["verification_result"])

    def test_eg04_invalid_token(self) -> None:
        status, payload, rendered = self.request("/health", token="invalid")
        self.assertEqual(401, status)
        self.assertEqual(service.ERRORS[401], payload["error"]["code"])
        self.assert_sanitized(rendered)

    def test_eg05_missing_token(self) -> None:
        status, payload, rendered = self.request("/v1/capabilities", token=None)
        self.assertEqual(401, status)
        self.assertEqual(service.ERRORS[401], payload["error"]["code"])
        self.assert_sanitized(rendered)

    def test_eg06_forbidden_operation(self) -> None:
        status, payload, rendered = self.request(
            "/v1/admin",
            payload={"action": "expand-scope"},
        )
        self.assertEqual(403, status)
        self.assertEqual(service.ERRORS[403], payload["error"]["code"])
        self.assert_sanitized(rendered)

    def test_eg07_malformed_json(self) -> None:
        status, payload, rendered = self.request(
            "/v1/evaluate",
            raw_body=b"{not-json",
        )
        self.assertEqual(400, status)
        self.assertEqual(service.ERRORS[400], payload["error"]["code"])
        self.assert_sanitized(rendered)

    def test_eg08_oversized_request(self) -> None:
        status, payload, rendered = self.request(
            "/v1/evaluate",
            raw_body=b"{}",
            content_length=service.MAX_REQUEST_BYTES + 1,
        )
        self.assertEqual(413, status)
        self.assertEqual(service.ERRORS[413], payload["error"]["code"])
        self.assert_sanitized(rendered)

    def test_eg09_unknown_contract_version(self) -> None:
        request = self.valid_evaluation()
        request["contract_version"] = "999.0.0"
        status, payload, rendered = self.request("/v1/evaluate", payload=request)
        self.assertEqual(409, status)
        self.assertEqual(service.ERRORS[409], payload["error"]["code"])
        self.assert_sanitized(rendered)

    def test_eg10_unknown_profile(self) -> None:
        request = self.valid_evaluation()
        request["declared_profile"] = "UNKNOWN"
        status, payload, rendered = self.request("/v1/evaluate", payload=request)
        self.assertEqual(404, status)
        self.assertEqual(service.ERRORS[404], payload["error"]["code"])
        self.assert_sanitized(rendered)
        request = self.valid_evaluation()
        request["declared_object"] = {}
        status, payload, rendered = self.request("/v1/evaluate", payload=request)
        self.assertEqual(422, status)
        self.assertEqual(service.ERRORS[422], payload["error"]["code"])
        self.assert_sanitized(rendered)

    def test_eg11_internal_exception_sanitization(self) -> None:
        self.gateway._force_internal_failure = True
        status, payload, rendered = self.request("/v1/evaluate", payload={})
        self.assertEqual(500, status)
        self.assertEqual(service.ERRORS[500], payload["error"]["code"])
        self.assert_sanitized(rendered)

    def test_eg12_session_expiry(self) -> None:
        self.gateway.session.max_requests = 0
        status, payload, _ = self.request("/health")
        self.assertEqual(429, status)
        self.assertEqual(service.ERRORS[429], payload["error"]["code"])
        self.gateway.session.max_requests = 32
        self.gateway.session.expires_at = time.monotonic() - 1
        status, payload, rendered = self.request("/health")
        self.assertEqual(401, status)
        self.assertEqual(service.ERRORS[401], payload["error"]["code"])
        self.assert_sanitized(rendered)

    def test_eg13_loopback_binding(self) -> None:
        self.assertEqual(service.LOOPBACK_HOST, self.gateway.bound_address[0])
        with self.assertRaises(ValueError):
            service.GatewayService(PROJECT_ROOT, host="0.0.0.0")

    def test_eg14_customer_workspace_isolation(self) -> None:
        counts = workspace.inspect_customer_workspace(
            self.gateway.workspaces.customer_root
        )
        self.assertEqual(
            {
                "CUSTOMER_WORKSPACE_CORE_SOURCE_COUNT": 0,
                "CUSTOMER_WORKSPACE_INTERNAL_TEST_COUNT": 0,
                "CUSTOMER_WORKSPACE_GIT_METADATA_COUNT": 0,
                "CUSTOMER_WORKSPACE_PRIVATE_PATH_COUNT": 0,
            },
            counts,
        )
        copied = {
            path.name
            for path in self.gateway.workspaces.customer_bundle.iterdir()
            if path.is_file()
        }
        self.assertEqual(set(workspace.CUSTOMER_BUNDLE_FILES), copied)
        self.assertFalse(
            (self.gateway.workspaces.customer_bundle / "gateway").exists()
        )

    def test_eg15_response_capture(self) -> None:
        self.request("/health")
        self.request("/v1/evaluate", raw_body=b"{not-json")
        envelopes = sorted(
            self.gateway.workspaces.capture_directory.glob("*.envelope.json")
        )
        self.assertEqual(2, len(envelopes))
        for path in envelopes:
            envelope = json.loads(path.read_text(encoding="utf-8"))
            for field in (
                "attempt_id",
                "customer_session_id",
                "requested_operation",
                "request_contract_sha256",
                "request_body_sha256",
                "dispatch_started_at",
                "response_status",
                "response_body_sha256",
                "final_state",
            ):
                self.assertIn(field, envelope)
            self.assertEqual(
                self.gateway.session.customer_session_id,
                envelope["customer_session_id"],
            )
            self.assertTrue(envelope["response_body_sha256"])
            self.assertNotIn(self.gateway.customer_token, json.dumps(envelope))
        for root in (
            self.gateway.workspaces.core_root,
            self.gateway.workspaces.customer_root,
        ):
            for path in root.rglob("*"):
                if path.is_file():
                    self.assertNotIn(
                        self.gateway.customer_token,
                        path.read_text(encoding="utf-8"),
                    )

    def test_eg16_shutdown_cleanup(self) -> None:
        self.request("/health")
        token = self.gateway.customer_token
        core_root = self.gateway.workspaces.core_root
        customer_root = self.gateway.workspaces.customer_root
        host, port = self.gateway.bound_address
        self.gateway.stop()
        self.assertIsNone(self.gateway.session.token)
        self.assertTrue(self.gateway.session.revoked)
        self.assertNotIn(token, json.dumps(self.gateway.audit_log))
        self.assertFalse(core_root.exists())
        self.assertFalse(customer_root.exists())
        with self.assertRaises(OSError):
            socket.create_connection((host, port), timeout=0.1)


if __name__ == "__main__":
    unittest.main()
