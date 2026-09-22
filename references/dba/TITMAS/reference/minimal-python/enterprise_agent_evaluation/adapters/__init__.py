"""Shared, fail-closed contracts for the private R2A route adapters.

This package is a removable reference adapter layer.  It does not create a
runtime, credential store, evidence authority, approval chain, or retry path.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Callable, Mapping


CONFIGURED_MODEL_ID = "qwen3.7-max"
EVIDENCE_LEVEL = "E1"
REQUEST_FIELDS = {
    "phase",
    "case_id",
    "prompt",
    "input_variables",
    "configured_model_id",
    "application_version",
    "knowledge_base_version",
    "source_document_sha256",
    "direct_context_sha256",
    "common_parameters",
    "privacy_classification",
}
COMMON_PARAMETER_FIELDS = {
    "temperature",
    "top_p",
    "max_tokens",
    "enable_thinking",
    "enable_search",
    "response_format",
}
OPTIONAL_COMMON_PARAMETER_FIELDS = {"seed"}
EVENT_FIELDS = {
    "route_id",
    "provider",
    "configured_model_id",
    "reported_model_id",
    "model_id_source",
    "model_id_observability",
    "application_version",
    "knowledge_base_version",
    "request_id",
    "run_id",
    "status",
    "output_text",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "elapsed_ms",
    "estimated_cost_cny",
    "node_events",
    "not_assessed_fields",
    "raw_response_sha256",
    "evidence_ref",
}
MODEL_ALIGNMENT_STATES = {
    "SAME_MODEL_SNAPSHOT_CONFIRMED",
    "SAME_MODEL_ALIAS_CONFIGURED",
    "MODEL_ID_NOT_OBSERVABLE",
    "MODEL_MISMATCH",
}
ACTION_VALUES = {"ANSWER", "ASK", "ESCALATE"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DATED_MODEL_RE = re.compile(r".+-20\d{2}-\d{2}-\d{2}$")


class R2AContractError(ValueError):
    """A frozen R2A input or output contract was not satisfied."""


class R2ATransportError(RuntimeError):
    """A provider request failed without exposing response or credential data."""


@dataclass(frozen=True)
class TransportResult:
    """One HTTP attempt result returned by an injected or standard transport."""

    status_code: int
    body: dict[str, Any]


Transport = Callable[
    [str, Mapping[str, str], dict[str, Any], float],
    TransportResult,
]


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def masked_presence(value: str | None) -> str:
    """Return only presence state; never return a secret or its digest."""

    return "PRESENT" if isinstance(value, str) and value else "MISSING"


def validate_request(request: dict[str, Any]) -> None:
    if set(request) != REQUEST_FIELDS:
        raise R2AContractError("request fields do not match the frozen R2A contract")
    if request["phase"] not in {"A0_DIRECT_CONTEXT_PARITY", "A1_NATIVE_RAG_SMOKE"}:
        raise R2AContractError("unknown R2A phase")
    if not isinstance(request["case_id"], str) or not request["case_id"]:
        raise R2AContractError("case_id is required")
    if not isinstance(request["prompt"], str) or not request["prompt"]:
        raise R2AContractError("prompt is required")
    if not isinstance(request["input_variables"], dict):
        raise R2AContractError("input_variables must be an object")
    if request["configured_model_id"] != CONFIGURED_MODEL_ID:
        raise R2AContractError("configured model must remain qwen3.7-max")
    for field in ("application_version", "knowledge_base_version"):
        if not isinstance(request[field], str) or not request[field]:
            raise R2AContractError(f"{field} is required")
    for field in ("source_document_sha256", "direct_context_sha256"):
        if not isinstance(request[field], str) or SHA256_RE.fullmatch(request[field]) is None:
            raise R2AContractError(f"{field} must be a lowercase SHA-256 digest")
    if request["privacy_classification"] != "SYNTHETIC":
        raise R2AContractError("R2A accepts synthetic data only")

    parameters = request["common_parameters"]
    if not isinstance(parameters, dict):
        raise R2AContractError("common_parameters must be an object")
    keys = set(parameters)
    if not COMMON_PARAMETER_FIELDS <= keys:
        raise R2AContractError("common parameter intersection is incomplete")
    if not keys <= COMMON_PARAMETER_FIELDS | OPTIONAL_COMMON_PARAMETER_FIELDS:
        raise R2AContractError("unsupported parameter is outside the common intersection")
    if parameters["enable_thinking"] is not False:
        raise R2AContractError("thinking must remain disabled")
    if parameters["enable_search"] is not False:
        raise R2AContractError("web search must remain disabled")
    if parameters["response_format"] != "text":
        raise R2AContractError("native structured output is not permitted")
    if not isinstance(parameters["max_tokens"], int) or isinstance(parameters["max_tokens"], bool):
        raise R2AContractError("max_tokens must be an integer")
    if parameters["max_tokens"] < 1 or parameters["max_tokens"] > 4096:
        raise R2AContractError("max_tokens is outside the bounded range")
    for field in ("temperature", "top_p"):
        if not isinstance(parameters[field], (int, float)) or isinstance(parameters[field], bool):
            raise R2AContractError(f"{field} must be numeric")


def existing_evidence_reference(
    *,
    route_id: str,
    case_id: str,
    phase: str,
    request_digest: str,
) -> dict[str, Any]:
    """Bind to the existing reference without creating canonical Evidence."""

    return {
        "source_contract_ref": "TITMAS/reference/minimal-python/titmas_reference.py",
        "source_route_id": route_id,
        "source_case_id": case_id,
        "source_phase": phase,
        "request_digest": request_digest,
        "evidence_level": EVIDENCE_LEVEL,
        "admission_status": "REFERENCE_ONLY_NOT_DBOS_ADMITTED",
        "canonical_evidence_object_created": False,
        "truth_effect": "NONE",
        "authority_effect": "NONE",
    }


def validate_event(event: dict[str, Any]) -> None:
    if set(event) != EVENT_FIELDS:
        raise R2AContractError("adapter event fields do not match the frozen R2A event contract")
    if event["status"] not in {"SUCCEEDED", "FAILED", "NOT_ASSESSED"}:
        raise R2AContractError("invalid adapter event status")
    if event["configured_model_id"] != CONFIGURED_MODEL_ID:
        raise R2AContractError("event configured model drifted")
    if not isinstance(event["node_events"], list):
        raise R2AContractError("node_events must be an array")
    if not isinstance(event["not_assessed_fields"], list):
        raise R2AContractError("not_assessed_fields must be an array")
    if SHA256_RE.fullmatch(event["raw_response_sha256"]) is None:
        raise R2AContractError("raw response digest is invalid")
    evidence = event["evidence_ref"]
    if evidence.get("canonical_evidence_object_created") is not False:
        raise R2AContractError("adapter cannot create canonical Evidence")
    if evidence.get("authority_effect") != "NONE":
        raise R2AContractError("adapter cannot create authority")


def parse_text_contract(output_text: str) -> dict[str, str]:
    """Parse the common plain-text output without a model repair call."""

    if not isinstance(output_text, str) or not output_text.strip():
        raise R2AContractError("OUTPUT_CONTRACT_FAIL")
    pattern = re.compile(
        r"\AACTION:\s*(ANSWER|ASK|ESCALATE)\s*\n"
        r"REPLY:\s*(.*?)\s*\n"
        r"POLICY_REF:\s*(.*?)\s*\n"
        r"LIMITATION:\s*(.*?)\s*\Z",
        re.DOTALL,
    )
    match = pattern.fullmatch(output_text.strip())
    if match is None:
        raise R2AContractError("OUTPUT_CONTRACT_FAIL")
    action, reply, policy_ref, limitation = (item.strip() for item in match.groups())
    if action not in ACTION_VALUES or not reply or not policy_ref or not limitation:
        raise R2AContractError("OUTPUT_CONTRACT_FAIL")
    return {
        "action": action,
        "reply": reply,
        "policy_ref": policy_ref,
        "limitation": limitation,
    }


def determine_model_alignment(events: list[dict[str, Any]]) -> str:
    """Apply the four-state model-alignment rule to one event per route."""

    if not events:
        raise R2AContractError("model alignment requires observed events")
    if {event["configured_model_id"] for event in events} != {CONFIGURED_MODEL_ID}:
        return "MODEL_MISMATCH"
    reported = [event["reported_model_id"] for event in events]
    if any(value is None or value == "" for value in reported):
        return "MODEL_ID_NOT_OBSERVABLE"
    sources = {event["model_id_source"] for event in events}
    provider_observed = {"PROVIDER_USAGE", "PROVIDER_RESPONSE"}
    if len(set(reported)) != 1:
        compatible_alias_or_snapshot = all(
            value == CONFIGURED_MODEL_ID or value.startswith(CONFIGURED_MODEL_ID + "-")
            for value in reported
        )
        if not compatible_alias_or_snapshot:
            return "MODEL_MISMATCH"
        if sources <= provider_observed:
            return "MODEL_MISMATCH"
        return "MODEL_ID_NOT_OBSERVABLE"
    if all(DATED_MODEL_RE.fullmatch(value) is not None for value in reported):
        if sources <= provider_observed:
            return "SAME_MODEL_SNAPSHOT_CONFIRMED"
        return "MODEL_ID_NOT_OBSERVABLE"
    if set(reported) == {CONFIGURED_MODEL_ID}:
        return "SAME_MODEL_ALIAS_CONFIGURED"
    return "MODEL_MISMATCH"


__all__ = [
    "CONFIGURED_MODEL_ID",
    "EVENT_FIELDS",
    "MODEL_ALIGNMENT_STATES",
    "R2AContractError",
    "R2ATransportError",
    "Transport",
    "TransportResult",
    "canonical_json_bytes",
    "determine_model_alignment",
    "existing_evidence_reference",
    "masked_presence",
    "parse_text_contract",
    "sha256_text",
    "sha256_value",
    "validate_event",
    "validate_request",
]
