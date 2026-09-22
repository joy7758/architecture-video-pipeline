"""Thin Alibaba Cloud Model Studio workflow adapter for private R2A smoke use."""

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


DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/api/v1/apps"
MAX_RESPONSE_BYTES = 1_000_000
INPUT_PRICE_CNY_PER_MILLION = 12.0
OUTPUT_PRICE_CNY_PER_MILLION = 36.0


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
        raise R2ATransportError("Aliyun provider transport failed") from exc
    if len(raw) > MAX_RESPONSE_BYTES:
        raise R2ATransportError("Aliyun provider response exceeded the bounded size")
    try:
        body = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise R2ATransportError("Aliyun provider returned invalid JSON") from exc
    if not isinstance(body, dict):
        raise R2ATransportError("Aliyun provider response was not an object")
    return TransportResult(status_code=status_code, body=body)


def _sanitize_workflow_message(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, dict):
        return []
    allowed = {
        "node_status",
        "node_type",
        "node_name",
        "node_is_completed",
        "node_id",
        "parent_node_id",
    }
    return [{key: value[key] for key in sorted(allowed & set(value))}]


def _token_usage(body: dict[str, Any]) -> tuple[int | None, int | None, int | None, str | None, str, str]:
    models = body.get("usage", {}).get("models", [])
    if not isinstance(models, list) or not models:
        return None, None, None, None, "NONE", "NOT_OBSERVABLE"
    valid = [item for item in models if isinstance(item, dict)]
    input_tokens = sum(item.get("input_tokens", 0) for item in valid)
    output_tokens = sum(item.get("output_tokens", 0) for item in valid)
    if not all(isinstance(item.get("input_tokens", 0), int) for item in valid):
        input_tokens = None
    if not all(isinstance(item.get("output_tokens", 0), int) for item in valid):
        output_tokens = None
    total_tokens = (
        input_tokens + output_tokens
        if input_tokens is not None and output_tokens is not None
        else None
    )
    model_ids = {
        item.get("model_id")
        for item in valid
        if isinstance(item.get("model_id"), str) and item["model_id"]
    }
    if len(model_ids) == 1:
        return input_tokens, output_tokens, total_tokens, next(iter(model_ids)), "PROVIDER_USAGE", "OBSERVABLE"
    if len(model_ids) > 1:
        return input_tokens, output_tokens, total_tokens, None, "PROVIDER_USAGE", "AMBIGUOUS"
    return input_tokens, output_tokens, total_tokens, None, "NONE", "NOT_OBSERVABLE"


class AliyunBailianWorkflowAdapter:
    """One-attempt adapter for the official DashScope application endpoint."""

    route_id = "route_a_aliyun_bailian_workflow"
    provider = "ALIBABA_CLOUD_MODEL_STUDIO"

    def __init__(
        self,
        *,
        api_key: str,
        app_id: str,
        workspace_id: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout_seconds: float = 100.0,
        transport: Transport | None = None,
    ) -> None:
        if not api_key or not app_id:
            raise R2AContractError("Aliyun credential or application configuration is missing")
        if not base_url.startswith("https://"):
            raise R2AContractError("Aliyun base URL must use HTTPS")
        self._api_key = api_key
        self._app_id = app_id
        self._workspace_id = workspace_id
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._transport = transport or _default_transport

    def invoke(self, request: dict[str, Any]) -> dict[str, Any]:
        validate_request(request)
        payload = {
            "input": {
                "prompt": request["prompt"],
                "biz_params": request["input_variables"],
            },
            "parameters": {"has_thoughts": False},
            "debug": {},
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        if self._workspace_id:
            headers["X-DashScope-WorkSpace"] = self._workspace_id
        started = time.monotonic()
        result = self._transport(
            f"{self._base_url}/{self._app_id}/completion",
            headers,
            payload,
            self._timeout_seconds,
        )
        elapsed_ms = max(0, round((time.monotonic() - started) * 1000))
        body = result.body
        output = body.get("output", {}) if isinstance(body.get("output", {}), dict) else {}
        output_text = output.get("text") if isinstance(output.get("text"), str) else ""
        success = result.status_code == 200 and bool(output_text)
        (
            input_tokens,
            output_tokens,
            total_tokens,
            reported_model_id,
            model_id_source,
            model_id_observability,
        ) = _token_usage(body)
        estimated_cost = None
        if input_tokens is not None and output_tokens is not None:
            estimated_cost = round(
                input_tokens * INPUT_PRICE_CNY_PER_MILLION / 1_000_000
                + output_tokens * OUTPUT_PRICE_CNY_PER_MILLION / 1_000_000,
                6,
            )
        request_id = body.get("request_id") if isinstance(body.get("request_id"), str) else None
        not_assessed = [
            "internal_reasoning",
            "final_business_correctness",
            "native_human_approval",
            "public_benchmark_permission",
        ]
        if model_id_observability != "OBSERVABLE":
            not_assessed.append("actual_model_snapshot")
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
            "request_id": request_id,
            "run_id": request_id,
            "status": "SUCCEEDED" if success else "FAILED",
            "output_text": output_text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "elapsed_ms": elapsed_ms,
            "estimated_cost_cny": estimated_cost,
            "node_events": _sanitize_workflow_message(output.get("workflow_message")),
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


__all__ = ["AliyunBailianWorkflowAdapter"]
