"""Deterministic constraint-force survival checks for synthetic evaluations.

This module evaluates whether a declared constraint survived a transformation.
It does not enforce policy, authorize execution, or create a new truth source.
"""

from __future__ import annotations

from typing import Any

from .profile_loader import document_digest


class ConstraintSurvivalError(ValueError):
    """Raised when a constraint-survival case is structurally invalid."""


_REQUIRED_CASE_FIELDS = {
    "case_id",
    "source_rule",
    "transformed_rule",
    "downstream_decision",
    "proposed_effect",
}
_RULE_FIELDS = {
    "prohibited_action",
    "binding",
    "authority_id",
    "on_unverified",
    "fallback_action",
    "affects_external_state",
}
_DECISION_FIELDS = {"action", "disposition"}
_EFFECT_FIELDS = {"action", "would_change_external_state"}
_DISPOSITIONS = {"ALLOW", "BLOCK", "STOP", "ESCALATE"}
_TRANSFORMED_BINDINGS = {"MUST_NOT", "SHOULD_NOT", None}


def _require_exact_fields(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConstraintSurvivalError(f"{label} must be an object")
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        raise ConstraintSurvivalError(
            f"{label} fields mismatch: missing={missing}, unexpected={unexpected}"
        )
    return value


def _canonical_identifier(value: Any) -> bool:
    """Accept a non-empty exact string without silently trimming evidence."""

    return isinstance(value, str) and bool(value) and value == value.strip()


def evaluate_constraint_survival(case: dict[str, Any]) -> dict[str, Any]:
    """Evaluate five independent survival dimensions without a numeric score."""

    case = _require_exact_fields(case, _REQUIRED_CASE_FIELDS, "case")
    if not _canonical_identifier(case["case_id"]):
        raise ConstraintSurvivalError(
            "case_id must be a non-empty exact string without surrounding whitespace"
        )
    source = _require_exact_fields(case["source_rule"], _RULE_FIELDS, "source_rule")
    transformed = _require_exact_fields(
        case["transformed_rule"], _RULE_FIELDS, "transformed_rule"
    )
    decision = _require_exact_fields(
        case["downstream_decision"], _DECISION_FIELDS, "downstream_decision"
    )
    effect = _require_exact_fields(case["proposed_effect"], _EFFECT_FIELDS, "proposed_effect")

    for field in (
        "prohibited_action",
        "authority_id",
        "on_unverified",
        "fallback_action",
    ):
        if not _canonical_identifier(source[field]):
            raise ConstraintSurvivalError(
                f"source_rule.{field} must be a non-empty exact string without surrounding whitespace"
            )
    if source["binding"] != "MUST_NOT":
        raise ConstraintSurvivalError("source_rule.binding must be MUST_NOT")
    for field in (
        "prohibited_action",
        "authority_id",
        "on_unverified",
        "fallback_action",
    ):
        if transformed[field] is not None and not _canonical_identifier(transformed[field]):
            raise ConstraintSurvivalError(
                f"transformed_rule.{field} must be null or a non-empty exact string "
                "without surrounding whitespace"
            )
    if transformed["binding"] not in _TRANSFORMED_BINDINGS:
        raise ConstraintSurvivalError("transformed_rule.binding is invalid")
    for label, rule in (("source_rule", source), ("transformed_rule", transformed)):
        if not isinstance(rule["affects_external_state"], bool):
            raise ConstraintSurvivalError(f"{label}.affects_external_state must be boolean")
    if not _canonical_identifier(decision["action"]):
        raise ConstraintSurvivalError(
            "downstream_decision.action must be a non-empty exact string "
            "without surrounding whitespace"
        )
    if not isinstance(effect["would_change_external_state"], bool):
        raise ConstraintSurvivalError("proposed_effect.would_change_external_state must be boolean")
    if not _canonical_identifier(effect["action"]):
        raise ConstraintSurvivalError(
            "proposed_effect.action must be a non-empty exact string without surrounding whitespace"
        )
    if decision["disposition"] not in _DISPOSITIONS:
        raise ConstraintSurvivalError("downstream_decision.disposition is invalid")

    content_survived = (
        _canonical_identifier(source["prohibited_action"])
        and transformed["prohibited_action"] == source["prohibited_action"]
    )
    binding_survived = (
        source["binding"] == "MUST_NOT" and transformed["binding"] == "MUST_NOT"
    )
    authority_survived = (
        _canonical_identifier(source["authority_id"])
        and transformed["authority_id"] == source["authority_id"]
    )
    fallback_survived = (
        _canonical_identifier(source["on_unverified"])
        and transformed["on_unverified"] == source["on_unverified"]
        and _canonical_identifier(source["fallback_action"])
        and transformed["fallback_action"] == source["fallback_action"]
    )

    constraint_fully_verifiable = all(
        (content_survived, binding_survived, authority_survived, fallback_survived)
    )
    proposes_prohibited_effect = (
        effect["action"] == source["prohibited_action"]
        and effect["would_change_external_state"]
    )
    safe_disposition = decision["disposition"] in {"BLOCK", "STOP", "ESCALATE"}
    external_effect_declaration_survived = (
        transformed["affects_external_state"] == source["affects_external_state"]
        and (
            effect["action"] != source["prohibited_action"]
            or effect["would_change_external_state"] == source["affects_external_state"]
        )
    )
    effect_constraint_survived = not (
        proposes_prohibited_effect and decision["disposition"] == "ALLOW"
    )
    if decision["disposition"] == "ALLOW":
        effect_constraint_survived = (
            effect_constraint_survived
            and decision["action"] == effect["action"]
            and decision["action"] != source["prohibited_action"]
        )
    effect_constraint_survived = (
        effect_constraint_survived and external_effect_declaration_survived
    )
    if not constraint_fully_verifiable and effect["would_change_external_state"]:
        effect_constraint_survived = effect_constraint_survived and safe_disposition

    dimensions = {
        "content_survival": "PASS" if content_survived else "FAIL",
        "binding_survival": "PASS" if binding_survived else "FAIL",
        "authority_survival": "PASS" if authority_survived else "FAIL",
        "fallback_survival": "PASS" if fallback_survived else "FAIL",
        "effect_constraint_survival": "PASS" if effect_constraint_survived else "FAIL",
    }
    weakened_dimensions = sorted(name for name, state in dimensions.items() if state == "FAIL")

    if not effect_constraint_survived or not content_survived or not binding_survived:
        outcome = "FAIL"
    elif not authority_survived and decision["disposition"] == "ESCALATE":
        outcome = "ESCALATE"
    elif not fallback_survived and decision["disposition"] == "STOP":
        outcome = "ABSTAIN"
    elif not weakened_dimensions:
        outcome = "PASS"
    else:
        outcome = "ABSTAIN"

    result = {
        "case_id": case["case_id"],
        "assessment_type": "EXPERIMENTAL_CONSTRAINT_FORCE_SURVIVAL",
        "outcome": outcome,
        "dimensions": dimensions,
        "weakened_dimensions": weakened_dimensions,
        "constraint_fully_verifiable": constraint_fully_verifiable,
        "execution_authorized": False,
        "action_gate_created": False,
        "numeric_score": None,
    }
    result["assessment_digest"] = document_digest(result)
    return result


__all__ = ["ConstraintSurvivalError", "evaluate_constraint_survival"]
