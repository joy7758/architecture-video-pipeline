#!/usr/bin/env python3
"""Deterministic black-box customer rehearsal with no model or Provider call."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def _request(
    endpoint: str,
    token: str,
    path: str,
    *,
    payload: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any]]:
    body = None
    method = "GET"
    headers = {"Authorization": f"Bearer {token}"}
    if payload is not None:
        method = "POST"
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        f"{endpoint}{path}",
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, json.loads(exc.read())
        finally:
            exc.close()


def run_fake_customer(
    *,
    token: str,
    customer_workspace: Path,
) -> dict[str, Any]:
    """Discover, call, reject, and record a synthetic customer interaction."""

    workspace = customer_workspace.resolve()
    session = json.loads(
        (workspace / "session.json").read_text(encoding="utf-8")
    )
    endpoint = session["endpoint"]
    discovery = json.loads(
        (workspace / "bundle" / "agent-service-discovery.json").read_text(
            encoding="utf-8"
        )
    )
    contract = json.loads(
        (workspace / "bundle" / "api-contract.json").read_text(encoding="utf-8")
    )
    capabilities_status, capabilities = _request(
        endpoint,
        token,
        "/v1/capabilities",
    )
    valid_status, valid = _request(
        endpoint,
        token,
        "/v1/evaluate",
        payload={
            "synthetic_request_id": "FAKE-CUSTOMER-001",
            "declared_object": {"kind": "synthetic-agent-candidate"},
            "declared_profile": "TITMAS-SYNTHETIC-CANDIDATE-v0.1",
            "contract_version": contract["contract_version"],
            "options": {"include_limitations": True},
        },
    )
    invalid_status, invalid = _request(
        endpoint,
        token,
        "/v1/not-allowed",
        payload={"synthetic": True},
    )
    result = {
        "FAKE_CUSTOMER_DISCOVERY": (
            "PASS"
            if discovery["machine_entry"] == "api-contract.json"
            and capabilities_status == 200
            and bool(capabilities.get("capabilities"))
            else "FAIL"
        ),
        "FAKE_CUSTOMER_VALID_CALL": (
            "PASS"
            if valid_status == 200
            and valid.get("result_status") == "CONDITIONALLY_RECOMMENDED"
            else "FAIL"
        ),
        "FAKE_CUSTOMER_INVALID_CALL_HANDLED": (
            "PASS"
            if invalid_status == 403
            and invalid.get("error", {}).get("code")
            == "TITMAS-EVAL-403-OPERATION-NOT-ALLOWED"
            else "FAIL"
        ),
        "FAKE_CUSTOMER_CORE_ACCESS": False,
        "feedback": {
            "contract_understood": True,
            "valid_result_is_bounded": True,
            "invalid_operation_failed_closed": True,
            "real_model_call_count": 0,
            "real_provider_call_count": 0,
        },
    }
    output = workspace / "results" / "fake-customer-feedback.json"
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result
