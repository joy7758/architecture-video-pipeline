"""Thin Dify Cloud Workflow adapter for private R2A smoke use."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Mapping

from . import (
    R2AContractError,
    R2ATransportError,
    Transport,
    TransportResult,
    canonical_json_bytes,
    existing_evidence_reference,
    sha256_value,
    validate_event,
    validate_request,
)


MAX_RESPONSE_BYTES = 1_000_000
CONSERVATIVE_TOKEN_PRICE_CNY_PER_MILLION = 36.0


def _default_transport(
    url: str,
    headers: Mapping[str, str],
    payload: dict[str, Any],
    timeout_seconds: float,
) -> TransportResult:
    request = urllib.request.Request(
        url,
        data=canonical_json_bytes(payload),
        headers=dict(headers),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            status_code = int(response.status)
    except urllib.error.HTTPError as exc:
        raw = exc.read(MAX_RESPONSE_BYTES + 1)
        status_code = int(exc.code)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise R2ATransportError("Dify provider transport failed") from exc
    if len(raw) > MAX_RESPONSE_BYTES:
        raise R2ATransportError("Dify provider response exceeded the bounded size")
    try:
        body = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise R2ATransportError("Dify provider returned invalid JSON") from exc
    if not isinstance(body, dict):
        raise R2ATransportError("Dify provider response was not an object")
    return TransportResult(status_code=status_code, body=body)


def _output_text(outputs: Any) -> str:
    if not isinstance(outputs, dict):
        return ""
    for key in ("result", "output_text", "text"):
        if isinstance(outputs.get(key), str):
            return outputs[key]
    return ""


class DifyWorkflowAdapter:
    """One-attempt adapter for a published Dify Workflow application."""

    route_id = "route_b_dify_cloud_workflow"
    provider = "DIFY_CLOUD"

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        timeout_seconds: float = 100.0,
        transport: Transport | None = None,
    ) -> None:
        if not api_key or not base_url:
            raise R2AContractError("Dify credential or base URL is missing")
        if not base_url.startswith("https://"):
            raise R2AContractError("Dify base URL must use HTTPS")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._transport = transport or _default_transport

    def invoke(self, request: dict[str, Any]) -> dict[str, Any]:
        validate_request(request)
        payload = {
            "inputs": request["input_variables"],
            "response_mode": "blocking",
            "user": "titmas-r2a-synthetic",
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        started = time.monotonic()
        result = self._transport(
            f"{self._base_url}/workflows/run",
            headers,
            payload,
            self._timeout_seconds,
        )
        elapsed_ms_measured = max(0, round((time.monotonic() - started) * 1000))
        body = result.body
        data = body.get("data", {}) if isinstance(body.get("data", {}), dict) else {}
        outputs = data.get("outputs", {}) if isinstance(data.get("outputs", {}), dict) else {}
        output_text = _output_text(outputs)
        provider_status = data.get("status") if isinstance(data.get("status"), str) else ""
        success = result.status_code == 200 and provider_status == "succeeded" and bool(output_text)
        task_id = body.get("task_id") if isinstance(body.get("task_id"), str) else None
        run_id = body.get("workflow_run_id") if isinstance(body.get("workflow_run_id"), str) else None
        total_tokens = data.get("total_tokens") if isinstance(data.get("total_tokens"), int) else None
        input_tokens = outputs.get("input_tokens") if isinstance(outputs.get("input_tokens"), int) else None
        output_tokens = outputs.get("output_tokens") if isinstance(outputs.get("output_tokens"), int) else None
        if input_tokens is not None and output_tokens is not None:
            estimated_cost = round(
                input_tokens * 12.0 / 1_000_000 + output_tokens * 36.0 / 1_000_000,
                6,
            )
        elif total_tokens is not None:
            estimated_cost = round(
                total_tokens * CONSERVATIVE_TOKEN_PRICE_CNY_PER_MILLION / 1_000_000,
                6,
            )
        else:
            estimated_cost = None
        reported_model_id = (
            outputs.get("reported_model_id")
            if isinstance(outputs.get("reported_model_id"), str) and outputs["reported_model_id"]
            else None
        )
        if reported_model_id:
            model_id_source = "WORKFLOW_OUTPUT_DECLARATION"
            model_id_observability = "ALIAS_ONLY"
        else:
            model_id_source = "NONE"
            model_id_observability = "NOT_OBSERVABLE"
        elapsed_seconds = data.get("elapsed_time")
        elapsed_ms = (
            max(0, round(elapsed_seconds * 1000))
            if isinstance(elapsed_seconds, (int, float)) and not isinstance(elapsed_seconds, bool)
            else elapsed_ms_measured
        )
        not_assessed = [
            "internal_reasoning",
            "final_business_correctness",
            "node_level_events_in_blocking_mode",
            "actual_model_snapshot",
            "public_competitive_benchmark_permission",
        ]
        if input_tokens is None or output_tokens is None:
            not_assessed.append("exact_input_output_token_split")
        if estimated_cost is None:
            not_assessed.append("exact_provider_cost")
        event = {
            "route_id": self.route_id,
            "provider": self.provider,
            "configured_model_id": request["configured_model_id"],
            "reported_model_id": reported_model_id,
            "model_id_source": model_id_source,
            "model_id_observability": model_id_observability,
            "application_version": request["application_version"],
            "knowledge_base_version": request["knowledge_base_version"],
            "request_id": task_id,
            "run_id": run_id,
            "status": "SUCCEEDED" if success else "FAILED",
            "output_text": output_text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "elapsed_ms": elapsed_ms,
            "estimated_cost_cny": estimated_cost,
            "node_events": [],
            "not_assessed_fields": sorted(set(not_assessed)),
            "raw_response_sha256": sha256_value(body),
            "evidence_ref": existing_evidence_reference(
                route_id=self.route_id,
                case_id=request["case_id"],
                phase=request["phase"],
                request_digest=sha256_value(payload),
            ),
        }
        validate_event(event)
        return event


__all__ = ["DifyWorkflowAdapter"]
