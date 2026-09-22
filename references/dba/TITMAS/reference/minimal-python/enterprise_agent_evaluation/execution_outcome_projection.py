"""Experimental execution-result evidence projection beside frozen EEOAP.

The sidecar keeps command acceptance, completion, report, effect, and settled
outcome distinct.  It references an existing statement and never mutates or
extends the EEOAP v0.1 core object.
"""

from __future__ import annotations

from typing import Any

from .profile_loader import document_digest


class ExecutionOutcomeProjectionError(ValueError):
    """Raised when an experimental outcome projection is structurally invalid."""


LAYER_NAMES = (
    "command_accepted",
    "execution_completed",
    "reported_state",
    "observed_effect",
    "settled_outcome",
)
LAYER_STATES = {
    "NOT_APPLICABLE",
    "NOT_OBSERVED",
    "UNVERIFIED",
    "VERIFIED",
    "CONTRADICTED",
}
LEGACY_MAPPING_LAYERS = {"command_accepted", "execution_completed", "reported_state"}
WITNESS_TYPES = {
    "SYSTEM_REPORT",
    "INDEPENDENT_OBSERVER",
    "SENSOR",
    "STATE_STORE",
    "MODEL_JUDGE",
    "SIMULATOR",
}
INDEPENDENCE_STATES = {"INDEPENDENT", "SHARED_DEPENDENCY", "NOT_ASSESSED"}
REALITY_WITNESSES = {"INDEPENDENT_OBSERVER", "SENSOR", "STATE_STORE"}


