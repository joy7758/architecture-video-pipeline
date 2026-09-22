#!/usr/bin/env python3
"""Reconstruct the bounded private Stage 5 protocol surface.

The builder is allowlist-only and default-deny. It emits contracts,
documentation and synthetic examples, never private implementation source,
internal tests, credentials, Provider configuration, Git history, real
Evidence or customer data.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any


TITMAS_ROOT = Path(__file__).resolve().parents[1]
DBA_ROOT = TITMAS_ROOT.parent
OUTPUT_ROOT = TITMAS_ROOT / "private-stage5-protocol-surface"
SCHEMA_ROOT = TITMAS_ROOT / "conformance" / "schemas"
BUILDER_REF = "TITMAS/private-governance/build_stage5_protocol_surface.py"

CANONICAL_SCHEMAS = {
    "schemas/specification-proposal.schema.json":
        "stage5-specification-proposal.schema.json",
    "schemas/adapter-mapping.schema.json":
        "stage5-adapter-mapping.schema.json",
    "schemas/test-vector.schema.json":
        "stage5-test-vector.schema.json",
    "schemas/contribution-result.schema.json":
        "stage5-contribution-result.schema.json",
    "schemas/review.schema.json":
        "stage5-review.schema.json",
}

CLASSIFICATIONS = {
    "README.md": "COMMERCIAL_CUSTOMER_ONLY",
    "standard-catalog.json": "COMMERCIAL_CUSTOMER_ONLY",
    "task-catalog.json": "COMMERCIAL_CUSTOMER_ONLY",
    "api-contract.json": "COMMERCIAL_CUSTOMER_ONLY",
    "error-codes.json": "COMMERCIAL_CUSTOMER_ONLY",
    "synthetic-examples.json": "PUBLIC_SYNTHETIC_EXAMPLE",
    **{name: "PUBLIC_PROTOCOL" for name in CANONICAL_SCHEMAS},
}

PRIVATE_PATHS = re.compile(r"/(?:Users|private|home|var|tmp)/|[A-Za-z]:\\")
SECRETS = re.compile(
    r"sk-(?:proj|sp)-[A-Za-z0-9._-]{12,}|"
    r"Authorization\s*:\s*Bearer\s+[A-Za-z0-9._~+/=-]{12,}|"
    r"(?:DASHSCOPE|QIANFAN|ARK|OPENAI|DEEPSEEK)_API_KEY\s*=",
    re.IGNORECASE,
)
CORE_SYMBOLS = re.compile(
    r"\b(?:GatewayService|AtomicJSONWriter|capture_response|"
    r"build_public_surface_candidate|source-classification-registry)\b"
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_blob_sha(value: bytes) -> str:
    header = f"blob {len(value)}\0".encode("ascii")
    return hashlib.sha1(header + value).hexdigest()


def read_bytes(relative: str) -> bytes:
    path = (DBA_ROOT / relative).resolve()
    if not path.is_relative_to(DBA_ROOT.resolve()):
        raise ValueError("source escapes DBA root")
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"invalid source: {relative}")
    return path.read_bytes()


def disclosure(assisted: bool = False) -> dict[str, Any]:
    return {
        "assisted": assisted,
        "provider": "NONE" if not assisted else "DECLARATION_REQUIRED",
        "model": "NONE" if not assisted else "EXACT_MODEL_REQUIRED",
        "scope": "DETERMINISTIC_SYNTHETIC_EXAMPLE",
        "human_accountability": "REQUIRED",
    }


def synthetic_proposal() -> dict[str, Any]:
    return {
        "proposal_id": "STAGE5-PROP-IDENTITY-HANDOFF",
        "title": "Bounded identity handoff failure code",
        "problem": "Developers need one interoperable failure code when identity handoff provenance is missing.",
        "developer_value": "A stable failure classification reduces framework ambiguity without granting Authority.",
        "scope": ["Define one failure code and fail-closed behavior."],
        "non_goals": ["Do not create identity, Permission or Authority."],
        "affected_objects": ["IDENTITY_OBJECT"],
        "proposed_change": {
            "summary": "Add a bounded MISSING_IDENTITY_PROVENANCE reason code to the Development profile.",
            "field_changes": ["Add one reason-code enum without changing identity ownership."],
        },
        "compatibility": "BACKWARD_COMPATIBLE",
        "positive_cases": ["Complete provenance continues through handoff."],
        "negative_cases": ["Missing provenance returns the bounded reason code."],
        "failure_behavior": "Return NOT_ASSESSED and require Human review; never infer identity.",
        "source_refs": ["catalog:DRAFT-ID-CORE-INTEROP-001"],
        "ai_assistance_disclosure": disclosure(),
        "human_decisions_required": ["Human Maintainer decides candidate inclusion."],
    }


def synthetic_adapter() -> dict[str, Any]:
    return {
        "adapter_id": "STAGE5-ADAPTER-SYNTHETIC-TRACE",
        "source_system": "SyntheticTrace",
        "source_version": "1.0",
        "source_license": "Synthetic fixture only",
        "source_semantics": ["trace_id identifies an observation, not Evidence Truth."],
        "titmas_bindings": [{
            "source_field": "trace_id",
            "titmas_object": "EXECUTION_OBJECT",
            "titmas_field": "observation_reference",
            "mapping_rule": "Map as an observation reference only.",
        }],
        "unsupported_fields": ["raw_payload"],
        "conflicts": ["Observation must not be elevated to Evidence Truth."],
        "positive_cases": ["A trace identifier maps to an observation reference."],
        "negative_cases": ["A trace identifier cannot authorize execution."],
        "limitations": ["SYNTHETIC_MAPPING_ONLY"],
        "ai_assistance_disclosure": disclosure(),
    }


def synthetic_vector() -> dict[str, Any]:
    return {
        "vector_id": "STAGE5-VECTOR-MISSING-PROVENANCE",
        "target_specification": "DRAFT-ID-CORE-INTEROP-001",
        "input": {"identity_provenance": None},
        "expected_result": {"status": "NOT_ASSESSED"},
        "expected_reason_code": "TITMAS-MISSING-IDENTITY-PROVENANCE",
        "positive_or_negative": "NEGATIVE",
        "failure_classification": "BOUNDARY",
        "source_refs": ["catalog:DRAFT-ID-CORE-INTEROP-001"],
        "limitations": ["SYNTHETIC_TEST_VECTOR_ONLY"],
    }


def readme() -> str:
    return """# TITMAS Stage 5 Private Protocol Surface

