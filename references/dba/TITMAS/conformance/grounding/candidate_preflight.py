#!/usr/bin/env python3
"""Community contribution grounding and reviewer evidence gate.

This module is deterministic and local. It does not call a model, modify
authority, merge a contribution, publish a release, or write outside an
isolated candidate copy.
"""

from __future__ import annotations

import json
import hashlib
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Callable

from local_resource_resolver import LocalResourceResolver


CANDIDATE_STATUSES = {
    "CANDIDATE_PRODUCED",
    "ABSTAINED_INSUFFICIENT_CONTEXT",
    "ABSTAINED_NO_VALID_TARGET",
    "ABSTAINED_OUT_OF_SCOPE",
}
ABSTENTION_STATUSES = CANDIDATE_STATUSES - {"CANDIDATE_PRODUCED"}
REVIEWER_VERDICTS = {
    "PASS",
    "REVISION_REQUIRED",
    "REJECT",
    "ABSTAIN_INSUFFICIENT_EVIDENCE",
}
GROUNDING_STATUSES = {
    "GROUNDED",
    "PARTIALLY_GROUNDED",
    "UNGROUNDED",
    "NOT_ASSESSED",
}
FORBIDDEN_CLAIMS = {
    "VALUE_PROVEN=true",
    "PUBLIC_LAUNCH_AUTHORIZED=true",
    "COMMUNITY_ESTABLISHED=true",
    "RELEASE_AUTHORIZED=true",
    "RESOURCE_RESOLUTION_RECEIPT_IS_TRUTH=true",
    "RESOURCE_RESOLUTION_RECEIPT_IS_AUTHORITY=true",
}


