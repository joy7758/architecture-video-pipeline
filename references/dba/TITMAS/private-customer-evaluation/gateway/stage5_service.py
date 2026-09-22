#!/usr/bin/env python3
"""Private Stage 5 contribution mode for the existing loopback Gateway."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import service
from stage5_workspace import install_stage5_customer_assets


DEFAULT_SCOPES = (
    "standards:read",
    "tasks:read",
    "sandbox:execute",
    "proposal:submit",
    "adapter:submit",
    "test-vector:submit",
    "conformance:execute",
    "review:submit",
    "feedback:submit",
)
PROHIBITED_SCOPES = {
    "core-source:read",
    "private-repository:read",
    "internal-test:read",
    "policy:write",
    "admin",
    "release",
    "deployment",
    "security-setting:write",
    "standard:adopt",
}
ROUTE_SCOPES = {
    "GET /health": "standards:read",
    "GET /v1/capabilities": "standards:read",
    "GET /v1/standards/catalog": "standards:read",
    "GET /v1/standards/tasks": "tasks:read",
    "POST /v1/evaluate": "sandbox:execute",
    "POST /v1/verify": "sandbox:execute",
    "POST /v1/contributions/proposals": "proposal:submit",
    "POST /v1/contributions/adapters": "adapter:submit",
    "POST /v1/contributions/test-vectors": "test-vector:submit",
}
STAGE5_ERRORS = {
    400: "TITMAS-STAGE5-400-MALFORMED",
    401: "TITMAS-STAGE5-401-INVALID-KEY",
    403: "TITMAS-STAGE5-403-SCOPE-DENIED",
    404: "TITMAS-STAGE5-404-NOT-FOUND",
    409: "TITMAS-STAGE5-409-STATE-CONFLICT",
    413: "TITMAS-STAGE5-413-TOO-LARGE",
    422: "TITMAS-STAGE5-422-CONFORMANCE-FAIL",
    429: "TITMAS-STAGE5-429-USAGE-LIMIT",
    500: "TITMAS-STAGE5-500-BOUNDED-FAILURE",
}


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _iso_time(epoch: float) -> str:
    return (
        datetime.fromtimestamp(epoch, timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _load_conformance(project_root: Path):
    path = project_root / "TITMAS" / "conformance" / "stage5_contributions.py"
    spec = importlib.util.spec_from_file_location("titmas_stage5_gateway_conformance", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Stage 5 Conformance extension unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@dataclass
class SandboxKeyBinding:
    principal_ref: str
    agent_ref: str
    scopes: tuple[str, ...]
    allowed_operations: tuple[str, ...]
    usage_limit: int
    expires_at_epoch: float
    data_classification: str = "NONCONFIDENTIAL_SYNTHETIC_STANDARD_CONTRIBUTION"
    revocation_status: str = "ACTIVE"
    token_hash_prefix: str = ""
    usage_count: int = 0

    def authorize(self, scope: str, operation: str) -> bool:
        if (
            self.revocation_status != "ACTIVE"
            or time.time() >= self.expires_at_epoch
            or self.usage_count >= self.usage_limit
        ):
            return False
        return scope in self.scopes and operation in self.allowed_operations

    def consume(self) -> None:
        self.usage_count += 1

    def revoke(self) -> None:
        self.revocation_status = "REVOKED"

    def public_metadata(self) -> dict[str, Any]:
        return {
            "principal_ref": self.principal_ref,
            "agent_ref": self.agent_ref,
            "scopes": list(self.scopes),
            "allowed_operations": list(self.allowed_operations),
            "usage_limit": self.usage_limit,
            "expires_at": _iso_time(self.expires_at_epoch),
            "data_classification": self.data_classification,
            "revocation_status": self.revocation_status,
            "token_hash_prefix": self.token_hash_prefix,
            "sandbox_key_ephemeral": True,
            "sandbox_key_revocable": True,
            "sandbox_key_plaintext_persisted": False,
            "sandbox_key_reused": False,
        }


@dataclass
class ContributionRecord:
    submission_id: str
    contribution_type: str
    contribution: dict[str, Any]
    source: str
    contributor_kind: str
    status: str = "RECEIVED"
    conformance_status: str = "NOT_RUN"
    review_status: str = "NOT_RUN"
    human_disposition_required: bool = True
    reason_codes: list[str] = field(
        default_factory=lambda: ["TITMAS-STAGE5-SUBMISSION-RECEIVED"]
    )
    review: dict[str, Any] | None = None
    limitations: list[str] = field(default_factory=lambda: [
        "PRIVATE_STAGE5_PILOT_ONLY",
        "PILOT_ACCEPTANCE_NE_STANDARD_ADOPTION",
    ])


class ContributionStore:
    """Ephemeral in-memory records; not a database or canonical truth store."""

    def __init__(
        self,
        *,
        id_factory: Callable[[], str] | None = None,
    ):
        self._records: dict[str, ContributionRecord] = {}
        self._id_factory = id_factory or (
            lambda: f"stage5-submission-{uuid.uuid4().hex}"
        )

    def submit(
        self,
        contribution_type: str,
        contribution: dict[str, Any],
        *,
        source: str,
        contributor_kind: str,
    ) -> ContributionRecord:
        submission_id = self._id_factory()
        if submission_id in self._records:
            raise ValueError("duplicate submission id")
        record = ContributionRecord(
            submission_id=submission_id,
            contribution_type=contribution_type,
            contribution=contribution,
            source=source,
            contributor_kind=contributor_kind,
        )
        self._records[submission_id] = record
        return record

    def get(self, submission_id: str) -> ContributionRecord | None:
        return self._records.get(submission_id)


@dataclass
class Stage5GatewayService(service.GatewayService):
    """One private contribution session extending the existing Gateway."""

    principal_ref: str = "zhangbin"
    agent_ref: str = "STAGE5-PROGRAMMATIC-PILOT"
    scopes: tuple[str, ...] = DEFAULT_SCOPES
    sandbox_usage_limit: int = 64
    store: ContributionStore | None = None
    contributor_kind: str = "PROGRAMMATIC"
    sandbox_key: SandboxKeyBinding = field(init=False)
    stage5_assets: dict[str, Path] = field(init=False)
    _stage5_conformance: Any = field(init=False)

    def __post_init__(self) -> None:
        if set(self.scopes) & PROHIBITED_SCOPES:
            raise ValueError("prohibited Sandbox Key scope")
        super().__post_init__()
        self.store = self.store or ContributionStore()
        self.stage5_assets = install_stage5_customer_assets(
            self.project_root, self.workspaces.customer_root
        )
        self._stage5_conformance = _load_conformance(self.project_root)
        allowed = tuple(
            operation
            for operation, scope in ROUTE_SCOPES.items()
            if scope in self.scopes
        )
        dynamic = []
        if "conformance:execute" in self.scopes:
            dynamic.extend(["POST /v1/contributions/{id}/validate"])
        if "review:submit" in self.scopes:
            dynamic.extend(["POST /v1/contributions/{id}/reviews"])
        if {"standards:read", "tasks:read"} & set(self.scopes):
            dynamic.extend([
                "GET /v1/contributions/{id}",
                "GET /v1/contributions/{id}/result",
            ])
        expires_epoch = time.time() + self.session_ttl_seconds
        self.sandbox_key = SandboxKeyBinding(
            principal_ref=self.principal_ref,
            agent_ref=self.agent_ref,
            scopes=tuple(self.scopes),
            allowed_operations=allowed + tuple(dynamic),
            usage_limit=self.sandbox_usage_limit,
            expires_at_epoch=expires_epoch,
            token_hash_prefix=self.session.token_hash_prefix,
        )
        self.session.max_requests = self.sandbox_usage_limit

    def start(self) -> str:
        endpoint = super().start()
        metadata_path = self.workspaces.customer_root / "stage5-session.json"
        metadata_path.write_text(
            json.dumps(
                {
                    "endpoint": endpoint,
                    "key_binding": self.sandbox_key.public_metadata(),
                    "token_delivery": "IN_MEMORY_ONLY",
                    "token_persisted": False,
                    "protocol_surface": "stage5-protocol",
                    "sdk": "stage5-sdk-python",
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            ) + "\n",
            encoding="utf-8",
        )
        metadata_path.chmod(0o600)
        return endpoint

    def stop(self) -> None:
        self.sandbox_key.revoke()
        super().stop()

    def _operation_and_scope(
        self, method: str, route: str
    ) -> tuple[str, str] | None:
        operation = f"{method} {route}"
        if operation in ROUTE_SCOPES:
            return operation, ROUTE_SCOPES[operation]
        parts = route.strip("/").split("/")
        if len(parts) in {3, 4} and parts[:2] == ["v1", "contributions"]:
            if len(parts) == 3 and method == "GET":
                return "GET /v1/contributions/{id}", "standards:read"
            if len(parts) == 4 and parts[3] == "result" and method == "GET":
                return "GET /v1/contributions/{id}/result", "standards:read"
            if len(parts) == 4 and parts[3] == "validate" and method == "POST":
                return "POST /v1/contributions/{id}/validate", "conformance:execute"
            if len(parts) == 4 and parts[3] == "reviews" and method == "POST":
                return "POST /v1/contributions/{id}/reviews", "review:submit"
        return None

    def _dispatch(
        self,
        method: str,
        path: str,
        body: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        route = path.split("?", 1)[0]
        binding = self._operation_and_scope(method, route)
        if binding is None:
            return 403, self._stage5_error(403)
        operation, required_scope = binding
        if not self.sandbox_key.authorize(required_scope, operation):
            return 403, self._stage5_error(403)
        self.sandbox_key.consume()

        if method == "GET" and route == "/v1/standards/catalog":
            return 200, self._surface_json("standard-catalog.json")
        if method == "GET" and route == "/v1/standards/tasks":
            return 200, self._surface_json("task-catalog.json")
        contribution_routes = {
            "/v1/contributions/proposals": "SPECIFICATION_PROPOSAL",
            "/v1/contributions/adapters": "ADAPTER_MAPPING",
            "/v1/contributions/test-vectors": "TEST_VECTOR",
        }
        if method == "POST" and route in contribution_routes:
            if set(body) != {"contribution"} or not isinstance(
                body["contribution"], dict
            ):
                return 400, self._stage5_error(400)
            record = self.store.submit(
                contribution_routes[route],
                body["contribution"],
                source=self.agent_ref,
                contributor_kind=self.contributor_kind,
            )
            return 202, self._status(record)

        parts = route.strip("/").split("/")
        submission_id = parts[2] if len(parts) >= 3 else ""
        record = self.store.get(submission_id)
        if record is None:
            return 404, self._stage5_error(404)
        if method == "GET" and len(parts) == 3:
            return 200, self._status(record)
        if method == "POST" and len(parts) == 4 and parts[3] == "validate":
            if body:
                return 400, self._stage5_error(400)
            result = self._stage5_conformance.validate_contribution(
                record.contribution_type, record.contribution
            )
            record.conformance_status = result["conformance_status"]
            record.reason_codes = result["reason_codes"]
            if record.conformance_status == "CONFORMANCE_PASS":
                record.status = "HUMAN_DISPOSITION_REQUIRED"
                record.human_disposition_required = True
                return 200, self._result(record)
            record.status = "CONFORMANCE_FAIL"
            record.human_disposition_required = False
            return 422, self._result(record)
        if method == "POST" and len(parts) == 4 and parts[3] == "reviews":
            if record.conformance_status != "CONFORMANCE_PASS":
                return 409, self._stage5_error(409)
            if set(body) != {"review"} or not isinstance(body["review"], dict):
                return 400, self._stage5_error(400)
            validation = self._stage5_conformance.validate_review(body["review"])
            if not validation["valid"] or body["review"]["submission_id"] != submission_id:
                return 422, self._stage5_error(422)
            record.review = body["review"]
            record.review_status = body["review"]["verdict"]
            record.status = "HUMAN_DISPOSITION_REQUIRED"
            record.reason_codes = validation["reason_codes"]
            record.human_disposition_required = True
            return 200, self._result(record)
        if method == "GET" and len(parts) == 4 and parts[3] == "result":
            return 200, self._result(record)
        return 403, self._stage5_error(403)

    def _surface_json(self, name: str) -> dict[str, Any]:
        return json.loads(
            (self.stage5_assets["protocol_surface"] / name).read_text(
                encoding="utf-8"
            )
        )

    @staticmethod
    def _status(record: ContributionRecord) -> dict[str, Any]:
        return {
            "submission_id": record.submission_id,
            "contribution_type": record.contribution_type,
            "status": record.status,
            "conformance_status": record.conformance_status,
            "review_status": record.review_status,
            "human_disposition_required": record.human_disposition_required,
            "limitations": record.limitations,
        }

    def _result(self, record: ContributionRecord) -> dict[str, Any]:
        projection = {
            **self._status(record),
            "reason_codes": record.reason_codes,
            "limitations": record.limitations,
        }
        hashes = {
            "submission_sha256": _sha256(_canonical_bytes(record.contribution)),
            "result_sha256": _sha256(_canonical_bytes(projection)),
        }
        result = {
            "submission_id": record.submission_id,
            "contribution_type": record.contribution_type,
            "status": record.status,
            "conformance_status": record.conformance_status,
            "review_status": record.review_status,
            "human_disposition_required": record.human_disposition_required,
            "reason_codes": record.reason_codes,
            "hashes": hashes,
            "limitations": record.limitations,
        }
        harness = self._stage5_conformance._load_harness()
        schema = json.loads(
            (
                self.project_root
                / "TITMAS"
                / "conformance"
                / "schemas"
                / "stage5-contribution-result.schema.json"
            ).read_text(encoding="utf-8")
        )
        harness.validate_schema(result, schema)
        return result

    @staticmethod
    def _stage5_error(status: int) -> dict[str, Any]:
        return {
            "error": {
                "code": STAGE5_ERRORS[status],
                "message": "Request rejected by the bounded Stage 5 contract.",
            }
        }