def _require_exact_fields(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ExecutionOutcomeProjectionError(f"{label} must be an object")
    actual = set(value)
    if actual != expected:
        raise ExecutionOutcomeProjectionError(
            f"{label} fields mismatch: missing={sorted(expected - actual)}, "
            f"unexpected={sorted(actual - expected)}"
        )
    return value


def _present_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def evaluate_execution_outcome_projection(case: dict[str, Any]) -> dict[str, Any]:
    """Validate semantics and project layered outcome evidence deterministically."""

    case = _require_exact_fields(
        case,
        {
            "case_id",
            "source_statement_id",
            "legacy_success",
            "legacy_success_maps_to",
            "layers",
            "evidence_sources",
        },
        "case",
    )
    if not _present_string(case["case_id"]) or not _present_string(case["source_statement_id"]):
        raise ExecutionOutcomeProjectionError("case_id and source_statement_id are required")
    if case["legacy_success"] is not None and not isinstance(case["legacy_success"], bool):
        raise ExecutionOutcomeProjectionError("legacy_success must be boolean or null")

    layers = _require_exact_fields(case["layers"], set(LAYER_NAMES), "layers")
    normalized_layers: dict[str, dict[str, Any]] = {}
    referenced_by: dict[str, list[str]] = {}
    for layer_name in LAYER_NAMES:
        layer = _require_exact_fields(
            layers[layer_name], {"state", "evidence_refs"}, f"layers.{layer_name}"
        )
        if layer["state"] not in LAYER_STATES:
            raise ExecutionOutcomeProjectionError(f"layers.{layer_name}.state is invalid")
        if not isinstance(layer["evidence_refs"], list) or any(
            not _present_string(item) for item in layer["evidence_refs"]
        ):
            raise ExecutionOutcomeProjectionError(
                f"layers.{layer_name}.evidence_refs must contain non-empty strings"
            )
        if len(set(layer["evidence_refs"])) != len(layer["evidence_refs"]):
            raise ExecutionOutcomeProjectionError(f"layers.{layer_name} has duplicate evidence refs")
        normalized_layers[layer_name] = {
            "state": layer["state"],
            "evidence_refs": sorted(layer["evidence_refs"]),
        }
        for evidence_ref in layer["evidence_refs"]:
            referenced_by.setdefault(evidence_ref, []).append(layer_name)

    if not isinstance(case["evidence_sources"], list):
        raise ExecutionOutcomeProjectionError("evidence_sources must be an array")
    sources: dict[str, dict[str, Any]] = {}
    for index, raw_source in enumerate(case["evidence_sources"]):
        source = _require_exact_fields(
            raw_source,
            {
                "evidence_ref",
                "witness_type",
                "observer_id",
                "claim_scope",
                "observation_window",
                "settlement_delay_ms",
                "verifier_independence",
                "shared_dependency",
            },
            f"evidence_sources[{index}]",
        )
        evidence_ref = source["evidence_ref"]
        if not _present_string(evidence_ref) or evidence_ref in sources:
            raise ExecutionOutcomeProjectionError("evidence_ref must be non-empty and unique")
        if source["witness_type"] not in WITNESS_TYPES:
            raise ExecutionOutcomeProjectionError(f"{evidence_ref} has invalid witness_type")
        if not _present_string(source["observer_id"]):
            raise ExecutionOutcomeProjectionError(f"{evidence_ref} needs observer_id")
        if source["claim_scope"] not in LAYER_NAMES:
            raise ExecutionOutcomeProjectionError(f"{evidence_ref} has unscoped or aggregate evidence")
        window = source["observation_window"]
        if window is not None:
            _require_exact_fields(window, {"start", "end"}, f"{evidence_ref}.observation_window")
            if not _present_string(window["start"]) or not _present_string(window["end"]):
                raise ExecutionOutcomeProjectionError(f"{evidence_ref} has invalid observation window")
        delay = source["settlement_delay_ms"]
        if not isinstance(delay, int) or isinstance(delay, bool) or delay < 0:
            raise ExecutionOutcomeProjectionError(f"{evidence_ref} has invalid settlement delay")
        if source["verifier_independence"] not in INDEPENDENCE_STATES:
            raise ExecutionOutcomeProjectionError(f"{evidence_ref} has invalid independence state")
        dependency = source["shared_dependency"]
        if dependency is not None and not _present_string(dependency):
            raise ExecutionOutcomeProjectionError(f"{evidence_ref} has invalid shared_dependency")
        if dependency is not None and source["verifier_independence"] == "INDEPENDENT":
            raise ExecutionOutcomeProjectionError(
                f"{evidence_ref} cannot be independent while declaring a shared dependency"
            )
        if dependency is None and source["verifier_independence"] == "SHARED_DEPENDENCY":
            raise ExecutionOutcomeProjectionError(
                f"{evidence_ref} declares shared dependence without a dependency id"
            )
        sources[evidence_ref] = source

    issues: list[str] = []
    for evidence_ref, layer_names in sorted(referenced_by.items()):
        source = sources.get(evidence_ref)
        if source is None:
            issues.append(f"UNKNOWN_EVIDENCE_REF:{evidence_ref}")
            continue
        if len(layer_names) != 1 or source["claim_scope"] != layer_names[0]:
            issues.append(f"EVIDENCE_SCOPE_MISMATCH:{evidence_ref}")
    for evidence_ref in sorted(set(sources) - set(referenced_by)):
        issues.append(f"UNBOUND_EVIDENCE_SOURCE:{evidence_ref}")

    for layer_name, layer in normalized_layers.items():
        if layer["state"] in {"VERIFIED", "CONTRADICTED"} and not layer["evidence_refs"]:
            issues.append(f"EVIDENCE_REQUIRED:{layer_name}")
        if layer["state"] in {"NOT_APPLICABLE", "NOT_OBSERVED"} and layer["evidence_refs"]:
            issues.append(f"EVIDENCE_NOT_ALLOWED_FOR_STATE:{layer_name}")

    for layer_name in ("observed_effect", "settled_outcome"):
        layer = normalized_layers[layer_name]
        if layer["state"] in {"VERIFIED", "CONTRADICTED"}:
            if not any(
                sources.get(ref, {}).get("witness_type") in REALITY_WITNESSES
                for ref in layer["evidence_refs"]
            ):
                issues.append(f"REALITY_WITNESS_REQUIRED:{layer_name}")

    system_report_observers = {
        source["observer_id"]
        for source in sources.values()
        if source["witness_type"] == "SYSTEM_REPORT"
    }
    independent_candidates: dict[str, list[str]] = {}
    for evidence_ref, source in sources.items():
        if (
            source["witness_type"] in REALITY_WITNESSES
            and source["verifier_independence"] == "INDEPENDENT"
            and source["shared_dependency"] is None
        ):
            independent_candidates.setdefault(source["observer_id"], []).append(evidence_ref)
            if source["observer_id"] in system_report_observers:
                issues.append(f"SELF_REPORT_NOT_INDEPENDENT:{evidence_ref}")
    independent_observers = sorted(
        observer_id
        for observer_id in independent_candidates
        if observer_id not in system_report_observers
    )
    independent_reality_sources = sorted(
        evidence_ref
        for observer_id, evidence_refs in independent_candidates.items()
        if observer_id in independent_observers
        for evidence_ref in evidence_refs
    )
    settled = normalized_layers["settled_outcome"]
    valid_settlement_witness = False
    if settled["state"] == "VERIFIED":
        valid_settlement_witness = any(
            ref in independent_reality_sources
            and sources[ref]["claim_scope"] == "settled_outcome"
            and sources[ref]["observation_window"] is not None
            and sources[ref]["settlement_delay_ms"] > 0
            for ref in settled["evidence_refs"]
        )
        if not valid_settlement_witness:
            issues.append("INDEPENDENT_SETTLEMENT_WITNESS_REQUIRED:settled_outcome")
        if normalized_layers["observed_effect"]["state"] != "VERIFIED":
            issues.append("SETTLEMENT_REQUIRES_VERIFIED_OBSERVED_EFFECT")

    legacy_mapping = case["legacy_success_maps_to"]
    if case["legacy_success"] is None:
        if legacy_mapping is not None:
            issues.append("LEGACY_MAPPING_WITHOUT_LEGACY_SUCCESS")
    elif legacy_mapping not in LEGACY_MAPPING_LAYERS:
        issues.append("LEGACY_SUCCESS_MUST_MAP_TO_ONE_PRE_EFFECT_LAYER")
    elif case["legacy_success"] is True and normalized_layers[legacy_mapping]["state"] != "VERIFIED":
        issues.append("LEGACY_SUCCESS_MAPPING_NOT_VERIFIED")
    elif case["legacy_success"] is False and normalized_layers[legacy_mapping]["state"] != "CONTRADICTED":
        issues.append("LEGACY_FAILURE_MAPPING_NOT_CONTRADICTED")
    result = {
        "case_id": case["case_id"],
        "projection_type": "EXPERIMENTAL_EEOAP_EXECUTION_OUTCOME_SIDECAR",
        "source_statement_id": case["source_statement_id"],
        "projection_status": "VALID" if not issues else "INVALID",
        "issues": sorted(issues),
        "layers": normalized_layers,
        "legacy_success_mapping": legacy_mapping,
        "legacy_success_claims_global_outcome": False,
        "global_success_proven": False,
        "independent_observers": independent_observers,
        "independent_observer_count": len(independent_observers),
        "independent_reality_sources": independent_reality_sources,
        "independence_sufficient_for_settlement": valid_settlement_witness,
        "causal_attribution_proven": False,
        "eeoap_core_schema_modified": False,
        "canonical_evidence_created": False,
        "numeric_score": None,
    }
    result["projection_digest"] = document_digest(result)
    return result


__all__ = [
    "ExecutionOutcomeProjectionError",
    "LAYER_NAMES",
    "LAYER_STATES",
    "evaluate_execution_outcome_projection",
]
