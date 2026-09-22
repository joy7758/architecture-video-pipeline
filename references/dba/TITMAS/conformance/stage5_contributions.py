#!/usr/bin/env python3
"""Stage 5 contribution contracts extending the canonical TITMAS Conformance.

This is not a second Conformance service. It reuses ``harness.validate_schema``
and adds only Stage 5 contribution-specific semantic checks.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


CONFORMANCE_ROOT = Path(__file__).resolve().parent
TITMAS_ROOT = CONFORMANCE_ROOT.parent
SCHEMA_ROOT = CONFORMANCE_ROOT / "schemas"

CONTRIBUTION_TYPES = {
    "SPECIFICATION_PROPOSAL": "stage5-specification-proposal.schema.json",
    "ADAPTER_MAPPING": "stage5-adapter-mapping.schema.json",
    "TEST_VECTOR": "stage5-test-vector.schema.json",
}
ALLOWED_STATES = {
    "RECEIVED",
    "VALIDATING",
    "CONFORMANCE_PASS",
    "CONFORMANCE_FAIL",
    "REVIEW_REQUIRED",
    "HUMAN_DISPOSITION_REQUIRED",
    "PILOT_ACCEPTED",
    "PILOT_REJECTED",
}
PROHIBITED_ELEVATIONS = {
    "STANDARD_ADOPTED",
    "STABLE",
    "CERTIFIED",
    "EXTERNAL_ADOPTION",
}
FORBIDDEN_TEXT = (
    re.compile(r"(?:^|[\s\"'])/(?:Users|private|home|var|tmp)/"),
    re.compile(r"[A-Za-z]:\\"),
    re.compile(r"(?:^|[^A-Za-z0-9])sk-[A-Za-z0-9_.-]{8,}"),
    re.compile(r"Authorization\s*:\s*Bearer", re.IGNORECASE),
    re.compile(r"\b(?:DASHSCOPE|QIANFAN|ARK|OPENAI|DEEPSEEK)_API_KEY\b"),
    re.compile(r"(?:^|/)\.git(?:/|$)"),
    re.compile(r"TITMAS/private-(?:governance|customer-evaluation)"),
    re.compile(r"\b(?:GatewayService|AtomicJSONWriter|capture_response)\b"),
    re.compile(r"\b(?:STANDARD_ADOPTED|STABLE|CERTIFIED|EXTERNAL_ADOPTION)\b"),
    re.compile(r"\b(?:hidden prompt|system prompt|chain of thought)\b", re.IGNORECASE),
)


class Stage5ConformanceError(ValueError):
    """Fail-closed Stage 5 contribution validation error."""


def _load_harness():
    path = CONFORMANCE_ROOT / "harness.py"
    spec = importlib.util.spec_from_file_location("titmas_canonical_conformance", path)
    if spec is None or spec.loader is None:
        raise Stage5ConformanceError("canonical Conformance unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _scan(value: Any, path: str = "$", depth: int = 0) -> None:
    if depth > 32:
        raise Stage5ConformanceError(f"{path}: maximum depth exceeded")
    if isinstance(value, str):
        if len(value) > 4096:
            raise Stage5ConformanceError(f"{path}: text exceeds bounded length")
        for pattern in FORBIDDEN_TEXT:
            if pattern.search(value):
                raise Stage5ConformanceError(f"{path}: prohibited content")
    elif isinstance(value, list):
        if len(value) > 64:
            raise Stage5ConformanceError(f"{path}: array exceeds bounded size")
        for index, item in enumerate(value):
            _scan(item, f"{path}[{index}]", depth + 1)
    elif isinstance(value, dict):
        if len(value) > 64:
            raise Stage5ConformanceError(f"{path}: object exceeds bounded size")
        for key, item in value.items():
            if not isinstance(key, str) or len(key) > 128:
                raise Stage5ConformanceError(f"{path}: invalid object key")
            _scan(key, f"{path}.<key>", depth + 1)
            _scan(item, f"{path}.{key}", depth + 1)
    elif value is not None and not isinstance(value, (bool, int, float)):
        raise Stage5ConformanceError(f"{path}: unsupported value type")


def _schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


def _semantic_errors(contribution_type: str, payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    if any(value in rendered for value in PROHIBITED_ELEVATIONS):
        errors.append("TITMAS-STAGE5-SEMANTIC-ELEVATION")
    if contribution_type == "TEST_VECTOR":
        negative = payload.get("positive_or_negative") == "NEGATIVE"
        classification = payload.get("failure_classification")
        if negative and classification == "NONE":
            errors.append("TITMAS-STAGE5-NEGATIVE-VECTOR-WITHOUT-FAILURE-CLASS")
        if not negative and classification not in {"NONE", "NOT_ASSESSED"}:
            errors.append("TITMAS-STAGE5-POSITIVE-VECTOR-WITH-FAILURE-CLASS")
    if contribution_type == "SPECIFICATION_PROPOSAL":
        if payload.get("compatibility") == "BREAKING_CHANGE":
            decisions = payload.get("human_decisions_required", [])
            if not any("breaking" in item.lower() for item in decisions):
                errors.append("TITMAS-STAGE5-BREAKING-CHANGE-WITHOUT-HUMAN-DECISION")
    if contribution_type == "ADAPTER_MAPPING":
        bindings = payload.get("titmas_bindings", [])
        pairs = [
            (item.get("source_field"), item.get("titmas_object"), item.get("titmas_field"))
            for item in bindings
            if isinstance(item, dict)
        ]
        if len(pairs) != len(set(pairs)):
            errors.append("TITMAS-STAGE5-DUPLICATE-ADAPTER-BINDING")
    return errors


def validate_contribution(
    contribution_type: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    reason_codes: list[str] = []
    if contribution_type not in CONTRIBUTION_TYPES:
        return {
            "conformance_status": "CONFORMANCE_FAIL",
            "reason_codes": ["TITMAS-STAGE5-UNSUPPORTED-CONTRIBUTION-TYPE"],
            "submission_sha256": sha256_json(payload),
            "human_disposition_required": False,
            "limitations": ["NO_STANDARD_ADOPTION_EFFECT"],
        }
    try:
        if not isinstance(payload, dict):
            raise Stage5ConformanceError("contribution must be an object")
        _scan(payload)
        harness = _load_harness()
        harness.validate_schema(payload, _schema(CONTRIBUTION_TYPES[contribution_type]))
        reason_codes.extend(_semantic_errors(contribution_type, payload))
    except Exception:
        reason_codes.append("TITMAS-STAGE5-CONTRIBUTION-SCHEMA-OR-SANITIZATION-FAIL")
    passed = not reason_codes
    return {
        "conformance_status": (
            "CONFORMANCE_PASS" if passed else "CONFORMANCE_FAIL"
        ),
        "reason_codes": (
            ["TITMAS-STAGE5-CONTRIBUTION-CONFORMANT"]
            if passed
            else sorted(set(reason_codes))
        ),
        "submission_sha256": sha256_json(payload),
        "human_disposition_required": passed,
        "limitations": [
            "CONFORMANCE_NE_TRUTH",
            "CONFORMANCE_NE_AUTHORIZATION",
            "PILOT_ACCEPTANCE_NE_STANDARD_ADOPTION",
        ],
    }


def validate_review(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        _scan(payload)
        harness = _load_harness()
        harness.validate_schema(payload, _schema("stage5-review.schema.json"))
        if payload["requested_model"] != payload["returned_model"]:
            raise Stage5ConformanceError("silent model substitution")
        if payload["verdict"] == "PASS" and payload["blocking_findings"]:
            raise Stage5ConformanceError("PASS cannot retain blocking findings")
    except Exception:
        return {
            "valid": False,
            "reason_codes": ["TITMAS-STAGE5-REVIEW-CONFORMANCE-FAIL"],
        }
    return {
        "valid": True,
        "reason_codes": ["TITMAS-STAGE5-REVIEW-CONFORMANT"],
    }


def self_check() -> dict[str, Any]:
    schema_count = 0
    for name in (
        *CONTRIBUTION_TYPES.values(),
        "stage5-contribution-result.schema.json",
        "stage5-review.schema.json",
    ):
        schema = _schema(name)
        if schema.get("additionalProperties") is not False:
            raise Stage5ConformanceError(f"{name}: fail-closed object required")
        schema_count += 1
    if PROHIBITED_ELEVATIONS & ALLOWED_STATES:
        raise Stage5ConformanceError("prohibited states entered allowed state set")
    return {
        "stage5_contribution_schemas_checked": schema_count,
        "canonical_conformance_reused": True,
        "prohibited_elevation_states": len(PROHIBITED_ELEVATIONS),
    }
