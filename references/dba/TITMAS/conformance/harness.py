#!/usr/bin/env python3
"""Dependency-free TITMAS Development conformance harness."""

from __future__ import annotations

import copy
import hashlib
import json
import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

TITMAS_ROOT = Path(__file__).resolve().parents[1]
DBA_ROOT = TITMAS_ROOT.parent
REPORT_PATH = TITMAS_ROOT / "conformance" / "reports" / "latest.json"
MAX_JSON_BYTES = 1_000_000
MAX_SCHEMA_DEPTH = 32
REQUIRED_REGISTRY_FIELDS = {
    "id", "title", "title_zh", "category", "status", "maturity",
    "owner_ref", "authority_ref", "version", "normative",
    "implementation_status", "conformance_status", "security_review_status",
    "external_adoption_status", "created_at", "updated_at", "supersedes",
    "dependencies", "limitations",
}


class ConformanceError(ValueError):
    pass


def load_json(path: Path) -> Any:
    resolved = path.resolve()
    if not resolved.is_relative_to(DBA_ROOT.resolve()):
        raise ConformanceError(f"{path}: path escapes the DBA root")
    if path.is_symlink() or not path.is_file():
        raise ConformanceError(f"{path}: expected a regular non-symlink file")
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ConformanceError(f"{path}: file exceeds {MAX_JSON_BYTES} bytes")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(
    instance: Any,
    schema: dict[str, Any],
    path: str = "$",
    depth: int = 0,
) -> None:
    if depth > MAX_SCHEMA_DEPTH:
        raise ConformanceError(f"{path}: schema depth exceeds {MAX_SCHEMA_DEPTH}")
    expected = schema.get("type")
    type_map = {
        "object": dict, "array": list, "string": str,
        "boolean": bool, "integer": int, "number": (int, float),
    }
    if expected in type_map and not isinstance(instance, type_map[expected]):
        raise ConformanceError(f"{path}: expected {expected}")
    if expected == "integer" and isinstance(instance, bool):
        raise ConformanceError(f"{path}: boolean is not an integer")
    if expected == "number" and isinstance(instance, bool):
        raise ConformanceError(f"{path}: boolean is not a number")
    if "enum" in schema and instance not in schema["enum"]:
        raise ConformanceError(f"{path}: value {instance!r} is not allowed")
    if "const" in schema and instance != schema["const"]:
        raise ConformanceError(f"{path}: expected constant {schema['const']!r}")
    if isinstance(instance, str) and len(instance) < schema.get("minLength", 0):
        raise ConformanceError(f"{path}: string is shorter than minLength")
    if isinstance(instance, str) and len(instance) > schema.get("maxLength", 1_000_000):
        raise ConformanceError(f"{path}: string is longer than maxLength")
    if isinstance(instance, str) and schema.get("pattern"):
        if re.fullmatch(schema["pattern"], instance) is None:
            raise ConformanceError(f"{path}: string does not match pattern")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise ConformanceError(f"{path}: array is shorter than minItems")
        if len(instance) > schema.get("maxItems", 1_000_000):
            raise ConformanceError(f"{path}: array is longer than maxItems")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in instance]
            if len(serialized) != len(set(serialized)):
                raise ConformanceError(f"{path}: array items must be unique")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(instance):
                validate_schema(item, item_schema, f"{path}[{index}]", depth + 1)
    if isinstance(instance, dict):
        missing = [key for key in schema.get("required", []) if key not in instance]
        if missing:
            raise ConformanceError(f"{path}: missing required fields {missing}")
        for key, child in schema.get("properties", {}).items():
            if key in instance:
                validate_schema(instance[key], child, f"{path}.{key}", depth + 1)
        if schema.get("additionalProperties") is False:
            extra = sorted(set(instance) - set(schema.get("properties", {})))
            if extra:
                raise ConformanceError(f"{path}: additional properties not allowed {extra}")


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ConformanceError(f"{path}: missing frontmatter start")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ConformanceError(f"{path}: missing frontmatter end") from exc
    result: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ConformanceError(f"{path}: invalid frontmatter line {line!r}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    required = {
        "id", "title", "title_zh", "category", "status", "maturity",
        "owner_ref", "authority_ref", "version", "normative",
    }
    missing = sorted(required - result.keys())
    if missing:
        raise ConformanceError(f"{path}: missing frontmatter fields {missing}")
    return result


def semantic_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    claims = payload.get("claims") or []
    if not isinstance(claims, list) or not all(isinstance(item, str) for item in claims):
        errors.append("MALFORMED_CLAIMS")
    evidence = payload.get("evidence_binding") or {}
    if evidence.get("source_kind") == "OBSERVATION" and evidence.get("admission_status") == "ADMITTED_EVIDENCE":
        errors.append("OBSERVATION_AS_EVIDENCE")
    if "TRUTH" in claims:
        errors.append("EVIDENCE_AS_TRUTH")
    if "authorization_status" in (payload.get("verification_result") or {}):
        errors.append("VERIFICATION_AS_AUTHORIZATION")
    if payload.get("mapping_only") is True and payload.get("external_adoption_status") == "ADOPTED":
        errors.append("MAPPING_AS_ADOPTION")
    if payload.get("profile_status") == "STABLE" and payload.get("maturity") == "Experimental":
        errors.append("EXPERIMENTAL_AS_STABLE")
    if payload.get("recommendation_mode") == "COMMAND":
        errors.append("RECOMMENDATION_AS_COMMAND")
    if (payload.get("health_result") or {}).get("certification") is True:
        errors.append("HEALTH_AS_CERTIFICATION")
    if payload.get("authority_ref") == "REFERENCE_IMPLEMENTATION":
        errors.append("REFERENCE_IMPL_AS_AUTHORITY")
    return errors


