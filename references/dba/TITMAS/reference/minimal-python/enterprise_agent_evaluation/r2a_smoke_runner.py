"""Bounded private R2A two-route smoke coordinator.

Network use is disabled unless ``TITMAS_R2A_LIVE_AUTHORIZED=true`` and every
manual configuration gate is present.  The coordinator performs no retry,
creates no database, and writes live observations only outside the repository.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .adapters import (
    CONFIGURED_MODEL_ID,
    R2AContractError,
    canonical_json_bytes,
    determine_model_alignment,
    masked_presence,
    parse_text_contract,
    sha256_text,
    sha256_value,
)
from .adapters.aliyun_bailian_workflow import AliyunBailianWorkflowAdapter
from .adapters.dify_workflow import DifyWorkflowAdapter


PACKAGE_ROOT = Path(__file__).resolve().parent
DBA_ROOT = Path(__file__).resolve().parents[4]
FIXTURE_ROOT = PACKAGE_ROOT / "fixtures"
DEFAULT_CONTRACT_PATH = FIXTURE_ROOT / "r2a_route_contract.json"
DEFAULT_CASES_PATH = FIXTURE_ROOT / "r2a_smoke_cases.json"
PHASES = ("A0_DIRECT_CONTEXT_PARITY", "A1_NATIVE_RAG_SMOKE")
ROUTE_IDS = (
    "route_a_aliyun_bailian_workflow",
    "route_b_dify_cloud_workflow",
)
RAG_FIELDS = {
    "chunking_strategy",
    "chunk_size",
    "chunk_overlap",
    "embedding_model",
    "retrieval_top_k",
    "score_threshold",
    "reranker",
    "knowledge_base_version",
}


class R2ASmokeBlocked(RuntimeError):
    """The smoke run stopped at an explicit fail-closed gate."""

    def __init__(self, status: str, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.detail = detail


def _load_object(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise R2AContractError(f"{path}: expected a regular fixture file")
    if path.stat().st_size > 1_000_000:
        raise R2AContractError(f"{path}: fixture exceeds the bounded size")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise R2AContractError(f"{path}: invalid JSON fixture") from exc
    if not isinstance(value, dict):
        raise R2AContractError(f"{path}: top level must be an object")
    return value


def load_r2a_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    value = _load_object(path)
    required = {
        "contract_id",
        "contract_version",
        "stage",
        "scope",
        "publication_allowed",
        "evidence_level_cap",
        "comparison_entry_state",
        "configured_model_id",
        "live_authorization_env",
        "limits",
        "common_parameters",
        "output_contract",
        "routes",
        "native_rag_required_fields",
        "invariants",
    }
    if set(value) != required:
        raise R2AContractError("R2A route contract fields do not match the frozen shape")
    if value["stage"] != "R2A_PRIVATE_TWO_ROUTE_SMOKE":
        raise R2AContractError("R2A stage mismatch")
    if value["scope"] != "ENGINEERING_SMOKE_ONLY":
        raise R2AContractError("R2A scope must remain engineering-smoke-only")
    if value["publication_allowed"] is not False:
        raise R2AContractError("R2A publication must remain disabled")
    if value["evidence_level_cap"] != "E1":
        raise R2AContractError("R2A evidence level cannot exceed E1")
    if value["comparison_entry_state"] != "SAME_MODEL_ALIAS_CONFIGURATION_CANDIDATE":
        raise R2AContractError("R2A comparison entry state drifted")
    if value["configured_model_id"] != CONFIGURED_MODEL_ID:
        raise R2AContractError("R2A configured model drifted")
    if value["live_authorization_env"] != "TITMAS_R2A_LIVE_AUTHORIZED":
        raise R2AContractError("R2A live gate variable drifted")
    limits = value["limits"]
    if limits != {
        "max_real_model_calls": 16,
        "route_a_max_calls": 8,
        "route_b_max_calls": 8,
        "automatic_retries": 0,
        "cash_cap_cny": 5.0,
    }:
        raise R2AContractError("R2A call, retry, or cash limits drifted")
    if set(value["routes"]) != set(ROUTE_IDS):
        raise R2AContractError("R2A routes must remain exactly two")
    output_contract = value["output_contract"]
    if set(output_contract) != {
        "system_instruction",
        "template",
        "native_structured_output",
        "automatic_model_repair",
    }:
        raise R2AContractError("R2A plain-text output contract shape drifted")
    if output_contract["native_structured_output"] is not False:
        raise R2AContractError("R2A cannot assume native structured output")
    if output_contract["automatic_model_repair"] is not False:
        raise R2AContractError("R2A cannot repair output with another model call")
    if set(value["native_rag_required_fields"]) != RAG_FIELDS:
        raise R2AContractError("R2A native RAG record fields drifted")
    invariants = value["invariants"]
    required_invariants = {
        "observed_fact_ne_business_correctness": True,
        "provisional_assessment_ne_final_authority": True,
        "recommendation_index_ne_deployment_level": True,
        "red_line_cannot_be_offset_by_score": True,
        "evaluation_ne_execution_authority": True,
        "second_truth_source_created": False,
        "second_authority_chain_created": False,
        "automatic_model_repair": False,
    }
    if invariants != required_invariants:
        raise R2AContractError("R2A authority or evidence invariant drifted")
    return value


def load_r2a_cases(path: Path = DEFAULT_CASES_PATH) -> dict[str, Any]:
    value = _load_object(path)
    required = {
        "fixture_id",
        "fixture_version",
        "privacy_classification",
        "source_document",
        "cases",
    }
    if set(value) != required:
        raise R2AContractError("R2A case fixture fields do not match the frozen shape")
    if value["privacy_classification"] != "SYNTHETIC":
        raise R2AContractError("R2A cases must remain synthetic")
    source = value["source_document"]
    if set(source) != {"document_id", "version", "content", "size_bytes", "sha256"}:
        raise R2AContractError("R2A source document fields do not match the frozen shape")
    encoded = source["content"].encode("utf-8")
    if source["size_bytes"] != len(encoded) or source["sha256"] != sha256_text(source["content"]):
        raise R2AContractError("R2A source document size or digest mismatch")
    cases = value["cases"]
    if not isinstance(cases, list) or len(cases) != 6:
        raise R2AContractError("R2A requires exactly six synthetic cases")
    case_ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
    if len(case_ids) != 6 or len(set(case_ids)) != 6:
        raise R2AContractError("R2A case identifiers must be unique")
    a0_count = sum("A0_DIRECT_CONTEXT_PARITY" in case.get("phases", []) for case in cases)
    a1_count = sum("A1_NATIVE_RAG_SMOKE" in case.get("phases", []) for case in cases)
    if (a0_count, a1_count) != (2, 6):
        raise R2AContractError("R2A phase distribution must remain 2 and 6")
    expected_fields = {
        "case_id",
        "category",
        "query",
        "phases",
        "expected_action",
        "red_line_actions",
    }
    for case in cases:
        if set(case) != expected_fields:
            raise R2AContractError("R2A case fields do not match the frozen shape")
        if case["category"] not in {"NORMAL", "AMBIGUOUS_OR_CONFLICT", "RED_LINE_OR_FAILURE"}:
            raise R2AContractError("R2A case category is invalid")
        if case["expected_action"] not in {"ANSWER", "ASK", "ESCALATE"}:
            raise R2AContractError("R2A expected action is invalid")
        if not isinstance(case["query"], str) or not case["query"]:
            raise R2AContractError("R2A case query is required")
        if not isinstance(case["red_line_actions"], list):
            raise R2AContractError("R2A red-line actions must be an array")
        if not set(case["phases"]) <= set(PHASES):
            raise R2AContractError("R2A case includes an unknown phase")
    return value


def build_request(
    *,
    contract: dict[str, Any],
    cases_fixture: dict[str, Any],
    case: dict[str, Any],
    phase: str,
    application_version: str,
    knowledge_base_version: str,
) -> dict[str, Any]:
    if phase not in PHASES or phase not in case["phases"]:
        raise R2AContractError("case is not admitted to the requested R2A phase")
    source = cases_fixture["source_document"]
    direct_context = source["content"] if phase == "A0_DIRECT_CONTEXT_PARITY" else ""
    context_instruction = (
        f"DIRECT_CONTEXT:\n{direct_context}"
        if phase == "A0_DIRECT_CONTEXT_PARITY"
        else "NATIVE_RAG_CONTEXT: Use only the published synthetic knowledge base."
    )
    output_shape = contract["output_contract"]["template"]
    prompt = (
        f"{contract['output_contract']['system_instruction']}\n\n"
        f"PHASE: {phase}\n"
        f"{context_instruction}\n"
        f"CUSTOMER_QUERY: {case['query']}\n\n"
        f"Return only this plain-text shape:\n{output_shape}"
    )
    input_variables = {
        "phase": phase,
        "case_id": case["case_id"],
        "query": case["query"],
        "direct_context": direct_context,
        "source_document_sha256": source["sha256"],
        "prompt": prompt,
    }
    return {
        "phase": phase,
        "case_id": case["case_id"],
        "prompt": prompt,
        "input_variables": input_variables,
        "configured_model_id": contract["configured_model_id"],
        "application_version": application_version,
        "knowledge_base_version": knowledge_base_version,
        "source_document_sha256": source["sha256"],
        "direct_context_sha256": sha256_text(direct_context),
        "common_parameters": contract["common_parameters"],
        "privacy_classification": cases_fixture["privacy_classification"],
    }


@dataclass
class SmokeBudget:
    max_calls: int = 16
    per_route_max: int = 8
    cash_cap_cny: float = 5.0
    total_calls: int = 0
    route_calls: dict[str, int] = field(default_factory=lambda: {route: 0 for route in ROUTE_IDS})
    total_cost_cny: float = 0.0

    def reserve(self, route_id: str) -> None:
        if route_id not in self.route_calls:
            raise R2ASmokeBlocked("R2A_BLOCKED_SCOPE_EXPANSION", "unknown route")
        if self.total_calls >= self.max_calls or self.route_calls[route_id] >= self.per_route_max:
            raise R2ASmokeBlocked(
                "R2A_BLOCKED_BUDGET_OR_CALL_CAP",
                "real model call cap reached",
            )
        self.total_calls += 1
        self.route_calls[route_id] += 1

    def add_cost(self, cost_cny: float | None) -> None:
        if cost_cny is None:
            raise R2ASmokeBlocked(
                "R2A_BLOCKED_OBSERVABILITY",
                "bounded cost could not be observed or conservatively estimated",
            )
        self.total_cost_cny = round(self.total_cost_cny + cost_cny, 6)
        if self.total_cost_cny > self.cash_cap_cny:
            raise R2ASmokeBlocked(
                "R2A_BLOCKED_BUDGET_OR_CALL_CAP",
                "cash cap exceeded",
            )


def native_rag_differences(route_metadata: Mapping[str, dict[str, Any]]) -> dict[str, Any]:
    for route_id in ROUTE_IDS:
        config = route_metadata[route_id].get("rag_configuration")
        if not isinstance(config, dict) or set(config) != RAG_FIELDS:
            raise R2AContractError("native RAG configuration record is incomplete")
        if config["knowledge_base_version"] != route_metadata[route_id].get("knowledge_base_version"):
            raise R2AContractError("native RAG knowledge-base version binding is inconsistent")
    differences = {}
    route_a = route_metadata[ROUTE_IDS[0]]["rag_configuration"]
    route_b = route_metadata[ROUTE_IDS[1]]["rag_configuration"]
    for field_name in sorted(RAG_FIELDS):
        if route_a[field_name] != route_b[field_name]:
            differences[field_name] = {
                ROUTE_IDS[0]: route_a[field_name],
                ROUTE_IDS[1]: route_b[field_name],
            }
    return {
        "status": "NATIVE_RAG_CONFIGURATION_DIFFERENCE" if differences else "MATCH_RECORDED",
        "differences": differences,
        "comparison_object": "COMPLETE_DEPLOYMENT_ROUTE",
    }


def _outside_repository(path: Path) -> bool:
    resolved = path.resolve()
    return resolved != DBA_ROOT and DBA_ROOT not in resolved.parents


def _write_private_event(output_dir: Path, sequence: int, event: dict[str, Any]) -> None:
    if not _outside_repository(output_dir):
        raise R2ASmokeBlocked(
            "R2A_BLOCKED_SCOPE_EXPANSION",
            "live output directory must remain outside the repository",
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"event-{sequence:02d}.json"
    path.write_bytes(canonical_json_bytes(event) + b"\n")


def run_private_smoke(
    *,
    adapters: Mapping[str, Any],
    route_metadata: Mapping[str, dict[str, Any]],
    contract: dict[str, Any] | None = None,
    cases_fixture: dict[str, Any] | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    contract = contract or load_r2a_contract()
    cases_fixture = cases_fixture or load_r2a_cases()
    if set(adapters) != set(ROUTE_IDS) or set(route_metadata) != set(ROUTE_IDS):
        raise R2ASmokeBlocked("R2A_BLOCKED_SCOPE_EXPANSION", "exactly two frozen routes are required")
    output_dir = output_dir or Path(tempfile.mkdtemp(prefix="titmas-r2a-"))
    if not _outside_repository(output_dir):
        raise R2ASmokeBlocked("R2A_BLOCKED_SCOPE_EXPANSION", "output path is inside repository")
    rag_result = native_rag_differences(route_metadata)
    budget = SmokeBudget()
    events_by_phase: dict[str, list[dict[str, Any]]] = {phase: [] for phase in PHASES}
    parsed_outputs: list[dict[str, Any]] = []

    for phase in PHASES:
        phase_cases = [case for case in cases_fixture["cases"] if phase in case["phases"]]
        for case in phase_cases:
            request_digests = set()
            case_events = []
            for route_id in ROUTE_IDS:
                metadata = route_metadata[route_id]
                request = build_request(
                    contract=contract,
                    cases_fixture=cases_fixture,
                    case=case,
                    phase=phase,
                    application_version=metadata["application_version"],
                    knowledge_base_version=metadata["knowledge_base_version"],
                )
                request_digests.add(sha256_value({
                    "prompt": request["prompt"],
                    "input_variables": request["input_variables"],
                    "common_parameters": request["common_parameters"],
                }))
                budget.reserve(route_id)
                try:
                    event = adapters[route_id].invoke(request)
                except Exception as exc:
                    raise R2ASmokeBlocked(
                        "R2A_BLOCKED_OBSERVABILITY",
                        "provider attempt failed without retry",
                    ) from exc
                budget.add_cost(event["estimated_cost_cny"])
                _write_private_event(output_dir, budget.total_calls, event)
                if event["status"] != "SUCCEEDED":
                    raise R2ASmokeBlocked("R2A_BLOCKED_OBSERVABILITY", "provider call did not succeed")
                try:
                    parsed = parse_text_contract(event["output_text"])
                except R2AContractError as exc:
                    raise R2ASmokeBlocked(
                        "R2A_BLOCKED_CONFORMANCE",
                        "OUTPUT_CONTRACT_FAIL",
                    ) from exc
                action_matches = parsed["action"] == case["expected_action"]
                parsed_outputs.append({
                    "route_id": route_id,
                    "case_id": case["case_id"],
                    "phase": phase,
                    "parsed_output": parsed,
                    "expected_action": case["expected_action"],
                    "expected_action_match": action_matches,
                    "red_line_events": [] if action_matches else case["red_line_actions"],
                    "human_judgment_required": True,
                    "final_authority_effect": "NONE",
                })
                events_by_phase[phase].append(event)
                case_events.append(event)
            if len(request_digests) != 1:
                raise R2ASmokeBlocked("R2A_BLOCKED_INPUT_CONTRACT", "route inputs were not identical")
            case_alignment = determine_model_alignment(case_events)
            if case_alignment == "MODEL_MISMATCH":
                raise R2ASmokeBlocked(
                    "R2A_BLOCKED_MODEL_MISMATCH",
                    "provider model identifiers differ",
                )

        if phase == "A0_DIRECT_CONTEXT_PARITY":
            alignment = determine_model_alignment(events_by_phase[phase])
            if alignment == "MODEL_MISMATCH":
                raise R2ASmokeBlocked("R2A_BLOCKED_MODEL_MISMATCH", "provider model identifiers differ")
            if len(events_by_phase[phase]) != 4:
                raise R2ASmokeBlocked("R2A_BLOCKED_CONFORMANCE", "A0 did not produce four calls")

    if len(events_by_phase["A1_NATIVE_RAG_SMOKE"]) != 12:
        raise R2ASmokeBlocked("R2A_BLOCKED_CONFORMANCE", "A1 did not produce twelve calls")
    all_events = events_by_phase["A0_DIRECT_CONTEXT_PARITY"] + events_by_phase["A1_NATIVE_RAG_SMOKE"]
    alignment = determine_model_alignment(all_events)
    if alignment == "MODEL_MISMATCH":
        raise R2ASmokeBlocked(
            "R2A_BLOCKED_MODEL_MISMATCH",
            "provider model identifiers differ",
        )
    all_not_assessed = sorted({
        field_name
        for event in all_events
        for field_name in event["not_assessed_fields"]
    })
    summary = {
        "status": "R2A_PASS_RECOMMEND_R2B",
        "stage": contract["stage"],
        "scope": contract["scope"],
        "model_alignment_status": alignment,
        "a0_direct_context_calls": len(events_by_phase["A0_DIRECT_CONTEXT_PARITY"]),
        "a1_native_rag_calls": len(events_by_phase["A1_NATIVE_RAG_SMOKE"]),
        "total_real_model_calls": budget.total_calls,
        "route_calls": budget.route_calls,
        "total_cost_cny": budget.total_cost_cny,
        "automatic_retries": 0,
        "common_parameter_intersection": contract["common_parameters"],
        "seed_status": (
            "APPLIED_TO_BOTH"
            if "seed" in contract["common_parameters"]
            else "NOT_IN_COMMON_INTERSECTION"
        ),
        "output_contract_status": "PASS",
        "source_document_sha256": cases_fixture["source_document"]["sha256"],
        "source_document_hash_match": True,
        "native_rag_configuration": rag_result,
        "route_status": {route_id: "SUCCEEDED" for route_id in ROUTE_IDS},
        "observability_status": "PASS_WITH_NOT_ASSESSED_FIELDS",
        "not_assessed_fields": all_not_assessed,
        "observed_facts": all_events,
        "provisional_assessments": parsed_outputs,
        "human_judgments": [],
        "human_judgment_status": "NOT_ASSESSED",
        "recommendation_index_calculated": False,
        "deployment_level_calculated": False,
        "evidence_level": "E1",
        "evidence_mapping_status": "EXISTING_TITMAS_REFERENCE_REUSED",
        "second_truth_source_created": False,
        "second_authority_chain_created": False,
        "decision_effect": "NONE",
        "publication_allowed": False,
        "claims_not_supported": [
            "VENDOR_SUPERIORITY",
            "PRODUCTION_READINESS",
            "LONG_TERM_STABILITY",
            "CUSTOMER_VALUE_PROVEN",
            "PUBLIC_RANKING",
            "CERTIFICATION",
        ],
        "r2b_entry_authorized": False,
        "output_directory": str(output_dir.resolve()),
    }
    (output_dir / "summary.json").write_bytes(canonical_json_bytes(summary) + b"\n")
    return summary


def _parse_json_env(environment: Mapping[str, str], name: str) -> dict[str, Any] | None:
    raw = environment.get(name)
    if not raw:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def live_preflight(environment: Mapping[str, str] | None = None) -> dict[str, Any]:
    if environment is None:
        environment = os.environ
    required_presence = {
        "DASHSCOPE_API_KEY",
        "BAILIAN_APP_ID",
        "DIFY_WORKFLOW_API_KEY",
        "DIFY_BASE_URL",
        "R2A_BAILIAN_APP_VERSION",
        "R2A_BAILIAN_KB_VERSION",
        "R2A_DIFY_APP_VERSION",
        "R2A_DIFY_KB_VERSION",
        "R2A_DIFY_DSL_SHA256",
        "R2A_SOURCE_DOCUMENT_SHA256",
        "R2A_BAILIAN_CONFIGURED_MODEL_ID",
        "R2A_DIFY_CONFIGURED_MODEL_ID",
        "R2A_COMMON_PARAMETERS_JSON",
        "R2A_ROUTE_A_RAG_CONFIGURATION_JSON",
        "R2A_ROUTE_B_RAG_CONFIGURATION_JSON",
    }
    required_true = {
        "R2A_BAILIAN_WORKFLOW_PUBLISHED",
        "R2A_BAILIAN_SOURCE_HASH_CONFIRMED",
        "R2A_BAILIAN_MODEL_ALIAS_CONFIRMED",
        "R2A_BAILIAN_THINKING_DISABLED",
        "R2A_BAILIAN_SEARCH_DISABLED",
        "R2A_DIFY_SANDBOX_READY",
        "R2A_DIFY_WORKFLOW_PUBLISHED",
        "R2A_DIFY_TONGYI_PLUGIN_INSTALLED",
        "R2A_DIFY_BYOK_CONFIRMED",
        "R2A_DIFY_SOURCE_HASH_CONFIRMED",
        "R2A_DIFY_MODEL_ALIAS_CONFIRMED",
        "R2A_DIFY_THINKING_DISABLED",
        "R2A_DIFY_SEARCH_DISABLED",
        "R2A_PHASE_ROUTING_CONFIRMED",
        "R2A_COMMON_PARAMETER_INTERSECTION_CONFIRMED",
    }
    missing = sorted(name for name in required_presence if not environment.get(name))
    unconfirmed = sorted(name for name in required_true if environment.get(name) != "true")
    rag_a = _parse_json_env(environment, "R2A_ROUTE_A_RAG_CONFIGURATION_JSON")
    rag_b = _parse_json_env(environment, "R2A_ROUTE_B_RAG_CONFIGURATION_JSON")
    common_parameters = _parse_json_env(environment, "R2A_COMMON_PARAMETERS_JSON")
    invalid = []
    if rag_a is not None and set(rag_a) != RAG_FIELDS:
        invalid.append("R2A_ROUTE_A_RAG_CONFIGURATION_JSON")
    if rag_b is not None and set(rag_b) != RAG_FIELDS:
        invalid.append("R2A_ROUTE_B_RAG_CONFIGURATION_JSON")
    if common_parameters is not None and common_parameters != load_r2a_contract()["common_parameters"]:
        invalid.append("R2A_COMMON_PARAMETERS_JSON")
    expected_source_digest = load_r2a_cases()["source_document"]["sha256"]
    if (
        environment.get("R2A_SOURCE_DOCUMENT_SHA256")
        and environment["R2A_SOURCE_DOCUMENT_SHA256"] != expected_source_digest
    ):
        invalid.append("R2A_SOURCE_DOCUMENT_SHA256")
    for model_variable in (
        "R2A_BAILIAN_CONFIGURED_MODEL_ID",
        "R2A_DIFY_CONFIGURED_MODEL_ID",
    ):
        if environment.get(model_variable) and environment[model_variable] != CONFIGURED_MODEL_ID:
            invalid.append(model_variable)
    if (
        environment.get("R2A_DIFY_DSL_SHA256")
        and re.fullmatch(r"[0-9a-f]{64}", environment["R2A_DIFY_DSL_SHA256"]) is None
    ):
        invalid.append("R2A_DIFY_DSL_SHA256")
    live_authorized = environment.get("TITMAS_R2A_LIVE_AUTHORIZED") == "true"
    ready = live_authorized and not missing and not unconfirmed and not invalid
    return {
        "status": "READY" if ready else "R2A_BLOCKED_ACCOUNT_OR_APP_CONFIGURATION",
        "live_authorized": live_authorized,
        "missing": missing,
        "unconfirmed": unconfirmed,
        "invalid": sorted(set(invalid)),
        "credential_presence": {
            "DASHSCOPE_API_KEY": masked_presence(environment.get("DASHSCOPE_API_KEY")),
            "DIFY_WORKFLOW_API_KEY": masked_presence(environment.get("DIFY_WORKFLOW_API_KEY")),
        },
    }


def _live_configuration(environment: Mapping[str, str]) -> tuple[dict[str, Any], dict[str, Any]]:
    rag_a = _parse_json_env(environment, "R2A_ROUTE_A_RAG_CONFIGURATION_JSON")
    rag_b = _parse_json_env(environment, "R2A_ROUTE_B_RAG_CONFIGURATION_JSON")
    if rag_a is None or rag_b is None:
        raise R2ASmokeBlocked("R2A_BLOCKED_ACCOUNT_OR_APP_CONFIGURATION", "RAG metadata missing")
    adapters = {
        ROUTE_IDS[0]: AliyunBailianWorkflowAdapter(
            api_key=environment["DASHSCOPE_API_KEY"],
            app_id=environment["BAILIAN_APP_ID"],
            workspace_id=environment.get("BAILIAN_WORKSPACE_ID"),
        ),
        ROUTE_IDS[1]: DifyWorkflowAdapter(
            api_key=environment["DIFY_WORKFLOW_API_KEY"],
            base_url=environment["DIFY_BASE_URL"],
        ),
    }
    metadata = {
        ROUTE_IDS[0]: {
            "application_version": environment["R2A_BAILIAN_APP_VERSION"],
            "knowledge_base_version": environment["R2A_BAILIAN_KB_VERSION"],
            "rag_configuration": rag_a,
        },
        ROUTE_IDS[1]: {
            "application_version": (
                environment["R2A_DIFY_APP_VERSION"]
                + "@sha256:"
                + environment["R2A_DIFY_DSL_SHA256"]
            ),
            "knowledge_base_version": environment["R2A_DIFY_KB_VERSION"],
            "rag_configuration": rag_b,
        },
    }
    return adapters, metadata


def main() -> int:
    preflight = live_preflight()
    if preflight["status"] != "READY":
        print(json.dumps(preflight, ensure_ascii=False, sort_keys=True))
        return 2
    try:
        adapters, metadata = _live_configuration(os.environ)
        result = run_private_smoke(adapters=adapters, route_metadata=metadata)
    except R2ASmokeBlocked as exc:
        print(json.dumps({"status": exc.status, "detail": exc.detail}, ensure_ascii=False, sort_keys=True))
        return 3
    print(json.dumps({
        "status": result["status"],
        "output_directory": result["output_directory"],
        "total_real_model_calls": result["total_real_model_calls"],
        "total_cost_cny": result["total_cost_cny"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "R2ASmokeBlocked",
    "SmokeBudget",
    "build_request",
    "live_preflight",
    "load_r2a_cases",
    "load_r2a_contract",
    "native_rag_differences",
    "run_private_smoke",
]
