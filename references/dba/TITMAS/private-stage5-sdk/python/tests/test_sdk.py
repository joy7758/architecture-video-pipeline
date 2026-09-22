#!/usr/bin/env python3
"""Minimal Stage 5 Python SDK unit tests."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SDK_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_ROOT = PROJECT_ROOT / "TITMAS" / "private-stage5-protocol-surface" / "schemas"
SPEC = importlib.util.spec_from_file_location(
    "titmas_stage5_sdk_tested", SDK_ROOT / "titmas_stage5_sdk.py"
)
assert SPEC and SPEC.loader
SDK = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SDK
SPEC.loader.exec_module(SDK)


class SDKTests(unittest.TestCase):
    def client(self, transport):
        return SDK.Stage5Client(
            "http://127.0.0.1:12345",
            "synthetic-in-memory-key",
            SCHEMA_ROOT,
            transport=transport,
        )

    def test_catalog_request(self) -> None:
        seen = []

        def transport(method, path, payload, token):
            seen.append((method, path, payload, token))
            return 200, {"specifications": []}

        result = self.client(transport).get_standard_catalog()
        self.assertEqual([], result["specifications"])
        self.assertEqual("GET", seen[0][0])

    def test_schema_preflight_blocks_extra_field_before_transport(self) -> None:
        called = False

        def transport(*args):
            nonlocal called
            called = True
            return 200, {}

        with self.assertRaises(ValueError):
            self.client(transport).submit_test_vector({"unexpected": True})
        self.assertFalse(called)

    def test_403_is_not_retried(self) -> None:
        calls = 0

        def transport(*args):
            nonlocal calls
            calls += 1
            return 403, {
                "error": {
                    "code": "TITMAS-STAGE5-403-SCOPE-DENIED",
                    "message": "Scope denied.",
                }
            }

        with self.assertRaises(SDK.TITMASClientError) as caught:
            self.client(transport).get_tasks()
        self.assertEqual("REQUEST_HUMAN_SCOPE_REVIEW", caught.exception.retry_advice)
        self.assertEqual(1, calls)

    def test_non_loopback_endpoint_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            SDK.Stage5Client(
                "https://example.invalid",
                "synthetic",
                SCHEMA_ROOT,
            )


if __name__ == "__main__":
    unittest.main()
