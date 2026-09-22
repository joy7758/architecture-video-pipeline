#!/usr/bin/env python3
"""Minimal non-core Python client for the TITMAS private Stage 5 Sandbox."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


SCHEMA_FILES = {
    "SPECIFICATION_PROPOSAL": "specification-proposal.schema.json",
    "ADAPTER_MAPPING": "adapter-mapping.schema.json",
    "TEST_VECTOR": "test-vector.schema.json",
    "REVIEW": "review.schema.json",
}


@dataclass(frozen=True)
class TITMASClientError(RuntimeError):
    status: int
    code: str
    message: str
    retry_advice: str

    def __str__(self) -> str:
        return f"{self.status} {self.code}: {self.message}"


def _preflight(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    expected = schema.get("type")
    expected_types = {
        "object": dict,
        "array": list,
        "string": str,
        "boolean": bool,
        "integer": int,
    }
    if expected in expected_types and not isinstance(value, expected_types[expected]):
        raise ValueError(f"{path}: expected {expected}")
    if expected == "integer" and isinstance(value, bool):
        raise ValueError(f"{path}: boolean is not integer")
    if "const" in schema and value != schema["const"]:
        raise ValueError(f"{path}: constant mismatch")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{path}: unsupported enum value")
    if isinstance(value, dict):
        missing = [key for key in schema.get("required", []) if key not in value]
        if missing:
            raise ValueError(f"{path}: missing required fields {missing}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise ValueError(f"{path}: additional fields {extra}")
        for key, child in properties.items():
            if key in value:
                _preflight(value[key], child, f"{path}.{key}")
    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(value):
            _preflight(item, schema["items"], f"{path}[{index}]")


class Stage5Client:
    """Request-only client; it owns no Conformance or retry executor."""

    def __init__(
        self,
        endpoint: str,
        token: str,
        schema_directory: Path,
        *,
        timeout_seconds: float = 3.0,
        transport: Callable[..., tuple[int, dict[str, Any]]] | None = None,
    ):
        if not endpoint.startswith("http://127.0.0.1:"):
            raise ValueError("Stage 5 SDK accepts loopback endpoints only")
        if not token:
            raise ValueError("Sandbox Key is required")
        self.endpoint = endpoint.rstrip("/")
        self._token = token
        self.schema_directory = schema_directory.resolve()
        self.timeout_seconds = timeout_seconds
        self._transport = transport

    def _schema(self, contribution_type: str) -> dict[str, Any]:
        name = SCHEMA_FILES[contribution_type]
        return json.loads(
            (self.schema_directory / name).read_text(encoding="utf-8")
        )

    def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self._transport is not None:
            status, response = self._transport(method, path, payload, self._token)
        else:
            body = None
            headers = {"Authorization": f"Bearer {self._token}"}
            if payload is not None:
                body = json.dumps(payload, sort_keys=True).encode("utf-8")
                headers["Content-Type"] = "application/json"
            request = urllib.request.Request(
                f"{self.endpoint}{path}",
                data=body,
                headers=headers,
                method=method,
            )
            try:
                with urllib.request.urlopen(
                    request, timeout=self.timeout_seconds
                ) as response_handle:
                    status = response_handle.status
                    response = json.loads(response_handle.read())
            except urllib.error.HTTPError as exc:
                try:
                    status = exc.code
                    response = json.loads(exc.read())
                finally:
                    exc.close()
        if 200 <= status < 300:
            if not isinstance(response, dict):
                raise TITMASClientError(
                    status, "TITMAS-STAGE5-MALFORMED-RESPONSE",
                    "Sandbox response is not an object.", "DO_NOT_RETRY"
                )
            return response
        error = response.get("error", {}) if isinstance(response, dict) else {}
        advice = {
            401: "REAUTHORIZE_WITH_NEW_EPHEMERAL_KEY",
            403: "REQUEST_HUMAN_SCOPE_REVIEW",
            409: "REFRESH_SUBMISSION_STATE",
            422: "REVISE_CONTRIBUTION",
            429: "NO_AUTOMATIC_RETRY_REQUEST_NEW_SESSION",
            500: "NO_AUTOMATIC_RETRY_ESCALATE",
        }.get(status, "DO_NOT_RETRY")
        raise TITMASClientError(
            status,
            str(error.get("code", "TITMAS-STAGE5-UNKNOWN-ERROR")),
            str(error.get("message", "Sandbox request failed.")),
            advice,
        )

    def get_standard_catalog(self) -> dict[str, Any]:
        return self._request("GET", "/v1/standards/catalog")

    def get_tasks(self) -> dict[str, Any]:
        return self._request("GET", "/v1/standards/tasks")

    def _submit(
        self,
        contribution_type: str,
        route: str,
        contribution: dict[str, Any],
    ) -> dict[str, Any]:
        _preflight(contribution, self._schema(contribution_type))
        return self._request("POST", route, {"contribution": contribution})

    def submit_proposal(self, contribution: dict[str, Any]) -> dict[str, Any]:
        return self._submit(
            "SPECIFICATION_PROPOSAL",
            "/v1/contributions/proposals",
            contribution,
        )

    def submit_adapter_mapping(
        self, contribution: dict[str, Any]
    ) -> dict[str, Any]:
        return self._submit(
            "ADAPTER_MAPPING",
            "/v1/contributions/adapters",
            contribution,
        )

    def submit_test_vector(
        self, contribution: dict[str, Any]
    ) -> dict[str, Any]:
        return self._submit(
            "TEST_VECTOR",
            "/v1/contributions/test-vectors",
            contribution,
        )

    def validate_submission(self, submission_id: str) -> dict[str, Any]:
        return self._request(
            "POST", f"/v1/contributions/{submission_id}/validate", {}
        )

    def get_submission_status(self, submission_id: str) -> dict[str, Any]:
        return self._request("GET", f"/v1/contributions/{submission_id}")

    def get_submission_result(self, submission_id: str) -> dict[str, Any]:
        return self._request("GET", f"/v1/contributions/{submission_id}/result")

    def submit_review(
        self,
        submission_id: str,
        review: dict[str, Any],
    ) -> dict[str, Any]:
        _preflight(review, self._schema("REVIEW"))
        return self._request(
            "POST",
            f"/v1/contributions/{submission_id}/reviews",
            {"review": review},
        )