中文：TITMAS 第五阶段私有协议表面。

This private candidate explains how an AI Agent or developer can discover and
submit a bounded Specification Proposal, Adapter Mapping or Test Vector without
receiving private core source. It is not a public release, implementation
license, standard adoption, Runtime, certification or commercial agreement.

## Position and core terms

- **Specification Proposal** describes a bounded standards problem and change.
- **Adapter Mapping** maps source semantics without claiming adoption.
- **Test Vector** states synthetic input, expected result and failure behavior.
- **Conformance** validates the declared Development contract; it is not Truth.
- **Sandbox Key** controls ephemeral access, not source ownership.
- **Human Maintainer** makes final pilot and candidate disposition.

## Files

- `standard-catalog.json`: bounded Development specification catalog.
- `task-catalog.json`: customer-safe problem catalog.
- `api-contract.json`: loopback Sandbox contract.
- `error-codes.json`: customer-visible failure codes.
- `schemas/`: contribution, result and review contracts.
- `synthetic-examples.json`: non-confidential examples.

## Conformance client

Submit one object through the SDK, then call the submission validation
operation. `CONFORMANCE_PASS` advances only to
`HUMAN_DISPOSITION_REQUIRED`; it never becomes `STANDARD_ADOPTED`, `STABLE` or
`CERTIFIED`. A malformed or semantically elevated object fails closed.

## SDK interface

The Python client supports catalog and task discovery, three submission
methods, explicit validation, status retrieval and review submission. It
constructs authenticated requests, performs bounded Schema preflight and parses
customer-visible errors. It never retries a dispatched request automatically.

## Version rules

This surface is `1.0.0` Development preview material. Additive fields require a
minor version and explicit compatibility declaration. Breaking changes require
a new major version and Human Decision. Version change is not deployment or
adoption.

## AI assistance disclosure

Every Proposal and Adapter Mapping declares whether AI assisted, exact Provider
and model identity, assistance scope and required Human accountability. Model
output cannot self-approve, assign Authority or become an adopted standard.

## Non-claims

