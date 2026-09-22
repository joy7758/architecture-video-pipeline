#!/usr/bin/env python3
"""Stage 5 loopback Gateway, scope and SDK integration tests."""

from __future__ import annotations

import importlib.util
import json
import sys
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path


GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[4]
SDK_PATH = (
    PROJECT_ROOT / "TITMAS" / "private-stage5-sdk" / "python"
    / "titmas_stage5_sdk.py"
)
sys.path.insert(0, str(GATEWAY_ROOT))
import stage5_service  # noqa: E402
import stage5_workspace  # noqa: E402

SDK_SPEC = importlib.util.spec_from_file_location("stage5_gateway_sdk", SDK_PATH)
assert SDK_SPEC and SDK_SPEC.loader
SDK = importlib.util.module_from_spec(SDK_SPEC)
sys.modules[SDK_SPEC.name] = SDK
SDK_SPEC.loader.exec_module(SDK)


class FixedIds:
    def __init__(self) -> None:
        self.index = 0

    def __call__(self) -> str:
        self.index += 1
        return f"stage5-submission-TEST-{self.index:02d}"


def examples() -> dict:
    return json.loads(
        (
            PROJECT_ROOT / "TITMAS" / "private-stage5-protocol-surface"
            / "synthetic-examples.json"
        ).read_text(encoding="utf-8")
    )


class Stage5GatewayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = stage5_service.ContributionStore(id_factory=FixedIds())
        self.gateway = stage5_service.Stage5GatewayService(
            PROJECT_ROOT, store=self.store
        )
        self.endpoint = self.gateway.start()
        self.client = SDK.Stage5Client(
            self.endpoint,
            self.gateway.customer_token,
            self.gateway.stage5_assets["protocol_surface"] / "schemas",
        )

    def tearDown(self) -> None:
        self.gateway.stop()

    def raw_request(self, path: str, token: str) -> int:
        request = urllib.request.Request(
            f"{self.endpoint}{path}",
            headers={"Authorization": f"Bearer {token}"},
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status
        except urllib.error.HTTPError as exc:
            try:
                return exc.code
            finally:
                exc.close()

    def test_catalog_and_tasks(self) -> None:
        self.assertTrue(self.client.get_standard_catalog()["specifications"])
        self.assertTrue(self.client.get_tasks()["tasks"])

    def test_valid_proposal_conformance(self) -> None:
        received = self.client.submit_proposal(examples()["specification_proposal"])
        result = self.client.validate_submission(received["submission_id"])
        self.assertEqual("CONFORMANCE_PASS", result["conformance_status"])
        self.assertEqual("HUMAN_DISPOSITION_REQUIRED", result["status"])

    def test_valid_adapter_conformance(self) -> None:
        received = self.client.submit_adapter_mapping(examples()["adapter_mapping"])
        result = self.client.validate_submission(received["submission_id"])
        self.assertEqual("CONFORMANCE_PASS", result["conformance_status"])

    def test_semantically_invalid_vector_fails(self) -> None:
        value = examples()["test_vector"]
        value["failure_classification"] = "NONE"
        received = self.client.submit_test_vector(value)
        with self.assertRaises(SDK.TITMASClientError) as caught:
            self.client.validate_submission(received["submission_id"])
        self.assertEqual(422, caught.exception.status)
        status = self.client.get_submission_status(received["submission_id"])
        self.assertEqual("CONFORMANCE_FAIL", status["status"])

    def test_missing_scope_is_403(self) -> None:
        restricted = stage5_service.Stage5GatewayService(
            PROJECT_ROOT,
            scopes=("standards:read",),
            store=self.store,
        )
        endpoint = restricted.start()
        client = SDK.Stage5Client(
            endpoint,
            restricted.customer_token,
            restricted.stage5_assets["protocol_surface"] / "schemas",
        )
        try:
            with self.assertRaises(SDK.TITMASClientError) as caught:
                client.get_tasks()
            self.assertEqual(403, caught.exception.status)
        finally:
            restricted.stop()

    def test_expired_key_is_401(self) -> None:
        self.gateway.session.expires_at = time.monotonic() - 1
        self.assertEqual(401, self.raw_request("/v1/standards/catalog", self.gateway.customer_token))

    def test_non_loopback_host_rejected(self) -> None:
        with self.assertRaises(ValueError):
            stage5_service.Stage5GatewayService(
                PROJECT_ROOT, host="0.0.0.0"
            )

    def test_key_metadata_contains_no_plaintext(self) -> None:
        metadata = json.loads(
            (
                self.gateway.workspaces.customer_root / "stage5-session.json"
            ).read_text(encoding="utf-8")
        )
        rendered = json.dumps(metadata)
        self.assertNotIn(self.gateway.customer_token, rendered)
        self.assertFalse(metadata["token_persisted"])
        self.assertTrue(metadata["key_binding"]["sandbox_key_ephemeral"])

    def test_customer_assets_have_no_core_disclosure(self) -> None:
        findings = stage5_workspace.inspect_stage5_customer_assets(
            self.gateway.stage5_assets["protocol_surface"],
            self.gateway.stage5_assets["sdk"],
        )
        self.assertEqual(0, sum(findings.values()))

    def test_prohibited_scope_rejected(self) -> None:
        with self.assertRaises(ValueError):
            stage5_service.Stage5GatewayService(
                PROJECT_ROOT, scopes=("admin",)
            )


if __name__ == "__main__":
    unittest.main()