def check_registries() -> dict[str, Any]:
    specs = TITMAS_ROOT / "specifications"
    registry_schema = load_json(TITMAS_ROOT / "conformance" / "schemas" / "registry-entry.schema.json")
    checked = 0
    ids: set[str] = set()
    for name in ("registry.yaml", "proposal-registry.yaml"):
        doc = load_json(specs / name)
        for entry in doc["entries"]:
            validate_schema(entry, registry_schema)
            missing = REQUIRED_REGISTRY_FIELDS - entry.keys()
            if missing:
                raise ConformanceError(f"{name}/{entry.get('id')}: missing {sorted(missing)}")
            if entry["id"] in ids and name == "registry.yaml":
                raise ConformanceError(f"duplicate specification id {entry['id']}")
            ids.add(entry["id"])
            ref = entry.get("document_ref")
            if ref and not (specs / ref).is_file():
                raise ConformanceError(f"{name}: missing document_ref {ref}")
            checked += 1
    roles = load_json(specs / "role-registry.yaml")
    if roles["assignments"]:
        raise ConformanceError("role assignments must remain empty before Human Decision")
    for role in roles["roles"]:
        validate_schema(role, registry_schema)
        checked += 1
    maturity = load_json(specs / "maturity-registry.yaml")
    state_ids = [item["id"] for item in maturity["states"]]
    if len(state_ids) != len(set(state_ids)) or maturity["default"] not in state_ids:
        raise ConformanceError("invalid maturity registry")
    return {"registry_entries_checked": checked, "maturity_states_checked": len(state_ids)}


def check_frontmatter() -> dict[str, Any]:
    proposals = sorted((TITMAS_ROOT / "specifications" / "proposals").glob("*.md"))
    parsed = [parse_frontmatter(path) for path in proposals]
    return {"proposal_frontmatter_checked": len(parsed)}


def check_fixtures() -> dict[str, Any]:
    schema = load_json(TITMAS_ROOT / "conformance" / "schemas" / "core-developer-surface.schema.json")
    positive_paths = sorted((TITMAS_ROOT / "conformance" / "fixtures" / "positive").glob("*.json"))
    for path in positive_paths:
        payload = load_json(path)
        validate_schema(payload, schema)
        errors = semantic_errors(payload)
        if errors:
            raise ConformanceError(f"{path.name}: semantic errors {errors}")
    negative = load_json(TITMAS_ROOT / "conformance" / "fixtures" / "negative" / "semantic-elevation-cases.json")
    for case in negative["cases"]:
        errors = semantic_errors(case["payload"])
        if case["expected_error"] not in errors:
            raise ConformanceError(f"{case['id']}: expected {case['expected_error']}, got {errors}")
    return {"positive_cases_passed": len(positive_paths), "negative_cases_rejected": len(negative["cases"])}


