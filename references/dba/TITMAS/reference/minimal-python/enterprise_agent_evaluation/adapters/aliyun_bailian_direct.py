"""Bounded Alibaba Cloud Model Studio direct-model adapter.

The adapter makes exactly one OpenAI-compatible Model Studio request for one
synthetic evaluation case.  It is deliberately not an Agent runtime, a retry
orchestration layer, a credential store, or an Evidence authority.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from typing import Any, Mapping

from . import R2AContractError, R2ATransportError, Transport, TransportResult, canonical_json_bytes, existing_evidence_reference, sha256_value


DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MAX_RESPONSE_BYTES = 1_000_000
INPUT_PRICE_CNY_PER_MILLION = 12.0
OUTPUT_PRICE_CNY_PER_MILLION = 36.0
ALLOWED_MODELS = {"qwen3.7-max", "qwen3.7-max-2026-05-20"}
SNAPSHOT_MODEL = "qwen3.7-max-2026-05-20"


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
        raise R2ATransportError("Alibaba Cloud direct-model transport failed") from exc
    if len(raw) > MAX_RESPONSE_BYTES:
        raise R2ATransportError("Alibaba Cloud direct-model response exceeded the bounded size")
    try:
        body = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise R2ATransportError("Alibaba Cloud direct-model response was not JSON") from exc
    if not isinstance(body, dict):
        raise R2ATransportError("Alibaba Cloud direct-model response was not an object")
    return TransportResult(status_code=status_code, body=body)


def _token_usage(body: dict[str, Any]) -> tuple[int | None, int | None, int | None]:
    usage = body.get("usage")
    if not isinstance(usage, dict):
        return None, None, None
    input_tokens = usage.get("prompt_tokens")
    output_tokens = usage.get("completion_tokens")
    total_tokens = usage.get("total_tokens")
    if not isinstance(input_tokens, int) or isinstance(input_tokens, bool):
        input_tokens = None
    if not isinstance(output_tokens, int) or isinstance(output_tokens, bool):
        output_tokens = None
    if not isinstance(total_tokens, int) or isinstance(total_tokens, bool):
        total_tokens = (
            input_tokens + output_tokens
            if input_tokens is not None and output_tokens is not None
            else None
        )
    return input_tokens, output_tokens, total_tokens


def _text_cost(prompt: str, output: str) -> float:
    """Conservative character-based fallback when provider token usage is absent."""

    input_tokens = max(1, (len(prompt.encode("utf-8")) + 3) // 4)
    output_tokens = max(1, (len(output.encode("utf-8")) + 3) // 4)
    return round(
        input_tokens * INPUT_PRICE_CNY_PER_MILLION / 1_000_000
        + output_tokens * OUTPUT_PRICE_CNY_PER_MILLION / 1_000_000,
        6,
    )


class BailianDirectModelAdapter:
    """Map one synthetic TITMAS review request to one direct model invocation."""

    provider = "ALIBABA_CLOUD_MODEL_STUDIO"
    provider_mode = "BAILIAN_DIRECT_MODEL"

    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout_seconds: float = 90.0,
        transport: Transport | None = None,
    ) -> None:
        if not api_key:
            raise R2AContractError("Alibaba Cloud direct-model credential is missing")
        if model not in ALLOWED_MODELS:
            raise R2AContractError("Alibaba Cloud direct-model is outside the approved model set")
        if not base_url.startswith("https://"):
            raise R2AContractError("Alibaba Cloud direct-model base URL must use HTTPS")
        self._api_key = api_key
        self.model = model
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._transport = transport or _default_transport

    @property
    def model_pinning_status(self) -> str:
        return "SNAPSHOT_PINNED" if self.model == SNAPSHOT_MODEL else "ROLLING_ALIAS"

    def invoke(self, request: dict[str, Any]) -> dict[str, Any]:
        required = {
            "case_id",
            "run_id",
            "prompt",
            "policy_context",
            "common_parameters",
            "privacy_classification",
        }
        if set(request) != required:
            raise R2AContractError("direct-model request fields do not match the beta contract")
        if request["privacy_classification"] != "SYNTHETIC":
            raise R2AContractError("direct-model evaluation accepts synthetic data only")
        parameters = request["common_parameters"]
        if not isinstance(parameters, dict) or parameters.get("enable_search") is not False:
            raise R2AContractError("direct-model search must remain disabled")
        if parameters.get("enable_thinking") is not False:
            raise R2AContractError("direct-model thinking must remain disabled")
        if not isinstance(parameters.get("max_tokens"), int):
            raise R2AContractError("direct-model max_tokens is required")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": request["policy_context"]},
                {"role": "user", "content": request["prompt"]},
            ],
            "temperature": parameters["temperature"],
            "top_p": parameters["top_p"],
            "max_tokens": parameters["max_tokens"],
            "stream": False,
            "enable_search": False,
            "enable_thinking": False,
        }
        started = time.monotonic()
        result = self._transport(
            self._base_url + "/chat/completions",
            {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"},
            payload,
            self._timeout_seconds,
        )
        elapsed_ms = max(0, round((time.monotonic() - started) * 1000))
        body = result.body
        choices = body.get("choices") if isinstance(body.get("choices"), list) else []
        message = choices[0].get("message") if choices and isinstance(choices[0], dict) else {}
        output_text = message.get("content") if isinstance(message, dict) and isinstance(message.get("content"), str) else ""
        input_tokens, output_tokens, total_tokens = _token_usage(body)
        if input_tokens is not None and output_tokens is not None:
            estimated_cost = round(
                input_tokens * INPUT_PRICE_CNY_PER_MILLION / 1_000_000
                + output_tokens * OUTPUT_PRICE_CNY_PER_MILLION / 1_000_000,
                6,
            )
            cost_basis = "PROVIDER_TOKEN_USAGE_ESTIMATE"
        else:
            estimated_cost = _text_cost(request["policy_context"] + request["prompt"], output_text)
            cost_basis = "CONSERVATIVE_TEXT_LENGTH_ESTIMATE"
        reported_model = body.get("model") if isinstance(body.get("model"), str) else None
        request_id = body.get("id") if isinstance(body.get("id"), str) else None
        error_code = None
        error = body.get("error")
        if result.status_code != 200:
            error_code = (
                error.get("code")
                if isinstance(error, dict) and isinstance(error.get("code"), str)
                else f"HTTP_{result.status_code}"
            )
        return {
            "event_type": "TITMAS_ENTERPRISE_AGENT_REVIEW_DIRECT_MODEL_EVENT",
            "provider": self.provider,
            "provider_mode": self.provider_mode,
            "case_id": request["case_id"],
            "run_id": request["run_id"],
            "configured_model_id": self.model,
            "reported_model_id": reported_model,
            "model_pinning_status": self.model_pinning_status,
            "model_id_observability": "OBSERVABLE" if reported_model else "NOT_OBSERVABLE",
            "status": "SUCCEEDED" if result.status_code == 200 and bool(output_text) else "FAILED",
            "failure_reason_code": error_code,
            "output_text": output_text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "elapsed_ms": elapsed_ms,
            "estimated_cost_cny": estimated_cost,
            "cost_basis": cost_basis,
            "request_id": request_id,
            "raw_response_sha256": sha256_value(body),
            "evidence_ref": existing_evidence_reference(
                route_id="bailian-direct",
                case_id=request["case_id"],
                phase="COMMERCIAL_BETA_SYNTHETIC_REVIEW",
                request_digest=sha256_value(payload),
            ),
            "limitations": [
                "SYNTHETIC_CASE_ONLY",
                "MODEL_OUTPUT_NE_BUSINESS_TRUTH",
                "EVIDENCE_REFERENCE_NE_CANONICAL_EVIDENCE_OBJECT",
                "EVALUATION_NE_EXECUTION_AUTHORIZATION",
            ],
        }


__all__ = ["BailianDirectModelAdapter", "SNAPSHOT_MODEL"]
