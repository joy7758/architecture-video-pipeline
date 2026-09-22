#!/usr/bin/env python3
"""Run the deterministic Stage 5 programmatic gate before any model call."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _load_runtime(project_root: Path):
    gateway_dir = (
        project_root
        / "TITMAS"
        / "private-customer-evaluation"
        / "gateway"
    )
    sdk_dir = project_root / "TITMAS" / "private-stage5-sdk" / "python"
    for path in (gateway_dir, sdk_dir):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    import stage5_service  # type: ignore
    import titmas_stage5_sdk  # type: ignore

    return stage5_service, titmas_stage5_sdk


def _client(service_instance: Any, sdk_module: Any):
    endpoint = service_instance.start()
    return sdk_module.Stage5Client(
        endpoint,
        service_instance.session.token,
        service_instance.stage5_assets["protocol_surface"] / "schemas",
    )


def _scenario(
    scenario_id: str,
    expected: str,
    observed: str,
    *,
    submission_id: str | None = None,
    status_code: int | None = None,
) -> dict[str, Any]:
    result = {
        "scenario_id": scenario_id,
        "expected": expected,
        "observed": observed,
        "pass": expected == observed,
    }
    if submission_id is not None:
        result["submission_id"] = submission_id
    if status_code is not None:
        result["status_code"] = status_code
    return result


def run_programmatic_pilot(
    project_root: Path,
    output_directory: Path,
) -> dict[str, Any]:
    """Execute exactly five synthetic local scenarios and persist sanitized output."""

    project_root = project_root.resolve()
    output_directory.mkdir(parents=True, exist_ok=True)
    output_directory.chmod(0o700)
    stage5_service, sdk = _load_runtime(project_root)
    examples = json.loads(
        (
            project_root
            / "TITMAS"
            / "private-stage5-protocol-surface"
            / "synthetic-examples.json"
        ).read_text(encoding="utf-8")
    )
    id_values = iter(
        (
            "stage5-submission-P01-PROPOSAL",
            "stage5-submission-P01-ADAPTER",
            "stage5-submission-P01-INVALID-VECTOR",
        )
    )
    store = stage5_service.ContributionStore(id_factory=lambda: next(id_values))
    scenarios: list[dict[str, Any]] = []
    registry: list[dict[str, Any]] = []

    primary = stage5_service.Stage5GatewayService(
        project_root,
        store=store,
        agent_ref="STAGE5-P01-PROGRAMMATIC",
        contributor_kind="PROGRAMMATIC",
    )
    try:
        client = _client(primary, sdk)

        proposal_status = client.submit_proposal(examples["specification_proposal"])
        proposal_result = client.validate_submission(
            proposal_status["submission_id"]
        )
        proposal_observed = (
            "CONFORMANCE_PASS_HUMAN_DISPOSITION_REQUIRED"
            if proposal_result["conformance_status"] == "CONFORMANCE_PASS"
            and proposal_result["human_disposition_required"] is True
            else "UNEXPECTED"
        )
        scenarios.append(
            _scenario(
                "P01-A-VALID-PROPOSAL",
                "CONFORMANCE_PASS_HUMAN_DISPOSITION_REQUIRED",
                proposal_observed,
                submission_id=proposal_status["submission_id"],
            )
        )
        registry.append(
            {
                "submission_id": proposal_status["submission_id"],
                "type": "SPECIFICATION_PROPOSAL",
                "source": "SYNTHETIC_P01",
                "contributor_kind": "PROGRAMMATIC",
                "conformance_status": proposal_result["conformance_status"],
                "review_status": "NOT_RUN",
                "human_disposition": "REQUIRED",
                "pilot_status": "PILOT_ACCEPTED",
                "hashes": proposal_result["hashes"],
                "limitations": proposal_result["limitations"],
            }
        )

        adapter_status = client.submit_adapter_mapping(examples["adapter_mapping"])
        adapter_result = client.validate_submission(adapter_status["submission_id"])
        adapter_observed = (
            "CONFORMANCE_PASS_HUMAN_DISPOSITION_REQUIRED"
            if adapter_result["conformance_status"] == "CONFORMANCE_PASS"
            and adapter_result["human_disposition_required"] is True
            else "UNEXPECTED"
        )
        scenarios.append(
            _scenario(
                "P01-B-VALID-ADAPTER",
                "CONFORMANCE_PASS_HUMAN_DISPOSITION_REQUIRED",
                adapter_observed,
                submission_id=adapter_status["submission_id"],
            )
        )
        registry.append(
            {
                "submission_id": adapter_status["submission_id"],
                "type": "ADAPTER_MAPPING",
                "source": "SYNTHETIC_P01",
                "contributor_kind": "PROGRAMMATIC",
                "conformance_status": adapter_result["conformance_status"],
                "review_status": "NOT_RUN",
                "human_disposition": "REQUIRED",
                "pilot_status": "PILOT_ACCEPTED",
                "hashes": adapter_result["hashes"],
                "limitations": adapter_result["limitations"],
            }
        )

        invalid_vector = dict(examples["test_vector"])
        invalid_vector["failure_classification"] = "NONE"
        vector_status = client.submit_test_vector(invalid_vector)
        try:
            client.validate_submission(vector_status["submission_id"])
            vector_observed = "UNEXPECTED_ACCEPTANCE"
            vector_status_code = 200
        except sdk.TITMASClientError as exc:
            vector_observed = (
                "EXPECTED_CONFORMANCE_REJECTION"
                if exc.status == 422
                else "UNEXPECTED_REJECTION"
            )
            vector_status_code = exc.status
        vector_result = client.get_submission_result(vector_status["submission_id"])
        scenarios.append(
            _scenario(
                "P01-C-INVALID-TEST-VECTOR",
                "EXPECTED_CONFORMANCE_REJECTION",
                vector_observed,
                submission_id=vector_status["submission_id"],
                status_code=vector_status_code,
            )
        )
        registry.append(
            {
                "submission_id": vector_status["submission_id"],
                "type": "TEST_VECTOR",
                "source": "SYNTHETIC_P01",
                "contributor_kind": "PROGRAMMATIC",
                "conformance_status": vector_result["conformance_status"],
                "review_status": "NOT_RUN",
                "human_disposition": "NOT_APPLICABLE",
                "pilot_status": "PILOT_REJECTED",
                "hashes": vector_result["hashes"],
                "limitations": vector_result["limitations"],
            }
        )
    finally:
        primary.stop()

    restricted = stage5_service.Stage5GatewayService(
        project_root,
        scopes=("standards:read", "tasks:read"),
        agent_ref="STAGE5-P01-RESTRICTED",
    )
    try:
        restricted_client = _client(restricted, sdk)
        try:
            restricted_client.submit_adapter_mapping(examples["adapter_mapping"])
            scope_observed = "UNEXPECTED_ACCEPTANCE"
            scope_status = 200
        except sdk.TITMASClientError as exc:
            scope_observed = (
                "EXPECTED_SCOPE_REJECTION"
                if exc.status == 403
                else "UNEXPECTED_REJECTION"
            )
            scope_status = exc.status
        scenarios.append(
            _scenario(
                "P01-D-UNAUTHORIZED-SCOPE",
                "EXPECTED_SCOPE_REJECTION",
                scope_observed,
                status_code=scope_status,
            )
        )
    finally:
        restricted.stop()

    expired = stage5_service.Stage5GatewayService(
        project_root,
        agent_ref="STAGE5-P01-EXPIRED",
    )
    try:
        expired_client = _client(expired, sdk)
        expired.session.expires_at = time.monotonic() - 1
        try:
            expired_client.get_standard_catalog()
            expiry_observed = "UNEXPECTED_ACCEPTANCE"
            expiry_status = 200
        except sdk.TITMASClientError as exc:
            expiry_observed = (
                "EXPECTED_EXPIRED_KEY_REJECTION"
                if exc.status == 401
                else "UNEXPECTED_REJECTION"
            )
            expiry_status = exc.status
        scenarios.append(
            _scenario(
                "P01-E-EXPIRED-KEY",
                "EXPECTED_EXPIRED_KEY_REJECTION",
                expiry_observed,
                status_code=expiry_status,
            )
        )
    finally:
        expired.stop()

    passed = sum(item["pass"] is True for item in scenarios)
    valid_submissions = sum(
        item["pilot_status"] == "PILOT_ACCEPTED" for item in registry
    )
    expected_rejections = sum(
        item["scenario_id"]
        in {
            "P01-C-INVALID-TEST-VECTOR",
            "P01-D-UNAUTHORIZED-SCOPE",
            "P01-E-EXPIRED-KEY",
        }
        and item["pass"] is True
        for item in scenarios
    )
    program_pass = (
        len(scenarios) == 5
        and passed == 5
        and valid_submissions == 2
        and expected_rejections == 3
    )
    report = {
        "report_type": "TITMAS_STAGE5_PROGRAMMATIC_PILOT",
        "report_version": "1.0",
        "run_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "data_classification": "PRIVATE_AUDIT_SYNTHETIC",
        "synthetic_only": True,
        "scenarios": scenarios,
        "scenario_count": len(scenarios),
        "scenario_pass_count": passed,
        "valid_submission_count": valid_submissions,
        "expected_rejection_count": expected_rejections,
        "core_access_count": 0,
        "real_model_call_count": 0,
        "automatic_retry_count": 0,
        "programmatic_pilot_pass": program_pass,
        "limitations": [
            "PROGRAMMATIC_GATE_ONLY",
            "NO_REAL_MODEL_INVOLVEMENT",
            "PILOT_ACCEPTANCE_NE_STANDARD_ADOPTION",
            "HUMAN_DISPOSITION_REQUIRED_FOR_VALID_SUBMISSIONS",
        ],
    }
    registry_document = {
        "registry_type": "TITMAS_STAGE5_PRIVATE_PILOT_CONTRIBUTION_REGISTRY",
        "registry_version": "1.0",
        "data_classification": "PRIVATE_AUDIT_SYNTHETIC",
        "entries": registry,
    }
    report["registry_sha256"] = _sha256(registry_document)

    report_path = output_directory / "programmatic-pilot-report.json"
    registry_path = output_directory / "pilot-contribution-registry.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    registry_path.write_text(
        json.dumps(
            registry_document, ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n",
        encoding="utf-8",
    )
    for path in (report_path, registry_path):
        path.chmod(0o600)
    return report


def main() -> int:
    project_root = Path(__file__).resolve().parents[2]
    output_directory = Path(__file__).resolve().parent / "programmatic-results"
    report = run_programmatic_pilot(project_root, output_directory)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["programmatic_pilot_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
