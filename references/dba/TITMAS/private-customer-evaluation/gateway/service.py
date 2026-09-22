#!/usr/bin/env python3
"""Loopback-only, one-session TITMAS private evaluation facade.

This module is a local synthetic black-box surface. It is not an Agent
Runtime, control plane, truth source, public API, or production service.
"""

from __future__ import annotations

import hashlib
import hmac
import importlib.util
import json
import secrets
import sys
import threading
import time
import uuid
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from workspace import IsolatedWorkspaces, create_isolated_workspaces


LOOPBACK_HOST = "127.0.0.1"
CONTRACT_VERSION = "0.1.0"
SYNTHETIC_PROFILE = "TITMAS-SYNTHETIC-CANDIDATE-v0.1"
MAX_REQUEST_BYTES = 65_536
LOCAL_MODEL_ID = "titmas-local-evaluation-facade"

CAPABILITIES = (
    "evaluate synthetic candidate",
    "validate declared contract",
    "produce bounded verification result",
    "return limitations",
)

ERRORS = {
    400: "TITMAS-EVAL-400-MALFORMED-REQUEST",
    401: "TITMAS-EVAL-401-INVALID-SESSION",
    403: "TITMAS-EVAL-403-OPERATION-NOT-ALLOWED",
    404: "TITMAS-EVAL-404-PROFILE-NOT-AVAILABLE",
    409: "TITMAS-EVAL-409-CONTRACT-VERSION-CONFLICT",
    413: "TITMAS-EVAL-413-REQUEST-TOO-LARGE",
    422: "TITMAS-EVAL-422-NOT-ASSESSABLE",
    429: "TITMAS-EVAL-429-SESSION-LIMIT",
    500: "TITMAS-EVAL-500-BOUNDED-INTERNAL-FAILURE",
}


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _load_response_capture(project_root: Path):
    path = (
        project_root
        / "TITMAS"
        / "agent-native"
        / "customer-cycle"
        / "response_capture.py"
    )
    spec = importlib.util.spec_from_file_location("titmas_gateway_response_capture", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("response capture unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@dataclass
class CustomerSession:
    customer_session_id: str
    token: str | None
    token_hash_prefix: str
    expires_at: float
    max_requests: int = 32
    request_count: int = 0
    revoked: bool = False

    def authorize(self, supplied: str | None) -> bool:
        if self.revoked or self.token is None or time.monotonic() >= self.expires_at:
            return False
        return supplied is not None and hmac.compare_digest(self.token, supplied)

    def revoke(self) -> None:
        self.revoked = True
        self.token = None


@dataclass
class GatewayService:
    """Own one loopback server, one customer session, and two temp workspaces."""

    project_root: Path
    host: str = LOOPBACK_HOST
    session_ttl_seconds: float = 300.0
    workspaces: IsolatedWorkspaces = field(init=False)
    session: CustomerSession = field(init=False)
    endpoint: str = field(init=False, default="")
    audit_log: list[dict[str, str]] = field(init=False, default_factory=list)
    _server: ThreadingHTTPServer | None = field(init=False, default=None)
    _thread: threading.Thread | None = field(init=False, default=None)
    _response_capture: Any = field(init=False)
    _attempt_counter: int = field(init=False, default=0)
    _force_internal_failure: bool = field(init=False, default=False)

    def __post_init__(self) -> None:
        if self.host != LOOPBACK_HOST:
            raise ValueError("gateway host must be 127.0.0.1")
        self.project_root = self.project_root.resolve()
        bundle_source = self.project_root / "TITMAS" / "private-customer-evaluation"
        self.workspaces = create_isolated_workspaces(bundle_source)
        self._response_capture = _load_response_capture(self.project_root)
        token = secrets.token_urlsafe(32)
        token_hash = _sha256(token.encode("utf-8"))
        self.session = CustomerSession(
            customer_session_id=f"customer-session-{uuid.uuid4().hex}",
            token=token,
            token_hash_prefix=token_hash[:12],
            expires_at=time.monotonic() + self.session_ttl_seconds,
        )
        self.audit_log.append(
            {
                "event": "SESSION_CREATED",
                "token_hash_prefix": self.session.token_hash_prefix,
            }
        )

    @property
    def customer_token(self) -> str:
        if self.session.token is None:
            raise RuntimeError("customer session is not active")
        return self.session.token

    @property
    def bound_address(self) -> tuple[str, int]:
        if self._server is None:
            raise RuntimeError("gateway is not started")
        host, port = self._server.server_address[:2]
        return str(host), int(port)

    def start(self) -> str:
        if self._server is not None:
            raise RuntimeError("gateway already started")
        service = self

        class Handler(BaseHTTPRequestHandler):
            server_version = "TITMAS-Evaluation"
            sys_version = ""

            def log_message(self, format: str, *args: object) -> None:
                del format, args

            def do_GET(self) -> None:
                service._handle(self)

            def do_POST(self) -> None:
                service._handle(self)

            def do_PUT(self) -> None:
                service._handle(self)

            def do_DELETE(self) -> None:
                service._handle(self)

        self._server = ThreadingHTTPServer((self.host, 0), Handler)
        self._server.daemon_threads = True
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            name="titmas-private-evaluation",
            daemon=True,
        )
        self._thread.start()
        host, port = self.bound_address
        self.endpoint = f"http://{host}:{port}"
        session_materials = {
            "customer_session_id": self.session.customer_session_id,
            "endpoint": self.endpoint,
            "authorization_scheme": "Bearer",
            "token_delivery": "IN_MEMORY_ONLY",
            "token_persisted": False,
            "scope": "EVALUATION_ONLY",
        }
        session_path = self.workspaces.customer_root / "session.json"
        session_path.write_text(
            json.dumps(
                session_materials,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        session_path.chmod(0o600)
        return self.endpoint

    def stop(self) -> None:
        self.session.revoke()
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        if self._thread is not None:
            self._thread.join(timeout=2)
            self._thread = None
        self.audit_log.append(
            {
                "event": "SESSION_REVOKED",
                "token_hash_prefix": self.session.token_hash_prefix,
            }
        )
        self.endpoint = ""
        self.workspaces.cleanup()

    def _supplied_token(self, handler: BaseHTTPRequestHandler) -> str | None:
        value = handler.headers.get("Authorization", "")
        if not value.startswith("Bearer "):
            return None
        return value[7:]

    def _read_body(
        self,
        handler: BaseHTTPRequestHandler,
    ) -> tuple[dict[str, Any] | None, bytes, int | None]:
        if handler.command != "POST":
            return {}, b"", None
        length_text = handler.headers.get("Content-Length")
        try:
            length = int(length_text or "")
        except ValueError:
            return None, b"", 400
        if length < 0:
            return None, b"", 400
        if length > MAX_REQUEST_BYTES:
            return None, b"", 413
        body = handler.rfile.read(length)
        try:
            parsed = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None, body, 400
        if not isinstance(parsed, dict):
            return None, body, 400
        return parsed, body, None

    def _handle(self, handler: BaseHTTPRequestHandler) -> None:
        body = b""
        parsed: dict[str, Any] = {}
        status = 500
        payload: dict[str, Any] = self._error(500)
        try:
            parsed_value, body, read_error = self._read_body(handler)
            parsed = parsed_value or {}
            if read_error is not None:
                status, payload = read_error, self._error(read_error)
            elif not self.session.authorize(self._supplied_token(handler)):
                status, payload = 401, self._error(401)
            elif self.session.request_count >= self.session.max_requests:
                status, payload = 429, self._error(429)
            else:
                self.session.request_count += 1
                status, payload = self._dispatch(handler.command, handler.path, parsed)
        except Exception:
            status, payload = 500, self._error(500)

        response_bytes = _canonical_bytes(payload)
        operation = f"{handler.command} {handler.path.split('?', 1)[0]}"
        try:
            self._capture(
                operation=operation,
                request_body=body,
                response_status=status,
                response_body=response_bytes,
            )
        except Exception:
            status, payload = 500, self._error(500)
            response_bytes = _canonical_bytes(payload)
        self._write_response(handler, status, response_bytes)

    def _dispatch(
        self,
        method: str,
        path: str,
        body: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        route = path.split("?", 1)[0]
        if self._force_internal_failure:
            raise RuntimeError("injected private implementation detail")
        if method == "GET" and route == "/health":
            return 200, {
                "status": "ready",
                "mode": "private-evaluation",
                "maturity": "development",
            }
        if method == "GET" and route == "/v1/capabilities":
            return 200, {
                "contract_version": CONTRACT_VERSION,
                "capabilities": list(CAPABILITIES),
            }
        if method == "POST" and route == "/v1/evaluate":
            return self._evaluate(body)
        if method == "POST" and route == "/v1/verify":
            return self._verify(body)
        return 403, self._error(403)

    def _evaluate(self, body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        required = {
            "synthetic_request_id",
            "declared_object",
            "declared_profile",
            "contract_version",
            "options",
        }
        if set(body) != required:
            return 400, self._error(400)
        if body["contract_version"] != CONTRACT_VERSION:
            return 409, self._error(409)
        if body["declared_profile"] != SYNTHETIC_PROFILE:
            return 404, self._error(404)
        if (
            not isinstance(body["synthetic_request_id"], str)
            or not body["synthetic_request_id"]
            or not isinstance(body["declared_object"], dict)
            or not isinstance(body["options"], dict)
            or not set(body["options"]).issubset({"include_limitations"})
        ):
            return 400, self._error(400)
        if not body["declared_object"] or body["declared_object"].get("assessable") is False:
            return 422, self._error(422)
        request_hash = _sha256(_canonical_bytes(body))
        return 200, {
            "accepted_request_id": body["synthetic_request_id"],
            "result_status": "CONDITIONALLY_RECOMMENDED",
            "public_reason_code": "SYNTHETIC_CONTRACT_MATCH_WITH_LIMITATIONS",
            "limitations": [
                "SYNTHETIC_INPUT_ONLY",
                "NOT_EVIDENCE_TRUTH",
                "NOT_AUTHORIZATION",
                "NOT_CUSTOMER_ADOPTION",
            ],
            "correlation_id": f"corr-{request_hash[:16]}",
        }

    def _verify(self, body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        if set(body) != {"verification_object", "expected_contract_version"}:
            return 400, self._error(400)
        if body["expected_contract_version"] != CONTRACT_VERSION:
            return 409, self._error(409)
        value = body["verification_object"]
        if not isinstance(value, dict):
            return 400, self._error(400)
        conformant = value.get("contract_conformant")
        if conformant is True:
            result = "PASS"
        elif conformant is False:
            result = "FAIL"
        else:
            result = "NOT_ASSESSED"
        return 200, {
            "contract_version": CONTRACT_VERSION,
            "verification_result": result,
            "limitations": [
                "VERIFICATION_IS_NOT_AUTHORIZATION",
                "EVIDENCE_IS_NOT_TRUTH",
            ],
        }

    def _capture(
        self,
        *,
        operation: str,
        request_body: bytes,
        response_status: int,
        response_body: bytes,
    ) -> None:
        self._attempt_counter += 1
        attempt_id = f"gateway-{self._attempt_counter:04d}"
        request_body_sha256 = _sha256(request_body)
        public_contract = {
            "contract_version": CONTRACT_VERSION,
            "operation": operation,
            "response": "BOUNDED_PUBLIC_JSON",
        }
        carrier_request = {
            "model": LOCAL_MODEL_ID,
            "messages": [
                {
                    "role": "user",
                    "content": f"request_body_sha256:{request_body_sha256}",
                }
            ],
            "temperature": 0,
            "stream": False,
        }
        parsed_response = json.loads(response_body)
        required_fields = list(parsed_response)
        transport = self._response_capture.FakeProvider(
            status=response_status,
            request_id=attempt_id,
            provider_request_id=f"local-{attempt_id}",
            returned_model=LOCAL_MODEL_ID,
            body=response_body,
        )
        result = self._response_capture.capture_response(
            provider="TITMAS_LOCAL_EVALUATION_FACADE",
            request=carrier_request,
            request_contract=public_contract,
            required_contract_fields=required_fields,
            capture_directory=self.workspaces.capture_directory,
            schema_path=(
                self.project_root
                / "TITMAS"
                / "agent-native"
                / "customer-cycle"
                / "response-capture-envelope.schema.json"
            ),
            transport=transport,
            attempt_id=attempt_id,
            gateway_audit={
                "customer_session_id": self.session.customer_session_id,
                "requested_operation": operation,
                "request_body_sha256": request_body_sha256,
            },
        )
        if result.envelope["response_body_sha256"] != _sha256(response_body):
            raise RuntimeError("bounded response capture mismatch")
        self.audit_log.append(
            {
                "event": "REQUEST_CAPTURED",
                "attempt_id": attempt_id,
                "token_hash_prefix": self.session.token_hash_prefix,
                "final_state": result.envelope["final_state"],
            }
        )

    @staticmethod
    def _error(status: int) -> dict[str, Any]:
        return {
            "error": {
                "code": ERRORS[status],
                "message": "Request rejected by the bounded evaluation contract.",
            }
        }

    @staticmethod
    def _write_response(
        handler: BaseHTTPRequestHandler,
        status: int,
        response_bytes: bytes,
    ) -> None:
        handler.send_response(status)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Content-Length", str(len(response_bytes)))
        handler.send_header("Cache-Control", "no-store")
        handler.end_headers()
        handler.wfile.write(response_bytes)
