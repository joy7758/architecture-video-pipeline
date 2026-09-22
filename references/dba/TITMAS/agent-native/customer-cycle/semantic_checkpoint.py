#!/usr/bin/env python3
"""Durable sanitized semantic checkpoints for future customer cycles.

The component persists only stage-specific, schema-validated customer results.
It owns no Provider client, performs no network call, and creates no Evidence
Truth, authorization, Runtime, database, or control plane.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "0.1.0"
CHECKPOINT_STATES = {"PERSISTING", "DURABLE"}
STAGES = {
    "CONTRIBUTOR_PLAN",
    "GATEWAY_CUSTOMER_PROJECTION",
    "CONTRIBUTOR_ASSESSMENT",
    "INDEPENDENT_REVIEW",
    "STANDARD_CONTRIBUTION",
    "STANDARD_REVIEW",
}
CUSTOMER_CYCLE_STAGES = (
    "CONTRIBUTOR_PLAN",
    "GATEWAY_CUSTOMER_PROJECTION",
    "CONTRIBUTOR_ASSESSMENT",
    "INDEPENDENT_REVIEW",
)
STANDARD_CONTRIBUTION_STAGES = (
    "CONTRIBUTOR_PLAN",
    "STANDARD_CONTRIBUTION",
    "STANDARD_REVIEW",
)
STAGE_ORDER = CUSTOMER_CYCLE_STAGES + (
    "STANDARD_CONTRIBUTION",
    "STANDARD_REVIEW",
)
STAGE_PREDECESSOR = {
    "GATEWAY_CUSTOMER_PROJECTION": "CONTRIBUTOR_PLAN",
    "CONTRIBUTOR_ASSESSMENT": "GATEWAY_CUSTOMER_PROJECTION",
    "INDEPENDENT_REVIEW": "CONTRIBUTOR_ASSESSMENT",
    "STANDARD_CONTRIBUTION": "CONTRIBUTOR_PLAN",
    "STANDARD_REVIEW": "STANDARD_CONTRIBUTION",
}
STAGE_SCHEMA_FILES = {
    "CONTRIBUTOR_PLAN": "contributor-plan.schema.json",
    "GATEWAY_CUSTOMER_PROJECTION": "gateway-customer-projection.schema.json",
    "CONTRIBUTOR_ASSESSMENT": "contributor-assessment.schema.json",
    "INDEPENDENT_REVIEW": "independent-review.schema.json",
    "STANDARD_CONTRIBUTION": "standard-contribution.schema.json",
    "STANDARD_REVIEW": "standard-review.schema.json",
}
SCHEMA_DIRECTORY = Path(__file__).with_name("schemas")
ENVELOPE_SCHEMA_PATH = SCHEMA_DIRECTORY / "semantic-checkpoint-envelope.schema.json"
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
PATH_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
RELATIVE_REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,255}$")

FORBIDDEN_TEXT_PATTERNS = (
    re.compile(r"(?:^|[\s\"'])/(?:Users|private|home|var|tmp)/"),
    re.compile(r"[A-Za-z]:\\"),
    re.compile(r"(?:^|[^A-Za-z0-9])sk-[A-Za-z0-9_.-]{6,}"),
    re.compile(r"Authorization\s*:\s*Bearer", re.IGNORECASE),
    re.compile(r"\b(?:DASHSCOPE|QIANFAN|ARK|OPENAI)_API_KEY\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{6,}", re.IGNORECASE),
    re.compile(r"(?:^|/)\.git(?:/|$)"),
    re.compile(r"TITMAS/private-governance"),
    re.compile(r"\b(?:GatewayService|AtomicJSONWriter|capture_response)\b"),
    re.compile(r"\btest_[A-Za-z0-9_]+\b"),
    re.compile(r"<\|(?:system|assistant|user)[^>]*\|>", re.IGNORECASE),
    re.compile(r"\b(?:hidden prompt|system prompt|chain of thought)\b", re.IGNORECASE),
    re.compile(r"\b(?:current ChatGPT conversation|internal commercial agreement)\b", re.IGNORECASE),
)


class SemanticCheckpointError(RuntimeError):
    """Base error for fail-closed semantic checkpoint operations."""


class SchemaValidationError(SemanticCheckpointError):
    """A record does not satisfy its declared checkpoint Schema."""


class SanitizationError(SemanticCheckpointError):
    """A structured result contains prohibited material."""


class IntegrityError(SemanticCheckpointError):
    """A persisted checkpoint no longer matches its integrity hashes."""


class StageGateError(SemanticCheckpointError):
    """A downstream stage lacks a durable predecessor."""


class InjectedCheckpointCrash(SemanticCheckpointError):
    """Test-only process interruption after a durable checkpoint write."""

    def __init__(self, checkpoint_path: Path):
        super().__init__("injected crash after durable semantic checkpoint")
        self.checkpoint_path = checkpoint_path


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SchemaValidationError(f"unreadable JSON: {path.name}") from exc
    if not isinstance(value, dict):
        raise SchemaValidationError(f"JSON root must be an object: {path.name}")
    return value


def _validate_schema(
    value: Any,
    schema: dict[str, Any],
    *,
    path: str = "$",
    depth: int = 0,
) -> None:
    if depth > 32:
        raise SchemaValidationError(f"{path}: maximum schema depth exceeded")
    expected = schema.get("type")
    type_map = {
        "object": dict,
        "array": list,
        "string": str,
        "boolean": bool,
        "integer": int,
        "number": (int, float),
    }
    if expected in type_map:
        if not isinstance(value, type_map[expected]):
            raise SchemaValidationError(f"{path}: expected {expected}")
        if expected in {"integer", "number"} and isinstance(value, bool):
            raise SchemaValidationError(f"{path}: boolean is not numeric")
    if "const" in schema and value != schema["const"]:
        raise SchemaValidationError(f"{path}: constant mismatch")
    if "enum" in schema and value not in schema["enum"]:
        raise SchemaValidationError(f"{path}: unsupported enum value")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise SchemaValidationError(f"{path}: string below minLength")
        if len(value) > schema.get("maxLength", 1_000_000):
            raise SchemaValidationError(f"{path}: string above maxLength")
        pattern = schema.get("pattern")
        if pattern and not re.fullmatch(pattern, value):
            raise SchemaValidationError(f"{path}: string does not match pattern")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise SchemaValidationError(f"{path}: array below minItems")
        if len(value) > schema.get("maxItems", 1_000_000):
            raise SchemaValidationError(f"{path}: array above maxItems")
        if schema.get("uniqueItems") and len({_canonical_bytes(item) for item in value}) != len(value):
            raise SchemaValidationError(f"{path}: array items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate_schema(item, item_schema, path=f"{path}[{index}]", depth=depth + 1)
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        missing = [key for key in schema.get("required", []) if key not in value]
        if missing:
            raise SchemaValidationError(f"{path}: missing required fields {missing}")
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            if extras:
                raise SchemaValidationError(f"{path}: additional fields {extras}")
        for key, child_schema in properties.items():
            if key in value:
                _validate_schema(
                    value[key],
                    child_schema,
                    path=f"{path}.{key}",
                    depth=depth + 1,
                )


def _scan_value(value: Any, *, path: str = "$") -> None:
    if isinstance(value, bytes):
        raise SanitizationError(f"{path}: binary content is prohibited")
    if isinstance(value, str):
        if len(value) > 4096:
            raise SanitizationError(f"{path}: free text exceeds bounded length")
        if any(ord(character) < 32 and character not in "\n\t\r" for character in value):
            raise SanitizationError(f"{path}: control characters are prohibited")
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            if pattern.search(value):
                raise SanitizationError(f"{path}: prohibited content pattern")
        return
    if isinstance(value, list):
        if len(value) > 64:
            raise SanitizationError(f"{path}: array exceeds bounded size")
        for index, item in enumerate(value):
            _scan_value(item, path=f"{path}[{index}]")
        return
    if isinstance(value, dict):
        if len(value) > 64:
            raise SanitizationError(f"{path}: object exceeds bounded size")
        for key, item in value.items():
            if not isinstance(key, str):
                raise SanitizationError(f"{path}: non-string object key")
            if len(key) > 128:
                raise SanitizationError(f"{path}: object key exceeds bounded length")
            _scan_value(key, path=f"{path}.<key>")
            _scan_value(item, path=f"{path}.{key}")
        return
    if value is not None and not isinstance(value, (bool, int, float)):
        raise SanitizationError(f"{path}: unsupported value type")


def _inside_git_worktree(path: Path) -> bool:
    return any((candidate / ".git").exists() for candidate in (path, *path.parents))


def _require_private_directory(path: Path) -> None:
    if not path.is_dir():
        raise SemanticCheckpointError("checkpoint directory must already exist")
    if stat.S_IMODE(path.stat().st_mode) != 0o700:
        raise SemanticCheckpointError("checkpoint directory mode must be 0700")
    if _inside_git_worktree(path.resolve()):
        raise SemanticCheckpointError("checkpoint directory must remain outside Git")


def _payload_hash(record: dict[str, Any]) -> str:
    payload = dict(record)
    payload.pop("checkpoint_payload_sha256", None)
    return _sha256(_canonical_bytes(payload))


def _validate_reference(reference: str) -> None:
    if not RELATIVE_REF.fullmatch(reference):
        raise SanitizationError("response_envelope_ref must be a bounded relative reference")
    if reference.startswith("/") or ".." in Path(reference).parts:
        raise SanitizationError("response_envelope_ref cannot escape its audit root")


class AtomicCheckpointWriter:
    """Durably replace one checkpoint in its pre-established private directory."""

    def write(self, target: Path, payload: dict[str, Any]) -> None:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{target.name}.",
            suffix=".tmp",
            dir=target.parent,
            text=True,
        )
        temporary = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, target)
            os.chmod(target, 0o600)
            _fsync_directory(target.parent)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise


@dataclass(frozen=True)
class CheckpointResult:
    checkpoint: dict[str, Any]
    checkpoint_path: Path


def stage_schema_path(stage: str) -> Path:
    if stage not in STAGES:
        raise SchemaValidationError("unsupported checkpoint stage")
    return SCHEMA_DIRECTORY / STAGE_SCHEMA_FILES[stage]


def validate_structured_result(stage: str, structured_result: dict[str, Any]) -> None:
    if not isinstance(structured_result, dict):
        raise SchemaValidationError("structured_result must be an object")
    _scan_value(structured_result)
    _validate_schema(structured_result, _load_json(stage_schema_path(stage)))


def _validate_checkpoint(record: dict[str, Any], *, require_durable: bool) -> None:
    _validate_schema(record, _load_json(ENVELOPE_SCHEMA_PATH))
    if require_durable and record["checkpoint_state"] != "DURABLE":
        raise IntegrityError("checkpoint is not durable")
    expected_dispatch_state = record["checkpoint_state"] == "DURABLE"
    if record["downstream_dispatch_authorized"] is not expected_dispatch_state:
        raise IntegrityError("checkpoint state and stage dispatch gate disagree")
    if expected_dispatch_state:
        if not record["persisted_at"] or not record["finalized_at"]:
            raise IntegrityError("durable checkpoint lacks persistence timestamps")
    elif record["persisted_at"] or record["finalized_at"]:
        raise IntegrityError("non-durable checkpoint has final timestamps")
    _scan_value(
        {
            "checkpoint_id": record["checkpoint_id"],
            "cycle_id": record["cycle_id"],
            "source_main": record["source_main"],
            "gateway_revision": record["gateway_revision"],
            "attempt_id": record["attempt_id"],
            "provider": record["provider"],
            "requested_model": record["requested_model"],
            "returned_model": record["returned_model"],
        },
        path="$.metadata",
    )
    _validate_reference(record["response_envelope_ref"])
    validate_structured_result(record["stage"], record["structured_result"])
    if record["structured_content_sha256"] != _sha256(
        _canonical_bytes(record["structured_result"])
    ):
        raise IntegrityError("structured result hash mismatch")
    if record["checkpoint_payload_sha256"] != _payload_hash(record):
        raise IntegrityError("checkpoint payload hash mismatch")
    if record["limitations"] != record["structured_result"].get("limitations", []):
        raise IntegrityError("checkpoint limitations projection mismatch")
    if any(
        record[field] is not False
        for field in (
            "raw_prompt_retained",
            "raw_response_retained",
            "hidden_reasoning_retained",
            "credential_material_retained",
        )
    ):
        raise IntegrityError("prohibited retention flag")


def load_checkpoint(
    checkpoint_path: Path,
    *,
    require_durable: bool = True,
) -> dict[str, Any]:
    path = checkpoint_path.resolve()
    record = _load_json(path)
    _validate_checkpoint(record, require_durable=require_durable)
    if stat.S_IMODE(path.stat().st_mode) != 0o600:
        raise IntegrityError("checkpoint file mode must be 0600")
    return record


def persist_checkpoint(
    *,
    checkpoint_directory: Path,
    checkpoint_id: str,
    cycle_id: str,
    stage: str,
    source_main: str,
    gateway_revision: str,
    attempt_id: str,
    provider: str,
    requested_model: str,
    returned_model: str,
    model_identity_status: str,
    response_capture_state: str,
    response_envelope_ref: str,
    response_body_sha256: str,
    structured_result: dict[str, Any],
    created_at: str | None = None,
    writer: AtomicCheckpointWriter | None = None,
    crash_after_durable_write: bool = False,
) -> CheckpointResult:
    """Persist and reload one semantic result before enabling downstream work."""

    directory = checkpoint_directory.resolve()
    _require_private_directory(directory)
    if not PATH_SAFE_ID.fullmatch(checkpoint_id):
        raise SchemaValidationError("checkpoint_id is not path safe")
    if stage not in STAGES:
        raise SchemaValidationError("unsupported checkpoint stage")
    if response_capture_state != "FINALIZED_SUCCESS":
        raise StageGateError("response capture must be FINALIZED_SUCCESS")
    if model_identity_status != "MATCH" or requested_model != returned_model:
        raise StageGateError("model identity must match before semantic persistence")
    if not HASH_PATTERN.fullmatch(response_body_sha256):
        raise SchemaValidationError("response_body_sha256 is invalid")
    _scan_value(
        {
            "checkpoint_id": checkpoint_id,
            "cycle_id": cycle_id,
            "source_main": source_main,
            "gateway_revision": gateway_revision,
            "attempt_id": attempt_id,
            "provider": provider,
            "requested_model": requested_model,
            "returned_model": returned_model,
        },
        path="$.metadata",
    )
    _validate_reference(response_envelope_ref)
    validate_structured_result(stage, structured_result)

    timestamp = created_at or _now()
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "checkpoint_id": checkpoint_id,
        "cycle_id": cycle_id,
        "stage": stage,
        "checkpoint_state": "PERSISTING",
        "source_main": source_main,
        "gateway_revision": gateway_revision,
        "attempt_id": attempt_id,
        "provider": provider,
        "requested_model": requested_model,
        "returned_model": returned_model,
        "model_identity_status": model_identity_status,
        "response_envelope_ref": response_envelope_ref,
        "response_body_sha256": response_body_sha256,
        "structured_content_sha256": _sha256(_canonical_bytes(structured_result)),
        "checkpoint_payload_sha256": "",
        "contract_schema": f"schemas/{STAGE_SCHEMA_FILES[stage]}",
        "contract_validation_status": "PASS",
        "sanitization_status": "PASS",
        "created_at": timestamp,
        "persisted_at": "",
        "finalized_at": "",
        "downstream_dispatch_authorized": False,
        "raw_prompt_retained": False,
        "raw_response_retained": False,
        "hidden_reasoning_retained": False,
        "credential_material_retained": False,
        "structured_result": structured_result,
        "limitations": structured_result.get("limitations", []),
    }
    record["checkpoint_payload_sha256"] = _payload_hash(record)
    _validate_checkpoint(record, require_durable=False)

    target = directory / f"{checkpoint_id}.checkpoint.json"
    if target.exists():
        raise SemanticCheckpointError("checkpoint already exists")
    durable_writer = writer or AtomicCheckpointWriter()
    durable_writer.write(target, record)
    reloaded = load_checkpoint(target, require_durable=False)
    if reloaded["checkpoint_state"] != "PERSISTING":
        raise IntegrityError("unexpected initial checkpoint state")

    finalized_at = _now()
    record.update(
        {
            "checkpoint_state": "DURABLE",
            "persisted_at": finalized_at,
            "finalized_at": finalized_at,
            "downstream_dispatch_authorized": True,
        }
    )
    record["checkpoint_payload_sha256"] = _payload_hash(record)
    durable_writer.write(target, record)
    if crash_after_durable_write:
        raise InjectedCheckpointCrash(target)
    final_record = load_checkpoint(target, require_durable=True)
    return CheckpointResult(final_record, target)


class CheckpointStageGate:
    """Require the previous semantic stage to be durable before dispatch."""

    def __init__(self, checkpoint_directory: Path, cycle_id: str):
        self.checkpoint_directory = checkpoint_directory.resolve()
        self.cycle_id = cycle_id

    def _stage_records(self) -> dict[str, dict[str, Any]]:
        records: dict[str, dict[str, Any]] = {}
        for path in sorted(self.checkpoint_directory.glob("*.checkpoint.json")):
            record = load_checkpoint(path)
            if record["cycle_id"] != self.cycle_id:
                continue
            if record["stage"] in records:
                raise IntegrityError("multiple durable checkpoints for one stage")
            records[record["stage"]] = record
        return records

    def authorize_dispatch(self, stage: str) -> bool:
        if stage not in STAGES:
            raise StageGateError("unsupported downstream stage")
        predecessor = STAGE_PREDECESSOR.get(stage)
        if predecessor is None:
            return True
        record = self._stage_records().get(predecessor)
        if (
            record is None
            or record["checkpoint_state"] != "DURABLE"
            or record["downstream_dispatch_authorized"] is not True
        ):
            raise StageGateError(
                f"{stage} requires durable {predecessor} checkpoint"
            )
        return True


def generate_audit_summary(
    checkpoint_directory: Path,
    *,
    cycle_id: str,
    review_outcome: str = "NOT_RUN",
) -> dict[str, Any]:
    """Generate a sanitized audit projection without a Provider or network call."""

    gate = CheckpointStageGate(checkpoint_directory, cycle_id)
    records = gate._stage_records()
    summary: dict[str, Any] = {
        "cycle_id": cycle_id,
        "checkpoint_ids": {
            stage: records[stage]["checkpoint_id"]
            for stage in CUSTOMER_CYCLE_STAGES
            if stage in records
        },
        "checkpoint_hashes": {
            stage: records[stage]["checkpoint_payload_sha256"]
            for stage in CUSTOMER_CYCLE_STAGES
            if stage in records
        },
        "plan_checkpoint_durable": "CONTRIBUTOR_PLAN" in records,
        "gateway_checkpoint_durable": "GATEWAY_CUSTOMER_PROJECTION" in records,
        "assessment_checkpoint_durable": "CONTRIBUTOR_ASSESSMENT" in records,
        "review_checkpoint_durable": "INDEPENDENT_REVIEW" in records,
        "customer_recommendation_available": "CONTRIBUTOR_ASSESSMENT" in records,
        "customer_recommendation": (
            records["CONTRIBUTOR_ASSESSMENT"]["structured_result"]["recommendation"]
            if "CONTRIBUTOR_ASSESSMENT" in records
            else "UNKNOWN"
        ),
        "independent_review_complete": "INDEPENDENT_REVIEW" in records,
        "review_outcome": (
            records["INDEPENDENT_REVIEW"]["structured_result"]["verdict"]
            if "INDEPENDENT_REVIEW" in records
            else review_outcome
        ),
        "cycle_complete": all(stage in records for stage in CUSTOMER_CYCLE_STAGES),
        "real_model_call_count": 0,
        "real_provider_call_count": 0,
        "limitations": [
            "SYNTHETIC_REPLAY_ONLY",
            "CHECKPOINT_NE_EVIDENCE_TRUTH",
            "CHECKPOINT_NE_AUTHORIZATION",
        ],
    }
    return summary


def replay_synthetic_d02(checkpoint_directory: Path) -> dict[str, Any]:
    """Replay the D02 failure shape with synthetic content and no Provider call."""

    cycle_id = "SYNTHETIC-D02-REPLAY"
    common = {
        "checkpoint_directory": checkpoint_directory,
        "cycle_id": cycle_id,
        "source_main": "a" * 40,
        "gateway_revision": "b" * 40,
        "response_capture_state": "FINALIZED_SUCCESS",
        "response_body_sha256": "c" * 64,
        "model_identity_status": "MATCH",
    }
    persist_checkpoint(
        **common,
        checkpoint_id="synthetic-plan",
        stage="CONTRIBUTOR_PLAN",
        attempt_id="synthetic-plan-attempt",
        provider="SYNTHETIC_PROVIDER",
        requested_model="synthetic-model",
        returned_model="synthetic-model",
        response_envelope_ref="captures/synthetic-plan.envelope.json",
        structured_result={
            "problem_understood": "Bounded synthetic customer evaluation.",
            "contract_version": "0.1.0",
            "relevance_preassessment": "RELEVANT",
            "selected_operation": "EVALUATE",
            "request_body": {"synthetic_request_id": "SYNTHETIC-REPLAY-001"},
            "expected_public_result_shape": {"result_status": "string"},
            "decision_criteria": ["Contract match is visible."],
            "limitations": ["SYNTHETIC_ONLY"],
            "non_claims": ["NOT_PRODUCTION_READY"],
        },
    )
    gate = CheckpointStageGate(checkpoint_directory, cycle_id)
    gate.authorize_dispatch("GATEWAY_CUSTOMER_PROJECTION")
    persist_checkpoint(
        **common,
        checkpoint_id="synthetic-gateway",
        stage="GATEWAY_CUSTOMER_PROJECTION",
        attempt_id="synthetic-gateway-attempt",
        provider="TITMAS_LOCAL_EVALUATION_FACADE",
        requested_model="titmas-local-evaluation-facade",
        returned_model="titmas-local-evaluation-facade",
        response_envelope_ref="captures/synthetic-gateway.envelope.json",
        structured_result={
            "operation": "EVALUATE",
            "http_status": 200,
            "public_reason_code": "SYNTHETIC_CONTRACT_MATCH_WITH_LIMITATIONS",
            "request_body_sha256": "d" * 64,
            "response_body_sha256": "e" * 64,
            "customer_visible_result": {
                "result_status": "CONDITIONALLY_RECOMMENDED"
            },
            "limitations": ["SYNTHETIC_ONLY"],
        },
    )
    gate.authorize_dispatch("CONTRIBUTOR_ASSESSMENT")
    persist_checkpoint(
        **common,
        checkpoint_id="synthetic-assessment",
        stage="CONTRIBUTOR_ASSESSMENT",
        attempt_id="synthetic-assessment-attempt",
        provider="SYNTHETIC_PROVIDER",
        requested_model="synthetic-model",
        returned_model="synthetic-model",
        response_envelope_ref="captures/synthetic-assessment.envelope.json",
        structured_result={
            "contract_understood": True,
            "operation_usable": True,
            "result_contract_match": True,
            "recommendation": "CONDITIONALLY_RECOMMEND_SERVICE",
            "recommendation_reason": "Synthetic contract matched with limitations.",
            "commercial_blockers": ["No production evidence."],
            "repeat_evaluation_recommended": True,
            "limitations": ["SYNTHETIC_ONLY"],
            "non_claims": ["NOT_CUSTOMER_ADOPTION"],
        },
    )
    gate.authorize_dispatch("INDEPENDENT_REVIEW")
    return generate_audit_summary(
        checkpoint_directory,
        cycle_id=cycle_id,
        review_outcome="POST_DISPATCH_OUTCOME_UNKNOWN",
    )