class GroundingContractError(ValueError):
    """Stable fail-closed contract error."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def candidate_hash(value: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _is_safe_candidate_path(value: str) -> bool:
    normalized, status = LocalResourceResolver.normalize_reference(value)
    return status == "VALID" and normalized == value


def validate_contributor_candidate_v11(
    candidate: dict[str, Any],
    allowed_candidate_files: set[str] | None = None,
) -> None:
    required = {
        "candidate_status",
        "finding_disposition",
        "candidate_files",
        "reference_claims",
        "created_resources",
        "modified_resources",
        "abstention_reason",
        "rationale",
        "limitations",
        "validation_plan",
    }
    if set(candidate) != required:
        raise GroundingContractError("CONTRIBUTOR_V11_FIELD_SET_INVALID")
    status = candidate["candidate_status"]
    if status not in CANDIDATE_STATUSES:
        raise GroundingContractError("CONTRIBUTOR_STATUS_INVALID")
    if not isinstance(candidate["candidate_files"], dict):
        raise GroundingContractError("CANDIDATE_FILES_NOT_OBJECT")
    if not isinstance(candidate["reference_claims"], list):
        raise GroundingContractError("REFERENCE_CLAIMS_NOT_ARRAY")
    for field in (
        "created_resources",
        "modified_resources",
        "limitations",
        "validation_plan",
    ):
        if not isinstance(candidate[field], list) or not all(
            isinstance(item, str) for item in candidate[field]
        ):
            raise GroundingContractError(f"{field.upper()}_NOT_STRING_ARRAY")
    for field in ("finding_disposition", "abstention_reason", "rationale"):
        if not isinstance(candidate[field], str):
            raise GroundingContractError(f"{field.upper()}_NOT_STRING")
    if status == "CANDIDATE_PRODUCED":
        if not candidate["candidate_files"]:
            raise GroundingContractError("PRODUCED_CANDIDATE_FILES_EMPTY")
        if candidate["abstention_reason"] != "NOT_APPLICABLE":
            raise GroundingContractError("PRODUCED_CANDIDATE_HAS_ABSTENTION_REASON")
        if not candidate["limitations"]:
            raise GroundingContractError("PRODUCED_CANDIDATE_LIMITATIONS_REQUIRED")
    else:
        if candidate["candidate_files"]:
            raise GroundingContractError("ABSTENTION_CANDIDATE_FILES_NOT_EMPTY")
        if not candidate["abstention_reason"]:
            raise GroundingContractError("ABSTENTION_REASON_REQUIRED")
    for name in candidate["candidate_files"]:
        if not _is_safe_candidate_path(name):
            raise GroundingContractError("CANDIDATE_PATH_INVALID")
        if allowed_candidate_files is not None and name not in allowed_candidate_files:
            raise GroundingContractError("CANDIDATE_SCOPE_EXPANSION")
    declared_created = set(candidate["created_resources"])
    declared_modified = set(candidate["modified_resources"])
    if any(
        not _is_safe_candidate_path(item)
        for item in declared_created | declared_modified
    ):
        raise GroundingContractError("DECLARED_RESOURCE_PATH_INVALID")
    if declared_created & declared_modified:
        raise GroundingContractError("RESOURCE_DECLARATION_OVERLAP")
    if declared_created | declared_modified != set(candidate["candidate_files"]):
        raise GroundingContractError("RESOURCE_DECLARATION_MISMATCH")
    for index, claim in enumerate(candidate["reference_claims"]):
        if not isinstance(claim, dict) or set(claim) != {
            "reference",
            "reference_type",
            "required_for_candidate",
            "expected_resolution_status",
            "justification",
        }:
            raise GroundingContractError(f"REFERENCE_CLAIM_{index}_INVALID")
        if not isinstance(claim["reference"], str) or not claim["reference"]:
            raise GroundingContractError(f"REFERENCE_CLAIM_{index}_EMPTY")
        if not isinstance(claim["required_for_candidate"], bool):
            raise GroundingContractError(f"REFERENCE_CLAIM_{index}_REQUIRED_NOT_BOOLEAN")
        if claim["expected_resolution_status"] not in {
            "RESOLVED",
            "NOT_FOUND",
            "AMBIGUOUS",
            "OUT_OF_SCOPE",
            "INVALID_REFERENCE",
            "NOT_ASSESSED",
        }:
            raise GroundingContractError(f"REFERENCE_CLAIM_{index}_STATUS_INVALID")
    serialized = canonical(candidate)
    for claim in FORBIDDEN_CLAIMS:
        if claim in serialized:
            raise GroundingContractError("SEMANTIC_ELEVATION_PROHIBITED")


def _machine_surface_references(value: Any) -> list[str]:
    result: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "machine_surfaces" and isinstance(child, dict):
                result.extend(
                    item for item in child.values() if isinstance(item, str)
                )
            result.extend(_machine_surface_references(child))
    elif isinstance(value, list):
        for item in value:
            result.extend(_machine_surface_references(item))
    return result


def _write_candidate_file(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        path.write_text(value, encoding="utf-8")
    else:
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def _candidate_parse_errors(candidate_root: Path, names: list[str]) -> list[str]:
    errors: list[str] = []
    for name in names:
        path = candidate_root / name
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"CANDIDATE_READ_FAILED:{name}")
            continue
        suffix = path.suffix.lower()
        if suffix == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError:
                errors.append(f"CANDIDATE_JSON_INVALID:{name}")
        elif suffix in {".yaml", ".yml"}:
            if "\t" in text or re.search(r"(^|\n)<<<<<<< ", text):
                errors.append(f"CANDIDATE_YAML_INVALID:{name}")
        elif suffix == ".md" and "\x00" in text:
            errors.append(f"CANDIDATE_MARKDOWN_INVALID:{name}")
    return errors


def _receipt_with_phase(receipt: dict[str, Any], phase: str) -> dict[str, Any]:
    return {**receipt, "resolution_phase": phase}


def run_candidate_preflight(
    candidate: dict[str, Any],
    dba_root: Path,
    source_revision: str,
    allowed_source_revision: str,
    allowed_roots: list[str],
    allowed_candidate_files: set[str] | None = None,
    created_at: str = "2026-07-29T00:00:00+08:00",
) -> dict[str, Any]:
    """Run schema, scope, resolution, apply and incremental conformance."""

    candidate_ref = "CC-" + LocalResourceResolver.normalize_reference(
        next(iter(candidate.get("candidate_files", {})), "ABSTENTION")
    )[0].replace("/", "-")
    errors: list[str] = []
    warnings: list[str] = []
    try:
        validate_contributor_candidate_v11(candidate, allowed_candidate_files)
    except GroundingContractError as exc:
        return {
            "preflight_id": "PF-CONTRACT-REJECTED",
            "candidate_ref": candidate_ref,
            "schema_status": "REJECTED",
            "scope_status": "NOT_ASSESSED",
            "resolution_receipts": [],
            "unresolved_required_references": [],
            "candidate_apply_status": "NOT_ASSESSED",
            "incremental_conformance_status": "NOT_ASSESSED",
            "errors": [exc.code],
            "warnings": [],
            "limitations": [
                "DETERMINISTIC_PREFLIGHT_ONLY",
                "PREFLIGHT_NE_FINAL_CONFORMANCE",
                "PREFLIGHT_NE_AGENT_NATIVE_VALUE_PROOF",
            ],
            "status": "REJECTED",
        }
    if candidate["candidate_status"] in ABSTENTION_STATUSES:
        return {
            "preflight_id": "PF-ABSTENTION-PASS",
            "candidate_ref": candidate_ref,
            "schema_status": "PASS",
            "scope_status": "PASS",
            "resolution_receipts": [],
            "unresolved_required_references": [],
            "candidate_apply_status": "NOT_APPLICABLE",
            "incremental_conformance_status": "PASS",
            "errors": [],
            "warnings": ["ABSTENTION_NE_FAILURE"],
            "limitations": [
                "NO_CANDIDATE_CREATED",
                "DETERMINISTIC_PREFLIGHT_ONLY",
                "PREFLIGHT_NE_AGENT_NATIVE_VALUE_PROOF",
            ],
            "status": "PASS",
        }

    temp_root = Path(tempfile.mkdtemp(prefix="titmas-candidate-preflight-"))
    try:
        pre_resolver = LocalResourceResolver(
            dba_root=dba_root,
            source_revision=source_revision,
            allowed_source_revision=allowed_source_revision,
            allowed_roots=allowed_roots,
            candidate_root=temp_root,
            created_at=created_at,
        )
        receipts: list[dict[str, Any]] = []
        for claim in candidate["reference_claims"]:
            receipts.append(
                _receipt_with_phase(
                    pre_resolver.resolve(
                        claim["reference"],
                        claim["reference_type"],
                        claim["required_for_candidate"],
                    ),
                    "BEFORE_CANDIDATE_APPLY",
                )
            )

        apply_status = "PASS"
        try:
            for name, value in candidate["candidate_files"].items():
                _write_candidate_file(temp_root / name, value)
        except (OSError, UnicodeError, TypeError, ValueError):
            apply_status = "FAIL"
            errors.append("CANDIDATE_APPLY_FAILED")

        post_resolver = LocalResourceResolver(
            dba_root=dba_root,
            source_revision=source_revision,
            allowed_source_revision=allowed_source_revision,
            allowed_roots=allowed_roots,
            candidate_root=temp_root,
            created_at=created_at,
        )
        post_receipts: list[dict[str, Any]] = []
        for claim in candidate["reference_claims"]:
            post_receipts.append(
                _receipt_with_phase(
                    post_resolver.resolve(
                        claim["reference"],
                        claim["reference_type"],
                        claim["required_for_candidate"],
                    ),
                    "AFTER_CANDIDATE_APPLY",
                )
            )
        receipts.extend(post_receipts)
        unresolved = [
            receipt["reference"]
            for receipt in post_receipts
            if receipt["required_for_candidate"]
            and receipt["status"] != "RESOLVED"
        ]
        if unresolved:
            errors.append("REQUIRED_REFERENCE_UNRESOLVED")

        errors.extend(
            _candidate_parse_errors(
                temp_root,
                sorted(candidate["candidate_files"]),
            )
        )
        claimed = {item["reference"] for item in candidate["reference_claims"]}
        machine_refs = {
            ref
            for value in candidate["candidate_files"].values()
            for ref in _machine_surface_references(value)
        }
        if machine_refs - claimed:
            errors.append("MACHINE_SURFACE_REFERENCE_CLAIM_MISSING")
        if any(
            path
            in {
                "TITMAS/community/community-status.json",
                "TITMAS/specifications/registry.yaml",
                "TITMAS/agent-native/tasks/task-registry.json",
            }
            for path in candidate["candidate_files"]
        ):
            errors.append("CANONICAL_SURFACE_DIRECT_MODIFICATION_PROHIBITED")
        if source_revision != allowed_source_revision:
            errors.append("SOURCE_REVISION_DRIFT")
        if apply_status != "PASS":
            errors.append("CANDIDATE_APPLY_NOT_SUCCESSFUL")
        incremental_status = "PASS" if not errors else "FAIL"
        hard_reject = any(
            item
            in {
                "CANONICAL_SURFACE_DIRECT_MODIFICATION_PROHIBITED",
                "SOURCE_REVISION_DRIFT",
                "CANDIDATE_APPLY_NOT_SUCCESSFUL",
            }
            for item in errors
        ) or any(
            receipt["status"] in {"OUT_OF_SCOPE", "INVALID_REFERENCE"}
            for receipt in post_receipts
            if receipt["required_for_candidate"]
        )
        status = (
            "PASS"
            if incremental_status == "PASS"
            else ("REJECTED" if hard_reject else "REVISION_REQUIRED")
        )
        return {
            "preflight_id": "PF-"
            + post_resolver.snapshot_hash.replace("git-tree:", "")[:16],
            "candidate_ref": candidate_ref,
            "schema_status": "PASS",
            "scope_status": "PASS",
            "resolution_receipts": receipts,
            "unresolved_required_references": sorted(set(unresolved)),
            "candidate_apply_status": apply_status,
            "incremental_conformance_status": incremental_status,
            "errors": sorted(set(errors)),
            "warnings": warnings,
            "limitations": [
                "DETERMINISTIC_PREFLIGHT_ONLY",
                "LOCAL_FROZEN_SNAPSHOT_ONLY",
                "PREFLIGHT_NE_FINAL_CONFORMANCE",
                "PREFLIGHT_NE_AGENT_NATIVE_VALUE_PROOF",
            ],
            "status": status,
        }
    finally:
        shutil.rmtree(temp_root)


def run_preflight_with_single_revision(
    initial_candidate: dict[str, Any],
    revision_candidate: dict[str, Any] | None,
    **preflight_kwargs: Any,
) -> dict[str, Any]:
    """Allow at most one deterministic revision, then stop fail-closed."""

    first = run_candidate_preflight(
        candidate=initial_candidate,
        **preflight_kwargs,
    )
    if first["status"] == "PASS":
        return {
            "status": "PASS",
            "revision_count": 0,
            "attempts": [first],
            "candidate_hashes": [candidate_hash(initial_candidate)],
            "review_stage_allowed": True,
            "reason_code": "INITIAL_PREFLIGHT_PASS",
        }
    if revision_candidate is None:
        return {
            "status": first["status"],
            "revision_count": 0,
            "attempts": [first],
            "candidate_hashes": [candidate_hash(initial_candidate)],
            "review_stage_allowed": False,
            "reason_code": "REVISION_REQUIRED_NOT_PROVIDED",
        }
    second = run_candidate_preflight(
        candidate=revision_candidate,
        **preflight_kwargs,
    )
    if second["status"] == "PASS":
        return {
            "status": "PASS",
            "revision_count": 1,
            "attempts": [first, second],
            "candidate_hashes": [
                candidate_hash(initial_candidate),
                candidate_hash(revision_candidate),
            ],
            "review_stage_allowed": True,
            "reason_code": "BOUNDED_REVISION_PREFLIGHT_PASS",
        }
    return {
        "status": "REJECTED",
        "revision_count": 1,
        "attempts": [first, second],
        "candidate_hashes": [
            candidate_hash(initial_candidate),
            candidate_hash(revision_candidate),
        ],
        "review_stage_allowed": False,
        "reason_code": "TASK_ENDED_AFTER_BOUNDED_REVISION_FAILURE",
    }


def validate_reviewer_assessment_v11(
    assessment: dict[str, Any],
    preflight: dict[str, Any],
) -> None:
    required = {
        "verdict",
        "caught_issues",
        "semantic_elevation_detected",
        "harmful_candidate",
        "required_corrections",
        "limitations",
        "reviewed_artifact_refs",
        "preflight_result_ref",
        "checks_performed",
        "verified_resource_refs",
        "resolution_receipt_refs",
        "unverified_claims",
        "abstention_reason",
    }
    if set(assessment) != required:
        raise GroundingContractError("REVIEWER_V11_FIELD_SET_INVALID")
    if assessment["verdict"] not in REVIEWER_VERDICTS:
        raise GroundingContractError("REVIEWER_VERDICT_INVALID")
    array_fields = required - {
        "verdict",
        "semantic_elevation_detected",
        "harmful_candidate",
        "preflight_result_ref",
        "abstention_reason",
    }
    for field in array_fields:
        if not isinstance(assessment[field], list) or not all(
            isinstance(item, str) for item in assessment[field]
        ):
            raise GroundingContractError(f"REVIEWER_{field.upper()}_INVALID")
    if assessment["preflight_result_ref"] != preflight["preflight_id"]:
        raise GroundingContractError("REVIEWER_PREFLIGHT_REFERENCE_MISMATCH")
    if assessment["verdict"] == "PASS":
        if preflight["status"] != "PASS":
            raise GroundingContractError("REVIEW_PASS_WITH_PREFLIGHT_NOT_PASS")
        if preflight["unresolved_required_references"]:
            raise GroundingContractError("REVIEW_PASS_WITH_UNRESOLVED_REFERENCE")
        required_receipts = {
            item["resolution_id"]
            for item in preflight["resolution_receipts"]
            if item["resolution_phase"] == "AFTER_CANDIDATE_APPLY"
            and item["required_for_candidate"]
        }
        if not required_receipts.issubset(
            set(assessment["resolution_receipt_refs"])
        ):
            raise GroundingContractError("REVIEW_PASS_RECEIPT_REFERENCE_MISSING")
        if not assessment["checks_performed"]:
            raise GroundingContractError("REVIEW_PASS_CHECKS_NOT_RECORDED")
        if assessment["unverified_claims"]:
            raise GroundingContractError("REVIEW_PASS_WITH_UNVERIFIED_CLAIMS")
    if assessment["verdict"] == "ABSTAIN_INSUFFICIENT_EVIDENCE":
        if not assessment["abstention_reason"]:
            raise GroundingContractError("REVIEWER_ABSTENTION_REASON_REQUIRED")


def validate_handoff_v11(handoff: dict[str, Any]) -> None:
    for field in (
        "grounding_status",
        "resource_resolution_receipt_refs",
        "preflight_result_ref",
        "unresolved_required_references",
        "from_role",
        "to_role",
    ):
        if field not in handoff:
            raise GroundingContractError(f"HANDOFF_{field.upper()}_MISSING")
    if handoff["grounding_status"] not in GROUNDING_STATUSES:
        raise GroundingContractError("HANDOFF_GROUNDING_STATUS_INVALID")
    if (
        handoff["from_role"] in {"Contributor", "RevisionResponse"}
        and handoff["to_role"] == "Reviewer"
        and handoff["grounding_status"] != "GROUNDED"
    ):
        raise GroundingContractError("HANDOFF_COMMIT_REJECTED")
    if (
        handoff["grounding_status"] == "GROUNDED"
        and handoff["unresolved_required_references"]
    ):
        raise GroundingContractError("GROUNDED_HANDOFF_HAS_UNRESOLVED_REFERENCE")


def complete_candidate_validation(
    preflight: dict[str, Any],
    reviewer: dict[str, Any] | None,
    final_conformance: dict[str, Any],
) -> dict[str, Any]:
    if preflight["status"] != "PASS":
        return {
            "status": "FAIL_CLOSED",
            "review_stage_reached": False,
            "reason_code": "PREFLIGHT_NOT_PASS",
        }
    if reviewer is None:
        return {
            "status": "FAIL_CLOSED",
            "review_stage_reached": False,
            "reason_code": "REVIEWER_RESULT_MISSING",
        }
    validate_reviewer_assessment_v11(reviewer, preflight)
    if reviewer["verdict"] != "PASS":
        return {
            "status": "FAIL_CLOSED",
            "review_stage_reached": True,
            "reason_code": "REVIEW_NOT_PASS",
        }
    if final_conformance.get("status") != "PASS":
        return {
            "status": "FAIL_CLOSED",
            "review_stage_reached": True,
            "reason_code": "FINAL_CONFORMANCE_FAILED_AFTER_INCREMENTAL_PASS",
        }
    return {
        "status": "PASS",
        "review_stage_reached": True,
        "reason_code": "PREFLIGHT_REVIEW_FINAL_CONFORMANCE_PASS",
    }


def compute_review_catch_metrics(
    records: list[dict[str, Any]],
    instrumentation_complete: bool = True,
) -> dict[str, Any]:
    if not instrumentation_complete:
        return {
            "review_opportunity_count": "NOT_ASSESSED",
            "review_catch_count": "NOT_ASSESSED",
            "review_miss_count": "NOT_ASSESSED",
            "preflight_catch_count": sum(
                bool(item.get("preflight_caught")) for item in records
            ),
            "review_catch_rate": "NOT_ASSESSED_INSTRUMENTATION_DEFECT",
            "measurement_status": "NOT_ASSESSED_INSTRUMENTATION_DEFECT",
        }
    preflight_catches = sum(bool(item.get("preflight_caught")) for item in records)
    reached = [item for item in records if item.get("review_stage_reached")]
    opportunities = [
        item
        for item in reached
        if not item.get("preflight_caught")
        and bool(item.get("reviewer_opportunity"))
    ]
    catches = sum(bool(item.get("reviewer_caught")) for item in opportunities)
    misses = len(opportunities) - catches
    if not reached:
        rate: float | str = "NOT_APPLICABLE"
        status = "NOT_APPLICABLE_REVIEW_STAGE_NOT_REACHED"
    elif not opportunities:
        rate = "NOT_APPLICABLE"
        status = "NOT_APPLICABLE_NO_REVIEWER_OPPORTUNITY"
    else:
        rate = catches / len(opportunities)
        status = "ASSESSED"
    return {
        "review_opportunity_count": len(opportunities),
        "review_catch_count": catches,
        "review_miss_count": misses,
        "preflight_catch_count": preflight_catches,
        "review_catch_rate": rate,
        "measurement_status": status,
    }


__all__ = [
    "GroundingContractError",
    "complete_candidate_validation",
    "compute_review_catch_metrics",
    "run_candidate_preflight",
    "run_preflight_with_single_revision",
    "validate_contributor_candidate_v11",
    "validate_handoff_v11",
    "validate_reviewer_assessment_v11",
]