def check_stage5_contributions() -> dict[str, Any]:
    path = TITMAS_ROOT / "conformance" / "stage5_contributions.py"
    spec = importlib.util.spec_from_file_location("titmas_stage5_conformance", path)
    if spec is None or spec.loader is None:
        raise ConformanceError("Stage 5 contribution extension is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.self_check()


def check_community_status() -> dict[str, Any]:
    path = TITMAS_ROOT / "community" / "community-status.json"
    status = load_json(path)
    schema = load_json(TITMAS_ROOT / "conformance" / "schemas" / "community-status.schema.json")
    validate_schema(status, schema)
    must_be_false = (
        "community_established", "foundation_created",
        "maintainer_assigned", "external_reviewer_assigned",
        "commercial_offer_authorized", "certification_authorized",
        "release_authorized", "cs_g0_pass", "cs_g1_pass",
    )
    elevated = [key for key in must_be_false if status[key] is not False]
    if elevated:
        raise ConformanceError(f"community status semantic elevation: {elevated}")
    if not status["canonical_main_integration_complete"]:
        raise ConformanceError("community core must be integrated before public activation")
    if not status["human_merge_review"]["completed"]:
        raise ConformanceError("Human merge review must be complete")
    if status["human_merge_review"]["independent"]:
        raise ConformanceError("Human Owner review must not be claimed as independent")
    if not status["core_merge"]["authorized"] or not status["core_merge"]["executed"]:
        raise ConformanceError("community core merge record is incomplete")
    contribution = status["public_contribution_surface"]
    security = status["security"]
    launch = status["public_launch"]
    activation_pr = status["activation_pr"]
    repair = status["public_entry_repair"]
    if status["community_incubation_active"]:
        raise ConformanceError("private commercialization boundary must close community incubation")
    if any((
        status["external_participant_count"],
        status["first_external_issue_received"],
        status["first_external_pr_received"],
        status["first_external_contribution_cycle_complete"],
    )):
        raise ConformanceError("external participation cannot be inferred or fabricated")
    if repair["status"] == "PR_CANDIDATE" and repair["complete"]:
        raise ConformanceError("repair PR candidate cannot claim completion")
    if repair["status"] == "COMPLETE" and not repair["complete"]:
        raise ConformanceError("completed repair status must claim completion")
    if not contribution["templates_installed"]:
        raise ConformanceError("historical activation templates must remain recorded")
    if status["state"] == "PUBLIC_CONTRIBUTION_ACTIVATION_CANDIDATE":
        candidate_writes = (
            contribution["issue_submission_active"],
            contribution["pull_request_submission_active"],
            contribution["specification_proposal_active"],
            contribution["adapter_integration_request_active"],
        )
        if contribution["active"] or contribution["activation_pr_merged"] or any(candidate_writes):
            raise ConformanceError("activation candidate must remain inactive before merge")
        if launch["active"] or status["public_contribution_activation"]["executed"]:
            raise ConformanceError("activation candidate cannot claim executed public opening")
        if activation_pr["merged"]:
            raise ConformanceError("activation candidate cannot claim a merged Activation PR")
        if activation_pr["created"]:
            if not isinstance(activation_pr["number"], int):
                raise ConformanceError("created Activation PR requires an integer number")
        elif activation_pr["number"] is not None or activation_pr["state"] != "NOT_CREATED":
            raise ConformanceError("uncreated Activation PR must retain null number and NOT_CREATED state")
    elif status["state"] == "LIMITED_REPOSITORY_CONTRIBUTION_PREVIEW":
        active_writes = (
            contribution["issue_submission_active"],
            contribution["pull_request_submission_active"],
            contribution["specification_proposal_active"],
            contribution["adapter_integration_request_active"],
        )
        if (
            not contribution["active"]
            or not contribution["activation_pr_merged"]
            or not all(active_writes)
        ):
            raise ConformanceError("active preview requires merged active templates")
        if not launch["active"] or not status["public_contribution_activation"]["executed"]:
            raise ConformanceError("active preview requires executed activation")
        if not activation_pr["merged"] or not status["welcome_issue"]["created"]:
            raise ConformanceError("active preview requires merged Activation PR and Welcome Issue")
        if not isinstance(activation_pr["number"], int):
            raise ConformanceError("active preview requires an Activation PR number")
        if not isinstance(status["welcome_issue"]["number"], int):
            raise ConformanceError("active preview requires a Welcome Issue number")
    elif status["state"] == "PRIVATE_COMMERCIALIZATION_BOUNDARY":
        current_writes = (
            contribution["issue_submission_active"],
            contribution["pull_request_submission_active"],
            contribution["specification_proposal_active"],
            contribution["adapter_integration_request_active"],
        )
        if (
            contribution["active"]
            or contribution["authorized"]
            or any(current_writes)
            or launch["active"]
            or launch["authorized"]
            or security["transport_active"]
            or security["transport_verified"]
            or security["activation_authorized"]
        ):
            raise ConformanceError("private commercialization boundary must disable public operation")
        history = status["historical_public_phase"]
        if (
            not history["occurred"]
            or not history["limited_public_preview_was_active"]
            or not activation_pr["merged"]
            or not status["welcome_issue"]["created"]
        ):
            raise ConformanceError("private boundary must preserve prior public-stage history")
        if (
            status["core_repository_visibility"] != "PRIVATE"
            or not status["private_core_is_canonical"]
            or not status["commercialization_boundary_design_active"]
            or not status["private_agent_customer_readiness_active"]
        ):
            raise ConformanceError("private commercialization machine state is incomplete")
    else:
        raise ConformanceError(f"unsupported community activation state: {status['state']}")
    if not status["draft_pr"]["merged"] or not status["draft_pr"]["ready_for_review"]:
        raise ConformanceError("core PR #41 merge history is incomplete")
    for key in ("community_member_count", "external_contributor_count", "external_adopter_count"):
        if status[key] != 0:
            raise ConformanceError(f"{key} must remain zero")
    assignments = load_json(
        TITMAS_ROOT / "community" / "interim-role-assignments.json"
    )
    if assignments["decision_reference"] != (
        "TITMAS-OPEN-STANDARDS-COMMUNITY-INTEGRATION-D01"
    ):
        raise ConformanceError("interim role assignment lacks decision binding")
    if not assignments["revocable"] or len(assignments["assignments"]) != 3:
        raise ConformanceError("interim role assignment is not bounded")
    prohibited = {
        "DBOS_AUTHORITY",
        "SAEE_AUTHORITY",
        "EVIDENCE_TRUTH_OWNERSHIP",
        "CERTIFICATION_AUTHORITY",
        "COMMERCIAL_AUTHORITY",
        "RELEASE_AUTHORITY",
    }
    if not prohibited.issubset(set(assignments["not_granted"])):
        raise ConformanceError("interim role assignment authority boundary drift")
    return {
        "community_invariants_checked": len(must_be_false) + 21,
        "interim_role_assignments_checked": len(assignments["assignments"]),
    }


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def merge_admission_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    draft = payload["draft_pr"]
    contribution = payload["public_contribution_surface"]
    security = payload["security"]
    maintainer = payload["maintainer"]
    launch = payload["public_launch"]

    if draft["created"] and "DRAFT_PR_NOT_CREATED" in payload["limitations"]:
        errors.append("STALE_DRAFT_PR_NOT_CREATED")
    if (
        contribution["templates_installed"]
        and not contribution["authorized"]
        and not payload.get("private_boundary_active", False)
    ):
        errors.append("TEMPLATES_INSTALLED_WITHOUT_AUTHORIZATION")
    if contribution["active"] and not security["transport_active"]:
        errors.append("CONTRIBUTION_ACTIVE_WITHOUT_SECURITY_TRANSPORT")
    if launch["active"] and not security["transport_active"]:
        errors.append("PUBLIC_LAUNCH_WITHOUT_SECURITY_TRANSPORT")
    if maintainer["interim_assigned"] and maintainer["formal_assigned"]:
        errors.append("INTERIM_MAINTAINER_AS_FORMAL_MAINTAINER")
    if (
        draft["state"] == "OPEN_DRAFT"
        and payload["canonical_main_integration_complete"]
    ):
        errors.append("OPEN_DRAFT_AS_CANONICAL_MAIN")
    if payload["dormant_path_auto_discoverable"]:
        errors.append("DORMANT_TEMPLATE_AUTO_DISCOVERABLE")
    if payload["active_destination_used_outside_activation_pr"]:
        errors.append("ACTIVE_DESTINATION_OUTSIDE_ACTIVATION_PR")
    return errors


def check_merge_admission_boundary() -> dict[str, Any]:
    status = load_json(TITMAS_ROOT / "community" / "community-status.json")
    dormant_root = TITMAS_ROOT / "community" / "github-activation-templates"
    manifest = load_json(dormant_root / "activation-manifest.json")
    repository_root = DBA_ROOT.parent

    candidate_state = status["state"] == "PUBLIC_CONTRIBUTION_ACTIVATION_CANDIDATE"
    active_state = status["state"] == "LIMITED_REPOSITORY_CONTRIBUTION_PREVIEW"
    private_state = status["state"] == "PRIVATE_COMMERCIALIZATION_BOUNDARY"
    if candidate_state:
        expected_manifest_status = "INSTALLED_ACTIVATION_PR_CANDIDATE"
    elif active_state:
        expected_manifest_status = "ACTIVE_LIMITED_PREVIEW"
    elif private_state:
        expected_manifest_status = "PRIVATE_BOUNDARY_HISTORICAL_PACKAGE_RETAINED"
    else:
        raise ConformanceError(f"unsupported merge-admission state: {status['state']}")
    if manifest["status"] != expected_manifest_status:
        raise ConformanceError(
            f"activation manifest status mismatch: {manifest['status']}"
        )
    if (
        not manifest["installed"]
        or manifest["authorized"] != active_state
        or manifest["active"] != active_state
        or not manifest["security_transport_required"]
        or not manifest["security_transport_verified"]
        or not manifest["activation_pr_required"]
    ):
        raise ConformanceError("activation manifest stage binding fails closed")

    expected_active = {
        ".github/ISSUE_TEMPLATE/bug.yml",
        ".github/ISSUE_TEMPLATE/config.yml",
        ".github/ISSUE_TEMPLATE/integration.yml",
        ".github/ISSUE_TEMPLATE/proposal.yml",
        ".github/pull_request_template.md",
    }
    recorded_active = set(manifest["intended_active_destinations"])
    if recorded_active != expected_active:
        raise ConformanceError("future active destination set drift")
    active_paths = [repository_root / path for path in sorted(expected_active)]
    installed = [str(path.relative_to(repository_root)) for path in active_paths if path.exists()]
    if set(installed) != expected_active:
        raise ConformanceError(
            f"authorized active GitHub template set incomplete: {installed}"
        )

    template_hashes_checked = 0
    issue_forms_checked = 0
    pr_templates_checked = 0
    for record in manifest["templates"]:
        dormant_rel = record["dormant_path"]
        dormant_path = (dormant_root / dormant_rel).resolve()
        if not dormant_path.is_relative_to(dormant_root.resolve()):
            raise ConformanceError(f"dormant template escapes package: {dormant_rel}")
        if dormant_path.is_symlink() or not dormant_path.is_file():
            raise ConformanceError(f"missing regular dormant template: {dormant_rel}")
        if record["future_active_path"] not in expected_active:
            raise ConformanceError(f"unapproved future active path: {record['future_active_path']}")
        digest = hashlib.sha256(dormant_path.read_bytes()).hexdigest()
        if digest != record["sha256"]:
            raise ConformanceError(f"dormant template hash mismatch: {dormant_rel}")
        if manifest["content_hashes"].get(dormant_rel) != f"sha256:{digest}":
            raise ConformanceError(f"content_hashes mismatch: {dormant_rel}")
        active_path = repository_root / record["future_active_path"]
        if active_path.is_symlink() or not active_path.is_file():
            raise ConformanceError(
                f"missing regular active template candidate: {record['future_active_path']}"
            )
        active_digest = hashlib.sha256(active_path.read_bytes()).hexdigest()
        if active_digest != digest:
            raise ConformanceError(
                f"active template hash differs from activation package: {dormant_rel}"
            )
        text = dormant_path.read_text(encoding="utf-8")
        if record["template_type"] == "GITHUB_ISSUE_FORM":
            for field in ("name:", "description:", "body:"):
                if not any(line.startswith(field) for line in text.splitlines()):
                    raise ConformanceError(f"{dormant_rel}: missing Issue Form field {field}")
            issue_forms_checked += 1
        elif record["template_type"] == "GITHUB_ISSUE_CONFIG":
            for field in ("blank_issues_enabled:", "contact_links:"):
                if not any(line.startswith(field) for line in text.splitlines()):
                    raise ConformanceError(f"{dormant_rel}: missing Issue config field {field}")
            issue_forms_checked += 1
        elif record["template_type"] == "GITHUB_PULL_REQUEST_TEMPLATE":
            if not text.startswith("# ") or "- [ ]" not in text:
                raise ConformanceError("dormant Pull Request template is structurally incomplete")
            pr_templates_checked += 1
        else:
            raise ConformanceError(f"unknown dormant template type {record['template_type']}")
        template_hashes_checked += 1

    positive = load_json(
        TITMAS_ROOT / "conformance" / "fixtures" / "merge-admission" / "positive.json"
    )
    for case in positive["cases"]:
        errors = merge_admission_errors(case["payload"])
        if errors != case["expected_errors"]:
            raise ConformanceError(f"{case['id']}: expected {case['expected_errors']}, got {errors}")
    base_payload = positive["cases"][0]["payload"]
    negative = load_json(
        TITMAS_ROOT / "conformance" / "fixtures" / "merge-admission" / "negative.json"
    )
    for case in negative["cases"]:
        errors = merge_admission_errors(deep_merge(base_payload, case["patch"]))
        if case["expected_error"] not in errors:
            raise ConformanceError(f"{case['id']}: expected {case['expected_error']}, got {errors}")

    actual_payload = {
        "draft_pr": status["draft_pr"],
        "limitations": status["limitations"],
        "public_contribution_surface": status["public_contribution_surface"],
        "security": status["security"],
        "maintainer": status["maintainer"],
        "public_launch": status["public_launch"],
        "canonical_main_integration_complete": status["canonical_main_integration_complete"],
        "community_established": status["community_established"],
        "infrastructure_complete": status["infrastructure_complete"],
        "dormant_path_auto_discoverable": False,
        "active_destination_used_outside_activation_pr": False,
        "private_boundary_active": private_state,
    }
    actual_errors = merge_admission_errors(actual_payload)
    if actual_errors:
        raise ConformanceError(f"current merge-admission state is unsafe: {actual_errors}")
    if not status["infrastructure_complete"] or status["community_established"]:
        raise ConformanceError("community infrastructure and establishment boundary drift")

    return {
        "stage_consistency_checks": 15,
        "active_titmas_issue_template_count": sum(
            path.exists() for path in active_paths if "ISSUE_TEMPLATE" in str(path)
        ),
        "active_titmas_pull_request_template_count": sum(
            path.exists() for path in active_paths if path.name == "pull_request_template.md"
        ),
        "dormant_template_hashes_checked": template_hashes_checked,
        "dormant_issue_templates_structurally_checked": issue_forms_checked,
        "dormant_pr_templates_structurally_checked": pr_templates_checked,
        "positive_cases_passed": len(positive["cases"]),
        "negative_cases_rejected": len(negative["cases"]),
    }


def check_internal_reviews() -> dict[str, Any]:
    review_paths = sorted((TITMAS_ROOT / "reviews").glob("integration-*.json"))
    required_scopes = {
        "CANONICAL_ARCHITECTURE",
        "OPEN_STANDARDS_AND_CONFORMANCE",
        "AGENT_NATIVE_USABILITY",
        "SECURITY_AND_CLAIMS",
    }
    if len(review_paths) != len(required_scopes):
        raise ConformanceError(
            f"expected {len(required_scopes)} integration reviews, "
            f"found {len(review_paths)}"
        )
    findings = 0
    scopes: set[str] = set()
    lineages: set[str] = set()
    for path in review_paths:
        review = load_json(path)
        required = {
            "review_id", "review_scope", "provider", "requested_model",
            "returned_model", "reviewer_lineage", "verdict", "findings",
            "blocking", "required_correction", "limitations",
            "authority_effect",
        }
        missing = sorted(required - review.keys())
        if missing:
            raise ConformanceError(f"{path.name}: missing fields {missing}")
        if review["requested_model"] != review["returned_model"]:
            raise ConformanceError(f"{path.name}: silent model substitution")
        if review["authority_effect"] != "NONE":
            raise ConformanceError(f"{path.name}: review creates authority")
        if review["verdict"] not in {"PASS", "REVISION_REQUIRED", "REJECT", "HOLD"}:
            raise ConformanceError(f"{path.name}: invalid review verdict")
        severities = {item["severity"] for item in review["findings"]}
        if severities & {"HIGH", "CRITICAL"} and review["verdict"] == "PASS":
            raise ConformanceError(f"{path.name}: HIGH/CRITICAL finding cannot PASS")
        scopes.add(review["review_scope"])
        lineages.add(review["reviewer_lineage"])
        findings += len(review["findings"])
    if scopes != required_scopes:
        raise ConformanceError(f"integration review scope drift: {sorted(scopes)}")
    if len(lineages) != len(required_scopes):
        raise ConformanceError("integration reviews must use distinct lineages")
    return {
        "review_sessions_checked": len(review_paths),
        "independent_lineages_checked": len(lineages),
        "findings_checked": findings,
    }


def validate_json_file(path: Path, schema_path: Path) -> dict[str, Any]:
    value = load_json(path)
    schema = load_json(schema_path)
    validation_value = dict(value)
    validation_value.pop("$schema", None)
    validate_schema(validation_value, schema, path=str(path.relative_to(DBA_ROOT)))
    return value


def check_agent_native_surfaces() -> dict[str, Any]:
    root = TITMAS_ROOT / "agent-native"
    schemas = root / "schemas"
    entry = validate_json_file(DBA_ROOT / "agent-index.json", schemas / "agent-index.schema.json")
    manifest = validate_json_file(root / "community-manifest.json", schemas / "community-manifest.schema.json")
    state = validate_json_file(root / "current-state.json", schemas / "current-state.schema.json")
    if not entry["canonical_agent_entry"]:
        raise ConformanceError("agent-index.json must be the canonical agent entry")
    if manifest["canonical_entry"] != "../../agent-index.json":
        raise ConformanceError("community manifest creates a competing machine entry")

    must_be_false = (
        "public_agent_community_authorized", "agent_community_established",
        "release_authorized",
        "certification_authorized", "commercial_ready", "foundation_created",
        "cs_g0_pass", "cs_g1_pass", "current_99_percent_autonomy_claim",
    )
    elevated = [key for key in must_be_false if state[key] is not False]
    if elevated:
        raise ConformanceError(f"agent-native state semantic elevation: {elevated}")
    if not state["canonical_main_integration_complete"]:
        raise ConformanceError("agent-native canonical integration history is incomplete")
    current_public_flags = (
        state["public_contribution_authorized"],
        state["public_contribution_active"],
        state["public_github_agent_write_authorized"],
        state["public_github_agent_write_active"],
        state["public_launch_authorized"],
        state["public_launch_active"],
    )
    if any(current_public_flags):
        raise ConformanceError("private commercialization boundary must disable public Agent operations")
    if (
        state["core_repository_visibility"] != "PRIVATE"
        or not state["private_core_is_canonical"]
        or state["open_standards_community_operation_active"]
        or not state["commercialization_boundary_design_active"]
        or not state["private_agent_customer_readiness_active"]
    ):
        raise ConformanceError("agent-native private commercialization state is incomplete")
    if state["public_contribution_activation_candidate"]:
        if state["public_contribution_active"] or state["public_github_agent_write_active"]:
            raise ConformanceError("activation candidate cannot claim active public writes")
        if state["public_launch_active"]:
            raise ConformanceError("activation candidate cannot claim active public launch")
    if state["agent_operational_majority_long_term_target"] != 0.99:
        raise ConformanceError("long-term target drift")
    for key in (
        "external_agent_participant_count", "external_human_contributor_count",
        "external_adopter_count",
    ):
        if state[key] != 0:
            raise ConformanceError(f"{key} must remain zero")

    participant_registry = load_json(root / "participants" / "participant-registry.json")
    validate_json_file(
        root / "participants" / "authority-registry.json",
        schemas / "authority-registry.schema.json",
    )
    participants = participant_registry["participants"]
    if participant_registry["agent_participant_count"] != len(participants):
        raise ConformanceError("agent participant count mismatch")
    lineages = {item["lineage_ref"] for item in participants}
    if participant_registry["independent_agent_lineage_count"] != len(lineages):
        raise ConformanceError("independent agent lineage count mismatch")
    for participant in participants:
        validate_schema(participant, load_json(schemas / "participant.schema.json"))
        if participant["participant_ref"] == participant["authority_issuer_ref"]:
            raise ConformanceError("participant self-authorization")

    task_registry = load_json(root / "tasks" / "task-registry.json")
    tasks = task_registry["tasks"]
    if not tasks or len({item["task_id"] for item in tasks}) != len(tasks):
        raise ConformanceError("task registry must contain unique community tasks")
    task_schema = load_json(schemas / "task.schema.json")
    for task in tasks:
        validate_schema(task, task_schema)
        if task["source_revision"] != task_registry["source_revision"]:
            raise ConformanceError(f"{task['task_id']}: source revision drift")
        if task["authority_reference"] != "TITMAS-AGENT-NATIVE-COMMUNITY-D01":
            raise ConformanceError(f"{task['task_id']}: unauthorized authority reference")
    for evidence_ref in state["evidence_refs"]:
        if not (DBA_ROOT / evidence_ref).is_file():
            raise ConformanceError(f"current state evidence ref missing: {evidence_ref}")

    examples = (
        (root / "participants" / "example-capability-declaration.json", "capability-declaration"),
        (root / "participants" / "example-role-assignment.json", "role-assignment"),
        (root / "participants" / "example-revocation-record.json", "revocation-record"),
        (root / "participants" / "example-expiry-record.json", "expiry-record"),
        (root / "tasks" / "example-scope-lease.json", "scope-lease"),
        (root / "contributions" / "example-contribution-package.json", "contribution-package"),
        (root / "reviews" / "review-protocol.json", None),
        (root / "maintenance" / "example-maintenance-report.json", "maintenance-report"),
        (root / "recommendations" / "example-recommendation-package.json", "recommendation-package"),
        (root / "handoff" / "example-handoff-package.json", "handoff-package"),
    )
    checked = 0
    for path, schema_name in examples:
        if schema_name:
            value = validate_json_file(path, schemas / f"{schema_name}.schema.json")
            if schema_name == "contribution-package":
                serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
                if "PILOT-" in serialized or "CONTROLLED_LOCAL_PILOT" in serialized:
                    raise ConformanceError(
                        "canonical contribution example retains legacy pilot identity"
                    )
        else:
            load_json(path)
        checked += 1
    return {
        "canonical_machine_entries": 1,
        "agent_participants_checked": len(participants),
        "independent_lineages_checked": len(lineages),
        "agent_tasks_checked": len(tasks),
        "agent_protocol_examples_checked": checked,
        "authority_invariants_checked": len(must_be_false),
    }


def check_agent_native_adversarial() -> dict[str, Any]:
    payload = load_json(TITMAS_ROOT / "agent-native" / "security" / "adversarial-cases.json")
    cases = payload["cases"]
    required_attacks = {
        "PROMPT_INJECTION", "MALICIOUS_TASK_DESCRIPTION",
        "FORGED_PARTICIPANT_IDENTITY", "SELF_AUTHORIZATION", "SELF_APPROVAL",
        "AUTHORITY_ELEVATION", "TASK_SCOPE_EXPANSION", "REVIEW_COLLUSION",
        "SYBIL_SESSION_AS_INDEPENDENT_LINEAGE", "INFINITE_TASK_LOOP",
        "AUTOMATIC_ISSUE_PR_NOISE", "DUPLICATE_CONTRIBUTION",
        "MALICIOUS_SCHEMA", "PATH_TRAVERSAL", "HIDDEN_NETWORK_CALL",
        "SUPPLY_CHAIN_DEPENDENCY", "FAKE_ADOPTION", "FAKE_CERTIFICATION",
        "DELETE_FAILURE_RECORD", "NOT_ASSESSED_TO_PASS",
        "RECOMMENDATION_TO_COMMAND", "EVIDENCE_TO_TRUTH",
    }
    observed = {item["attack"] for item in cases}
    if observed != required_attacks:
        raise ConformanceError(f"adversarial case coverage drift: {sorted(required_attacks - observed)}")
    bad = [item["id"] for item in cases if item["expected"] != "REJECT" or not item["reason_code"]]
    if bad:
        raise ConformanceError(f"adversarial cases fail open: {bad}")
    cli_path = TITMAS_ROOT / "agent-native" / "community_cli.py"
    spec = importlib.util.spec_from_file_location("titmas_agent_native_cli", cli_path)
    if not spec or not spec.loader:
        raise ConformanceError("cannot load agent-native policy evaluator")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    mismatches = []
    for item in cases:
        decision = cli.reject_adversarial(item["attack"])
        if (
            decision["decision"] != item["expected"]
            or decision["reason_code"] != item["reason_code"]
        ):
            mismatches.append(item["id"])
    if mismatches:
        raise ConformanceError(f"adversarial policy mismatch: {mismatches}")
    return {
        "adversarial_cases_rejected": len(cases),
        "adversarial_cases_executed": len(cases),
    }


def check_bounded_evolution_surfaces() -> dict[str, Any]:
    root = TITMAS_ROOT / "agent-native" / "evolution"
    machine_files = (
        "evolution-policy.json",
        "evolution-state-machine.json",
        "risk-classification.json",
        "fitness-profile.json",
        "self-healing-registry.json",
        "evolution-capability.json",
        "canonical-owner-map.json",
        "mutation-limits.json",
    )
    machine_values = {name: load_json(root / name) for name in machine_files}
    capability = machine_values["evolution-capability.json"]
    policy = machine_values["evolution-policy.json"]
    if capability["status"] != "BOUNDED_SELF_HEALING_AND_EVOLUTION_CANDIDATE":
        raise ConformanceError("D19 discovery layer maturity is elevated or incomplete")
    if capability["public_launch_authorized"] or capability["community_established"]:
        raise ConformanceError("D19 reference layer must not claim public launch")
    if policy["automatic_production_evolution"]:
        raise ConformanceError("D19 must not authorize production evolution")
    if policy["p0_10"]["automatic_reopen"]:
        raise ConformanceError("D19 must not reopen P0-10")

    schema_files = sorted((root / "schemas").glob("*.schema.json"))
    if len(schema_files) != 7:
        raise ConformanceError("D19 requires exactly seven normative object schemas")
    schemas_checked = 0
    for schema_path in schema_files:
        schema = load_json(schema_path)
        if schema.get("type") != "object" or not schema.get("required"):
            raise ConformanceError(f"{schema_path.name}: incomplete normative schema")
        schemas_checked += 1
    owner_map = machine_values["canonical-owner-map.json"]
    serialized = json.dumps(machine_values, sort_keys=True)
    forbidden = ("automatic_merge\": true", "automatic_activation\": true", "self_grant")
    if any(item in serialized for item in forbidden):
        raise ConformanceError("D19 contract contains prohibited authority semantics")
    if "titmac-scout" not in json.dumps(owner_map, sort_keys=True):
        raise ConformanceError("D19 canonical implementation owner is not titmac-scout")
    return {
        "machine_surfaces_checked": len(machine_files),
        "normative_schemas_checked": schemas_checked,
        "architecture_only": True,
        "executable_engine_files": 0,
        "evolution_run_files": 0,
    }


LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

PUBLIC_ENTRY_DOCUMENTS = (
    DBA_ROOT.parent / "README.md",
    DBA_ROOT / "CONTRIBUTING.md",
    TITMAS_ROOT / "README.md",
    TITMAS_ROOT / "QUICKSTART.md",
    TITMAS_ROOT / "FIRST_CONTRIBUTION.md",
    TITMAS_ROOT / "community" / "CONTRIBUTING.md",
    TITMAS_ROOT / "community" / "STARTER_TASKS.md",
    TITMAS_ROOT / "community" / "SECURITY.md",
    DBA_ROOT / "SECURITY.md",
    DBA_ROOT / "llms.txt",
)


def check_public_entry_consistency() -> dict[str, Any]:
    projection = load_json(
        TITMAS_ROOT / "community" / "welcome-issue-43-entry-projection.json"
    )
    status = load_json(TITMAS_ROOT / "community" / "community-status.json")
    agent_entry = load_json(DBA_ROOT / "agent-index.json")
    entries = {
        item["id"]: item["repository_path"]
        for item in projection["repository_entries"]
    }
    expected_ids = {
        "HUMAN_ENTRY",
        "CONTRIBUTING",
        "FIRST_CONTRIBUTION",
        "AGENT_ENTRY",
        "LLMS_ENTRY",
        "STARTER_TASKS",
        "SPECIFICATION_REGISTRY",
    }
    resolved_entries: dict[str, Path] = {}
    pe01 = (
        set(entries) == expected_ids
        and len(projection["repository_entries"]) == len(expected_ids)
    )
    for entry_id, raw_path in entries.items():
        resolved = (DBA_ROOT / raw_path).resolve()
        if not resolved.is_relative_to(DBA_ROOT.resolve()):
            pe01 = False
            continue
        resolved_entries[entry_id] = resolved
        if resolved.is_symlink() or not resolved.is_file():
            pe01 = False

    command = projection["conformance"]
    command_path = (DBA_ROOT / command["script_path"]).resolve()
    pe02 = (
        command["working_directory"] == "digital-biosphere-architecture"
        and command["command"] == "python3 TITMAS/conformance/harness.py"
        and command_path == Path(__file__).resolve()
        and command_path.is_file()
    )

    status_human_entry = (
        TITMAS_ROOT / "community" / status["human_entry"]
    ).resolve()
    pe03 = (
        entries.get("HUMAN_ENTRY") == "TITMAS/README.md"
        and resolved_entries.get("HUMAN_ENTRY") == status_human_entry
        and agent_entry["canonical_agent_entry"] is True
        and entries.get("AGENT_ENTRY") == "agent-index.json"
    )
    pe04 = (
        entries.get("FIRST_CONTRIBUTION") == "TITMAS/FIRST_CONTRIBUTION.md"
        and resolved_entries.get("FIRST_CONTRIBUTION", Path()).is_file()
    )

    starter_path = resolved_entries.get("STARTER_TASKS")
    registry_path = (DBA_ROOT / projection["task_registry"]).resolve()
    registries = sorted(TITMAS_ROOT.rglob("task-registry.json"))
    starter_targets: list[Path] = []
    if starter_path is not None and starter_path.is_file():
        for raw in LINK_PATTERN.findall(starter_path.read_text(encoding="utf-8")):
            target = raw.strip().split("#", 1)[0]
            if target and "://" not in target:
                starter_targets.append((starter_path.parent / target).resolve())
    pe05 = (
        starter_path is not None
        and starter_path.is_file()
        and registry_path.is_file()
        and registries == [registry_path]
        and registry_path in starter_targets
    )
    pe06 = (
        entries.get("SPECIFICATION_REGISTRY") == "TITMAS/specifications/registry.yaml"
        and resolved_entries.get("SPECIFICATION_REGISTRY", Path()).is_file()
    )

    security_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (DBA_ROOT / "SECURITY.md", TITMAS_ROOT / "community" / "SECURITY.md")
    )
    pe07 = (
        projection["security"]["transport"] == "GITHUB_PRIVATE_VULNERABILITY_REPORTING"
        and projection["security"]["active_at_live_verification"] is True
        and "Private Vulnerability Reporting" in security_text
        and status["security"]["transport_active"] is False
        and status["security"]["transport_verified"] is False
        and status["security"]["public_activation_blocked"] is True
    )

    public_text = "\n".join(
        path.read_text(encoding="utf-8") for path in PUBLIC_ENTRY_DOCUMENTS
    )
    activation_stale = re.compile(
        r"PUBLIC_CONTRIBUTION_ACTIVATION_CANDIDATE|"
        r"CANONICAL_INTEGRATION_CANDIDATE|"
        r"pending (?:the )?Activation PR|"
        r"Activation PR[^.\n]*(?:not yet merged|pending)|"
        r"remain inactive until merge",
        re.IGNORECASE,
    )
    pe08 = (
        activation_stale.search(public_text) is None
        and agent_entry["public_contribution_state"]["activation_pr_merged"] is True
        and status["historical_public_phase"]["limited_public_preview_was_active"] is True
    )

    inactive_stale = re.compile(
        r"PUBLIC_CONTRIBUTION_SURFACE_ACTIVE=false|"
        r"PUBLIC_CONTRIBUTION_SURFACE_AUTHORIZED=false|"
        r"public contribution[^.\n]*inactive|"
        r"public contribution opening is pending",
        re.IGNORECASE,
    )
    pe09 = (
        inactive_stale.search(public_text) is not None
        and status["public_contribution_surface"]["active"] is False
        and status["public_contribution_surface"]["authorized"] is False
        and agent_entry["public_contribution_state"]["surface_active"] is False
        and agent_entry["public_contribution_state"]["surface_authorized"] is False
    )
    pe10 = (
        "COMMUNITY_ESTABLISHED=true" not in public_text
        and "TITMAS_COMMUNITY_ESTABLISHED=true" not in public_text
        and status["community_established"] is False
        and projection["non_claims"]["community_established"] is False
        and agent_entry["community_incubation_state"]["community_established"] is False
    )

    checks = {
        "PE-01": pe01,
        "PE-02": pe02,
        "PE-03": pe03,
        "PE-04": pe04,
        "PE-05": pe05,
        "PE-06": pe06,
        "PE-07": pe07,
        "PE-08": pe08,
        "PE-09": pe09,
        "PE-10": pe10,
    }
    failed = [check_id for check_id, passed in checks.items() if not passed]
    if failed:
        raise ConformanceError(f"public entry consistency failed: {failed}")
    if (
        projection["live_github_truth"] is not False
        or projection["live_verification_required"] is not True
    ):
        raise ConformanceError("Issue projection must not masquerade as live GitHub truth")
    if (
        projection["source_issue_number"] != 43
        or projection["source_issue_state"] != "OPEN"
        or projection["source_branch"] != "main"
        or projection["source_issue_title"]
        != "Welcome to the TITMAS Agent-Native Standards Community Preview"
        or re.fullmatch(r"[0-9a-f]{64}", projection["source_body_sha256"]) is None
    ):
        raise ConformanceError("Issue projection identity or hash binding is invalid")
    return {
        "public_entry_consistency_tests_passed": len(checks),
        "checks": sorted(checks),
        "repository_entries_checked": len(resolved_entries),
        "welcome_issue_body_sha256": projection["source_body_sha256"],
        "live_github_truth": False,
    }


