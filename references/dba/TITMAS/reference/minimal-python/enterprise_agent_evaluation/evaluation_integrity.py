"""Typed evaluation stop states and multi-dimensional result integrity."""

from __future__ import annotations

from typing import Any

from .profile_loader import document_digest


class EvaluationIntegrityError(ValueError):
    """Raised when an evaluation-integrity case is structurally invalid."""


DIMENSIONS = (
    "answer_correctness",
    "trace_validity",
    "artifact_linkage",
    "evidence_sufficiency",
)
DIMENSION_STATES = {"PASS", "FAIL", "NOT_ASSESSED"}
STOP_STATES = {
    "EVIDENCE_INSUFFICIENT",
    "SEMANTICS_UNGROUNDED",
    "NON_COMPARABLE",
    "NON_IDENTIFIABLE",
    "ABSTAIN",
}


def _require_exact_fields(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EvaluationIntegrityError(f"{label} must be an object")
    actual = set(value)
    if actual != expected:
        raise EvaluationIntegrityError(
            f"{label} fields mismatch: missing={sorted(expected - actual)}, "
            f"unexpected={sorted(actual - expected)}"
        )
    return value


def evaluate_integrity(case: dict[str, Any]) -> dict[str, Any]:
    """Preserve dimension failures and stop rather than inventing a score."""

    case = _require_exact_fields(
        case,
        {
            "case_id",
            "dimensions",
            "semantic_grounding",
            "comparable",
            "identifiable",
            "abstain_requested",
            "stop_reason",
            "missing_evidence",
        },
        "case",
    )
    if not isinstance(case["case_id"], str) or not case["case_id"].strip():
        raise EvaluationIntegrityError("case_id must be a non-empty string")
    dimensions = _require_exact_fields(case["dimensions"], set(DIMENSIONS), "dimensions")
    for name, state in dimensions.items():
        if state not in DIMENSION_STATES:
            raise EvaluationIntegrityError(f"dimensions.{name} is invalid")
    for name in ("semantic_grounding", "comparable", "identifiable", "abstain_requested"):
        if not isinstance(case[name], bool):
            raise EvaluationIntegrityError(f"{name} must be boolean")
    if case["stop_reason"] is not None and (
        not isinstance(case["stop_reason"], str) or not case["stop_reason"].strip()
    ):
        raise EvaluationIntegrityError("stop_reason must be a non-empty string or null")
    if not isinstance(case["missing_evidence"], list) or any(
        not isinstance(item, str) or not item.strip() for item in case["missing_evidence"]
    ):
        raise EvaluationIntegrityError("missing_evidence must contain non-empty strings")

    stop_state: str | None = None
    if case["abstain_requested"]:
        stop_state = "ABSTAIN"
    elif dimensions["evidence_sufficiency"] in {"FAIL", "NOT_ASSESSED"}:
        stop_state = "EVIDENCE_INSUFFICIENT"
    elif not case["semantic_grounding"]:
        stop_state = "SEMANTICS_UNGROUNDED"
    elif not case["comparable"]:
        stop_state = "NON_COMPARABLE"
    elif not case["identifiable"]:
        stop_state = "NON_IDENTIFIABLE"

    if stop_state is not None and case["stop_reason"] is None:
        raise EvaluationIntegrityError("typed stop requires an explicit stop_reason")
    if stop_state == "EVIDENCE_INSUFFICIENT" and not case["missing_evidence"]:
        raise EvaluationIntegrityError(
            "EVIDENCE_INSUFFICIENT requires at least one missing_evidence item"
        )
    if stop_state is None and (case["stop_reason"] is not None or case["missing_evidence"]):
        raise EvaluationIntegrityError(
            "stop_reason and missing_evidence are allowed only for a typed stop"
        )

    if stop_state is not None:
        derived_outcome = "EVALUATION_STOPPED"
    elif dimensions["artifact_linkage"] == "FAIL":
        derived_outcome = "INCOMPLETE_ARTIFACT_BINDING"
    elif dimensions["answer_correctness"] == "PASS" and dimensions["trace_validity"] == "FAIL":
        derived_outcome = "ANSWER_CORRECT_TRACE_INVALID"
    elif dimensions["answer_correctness"] == "FAIL" and dimensions["trace_validity"] == "PASS":
        derived_outcome = "ANSWER_INCORRECT_TRACE_VALID"
    elif all(state == "PASS" for state in dimensions.values()):
        derived_outcome = "COMPLETE_FOR_DECLARED_SCOPE"
    else:
        derived_outcome = "MULTI_DIMENSIONAL_FAILURE"

    result = {
        "case_id": case["case_id"],
        "assessment_type": "EXPERIMENTAL_EVALUATION_INTEGRITY",
        "evaluation_status": "STOPPED" if stop_state else "EVALUATED",
        "stop_state": stop_state,
        "stop_reason": case["stop_reason"] if stop_state else None,
        "missing_evidence": sorted(set(case["missing_evidence"])) if stop_state else [],
        "dimensions": {name: dimensions[name] for name in DIMENSIONS},
        "derived_outcome": derived_outcome,
        "numeric_score": None,
        "ranking_eligible": False,
        "ranking_system_created": False,
        "ordinary_execution_failure": False,
        "overall_status_is_derived": True,
    }
    result["assessment_digest"] = document_digest(result)
    return result


__all__ = [
    "DIMENSIONS",
    "EvaluationIntegrityError",
    "STOP_STATES",
    "evaluate_integrity",
]