```text
PUBLIC_RELEASE_ALLOWED=false
PRIVATE_STAGE_5_USE_ALLOWED=true
PRIVATE_CORE_SOURCE_INCLUDED=false
KEY_IS_SOURCE_LICENSE=false
CONFORMANCE_PASS_NE_ADOPTION=true
PILOT_ACCEPTANCE_NE_STANDARD_ADOPTION=true
COMMUNITY_ESTABLISHED=false
```
"""


def build_payloads() -> dict[str, bytes]:
    registry = json.loads(
        read_bytes("TITMAS/specifications/registry.yaml").decode("utf-8")
    )
    tasks = json.loads(
        read_bytes("TITMAS/agent-native/tasks/task-registry.json").decode("utf-8")
    )
    catalog = {
        "surface_version": "1.0.0",
        "maturity": "Development",
        "specifications": [{
            "id": item["id"],
            "title": item["title"],
            "category": item["category"],
            "version": item["version"],
            "maturity": item["maturity"],
            "normative": item["normative"],
            "limitations": item["limitations"],
        } for item in registry["entries"]],
        "non_claims": ["NOT_PUBLIC_RELEASE", "NOT_STANDARD_ADOPTION"],
    }
    task_catalog = {
        "surface_version": "1.0.0",
        "tasks": [{
            "task_id": item["task_id"],
            "title": item["title"],
            "problem_context": item["problem_context"],
            "value_hypothesis": item["value_hypothesis"],
            "relevance_conditions": item["relevance_conditions"],
            "non_applicable_conditions": item["non_applicable_conditions"],
            "expected_outputs": item["expected_outputs"],
            "status": item["status"],
        } for item in tasks["tasks"]],
        "selection_policy": "AGENT_SELECTS_EXACTLY_ONE_BOUNDED_CONTRIBUTION",
    }
    api_contract = {
        "version": "1.0.0",
        "mode": "LOCAL_EPHEMERAL_PRIVATE_STAGE5",
        "endpoint_binding": "127.0.0.1:OS_ASSIGNED_EPHEMERAL_PORT",
        "operations": [
            "GET /v1/standards/catalog",
            "GET /v1/standards/tasks",
            "POST /v1/contributions/proposals",
            "POST /v1/contributions/adapters",
            "POST /v1/contributions/test-vectors",
            "GET /v1/contributions/{submission_id}",
            "POST /v1/contributions/{submission_id}/validate",
            "POST /v1/contributions/{submission_id}/reviews",
            "GET /v1/contributions/{submission_id}/result"
        ],
        "contribution_types": [
            "SPECIFICATION_PROPOSAL", "ADAPTER_MAPPING", "TEST_VECTOR"
        ],
        "states": [
            "RECEIVED", "VALIDATING", "CONFORMANCE_PASS", "CONFORMANCE_FAIL",
            "REVIEW_REQUIRED", "HUMAN_DISPOSITION_REQUIRED",
            "PILOT_ACCEPTED", "PILOT_REJECTED"
        ],
        "prohibited_states": ["STANDARD_ADOPTED", "STABLE", "CERTIFIED"],
        "authority_effect": "NONE",
    }
    errors = {
        "version": "1.0.0",
        "errors": [
            {"http_status": 400, "code": "TITMAS-STAGE5-400-MALFORMED"},
            {"http_status": 401, "code": "TITMAS-STAGE5-401-INVALID-KEY"},
            {"http_status": 403, "code": "TITMAS-STAGE5-403-SCOPE-DENIED"},
            {"http_status": 404, "code": "TITMAS-STAGE5-404-NOT-FOUND"},
            {"http_status": 409, "code": "TITMAS-STAGE5-409-STATE-CONFLICT"},
            {"http_status": 413, "code": "TITMAS-STAGE5-413-TOO-LARGE"},
            {"http_status": 422, "code": "TITMAS-STAGE5-422-CONFORMANCE-FAIL"},
            {"http_status": 429, "code": "TITMAS-STAGE5-429-USAGE-LIMIT"},
            {"http_status": 500, "code": "TITMAS-STAGE5-500-BOUNDED-FAILURE"}
        ],
        "response_policy": "SANITIZED_CUSTOMER_VISIBLE_JSON_ONLY",
    }
    examples = {
        "synthetic_only": True,
        "specification_proposal": synthetic_proposal(),
        "adapter_mapping": synthetic_adapter(),
        "test_vector": synthetic_vector(),
        "non_claims": ["NOT_REAL_EVIDENCE", "NOT_STANDARD_ADOPTION"],
    }
    payloads = {
        "README.md": readme().encode("utf-8"),
        "standard-catalog.json": canonical_bytes(catalog) + b"\n",
        "task-catalog.json": canonical_bytes(task_catalog) + b"\n",
        "api-contract.json": canonical_bytes(api_contract) + b"\n",
        "error-codes.json": canonical_bytes(errors) + b"\n",
        "synthetic-examples.json": canonical_bytes(examples) + b"\n",
    }
    for output_name, schema_name in CANONICAL_SCHEMAS.items():
        payloads[output_name] = read_bytes(
            f"TITMAS/conformance/schemas/{schema_name}"
        )
    return payloads


def primary_source(path: str) -> str:
    if path == "standard-catalog.json":
        return "TITMAS/specifications/registry.yaml"
    if path == "task-catalog.json":
        return "TITMAS/agent-native/tasks/task-registry.json"
    if path == "api-contract.json":
        return "TITMAS/private-customer-evaluation/api-contract.json"
    if path == "error-codes.json":
        return "TITMAS/private-customer-evaluation/error-codes.json"
    if path in CANONICAL_SCHEMAS:
        return f"TITMAS/conformance/schemas/{CANONICAL_SCHEMAS[path]}"
    return BUILDER_REF


def scan(payloads: dict[str, bytes]) -> dict[str, int]:
    result = {
        "protocol_surface_core_source_findings": 0,
        "protocol_surface_private_path_findings": 0,
        "protocol_surface_secret_findings": 0,
        "protocol_surface_symlink_findings": 0,
    }
    for path, value in payloads.items():
        text = value.decode("utf-8")
        result["protocol_surface_core_source_findings"] += int(bool(CORE_SYMBOLS.search(text)))
        result["protocol_surface_private_path_findings"] += int(bool(PRIVATE_PATHS.search(text)))
        result["protocol_surface_secret_findings"] += int(bool(SECRETS.search(text)))
        output = OUTPUT_ROOT / path
        result["protocol_surface_symlink_findings"] += int(output.is_symlink())
    return result


def build() -> dict[str, Any]:
    payloads = build_payloads()
    allowed = set(payloads) | {"protocol-surface-manifest.json"}
    if OUTPUT_ROOT.exists():
        unexpected = {
            str(path.relative_to(OUTPUT_ROOT))
            for path in OUTPUT_ROOT.rglob("*")
            if path.is_file() and str(path.relative_to(OUTPUT_ROOT)) not in allowed
        }
        if unexpected:
            raise ValueError(f"unexpected protocol surface files: {sorted(unexpected)}")
    findings = scan(payloads)
    if any(findings.values()):
        raise ValueError(f"protocol surface scan failed: {findings}")
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(OUTPUT_ROOT, 0o700)
    entries = []
    for relative, value in sorted(payloads.items()):
        target = OUTPUT_ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(target.parent, 0o700)
        target.write_bytes(value)
        os.chmod(target, 0o600)
        source = primary_source(relative)
        source_bytes = read_bytes(source)
        entries.append({
            "path": relative,
            "source_ref": source,
            "source_blob_sha": git_blob_sha(source_bytes),
            "output_sha256": sha256_bytes(value),
            "classification": CLASSIFICATIONS[relative],
            "legal_review_status": "NOT_ASSESSED_PRIVATE_USE_ONLY",
            "commercial_review_status": "PRIVATE_STAGE5_DECISION_BOUND",
            "security_review_status": "BOUNDED_RECONSTRUCTION_SCAN_PASS",
            "public_release_allowed": False,
            "private_stage_5_use_allowed": True,
        })
    manifest = {
        "manifest_version": "1.0.0",
        "decision_reference":
            "TITMAS-STAGE-5-PRIVATE-AGENT-NATIVE-CONTRIBUTION-PREVIEW-D01",
        "source_main": "7b7e36c3ac5513deb23b03c8d86e6fc8853f4af1",
        "publication_by_reconstruction": True,
        "private_core_is_canonical": True,
        "public_release_allowed": False,
        "private_stage_5_use_allowed": True,
        "git_tracking_default": False,
        "files": entries,
        "findings": findings,
        "non_claims": [
            "PROTOCOL_SURFACE_NE_PRIVATE_IMPLEMENTATION",
            "OPEN_STANDARD_NE_OPEN_CORE_SOURCE",
            "PRIVATE_PREVIEW_NE_PUBLIC_RELEASE",
        ],
    }
    manifest_bytes = json.dumps(
        manifest, ensure_ascii=False, indent=2, sort_keys=True
    ).encode("utf-8") + b"\n"
    manifest_path = OUTPUT_ROOT / "protocol-surface-manifest.json"
    manifest_path.write_bytes(manifest_bytes)
    os.chmod(manifest_path, 0o600)
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2, sort_keys=True))
