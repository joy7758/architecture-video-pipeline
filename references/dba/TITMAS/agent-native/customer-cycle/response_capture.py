#!/usr/bin/env python3
"""Fail-closed, provider-neutral response capture for agent customer tests.

The module owns no network client and performs no automatic retry. A caller
must inject a transport with a ``send(request)`` method. The included
``FakeProvider`` is deterministic and local-only.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


STATES = {
    "PREPARED",
    "DISPATCH_STARTED",
    "RESPONSE_HEADERS_CAPTURED",
    "RESPONSE_BODY_CAPTURED",
    "PARSE_COMPLETED",
    "FINALIZED_SUCCESS",
    "FAILED_BEFORE_DISPATCH",
    "FAILED_AFTER_DISPATCH_OUTCOME_UNKNOWN",
    "FAILED_HTTP_RESPONSE_CAPTURED",
    "FAILED_EMPTY_BODY",
    "FAILED_TRUNCATED_BODY",
    "FAILED_PARSE",
    "FAILED_MODEL_IDENTITY_MISSING",
    "FAILED_MODEL_IDENTITY_MISMATCH",
    "FAILED_ATOMIC_WRITE",
    "FAILED_RECOVERY_REQUIRED",
}

OUTCOMES = {
    "VALID_RESPONSE",
    "PROVIDER_HTTP_FAILURE_WITH_RESPONSE",
    "FAILED_BEFORE_DISPATCH",
    "POST_DISPATCH_OUTCOME_UNKNOWN",
    "RESPONSE_CAPTURE_FAILURE",
    "RESPONSE_PARSE_FAILURE",
    "MODEL_IDENTITY_FAILURE",
}

SAFE_REAUTHORIZE = "HUMAN_DECISION_REQUIRED_SAFE_TO_REAUTHORIZE"
NEW_DECISION_REQUIRED = "PROHIBITED_WITHOUT_NEW_HUMAN_DECISION"
NOT_APPLICABLE = "NOT_APPLICABLE"
DEFAULT_ALLOWED_REQUEST_FIELDS = {
    "model",
    "messages",
    "temperature",
    "top_p",
    "max_tokens",
    "stream",
    "enable_search",
}


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


class AtomicWriteError(OSError):
    """A durable write could not complete."""


class InjectedProcessCrash(RuntimeError):
    """Test-only crash after a durable body spool and envelope update."""

    def __init__(self, envelope_path: Path, spool_path: Path):
        super().__init__("injected crash after response body capture")
        self.envelope_path = envelope_path
        self.spool_path = spool_path


class HeadersCapturedInterrupt(ConnectionError):
    """A response began, then interrupted before a complete body."""

    def __init__(self, response: "FakeResponse"):
        super().__init__("connection interrupted after response headers")
        self.response = response


class AtomicJSONWriter:
    """Write JSON through a same-directory temporary file and atomic replace."""

    def __init__(self, fail_stage: str | None = None):
        self.fail_stage = fail_stage
        self._failure_consumed = False

    def _inject(self, stage: str) -> None:
        if self.fail_stage == stage and not self._failure_consumed:
            self._failure_consumed = True
            raise AtomicWriteError(f"injected atomic write failure at {stage}")

    def write(self, target: Path, payload: dict[str, Any]) -> None:
        if "final_state" in payload:
            payload["final_state"] = payload.get("state", "")
        if "response_status" in payload:
            payload["response_status"] = payload.get("http_status", 0)
        if not target.parent.is_dir():
            raise AtomicWriteError("target directory is not pre-established")
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
                self._inject("write")
                json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                self._inject("fsync_file")
                os.fsync(handle.fileno())
            self._inject("replace")
            os.replace(temporary, target)
            os.chmod(target, 0o600)
            self._inject("fsync_directory")
            _fsync_directory(target.parent)
        except Exception as exc:
            temporary.unlink(missing_ok=True)
            if isinstance(exc, AtomicWriteError):
                raise
            raise AtomicWriteError(str(exc)) from exc


@dataclass
class FakeResponse:
    """Synthetic response metadata and body for a local-only fake provider."""

    status: int = 200
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b"{}"
    request_id: str = "fake-request-001"
    provider_request_id: str = "fake-provider-request-001"
    returned_model: str | None = "fake-model"
    content_type: str = "application/json"
    truncated: bool = False
    crash_after_body: bool = False


class Transport(Protocol):
    def send(self, request: dict[str, Any]) -> FakeResponse:
        """Return a response or raise a transport exception."""


class FakeProvider:
    """Configurable deterministic transport that never accesses a network."""

    def __init__(
        self,
        *,
        status: int = 200,
        headers: dict[str, str] | None = None,
        request_id: str = "fake-request-001",
        provider_request_id: str = "fake-provider-request-001",
        returned_model: str | None = "fake-model",
        json_body: dict[str, Any] | None = None,
        body: bytes | None = None,
        empty_body: bool = False,
        truncate_body: bool = False,
        delay_seconds: float = 0,
        connection_interrupt: bool = False,
        interrupt_after_headers: bool = False,
        crash_after_body: bool = False,
    ):
        if body is not None and json_body is not None:
            raise ValueError("provide body or json_body, not both")
        encoded = body if body is not None else _canonical_bytes(json_body or {})
        if empty_body:
            encoded = b""
        if truncate_body and encoded:
            encoded = encoded[: max(1, len(encoded) // 2)]
        self.response = FakeResponse(
            status=status,
            headers=dict(headers or {}),
            body=encoded,
            request_id=request_id,
            provider_request_id=provider_request_id,
            returned_model=returned_model,
            truncated=truncate_body,
            crash_after_body=crash_after_body,
        )
        self.delay_seconds = delay_seconds
        self.connection_interrupt = connection_interrupt
        self.interrupt_after_headers = interrupt_after_headers
        self.calls = 0

    def send(self, request: dict[str, Any]) -> FakeResponse:
        del request
        self.calls += 1
        if self.delay_seconds:
            time.sleep(self.delay_seconds)
        if self.connection_interrupt:
            raise ConnectionError("injected connection interruption")
        if self.interrupt_after_headers:
            raise HeadersCapturedInterrupt(self.response)
        return self.response


@dataclass
class CaptureResult:
    envelope: dict[str, Any]
    envelope_path: Path
    spool_path: Path
    request_sent: bool


def _base_envelope(
    *,
    attempt_id: str,
    provider: str,
    requested_model: str,
    request_payload_sha256: str,
    request_contract_sha256: str,
    gateway_audit: dict[str, str] | None = None,
) -> dict[str, Any]:
    audit = gateway_audit or {}
    return {
        "schema_version": "0.1.0",
        "attempt_id": attempt_id,
        "provider": provider,
        "requested_model": requested_model,
        "returned_model": "",
        "model_identity_status": "NOT_ASSESSED",
        "request_payload_sha256": request_payload_sha256,
        "request_contract_sha256": request_contract_sha256,
        "customer_session_id": audit.get("customer_session_id", ""),
        "requested_operation": audit.get("requested_operation", ""),
        "request_body_sha256": audit.get(
            "request_body_sha256",
            request_payload_sha256,
        ),
        "response_status": 0,
        "final_state": "PREPARED",
        "state": "PREPARED",
        "failure_phase": "NONE",
        "outcome_classification": "FAILED_BEFORE_DISPATCH",
        "prepared_at": _now(),
        "dispatch_started_at": "",
        "response_received_at": "",
        "body_captured_at": "",
        "parsed_at": "",
        "finalized_at": "",
        "http_status": 0,
        "request_id": "",
        "provider_request_id": "",
        "finish_reason": "",
        "response_content_type": "",
        "response_body_length": 0,
        "response_body_sha256": "",
        "body_capture_complete": False,
        "parse_status": "NOT_STARTED",
        "contract_validation_status": "NOT_ASSESSED",
        "contract_fields_present": [],
        "usage_input_tokens": 0,
        "usage_output_tokens": 0,
        "usage_total_tokens": 0,
        "raw_prompt_retained": False,
        "raw_response_retained": False,
        "hidden_reasoning_retained": False,
        "credential_material_retained": False,
        "retry_eligibility": NOT_APPLICABLE,
        "retry_reason": "",
    }


def _schema_loadable(schema_path: Path) -> bool:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    required = set(schema.get("required", []))
    return {
        "schema_version",
        "attempt_id",
        "requested_model",
        "state",
        "outcome_classification",
    }.issubset(required)


def _inside_git_worktree(path: Path) -> bool:
    return any((candidate / ".git").exists() for candidate in (path, *path.parents))


def request_shape_preflight(
    request: dict[str, Any],
    *,
    capture_directory: Path,
    schema_path: Path,
    minimum_free_bytes: int = 1_048_576,
    allowed_request_fields: set[str] | None = None,
) -> dict[str, Any]:
    """Validate a request and capture destination without network dispatch."""

    errors: list[str] = []
    allowed = allowed_request_fields or DEFAULT_ALLOWED_REQUEST_FIELDS
    try:
        _canonical_bytes(request)
    except (TypeError, ValueError):
        errors.append("REQUEST_NOT_SERIALIZABLE")
    model = request.get("model")
    if not isinstance(model, str) or not model.strip():
        errors.append("MODEL_REQUIRED")
    messages = request.get("messages")
    if not isinstance(messages, list) or not messages:
        errors.append("MESSAGES_REQUIRED")
    else:
        for message in messages:
            if (
                not isinstance(message, dict)
                or not isinstance(message.get("role"), str)
                or not isinstance(message.get("content"), str)
            ):
                errors.append("MESSAGE_SHAPE_INVALID")
                break
    unsupported = sorted(set(request) - allowed)
    if unsupported:
        errors.append(f"UNSUPPORTED_REQUEST_FIELDS:{','.join(unsupported)}")
    if not capture_directory.is_dir():
        errors.append("CAPTURE_DIRECTORY_NOT_PREESTABLISHED")
    elif not os.access(capture_directory, os.W_OK):
        errors.append("CAPTURE_DIRECTORY_NOT_WRITABLE")
    elif _inside_git_worktree(capture_directory.resolve()):
        errors.append("CAPTURE_DIRECTORY_INSIDE_GIT_WORKTREE")
    if not _schema_loadable(schema_path):
        errors.append("ENVELOPE_SCHEMA_UNAVAILABLE")
    if capture_directory.is_dir():
        if shutil.disk_usage(capture_directory).free < minimum_free_bytes:
            errors.append("INSUFFICIENT_DISK_SPACE")
        probe = capture_directory / f".capture-preflight-{uuid.uuid4().hex}.json"
        try:
            AtomicJSONWriter().write(probe, {"preflight": True})
        except OSError:
            errors.append("ATOMIC_REPLACE_UNAVAILABLE")
        finally:
            probe.unlink(missing_ok=True)
            if capture_directory.exists():
                _fsync_directory(capture_directory)
    return {
        "request_shape_preflight": "PASS" if not errors else "FAIL",
        "capture_destination_preflight": "PASS" if not errors else "FAIL",
        "network_dispatch_performed": False,
        "errors": errors,
    }


def _write_spool(path: Path, body: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(path, 0o600)
        _fsync_directory(path.parent)
    except Exception:
        path.unlink(missing_ok=True)
        raise


def cleanup_spool(path: Path) -> None:
    path.unlink(missing_ok=True)
    if path.parent.exists():
        _fsync_directory(path.parent)


def _response_metadata(envelope: dict[str, Any], response: FakeResponse) -> None:
    envelope.update(
        {
            "state": "RESPONSE_HEADERS_CAPTURED",
            "http_status": response.status,
            "request_id": response.request_id,
            "provider_request_id": response.provider_request_id,
            "returned_model": response.returned_model or "",
            "response_content_type": response.content_type,
            "response_received_at": _now(),
        }
    )


def _usage(envelope: dict[str, Any], parsed: dict[str, Any]) -> None:
    usage = parsed.get("usage") if isinstance(parsed.get("usage"), dict) else {}
    envelope["usage_input_tokens"] = int(
        usage.get("input_tokens", usage.get("prompt_tokens", 0)) or 0
    )
    envelope["usage_output_tokens"] = int(
        usage.get("output_tokens", usage.get("completion_tokens", 0)) or 0
    )
    envelope["usage_total_tokens"] = int(usage.get("total_tokens", 0) or 0)


def _finish(
    envelope: dict[str, Any],
    *,
    writer: AtomicJSONWriter,
    envelope_path: Path,
    spool_path: Path,
    request_sent: bool,
) -> CaptureResult:
    envelope["finalized_at"] = _now()
    try:
        writer.write(envelope_path, envelope)
    except AtomicWriteError:
        envelope.update(
            {
                "state": "FAILED_ATOMIC_WRITE",
                "failure_phase": "PERSISTENCE",
                "outcome_classification": (
                    "RESPONSE_CAPTURE_FAILURE"
                    if request_sent
                    else "FAILED_BEFORE_DISPATCH"
                ),
                "retry_eligibility": (
                    NEW_DECISION_REQUIRED if request_sent else SAFE_REAUTHORIZE
                ),
                "retry_reason": (
                    "POST_DISPATCH_AUDIT_WRITE_FAILED"
                    if request_sent
                    else "DURABLE_ATTEMPT_RECORD_NOT_ESTABLISHED"
                ),
            }
        )
        if not request_sent:
            cleanup_spool(spool_path)
        return CaptureResult(envelope, envelope_path, spool_path, request_sent)
    cleanup_spool(spool_path)
    return CaptureResult(envelope, envelope_path, spool_path, request_sent)


def capture_response(
    *,
    provider: str,
    request: dict[str, Any],
    request_contract: dict[str, Any],
    required_contract_fields: list[str],
    capture_directory: Path,
    schema_path: Path,
    transport: Transport,
    attempt_id: str | None = None,
    writer: AtomicJSONWriter | None = None,
    fail_before_dispatch: bool = False,
    gateway_audit: dict[str, str] | None = None,
) -> CaptureResult:
    """Capture one injected transport call; never retries."""

    capture_directory = capture_directory.resolve()
    attempt = attempt_id or f"capture-{uuid.uuid4().hex}"
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", attempt):
        raise ValueError("attempt_id must be a bounded path-safe identifier")
    envelope_path = capture_directory / f"{attempt}.envelope.json"
    spool_path = capture_directory / f"{attempt}.response.spool"
    requested_model = request.get("model", "") if isinstance(request, dict) else ""
    try:
        request_payload_sha256 = _sha256(_canonical_bytes(request))
    except (TypeError, ValueError):
        request_payload_sha256 = _sha256(b"UNSERIALIZABLE_REQUEST")
    envelope = _base_envelope(
        attempt_id=attempt,
        provider=provider,
        requested_model=requested_model,
        request_payload_sha256=request_payload_sha256,
        request_contract_sha256=_sha256(_canonical_bytes(request_contract)),
        gateway_audit=gateway_audit,
    )
    durable_writer = writer or AtomicJSONWriter()
    request_sent = False

    preflight = request_shape_preflight(
        request,
        capture_directory=capture_directory,
        schema_path=schema_path,
    )
    if preflight["request_shape_preflight"] != "PASS":
        envelope.update(
            {
                "state": "FAILED_BEFORE_DISPATCH",
                "failure_phase": "PRE_DISPATCH",
                "outcome_classification": "FAILED_BEFORE_DISPATCH",
                "retry_eligibility": SAFE_REAUTHORIZE,
                "retry_reason": "REQUEST_OR_CAPTURE_PREFLIGHT_FAILED",
            }
        )
        try:
            return _finish(
                envelope,
                writer=durable_writer,
                envelope_path=envelope_path,
                spool_path=spool_path,
                request_sent=False,
            )
        except AtomicWriteError:
            envelope["state"] = "FAILED_ATOMIC_WRITE"
            envelope["failure_phase"] = "PERSISTENCE"
            envelope["outcome_classification"] = "FAILED_BEFORE_DISPATCH"
            return CaptureResult(envelope, envelope_path, spool_path, False)

    try:
        durable_writer.write(envelope_path, envelope)
        if fail_before_dispatch:
            envelope.update(
                {
                    "state": "FAILED_BEFORE_DISPATCH",
                    "failure_phase": "PRE_DISPATCH",
                    "outcome_classification": "FAILED_BEFORE_DISPATCH",
                    "retry_eligibility": SAFE_REAUTHORIZE,
                    "retry_reason": "INJECTED_FAILURE_BEFORE_DISPATCH",
                }
            )
            return _finish(
                envelope,
                writer=durable_writer,
                envelope_path=envelope_path,
                spool_path=spool_path,
                request_sent=False,
            )
        envelope["state"] = "DISPATCH_STARTED"
        envelope["dispatch_started_at"] = _now()
        envelope["retry_eligibility"] = NEW_DECISION_REQUIRED
        envelope["retry_reason"] = "DISPATCH_STARTED"
        durable_writer.write(envelope_path, envelope)
    except AtomicWriteError:
        envelope["state"] = "FAILED_ATOMIC_WRITE"
        envelope["failure_phase"] = "PERSISTENCE"
        envelope["outcome_classification"] = "FAILED_BEFORE_DISPATCH"
        envelope["retry_eligibility"] = SAFE_REAUTHORIZE
        envelope["retry_reason"] = "DURABLE_DISPATCH_RECORD_NOT_ESTABLISHED"
        return CaptureResult(envelope, envelope_path, spool_path, False)

    request_sent = True
    try:
        response = transport.send(request)
    except HeadersCapturedInterrupt as exc:
        _response_metadata(envelope, exc.response)
        envelope.update(
            {
                "state": "FAILED_AFTER_DISPATCH_OUTCOME_UNKNOWN",
                "failure_phase": "BODY",
                "outcome_classification": "POST_DISPATCH_OUTCOME_UNKNOWN",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "RESPONSE_INTERRUPTED_AFTER_HEADERS",
            }
        )
        return _finish(
            envelope,
            writer=durable_writer,
            envelope_path=envelope_path,
            spool_path=spool_path,
            request_sent=True,
        )
    except (ConnectionError, TimeoutError):
        envelope.update(
            {
                "state": "FAILED_AFTER_DISPATCH_OUTCOME_UNKNOWN",
                "failure_phase": "DISPATCH",
                "outcome_classification": "POST_DISPATCH_OUTCOME_UNKNOWN",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "PROVIDER_EXECUTION_OUTCOME_UNKNOWN",
            }
        )
        return _finish(
            envelope,
            writer=durable_writer,
            envelope_path=envelope_path,
            spool_path=spool_path,
            request_sent=True,
        )

    _response_metadata(envelope, response)
    try:
        durable_writer.write(envelope_path, envelope)
        _write_spool(spool_path, response.body)
    except (AtomicWriteError, OSError):
        envelope.update(
            {
                "state": "FAILED_ATOMIC_WRITE",
                "failure_phase": "PERSISTENCE",
                "outcome_classification": "RESPONSE_CAPTURE_FAILURE",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "POST_DISPATCH_RESPONSE_PERSISTENCE_FAILED",
            }
        )
        return CaptureResult(envelope, envelope_path, spool_path, True)
    envelope.update(
        {
            "state": "RESPONSE_BODY_CAPTURED",
            "response_body_length": len(response.body),
            "response_body_sha256": _sha256(response.body),
            "body_capture_complete": True,
            "body_captured_at": _now(),
        }
    )
    try:
        durable_writer.write(envelope_path, envelope)
    except AtomicWriteError:
        envelope.update(
            {
                "state": "FAILED_ATOMIC_WRITE",
                "failure_phase": "PERSISTENCE",
                "outcome_classification": "RESPONSE_CAPTURE_FAILURE",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "POST_DISPATCH_BODY_METADATA_WRITE_FAILED",
            }
        )
        return CaptureResult(envelope, envelope_path, spool_path, True)
    if response.crash_after_body:
        raise InjectedProcessCrash(envelope_path, spool_path)

    if response.status < 200 or response.status >= 300:
        envelope.update(
            {
                "state": "FAILED_HTTP_RESPONSE_CAPTURED",
                "failure_phase": "HEADERS",
                "outcome_classification": "PROVIDER_HTTP_FAILURE_WITH_RESPONSE",
                "parse_status": "NOT_ASSESSED",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "HTTP_RESPONSE_CAPTURED_AFTER_DISPATCH",
            }
        )
        return _finish(
            envelope,
            writer=durable_writer,
            envelope_path=envelope_path,
            spool_path=spool_path,
            request_sent=True,
        )
    if not response.body:
        envelope.update(
            {
                "state": "FAILED_EMPTY_BODY",
                "failure_phase": "BODY",
                "outcome_classification": "RESPONSE_CAPTURE_FAILURE",
                "parse_status": "FAIL",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "EMPTY_BODY_AFTER_DISPATCH",
            }
        )
        return _finish(
            envelope,
            writer=durable_writer,
            envelope_path=envelope_path,
            spool_path=spool_path,
            request_sent=True,
        )

    try:
        parsed = json.loads(response.body)
    except json.JSONDecodeError:
        envelope.update(
            {
                "state": "FAILED_TRUNCATED_BODY" if response.truncated else "FAILED_PARSE",
                "failure_phase": "PARSE",
                "outcome_classification": "RESPONSE_PARSE_FAILURE",
                "parse_status": "FAIL",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "RESPONSE_JSON_PARSE_FAILED",
            }
        )
        return _finish(
            envelope,
            writer=durable_writer,
            envelope_path=envelope_path,
            spool_path=spool_path,
            request_sent=True,
        )
    if not isinstance(parsed, dict):
        envelope.update(
            {
                "state": "FAILED_PARSE",
                "failure_phase": "PARSE",
                "outcome_classification": "RESPONSE_PARSE_FAILURE",
                "parse_status": "FAIL",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "RESPONSE_ROOT_NOT_OBJECT",
            }
        )
        return _finish(
            envelope,
            writer=durable_writer,
            envelope_path=envelope_path,
            spool_path=spool_path,
            request_sent=True,
        )

    envelope["parse_status"] = "PASS"
    envelope["parsed_at"] = _now()
    if not envelope["returned_model"] and isinstance(parsed.get("model"), str):
        envelope["returned_model"] = parsed["model"]
    if not envelope["returned_model"]:
        envelope.update(
            {
                "state": "FAILED_MODEL_IDENTITY_MISSING",
                "failure_phase": "IDENTITY",
                "outcome_classification": "MODEL_IDENTITY_FAILURE",
                "model_identity_status": "MISSING",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "RETURNED_MODEL_MISSING",
            }
        )
        return _finish(
            envelope,
            writer=durable_writer,
            envelope_path=envelope_path,
            spool_path=spool_path,
            request_sent=True,
        )
    if envelope["returned_model"] != requested_model:
        envelope.update(
            {
                "state": "FAILED_MODEL_IDENTITY_MISMATCH",
                "failure_phase": "IDENTITY",
                "outcome_classification": "MODEL_IDENTITY_FAILURE",
                "model_identity_status": "MISMATCH",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "SILENT_MODEL_FALLBACK_PROHIBITED",
            }
        )
        return _finish(
            envelope,
            writer=durable_writer,
            envelope_path=envelope_path,
            spool_path=spool_path,
            request_sent=True,
        )

    envelope["model_identity_status"] = "MATCH"
    present = [field for field in required_contract_fields if field in parsed]
    envelope["contract_fields_present"] = present
    if len(present) != len(required_contract_fields):
        envelope.update(
            {
                "state": "FAILED_PARSE",
                "failure_phase": "PARSE",
                "outcome_classification": "RESPONSE_PARSE_FAILURE",
                "contract_validation_status": "FAIL",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "REQUIRED_CONTRACT_FIELDS_MISSING",
            }
        )
        return _finish(
            envelope,
            writer=durable_writer,
            envelope_path=envelope_path,
            spool_path=spool_path,
            request_sent=True,
        )

    _usage(envelope, parsed)
    finish_reason = parsed.get("finish_reason")
    if not isinstance(finish_reason, str):
        choices = parsed.get("choices")
        if isinstance(choices, list) and choices and isinstance(choices[0], dict):
            finish_reason = choices[0].get("finish_reason")
    envelope["finish_reason"] = finish_reason if isinstance(finish_reason, str) else ""
    envelope["contract_validation_status"] = "PASS"
    envelope["state"] = "PARSE_COMPLETED"
    try:
        durable_writer.write(envelope_path, envelope)
    except AtomicWriteError:
        envelope.update(
            {
                "state": "FAILED_ATOMIC_WRITE",
                "failure_phase": "PERSISTENCE",
                "outcome_classification": "RESPONSE_CAPTURE_FAILURE",
                "retry_eligibility": NEW_DECISION_REQUIRED,
                "retry_reason": "POST_DISPATCH_PARSE_METADATA_WRITE_FAILED",
            }
        )
        return CaptureResult(envelope, envelope_path, spool_path, True)
    envelope.update(
        {
            "state": "FINALIZED_SUCCESS",
            "failure_phase": "NONE",
            "outcome_classification": "VALID_RESPONSE",
            "retry_eligibility": NOT_APPLICABLE,
            "retry_reason": "",
        }
    )
    return _finish(
        envelope,
        writer=durable_writer,
        envelope_path=envelope_path,
        spool_path=spool_path,
        request_sent=True,
    )


def recover_interrupted_capture(
    envelope_path: Path,
    spool_path: Path,
    *,
    writer: AtomicJSONWriter | None = None,
) -> CaptureResult:
    """Classify an unfinished post-body capture without parsing or retrying."""

    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    if envelope.get("state") not in {
        "RESPONSE_HEADERS_CAPTURED",
        "RESPONSE_BODY_CAPTURED",
        "PARSE_COMPLETED",
    }:
        raise ValueError("capture is not in a recoverable unfinished state")
    if spool_path.is_file():
        body = spool_path.read_bytes()
        envelope["response_body_length"] = len(body)
        envelope["response_body_sha256"] = _sha256(body)
        envelope["body_capture_complete"] = True
    envelope.update(
        {
            "state": "FAILED_RECOVERY_REQUIRED",
            "failure_phase": "RECOVERY",
            "outcome_classification": "RESPONSE_CAPTURE_FAILURE",
            "finalized_at": _now(),
            "retry_eligibility": NEW_DECISION_REQUIRED,
            "retry_reason": "CRASH_AFTER_DISPATCH_REQUIRES_HUMAN_REVIEW",
        }
    )
    durable_writer = writer or AtomicJSONWriter()
    durable_writer.write(envelope_path, envelope)
    return CaptureResult(envelope, envelope_path, spool_path, True)


def replay_cycle_001_failure(
    *,
    capture_directory: Path,
    schema_path: Path,
    writer: AtomicJSONWriter | None = None,
) -> CaptureResult:
    """Deterministically classify the known Cycle 001 post-dispatch failure."""

    request = {
        "model": "qwen3.7-max",
        "messages": [{"role": "user", "content": "public prompt hash only"}],
    }
    envelope = _base_envelope(
        attempt_id="cycle-001-replay",
        provider="ALIBABA_DASHSCOPE",
        requested_model="qwen3.7-max",
        request_payload_sha256=_sha256(_canonical_bytes(request)),
        request_contract_sha256=_sha256(_canonical_bytes({"type": "DISCOVERY"})),
    )
    envelope.update(
        {
            "state": "FAILED_AFTER_DISPATCH_OUTCOME_UNKNOWN",
            "dispatch_started_at": _now(),
            "failure_phase": "DISPATCH",
            "outcome_classification": "POST_DISPATCH_OUTCOME_UNKNOWN",
            "model_identity_status": "NOT_ASSESSED",
            "retry_eligibility": NEW_DECISION_REQUIRED,
            "retry_reason": "REQUEST_SENT_RESPONSE_AND_MODEL_IDENTITY_NOT_CAPTURED",
            "finalized_at": _now(),
        }
    )
    if not _schema_loadable(schema_path):
        raise ValueError("response capture schema unavailable")
    envelope_path = capture_directory / "cycle-001-replay.envelope.json"
    spool_path = capture_directory / "cycle-001-replay.response.spool"
    durable_writer = writer or AtomicJSONWriter()
    durable_writer.write(envelope_path, envelope)
    return CaptureResult(envelope, envelope_path, spool_path, True)
