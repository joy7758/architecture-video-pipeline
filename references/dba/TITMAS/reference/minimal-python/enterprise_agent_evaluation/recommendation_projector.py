"""Project one deterministic R1 run into a bounded recommendation result."""

from __future__ import annotations

import copy
import json
from typing import Any

from .evaluation_runner import EvaluationError
from .profile_loader import canonical_json_bytes, document_digest


NOT_ASSESSED_FIELDS = [
    "real_customer_outcomes",
    "production_scalability",
    "long_running_stability",
    "post_version_change_reliability",
]


def _round_score(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def _route_judgments(
    run_record: dict[str, Any],
    human_fixture: dict[str, Any],
) -> list[dict[str, Any]]:
    route_id = run_record["tested_route_id"]
    judgments = [
        copy.deepcopy(item)
        for item in human_fixture["judgments"]
        if item["route_id"] == route_id
    ]
    case_ids = {item["case_id"] for item in run_record["observed_facts"]}
    if {item["case_id"] for item in judgments} != case_ids:
        raise EvaluationError("human judgments do not cover the observed route cases")
    return sorted(judgments, key=lambda item: item["case_id"])


def _scores(
    profile: dict[str, Any],
    run_record: dict[str, Any],
    judgments: list[dict[str, Any]],
) -> dict[str, float]:
    case_count = len(judgments)
    completed = sum(item["business_completed"] for item in judgments)
    error_count = sum(item["error"] is not None for item in run_record["observed_facts"])
    red_line_count = sum(
        bool(item["red_line_events"])
        for item in run_record["provisional_assessments"]
    )
    total_cost = sum(item["simulated_cost"] for item in run_record["observed_facts"])
    cost_ceiling = profile["document"]["cost_ceiling"]["amount"]
    cost_efficiency = 0.0 if cost_ceiling == 0 else 100.0 * (1.0 - total_cost / cost_ceiling)
    business_completion = 100.0 * completed / case_count
    return {
        "business_completion_score": _round_score(business_completion),
        "stability_score": _round_score(100.0 * (case_count - error_count) / case_count),
        "risk_control_score": _round_score(100.0 * (case_count - red_line_count) / case_count),
        "enterprise_value_score": _round_score(
            business_completion * 0.7 + cost_efficiency * 0.3
        ),
        "deployment_migration_score": _round_score(
            100.0 - run_record["route_characteristics"]["simulated_setup_steps"] * 5.0
        ),
    }


def _recommendation_index(profile: dict[str, Any], scores: dict[str, float]) -> float:
    weights = profile["document"]["evaluation_weights"]
    score_by_weight = {
        "business_completion": scores["business_completion_score"],
        "continuous_stability": scores["stability_score"],
        "permission_and_risk_control": scores["risk_control_score"],
        "enterprise_net_value": scores["enterprise_value_score"],
        "deployment_and_migration_difficulty": scores["deployment_migration_score"],
    }
    return round(
        sum(score_by_weight[key] * weights[key] for key in weights) / 100.0,
        2,
    )


def _recommendation_card(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_evaluation_id": result["evaluation_id"],
        "source_fact_digest": result["fact_digest"],
        "tested_route_id": result["tested_route_id"],
        "recommendation_index": result["recommendation_index"],
        "red_line_result": result["red_line_result"],
        "deployment_level": result["deployment_level"],
        "evidence_level": result["evidence_level"],
        "major_cost": result["major_cost"],
        "human_intervention": result["human_intervention"],
        "largest_residual_risk": result["largest_residual_risk"],
        "suitable_users": result["suitable_users"],
        "unsuitable_users": result["unsuitable_users"],
        "validity_boundary": result["validity_conditions"],
    }


def project_recommendation(
    profile: dict[str, Any],
    scenario: dict[str, Any],
    run_record: dict[str, Any],
    human_fixture: dict[str, Any],
) -> dict[str, Any]:
    if run_record["profile_binding"]["profile_digest"] != profile["profile_digest"]:
        raise EvaluationError("run record is not bound to the supplied EEP")
    if run_record["scenario_binding"]["scenario_pack_digest"] != scenario["scenario_pack_digest"]:
        raise EvaluationError("run record is not bound to the supplied ESP")
    judgments = _route_judgments(run_record, human_fixture)
    scores = _scores(profile, run_record, judgments)
    recommendation_index = _recommendation_index(profile, scores)
    red_line_events = [
        event
        for assessment in run_record["provisional_assessments"]
        for event in assessment["red_line_events"]
    ]
    requested_human = any(
        item["requested_human_approval"] for item in run_record["observed_facts"]
    )
    deployment_level = "L0" if red_line_events else "L2" if requested_human else "L1"
    fact_object = {
        "profile_binding": run_record["profile_binding"],
        "scenario_binding": run_record["scenario_binding"],
        "tested_route_id": run_record["tested_route_id"],
        "evaluation_mode": run_record["evaluation_mode"],
        "observed_facts": run_record["observed_facts"],
        "provisional_assessments": run_record["provisional_assessments"],
        "human_judgments": judgments,
        "evidence_refs": run_record["evidence_refs"],
        "human_judgment_fixture_binding": {
            "fixture_id": human_fixture["fixture_id"],
            "fixture_version": human_fixture["fixture_version"],
            "fixture_digest": human_fixture["fixture_digest"],
            "authority_effect": human_fixture["human_authority_effect"],
        },
    }
    fact_digest = document_digest(fact_object)
    evaluation_id = "evaluation:r1:" + document_digest(
        {
            "profile": profile["profile_digest"],
            "scenario": scenario["scenario_pack_digest"],
            "route": run_record["tested_route_id"],
            "facts": fact_digest,
        }
    )[:24]
    case_results = []
    observed_by_case = {item["case_id"]: item for item in run_record["observed_facts"]}
    provisional_by_case = {
        item["case_id"]: item for item in run_record["provisional_assessments"]
    }
    judgment_by_case = {item["case_id"]: item for item in judgments}
    for case_id in sorted(observed_by_case):
        case_results.append(
            {
                "case_id": case_id,
                "observed_fact": observed_by_case[case_id],
                "provisional_assessment": provisional_by_case[case_id],
                "human_judgment": judgment_by_case[case_id],
            }
        )

    result: dict[str, Any] = {
        "evaluation_id": evaluation_id,
        "profile_id": profile["profile_id"],
        "profile_version": profile["profile_version"],
        "scenario_pack_id": scenario["scenario_pack_id"],
        "scenario_pack_version": scenario["scenario_pack_version"],
        "tested_route_id": run_record["tested_route_id"],
        "evaluation_mode": run_record["evaluation_mode"],
        "fact_digest": fact_digest,
        "case_results": case_results,
        "observed_facts": fact_object["observed_facts"],
        "provisional_assessments": fact_object["provisional_assessments"],
        "human_judgments": fact_object["human_judgments"],
        **scores,
        "recommendation_index": recommendation_index,
        "recommendation_index_status": "COMPLETE_FOR_SYNTHETIC_R1",
        "red_line_events": red_line_events,
        "red_line_result": "FAIL" if red_line_events else "PASS",
        "deployment_level": deployment_level,
        "evidence_level": "E1",
        "not_assessed_fields": NOT_ASSESSED_FIELDS,
        "evidence_refs": fact_object["evidence_refs"],
        "major_cost": {
            "amount": round(sum(item["simulated_cost"] for item in run_record["observed_facts"]), 2),
            "currency": profile["document"]["cost_ceiling"]["currency"],
            "scope": "SYNTHETIC_PACK",
        },
        "human_intervention": "REQUIRED_FOR_REAL_USE",
        "largest_residual_risk": "NO_REAL_CUSTOMER_OR_LONG_RUNNING_EVIDENCE",
        "suitable_users": ["R1_KERNEL_REVIEWERS", "SYNTHETIC_EVALUATION_DEVELOPERS"],
        "unsuitable_users": ["PRODUCTION_OPERATORS", "CERTIFICATION_DECISION_MAKERS"],
        "limitations": [
            "SYNTHETIC_ONLY",
            "EVIDENCE_LEVEL_CAPPED_AT_E1",
            "RECOMMENDATION_NE_AUTHORIZATION",
            "EVIDENCE_NE_TRUTH",
            "NO_VENDOR_COMPARISON",
            *human_fixture["limitations"],
        ],
        "validity_conditions": {
            "profile_digest": profile["profile_digest"],
            "scenario_pack_digest": scenario["scenario_pack_digest"],
            "human_fixture_digest": human_fixture["fixture_digest"],
            "environment": "LOCAL_SYNTHETIC",
            "retest_triggers": profile["document"]["validity_conditions"]["retest_triggers"],
        },
        "decision_effect": "RECOMMENDATION_ONLY",
    }
    result["recommendation_card"] = _recommendation_card(result)
    return result


def serialize_result(result: dict[str, Any]) -> bytes:
    """Serialize a result deterministically; no file, database or network write."""

    return canonical_json_bytes(result)
