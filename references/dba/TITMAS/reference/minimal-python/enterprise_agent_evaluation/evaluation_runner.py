"""Run two deterministic synthetic routes and retain observed facts only."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

from .profile_loader import ContractValidationError, document_digest, load_json_object


REFERENCE_MODULE_PATH = Path(__file__).resolve().parents[1] / "titmas_reference.py"
ROUTE_IDS = ("mock_route_a", "mock_route_b")


class EvaluationError(ValueError):
    """The deterministic evaluation could not preserve its frozen boundary."""


def _load_existing_reference_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "titmas_existing_minimal_reference",
        REFERENCE_MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise EvaluationError("existing TITMAS minimal reference is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXISTING_REFERENCE = _load_existing_reference_module()


ROUTE_CHARACTERISTICS = {
    "mock_route_a": {
        "label": "Deterministic Mock Route A",
        "simulated_setup_steps": 4,
        "base_latency_ms": 180,
        "base_cost": 0.62,
    },
    "mock_route_b": {
        "label": "Deterministic Mock Route B",
        "simulated_setup_steps": 2,
        "base_latency_ms": 80,
        "base_cost": 0.24,
    },
}


def load_human_judgments(
    path: Path,
    scenario: dict[str, Any],
) -> dict[str, Any]:
    fixture = load_json_object(path)
    required_top = {
        "fixture_id",
        "fixture_version",
        "fixture_scope",
        "human_authority_effect",
        "limitations",
        "judgments",
    }
    if set(fixture) != required_top:
        raise EvaluationError("human judgment fixture fields do not match the frozen R1 shape")
    if fixture["fixture_scope"] != "SYNTHETIC_TEST_ONLY":
        raise EvaluationError("human judgment fixture must remain synthetic-only")
    if fixture["human_authority_effect"] != "NONE":
        raise EvaluationError("R1 judgment fixture cannot create human authority")
    case_ids = {item["task_id"] for item in scenario["document"]["tasks"]}
    expected_pairs = {(route, case_id) for route in ROUTE_IDS for case_id in case_ids}
    actual_pairs: set[tuple[str, str]] = set()
    required_fields = {
        "route_id",
        "case_id",
        "business_completed",
        "applicable",
        "requires_modification",
        "business_failure",
        "failure_severity",
        "rationale",
        "judgment_version",
    }
    severities = {"NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
    for judgment in fixture["judgments"]:
        if set(judgment) != required_fields:
            raise EvaluationError("human judgment fields do not match the frozen R1 shape")
        pair = (judgment["route_id"], judgment["case_id"])
        if pair in actual_pairs:
            raise EvaluationError(f"duplicate human judgment {pair}")
        actual_pairs.add(pair)
        if judgment["failure_severity"] not in severities:
            raise EvaluationError(f"invalid failure severity for {pair}")
        for field in (
            "business_completed",
            "applicable",
            "requires_modification",
            "business_failure",
        ):
            if not isinstance(judgment[field], bool):
                raise EvaluationError(f"{pair}: {field} must be boolean")
        if not judgment["rationale"] or not judgment["judgment_version"]:
            raise EvaluationError(f"{pair}: judgment rationale and version are required")
    if actual_pairs != expected_pairs:
        raise EvaluationError("human judgment fixture must cover two routes and all six cases")
    return {
        **fixture,
        "fixture_digest": document_digest(fixture),
    }


def _simulate_route(route_id: str, task: dict[str, Any], index: int) -> dict[str, Any]:
    characteristics = ROUTE_CHARACTERISTICS[route_id]
    case_id = task["task_id"]
    requested_actions: list[str]
    requested_human_approval = False
    output_produced = True
    error: str | None = None

    if route_id == "mock_route_a":
        if case_id == "case-information-insufficient":
            requested_actions = ["request_more_information"]
        elif case_id in {"case-policy-conflict", "case-permission-redline"}:
            requested_actions = ["request_human_approval"]
            requested_human_approval = True
        elif case_id == "case-interface-failure":
            requested_actions = ["knowledge_lookup"]
            output_produced = False
            error = "SIMULATED_INTERFACE_FAILURE"
        else:
            requested_actions = list(task["required_actions"])
    else:
        if case_id == "case-permission-redline":
            requested_actions = [task["forbidden_action_ids"][0]]
        elif case_id == "case-interface-failure":
            requested_actions = ["draft_response"]
        else:
            requested_actions = ["draft_response"]

    return {
        "case_id": case_id,
        "route_id": route_id,
        "output_produced": output_produced,
        "tool_calls": [
            action
            for action in requested_actions
            if action in {"knowledge_lookup", "draft_response", "request_more_information", "request_human_approval"}
        ],
        "requested_actions": requested_actions,
        "requested_human_approval": requested_human_approval,
        "latency_ms": characteristics["base_latency_ms"] + index * 7,
        "simulated_cost": round(characteristics["base_cost"] + index * 0.01, 2),
        "error": error,
        "evidence_complete": True,
        "unobserved_fields": [
            "real_customer_outcome",
            "production_side_effects",
            "version_change_stability",
        ],
    }


def _evidence_reference(
    profile: dict[str, Any],
    scenario: dict[str, Any],
    observed_fact: dict[str, Any],
) -> dict[str, Any]:
    route_id = observed_fact["route_id"]
    case_id = observed_fact["case_id"]
    execution_id = f"synthetic-execution://r1/{route_id}/{case_id}"
    evidence_ref = f"synthetic://agent-evidence/r1/{route_id}/{case_id}"
    verification_ref = f"synthetic://verification/r1/{route_id}/{case_id}"
    payload = {
        "identity": {
            "id": route_id,
            "source": "synthetic://r1/mock-route-registry",
            "version": "1.0.0",
        },
        "boundary": {
            "allowed_actions": ["record_synthetic_observation"],
            "forbidden_actions": [],
            "constraints": ["LOCAL_ONLY", "SYNTHETIC_DATA_ONLY"],
        },
        "event": {
            "event_id": f"synthetic-event://r1/{route_id}/{case_id}",
            "action": "record_synthetic_observation",
            "result": "ERROR_RECORDED" if observed_fact["error"] else "OBSERVED",
            "timestamp": scenario["document"]["source_and_provenance"]["frozen_at"],
            "execution_id": execution_id,
            "requested_actions": observed_fact["requested_actions"],
            "profile_digest": profile["profile_digest"],
            "scenario_pack_digest": scenario["scenario_pack_digest"],
        },
        "existing_evidence_ref": evidence_ref,
        "existing_verification_ref": verification_ref,
        "limitations": [
            "SYNTHETIC_ONLY",
            "REFERENCE_ONLY_NOT_CANONICAL_EVIDENCE",
            "NO_TRUTH_CLAIM",
            "NO_AUTHORIZATION",
        ],
    }
    mapped = EXISTING_REFERENCE.transform(payload)
    return {
        "case_id": case_id,
        "execution_id": execution_id,
        "source_contract_ref": "TITMAS/reference/minimal-python/titmas_reference.py",
        "mapping_kind": "EXISTING_TITMAS_EVIDENCE_REFERENCE_BINDING",
        "canonical_execution_object_created": False,
        "canonical_evidence_object_created": False,
        "evidence_binding": mapped["evidence_binding"],
        "verification_result": mapped["verification_result"],
        "evaluation_handoff": mapped["evaluation_handoff"],
        "limitations": mapped["limitations"],
    }


def _provisional_assessment(
    profile: dict[str, Any],
    task: dict[str, Any],
    observed_fact: dict[str, Any],
) -> dict[str, Any]:
    red_line_rule_ids = {
        rule["rule_id"] for rule in profile["document"]["red_line_rules"]
    }
    red_line_events = [
        {
            "rule_id": action,
            "observed_requested_action": action,
            "status": "FAIL",
        }
        for action in observed_fact["requested_actions"]
        if action in task["forbidden_action_ids"] and action in red_line_rule_ids
    ]
    status = "FAIL" if red_line_events else "BLOCKED" if observed_fact["error"] else "PASS"
    return {
        "case_id": task["task_id"],
        "status": status,
        "assessment_scope": "DETERMINISTIC_STRUCTURE_AND_RED_LINE_ONLY",
        "deterministic_rule_hits": [event["rule_id"] for event in red_line_events],
        "red_line_events": red_line_events,
        "missing_required_fields": [],
        "human_judgment_required": True,
        "final_authority_effect": "NONE",
    }


def run_route(
    profile: dict[str, Any],
    scenario: dict[str, Any],
    route_id: str,
) -> dict[str, Any]:
    if route_id not in ROUTE_IDS:
        raise EvaluationError(f"unknown mock route {route_id!r}")
    expected_digest = profile["document"]["validity_conditions"]["scenario_pack_digest"]
    if expected_digest != scenario["scenario_pack_digest"]:
        raise EvaluationError("EEP scenario_pack_digest does not match the loaded ESP")
    profile_rules = {item["rule_id"] for item in profile["document"]["red_line_rules"]}
    scenario_rules = {
        item["action_id"] for item in scenario["document"]["forbidden_actions"]
    }
    if not scenario_rules.issubset(profile_rules):
        raise EvaluationError("ESP forbidden actions are not covered by EEP red-line rules")

    observed_facts: list[dict[str, Any]] = []
    provisional: list[dict[str, Any]] = []
    evidence_refs: list[dict[str, Any]] = []
    for index, task in enumerate(scenario["document"]["tasks"]):
        observed = _simulate_route(route_id, task, index)
        observed_facts.append(observed)
        provisional.append(_provisional_assessment(profile, task, observed))
        evidence_refs.append(_evidence_reference(profile, scenario, observed))

    record = {
        "run_record_type": "R1_SYNTHETIC_OBSERVED_FACT_SET",
        "evaluation_mode": "NATIVE",
        "tested_route_id": route_id,
        "route_characteristics": ROUTE_CHARACTERISTICS[route_id],
        "profile_binding": {
            "profile_id": profile["profile_id"],
            "profile_version": profile["profile_version"],
            "profile_digest": profile["profile_digest"],
            "schema_ref": profile["schema_ref"],
            "schema_digest": profile["schema_digest"],
        },
        "scenario_binding": {
            "scenario_pack_id": scenario["scenario_pack_id"],
            "scenario_pack_version": scenario["scenario_pack_version"],
            "scenario_pack_digest": scenario["scenario_pack_digest"],
            "schema_ref": scenario["schema_ref"],
            "schema_digest": scenario["schema_digest"],
        },
        "observed_facts": observed_facts,
        "provisional_assessments": provisional,
        "evidence_refs": evidence_refs,
        "limitations": [
            "SYNTHETIC_CASES_ONLY",
            "OBSERVED_FACT_NE_BUSINESS_CORRECTNESS",
            "PROVISIONAL_ASSESSMENT_NE_FINAL_AUTHORITY",
            "EVIDENCE_REFERENCE_NE_CANONICAL_EVIDENCE_OBJECT",
        ],
    }
    return {
        **record,
        "run_fact_digest": document_digest(record),
    }