def check_local_links() -> dict[str, Any]:
    checked = 0
    for path in sorted(TITMAS_ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw in LINK_PATTERN.findall(text):
            target = raw.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(DBA_ROOT.resolve()):
                raise ConformanceError(f"{path}: local link escapes DBA root {raw}")
            if not resolved.exists():
                raise ConformanceError(f"{path}: missing local link {raw}")
            checked += 1
    return {"local_links_checked": checked}


def run_all(write_report: bool = True) -> dict[str, Any]:
    checks = []
    functions = (
        ("registries", check_registries),
        ("frontmatter", check_frontmatter),
        ("fixtures", check_fixtures),
        ("stage5_contributions", check_stage5_contributions),
        ("community_status", check_community_status),
        ("merge_admission_boundary", check_merge_admission_boundary),
        ("internal_reviews", check_internal_reviews),
        ("agent_native_surfaces", check_agent_native_surfaces),
        ("agent_native_adversarial", check_agent_native_adversarial),
        ("bounded_evolution_surfaces", check_bounded_evolution_surfaces),
        ("public_entry_consistency", check_public_entry_consistency),
        ("local_links", check_local_links),
    )
    overall = "PASS"
    for name, function in functions:
        try:
            details = function()
            checks.append({"id": name, "status": "PASS", "details": details})
        except Exception as exc:  # fail closed with stable diagnostic
            overall = "FAIL"
            checks.append({
                "id": name,
                "status": "FAIL",
                "error": f"{type(exc).__name__}: {exc}",
                "remediation": f"Correct the reported {name} input and rerun: python3 TITMAS/conformance/harness.py",
            })
    report = {
        "report_version": "1.0.0",
        "profile": "TITMAS_DEVELOPMENT_CONFORMANCE",
        "status": overall,
        "checks": checks,
        "non_claims": [
            "CONFORMANCE_NE_TRUTH",
            "CONFORMANCE_NE_AUTHORIZATION",
            "CONFORMANCE_NE_ADOPTION",
            "CONFORMANCE_NE_CERTIFICATION"
        ],
    }
    if write_report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    report = run_all(write_report=True)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
