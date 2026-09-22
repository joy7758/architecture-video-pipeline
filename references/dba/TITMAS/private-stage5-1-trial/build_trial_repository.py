#!/usr/bin/env python3
"""Reconstruct the isolated TITMAS Stage 5.1 private trial repository.

The builder is exact-file allowlist only. It does not copy the core repository,
Git history, internal tests, private governance, Provider configuration,
credentials, response capture, semantic checkpoint implementation, customer
data or production Evidence.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import re
import subprocess
import zipfile
from pathlib import Path
from typing import Any


TITMAS_ROOT = Path(__file__).resolve().parents[1]
DBA_ROOT = TITMAS_ROOT.parent
BUILDER_REF = "TITMAS/private-stage5-1-trial/build_trial_repository.py"
SOURCE_REPOSITORY = "joy7758/digital-biosphere-architecture-specification"
DECISION_REFERENCE = (
    "TITMAS-STAGE-5-1-PRIVATE-EXTERNAL-DEVELOPER-TRIAL-CHANNEL-D01"
)

ALLOWED_ROOT_FILES = {
    "README.md",
    "llms.txt",
    "agent-index.json",
    "status.json",
    "trial-source-manifest.json",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "LICENSE-TRIAL.md",
}
ALLOWED_ROOT_DIRECTORIES = {
    "protocol",
    "schemas",
    "examples",
    "sdk",
    "tasks",
    "conformance-client",
    "feedback",
    "trial",
}

COPIED_SOURCES = {
    "protocol/api-contract.json":
        "TITMAS/private-stage5-protocol-surface/api-contract.json",
    "protocol/error-codes.json":
        "TITMAS/private-stage5-protocol-surface/error-codes.json",
    "protocol/standard-catalog.json":
        "TITMAS/private-stage5-protocol-surface/standard-catalog.json",
    "schemas/specification-proposal.schema.json":
        "TITMAS/private-stage5-protocol-surface/schemas/"
        "specification-proposal.schema.json",
    "schemas/adapter-mapping.schema.json":
        "TITMAS/private-stage5-protocol-surface/schemas/"
        "adapter-mapping.schema.json",
    "schemas/test-vector.schema.json":
        "TITMAS/private-stage5-protocol-surface/schemas/"
        "test-vector.schema.json",
    "schemas/contribution-result.schema.json":
        "TITMAS/private-stage5-protocol-surface/schemas/"
        "contribution-result.schema.json",
    "schemas/review.schema.json":
        "TITMAS/private-stage5-protocol-surface/schemas/review.schema.json",
    "examples/synthetic-examples.json":
        "TITMAS/private-stage5-protocol-surface/synthetic-examples.json",
    "sdk/python/titmas_stage5_sdk.py":
        "TITMAS/private-stage5-sdk/python/titmas_stage5_sdk.py",
    "sdk/python/README.md":
        "TITMAS/private-stage5-sdk/python/README.md",
}

CLASSIFICATIONS = {
    "README.md": "COMMERCIAL_CUSTOMER_ONLY",
    "llms.txt": "COMMERCIAL_CUSTOMER_ONLY",
    "agent-index.json": "COMMERCIAL_CUSTOMER_ONLY",
    "status.json": "COMMERCIAL_CUSTOMER_ONLY",
    "trial-source-manifest.json": "COMMERCIAL_CUSTOMER_ONLY",
    "CODE_OF_CONDUCT.md": "COMMERCIAL_CUSTOMER_ONLY",
    "SECURITY.md": "COMMERCIAL_CUSTOMER_ONLY",
    "LICENSE-TRIAL.md": "LEGAL_REVIEW_REQUIRED",
    "protocol/README.md": "COMMERCIAL_CUSTOMER_ONLY",
    "protocol/api-contract.json": "COMMERCIAL_CUSTOMER_ONLY",
    "protocol/error-codes.json": "COMMERCIAL_CUSTOMER_ONLY",
    "protocol/standard-catalog.json": "COMMERCIAL_CUSTOMER_ONLY",
    "examples/synthetic-examples.json": "PUBLIC_SYNTHETIC_EXAMPLE",
    "sdk/python/README.md": "PUBLIC_CLIENT_STUB_CANDIDATE",
    "sdk/python/pyproject.toml": "PUBLIC_CLIENT_STUB_CANDIDATE",
    "sdk/python/titmas_stage5_sdk.py": "PUBLIC_CLIENT_STUB_CANDIDATE",
    "sdk/python/titmas_private_trial_sdk-0.1.0-py3-none-any.whl":
        "PUBLIC_CLIENT_STUB_CANDIDATE",
    "tasks/trial-task-catalog.json": "COMMERCIAL_CUSTOMER_ONLY",
    "conformance-client/README.md": "PUBLIC_CLIENT_STUB_CANDIDATE",
    "conformance-client/titmas_conformance_client.py":
        "PUBLIC_CLIENT_STUB_CANDIDATE",
    "feedback/feedback-template.md": "COMMERCIAL_CUSTOMER_ONLY",
    "feedback/metrics-schema.json": "COMMERCIAL_CUSTOMER_ONLY",
    "trial/README.md": "COMMERCIAL_CUSTOMER_ONLY",
    "trial/TRIAL-PARTICIPATION-ACKNOWLEDGEMENT-v0.1.md":
        "LEGAL_REVIEW_REQUIRED",
    "trial/data-and-privacy-boundary.md": "COMMERCIAL_CUSTOMER_ONLY",
    **{
        name: "PUBLIC_PROTOCOL"
        for name in COPIED_SOURCES
        if name.startswith("schemas/")
    },
}

PRIVATE_PATHS = re.compile(
    r"/(?:Users|private/tmp|var/folders|home)/|[A-Za-z]:\\"
)
SECRETS = re.compile(
    r"sk-(?:proj|sp)-[A-Za-z0-9._-]{12,}|"
    r"Authorization\s*:\s*Bearer\s+[A-Za-z0-9._~+/=-]{12,}|"
    r"(?:DASHSCOPE|QIANFAN|ARK|OPENAI|DEEPSEEK|GITHUB)_API_KEY\s*=",
    re.IGNORECASE,
)
CORE_SYMBOLS = re.compile(
    r"\b(?:GatewayService|AtomicJSONWriter|capture_response|"
    r"semantic_checkpoint|source-classification-registry|"
    r"build_stage5_protocol_surface)\b"
)
PROVIDER_CONFIGURATION = re.compile(
    r"(?:qianfan|dashscope|deepseek|volcengine).*(?:endpoint|api[_ -]?key)",
    re.IGNORECASE,
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def pretty_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_blob_sha(value: bytes) -> str:
    header = f"blob {len(value)}\0".encode("ascii")
    return hashlib.sha1(header + value).hexdigest()


def wheel_hash(value: bytes) -> str:
    return "sha256=" + base64.urlsafe_b64encode(
        hashlib.sha256(value).digest()
    ).decode("ascii").rstrip("=")


def sdk_wheel(module: bytes) -> bytes:
    """Build a deterministic, dependency-free wheel for clean-clone use."""

    dist_info = "titmas_private_trial_sdk-0.1.0.dist-info"
    metadata = (
        "Metadata-Version: 2.1\n"
        "Name: titmas-private-trial-sdk\n"
        "Version: 0.1.0\n"
        "Summary: Request-only SDK for the private TITMAS developer trial\n"
        "Requires-Python: >=3.11\n\n"
    ).encode()
    wheel = (
        "Wheel-Version: 1.0\n"
        "Generator: TITMAS Stage 5.1 allowlist reconstruction\n"
        "Root-Is-Purelib: true\n"
        "Tag: py3-none-any\n\n"
    ).encode()
    top_level = b"titmas_stage5_sdk\n"
    files = {
        "titmas_stage5_sdk.py": module,
        f"{dist_info}/METADATA": metadata,
        f"{dist_info}/WHEEL": wheel,
        f"{dist_info}/top_level.txt": top_level,
    }
    record_path = f"{dist_info}/RECORD"
    record = "".join(
        f"{path},{wheel_hash(value)},{len(value)}\n"
        for path, value in sorted(files.items())
    )
    record += f"{record_path},,\n"
    files[record_path] = record.encode()

    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path, value in sorted(files.items()):
            info = zipfile.ZipInfo(path, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, value)
    return output.getvalue()


def read_source(relative: str) -> bytes:
    root = DBA_ROOT.resolve()
    path = (DBA_ROOT / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("source escapes core repository")
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"invalid allowlisted source: {relative}")
    return path.read_bytes()


def _git_root() -> Path:
    return Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=DBA_ROOT,
        text=True,
    ).strip()).resolve()


def _source_at_commit(source_commit: str, relative: str) -> bytes:
    git_root = _git_root()
    source = (DBA_ROOT / relative).resolve()
    repository_path = source.relative_to(git_root).as_posix()
    try:
        return subprocess.check_output(
            ["git", "show", f"{source_commit}:{repository_path}"],
            cwd=git_root,
        )
    except subprocess.CalledProcessError as exc:
        raise ValueError(
            f"source path is not present at source commit: {relative}"
        ) from exc


def validate_source_commit(source_commit: str) -> None:
    """Bind every exported source and the builder to one exact Git commit."""

    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("source commit must be a 40-character lowercase Git hash")
    git_root = _git_root()
    try:
        resolved = subprocess.check_output(
            ["git", "rev-parse", "--verify", f"{source_commit}^{{commit}}"],
            cwd=git_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise ValueError("source commit does not exist") from exc
    if resolved != source_commit:
        raise ValueError("source commit did not resolve exactly")

    sources = sorted({BUILDER_REF, *COPIED_SOURCES.values()})
    for relative in sources:
        if read_source(relative) != _source_at_commit(source_commit, relative):
            raise ValueError(
                f"working source does not match source commit: {relative}"
            )


def trial_tasks() -> dict[str, Any]:
    return {
        "catalog_version": "1.0.0",
        "selection_policy": "SELECT_EXACTLY_ONE_TASK_WITHOUT_ANSWER_HINTS",
        "tasks": [
            {
                "task_id": "TRIAL-01-NEGATIVE-TEST-VECTOR",
                "difficulty": "STARTER",
                "title": "Negative Test Vector",
                "objective": (
                    "Prepare a Test Vector that describes a condition TITMAS "
                    "must reject explicitly."
                ),
                "minimum_coverage": [
                    "invalid required field",
                    "semantic boundary violation",
                    "expected result is failure",
                    "public reason code",
                ],
                "submission_type": "TEST_VECTOR",
                "answer_hint_provided": False,
            },
            {
                "task_id": "TRIAL-02-ADAPTER-MAPPING",
                "difficulty": "INTERMEDIATE",
                "title": "Adapter Mapping",
                "objective": (
                    "Map a publicly documented event structure from a common "
                    "Agent framework to bounded TITMAS objects."
                ),
                "constraints": [
                    "Do not copy complete third-party source code.",
                    "Preserve unsupported fields and conflicts.",
                    "Mapping does not imply adoption.",
                ],
                "submission_type": "ADAPTER_MAPPING",
                "answer_hint_provided": False,
            },
            {
                "task_id": "TRIAL-03-SPECIFICATION-PROPOSAL",
                "difficulty": "ADVANCED",
                "title": "Specification Proposal",
                "objective": (
                    "Describe one real developer semantic or integration gap "
                    "and a bounded change proposal."
                ),
                "constraints": [
                    "Separate scope from non-goals.",
                    "Include positive and negative cases.",
                    "Do not grant Authority or claim adoption.",
                ],
                "submission_type": "SPECIFICATION_PROPOSAL",
                "answer_hint_provided": False,
            },
        ],
        "non_claims": [
            "TASK_SELECTION_NE_PERMISSION",
            "CONTRIBUTION_NE_STANDARD_ADOPTION",
            "TRIAL_NE_COMMERCIAL_ADOPTION",
        ],
    }


def generated_payloads(source_commit: str) -> dict[str, bytes]:
    status = {
        "schema_version": "1.0.0",
        "repository_role": "SEPARATE_PRIVATE_DEVELOPER_TRIAL",
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": source_commit,
        "visibility": "PRIVATE",
        "current_stage": "TITMAS_STAGE_5_PRIVATE_PREVIEW",
        "trial_repository_reconstructed_from_allowlist": True,
        "private_core_is_canonical": True,
        "core_repository_access_available": False,
        "public_core_clone_available": False,
        "external_trial_requires_explicit_access": True,
        "external_participant_invitation_authorized": False,
        "external_developer_trial_executed": False,
        "public_release_allowed": False,
        "formal_standard_change_authorized": False,
        "commercial_access_granted": False,
        "legal_review_status": "PENDING",
        "real_model_call_count": 0,
        "real_provider_call_count": 0,
        "community_established": False,
        "limitations": [
            "PRIVATE_TRIAL_ONLY",
            "NO_EXTERNAL_PARTICIPANT_INVITED",
            "LOCAL_CLONE_DELETION_DEPENDS_ON_PARTICIPANT_COMPLIANCE",
            "CONFORMANCE_NE_CERTIFICATION",
        ],
    }
    agent_index = {
        "schema_version": "1.0.0",
        "canonical_agent_entry": True,
        "name": "TITMAS Private External Developer Trial",
        "purpose": (
            "A bounded private repository for reading TITMAS protocol "
            "materials and preparing one structured contribution."
        ),
        "start_here": [
            "llms.txt",
            "status.json",
            "tasks/trial-task-catalog.json",
            "sdk/python/README.md",
            "trial/README.md",
        ],
        "allowed_contribution_types": [
            "SPECIFICATION_PROPOSAL",
            "ADAPTER_MAPPING",
            "TEST_VECTOR",
        ],
        "when_to_use": [
            "an explicitly invited developer evaluates one bounded TITMAS task",
            "a contribution must be prepared without core repository access",
        ],
        "when_not_to_use": [
            "requesting core source or internal tests",
            "claiming certification, adoption, production readiness or Authority",
            "submitting personal, customer or production data",
        ],
        "current_core_repository_visibility": "PRIVATE",
        "public_core_clone_available": False,
        "external_trial_requires_explicit_access": True,
        "sandbox_key_is_source_license": False,
        "human_maintainer_disposition_required": True,
        "external_participant_invitation_authorized": False,
        "public_release_allowed": False,
        "authority_boundaries": [
            "CONTRIBUTION_NE_AUTHORITY",
            "CONFORMANCE_NE_ADOPTION",
            "EVIDENCE_NE_TRUTH",
            "VERIFICATION_NE_AUTHORIZATION",
        ],
    }
    root_readme = """# TITMAS Private External Developer Trial

This is a separately reconstructed, private and time-bounded trial surface for
TITMAS standards contributions. It is not the TITMAS core repository and does
not contain core implementation, internal tests, private governance, Provider
configuration, credentials, response capture or private persistence code.

## Start

1. Read `llms.txt`, `agent-index.json` and `status.json`.
2. Choose exactly one task from `tasks/trial-task-catalog.json`.
3. Install the request-only Python SDK from `sdk/python/`.
4. Prepare one Proposal, Adapter Mapping or Test Vector.
5. Run local Schema preflight.
6. Submit only through the separately delivered loopback Sandbox endpoint and
   temporary key.
7. Prepare a Pull Request; Human Maintainer disposition remains required.

## Boundaries

```text
TRIAL_REPOSITORY_NE_CORE_REPOSITORY=true
TRIAL_ACCESS_NE_SOURCE_LICENSE=true
CONFORMANCE_NE_CERTIFICATION=true
CONTRIBUTION_NE_STANDARD_ADOPTION=true
PUBLIC_RELEASE_ALLOWED=false
EXTERNAL_PARTICIPANT_INVITATION_AUTHORIZED=false
```
"""
    llms = """# TITMAS private trial machine entry

Purpose: prepare one bounded standards contribution without core access.
Read: ./agent-index.json, ./status.json, ./tasks/trial-task-catalog.json
SDK: ./sdk/python/
Schemas: ./schemas/
Trial rules: ./trial/README.md

Current core repository visibility: PRIVATE
Public core clone available: false
External trial requires explicit access: true
External participant invitation authorized: false
Public protocol released: false

The Sandbox key controls temporary access. It is not a source license,
Permission grant, certification, adoption decision or Authority.
"""
    protocol_readme = """# Protocol surface

This directory contains the bounded API contract, public error codes and
Development catalog reconstructed from the private canonical source. Schemas
are in `../schemas/`; examples are synthetic and live in `../examples/`.

The protocol explains how to interoperate. It does not expose the core
Conformance implementation or grant access to the core repository.
"""
    sdk_pyproject = """[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "titmas-private-trial-sdk"
version = "0.1.0"
description = "Request-only SDK for the private TITMAS developer trial"
requires-python = ">=3.11"
dependencies = []

[tool.setuptools]
py-modules = ["titmas_stage5_sdk"]
"""
    conformance_readme = """# Conformance client

`titmas_conformance_client.py` calls the loopback Sandbox validation endpoint.
It does not implement TITMAS core Conformance and does not automatically retry.

```bash
python titmas_conformance_client.py SUBMISSION_ID
```

Provide `TITMAS_SANDBOX_ENDPOINT` and `TITMAS_SANDBOX_KEY` only for the current
session. Do not persist the key.
"""
    conformance_client = '''#!/usr/bin/env python3
"""Request a bounded Conformance result from the private loopback Sandbox."""

import json
import os
import sys
from pathlib import Path

from titmas_stage5_sdk import Stage5Client


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: titmas_conformance_client.py SUBMISSION_ID")
    endpoint = os.environ.get("TITMAS_SANDBOX_ENDPOINT", "")
    token = os.environ.get("TITMAS_SANDBOX_KEY", "")
    client = Stage5Client(endpoint, token, Path(__file__).parents[1] / "schemas")
    print(json.dumps(client.validate_submission(sys.argv[1]), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
    feedback_template = """# TITMAS private trial feedback

- participant_id:
- selected_trial_task:
- time_to_first_success:
- installation_failures:
- documentation_questions:
- task_understanding:
- sdk_usability:
- conformance_clarity:
- boundary_understanding:
- core_access_requests:
- human_help_count:
- submission_quality:
- trial_completion:

Do not include personal, customer, production or credential data.
"""
    metrics_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "TITMAS Private Trial Feedback Metrics",
        "type": "object",
        "required": [
            "participant_id",
            "selected_trial_task",
            "core_access_requests",
            "private_context_exposure_count",
            "authority_confusion_count",
            "trial_completion",
        ],
        "properties": {
            "participant_id": {"type": "string", "minLength": 1},
            "selected_trial_task": {"type": "string", "minLength": 1},
            "time_to_first_success": {"type": ["number", "null"], "minimum": 0},
            "installation_failures": {"type": "integer", "minimum": 0},
            "documentation_questions": {"type": "integer", "minimum": 0},
            "task_understanding": {"type": "string"},
            "sdk_usability": {"type": "string"},
            "conformance_clarity": {"type": "string"},
            "boundary_understanding": {"type": "string"},
            "core_access_requests": {"type": "integer", "minimum": 0},
            "human_help_count": {"type": "integer", "minimum": 0},
            "submission_quality": {"type": "string"},
            "private_context_exposure_count": {"type": "integer", "minimum": 0},
            "authority_confusion_count": {"type": "integer", "minimum": 0},
            "trial_completion": {"type": "boolean"},
        },
        "additionalProperties": False,
    }
    trial_readme = """# Trial workflow

1. Confirm the non-binding acknowledgement.
2. Select exactly one task without requesting an answer.
3. Work only in a feature branch.
4. Use synthetic or publicly documented material.
5. Run Schema preflight and the loopback Sandbox Conformance call.
6. Open a Pull Request. Direct push to `main` is prohibited.
7. Wait for required status checks and Human Maintainer review.
8. When access ends, delete the local clone and confirm deletion.

Repository access does not grant core source, formal standard, Release,
deployment, certification, commercial or governance Authority.
"""
    acknowledgement = """# TITMAS Trial Participation Acknowledgement v0.1

Status: `NON_BINDING_TRIAL_ACKNOWLEDGEMENT`

Legal review status: `PENDING`

By accepting a future trial invitation, the participant acknowledges:

- the repository contains confidential trial material and must not be
  forwarded or publicly released;
- personal data, customer data, credentials, real production Evidence and
  confidential third-party material must not be submitted;
- core source must not be requested, searched for or inferred from the trial;
- Conformance is not certification, Truth, adoption or production approval;
- trial participation is not commercial adoption, a contract or an SLA;
- local clones should be deleted when access ends;
- removal of GitHub access cannot technically delete copies already retained;
- bounded feedback may be used to improve TITMAS specifications.

No invitation is authorized by this document.
"""
    data_boundary = """# Data and privacy boundary

Allowed: synthetic data and limited references to publicly documented
semantics.

Prohibited: personal data, customer data, credentials, raw Provider responses,
real production Evidence, private repository content and absolute private
paths.

If uncertain, stop and request Human Maintainer review without attaching the
uncertain material.
"""
    code_of_conduct = """# Private trial Code of Conduct

Be respectful, keep work technically focused, disclose AI assistance, preserve
failure evidence and do not attempt to expand access or Authority. Harassment,
credential probing, core-source requests and publication of trial material are
not permitted.

This bounded trial conduct text does not establish a public community,
Foundation, membership class or independent governance authority.
"""
    security = """# Security

Do not include vulnerabilities, credentials or exploit details in a Pull
Request. Stop work and notify the repository owner through the private
participant coordination channel. No public security transport is represented
as active by this repository.

Do not test the core repository, external systems or production services.
"""
    license_trial = """# Private Trial Terms Notice

This repository is provided only for a bounded, confidential evaluation under
an explicit invitation. Access is not a source-code license, commercial
agreement, SLA, certification or permission to redistribute.

`LEGAL_REVIEW_STATUS=PENDING`

Owner-created public protocol fragments may retain their stated source
classification. No third-party material is relicensed by this notice.
"""
    return {
        "README.md": root_readme.encode(),
        "llms.txt": llms.encode(),
        "agent-index.json": pretty_json(agent_index),
        "status.json": pretty_json(status),
        "CODE_OF_CONDUCT.md": code_of_conduct.encode(),
        "SECURITY.md": security.encode(),
        "LICENSE-TRIAL.md": license_trial.encode(),
        "protocol/README.md": protocol_readme.encode(),
        "sdk/python/pyproject.toml": sdk_pyproject.encode(),
        "tasks/trial-task-catalog.json": pretty_json(trial_tasks()),
        "conformance-client/README.md": conformance_readme.encode(),
        "conformance-client/titmas_conformance_client.py":
            conformance_client.encode(),
        "feedback/feedback-template.md": feedback_template.encode(),
        "feedback/metrics-schema.json": pretty_json(metrics_schema),
        "trial/README.md": trial_readme.encode(),
        "trial/TRIAL-PARTICIPATION-ACKNOWLEDGEMENT-v0.1.md":
            acknowledgement.encode(),
        "trial/data-and-privacy-boundary.md": data_boundary.encode(),
    }


def source_for_output(path: str) -> str:
    return COPIED_SOURCES.get(path, BUILDER_REF)


def build_payloads(source_commit: str) -> dict[str, bytes]:
    payloads = generated_payloads(source_commit)
    for output, source in COPIED_SOURCES.items():
        payloads[output] = read_source(source)
    payloads[
        "sdk/python/titmas_private_trial_sdk-0.1.0-py3-none-any.whl"
    ] = sdk_wheel(payloads["sdk/python/titmas_stage5_sdk.py"])
    missing_classifications = set(payloads) - set(CLASSIFICATIONS)
    if missing_classifications:
        raise ValueError(
            f"missing trial classifications: {sorted(missing_classifications)}"
        )
    return payloads


def scan_payloads(payloads: dict[str, bytes]) -> dict[str, int]:
    findings = {
        "trial_repository_core_source_findings": 0,
        "trial_repository_secret_findings": 0,
        "trial_repository_private_path_findings": 0,
        "trial_repository_provider_configuration_findings": 0,
        "trial_repository_symlink_findings": 0,
        "trial_repository_git_history_findings": 0,
        "unauthorized_export_count": 0,
    }
    for value in payloads.values():
        text = value.decode("utf-8", errors="ignore")
        findings["trial_repository_core_source_findings"] += int(
            bool(CORE_SYMBOLS.search(text))
        )
        findings["trial_repository_secret_findings"] += int(
            bool(SECRETS.search(text))
        )
        findings["trial_repository_private_path_findings"] += int(
            bool(PRIVATE_PATHS.search(text))
        )
        findings["trial_repository_provider_configuration_findings"] += int(
            bool(PROVIDER_CONFIGURATION.search(text))
        )
    return findings


def _validate_output_path(relative: str) -> None:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe trial output path: {relative}")
    top = path.parts[0]
    if (
        relative not in ALLOWED_ROOT_FILES
        and top not in ALLOWED_ROOT_DIRECTORIES
    ):
        raise ValueError(f"output outside trial allowlist: {relative}")


def _manifest_entry(
    path: str,
    value: bytes,
    source_commit: str,
) -> dict[str, Any]:
    source = source_for_output(path)
    source_bytes = read_source(source)
    return {
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": source_commit,
        "source_path": source,
        "source_blob_sha": git_blob_sha(source_bytes),
        "classification": CLASSIFICATIONS[path],
        "trial_output_path": path,
        "trial_output_sha256": sha256_bytes(value),
        "hash_method": "RAW_SHA256",
        "security_scan_status": "PASS_ZERO_FINDINGS",
        "commercial_review_status": "PRIVATE_TRIAL_D01_APPROVED",
        "trial_release_status": "PRIVATE_TRIAL_ONLY",
        "public_release_allowed": False,
    }


def _with_manifest_self_hash(manifest: dict[str, Any]) -> dict[str, Any]:
    self_entry = {
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": manifest["source_commit"],
        "source_path": BUILDER_REF,
        "source_blob_sha": git_blob_sha(read_source(BUILDER_REF)),
        "classification": CLASSIFICATIONS["trial-source-manifest.json"],
        "trial_output_path": "trial-source-manifest.json",
        "trial_output_sha256": "SELF_HASH_PLACEHOLDER",
        "hash_method": "CANONICAL_JSON_SELF_HASH",
        "security_scan_status": "PASS_ZERO_FINDINGS",
        "commercial_review_status": "PRIVATE_TRIAL_D01_APPROVED",
        "trial_release_status": "PRIVATE_TRIAL_ONLY",
        "public_release_allowed": False,
    }
    manifest["files"].append(self_entry)
    manifest["files"].sort(key=lambda item: item["trial_output_path"])
    digest = sha256_bytes(canonical_bytes(manifest))
    self_entry["trial_output_sha256"] = digest
    return manifest


def build(output_root: Path, source_commit: str) -> dict[str, Any]:
    output_root = output_root.resolve()
    if output_root == DBA_ROOT.resolve() or output_root.is_relative_to(
        DBA_ROOT.resolve()
    ):
        raise ValueError("trial output must be outside the core repository")
    if output_root.exists() and any(output_root.iterdir()):
        raise ValueError("trial output directory must be empty")
    validate_source_commit(source_commit)
    output_root.mkdir(parents=True, exist_ok=True)

    payloads = build_payloads(source_commit)
    for path in payloads:
        _validate_output_path(path)
    findings = scan_payloads(payloads)
    if any(findings.values()):
        raise ValueError(f"trial reconstruction scan failed: {findings}")

    entries: list[dict[str, Any]] = []
    for relative, value in sorted(payloads.items()):
        target = output_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value)
        os.chmod(target, 0o644)
        entries.append(_manifest_entry(relative, value, source_commit))

    manifest = _with_manifest_self_hash({
        "manifest_version": "1.0.0",
        "decision_reference": DECISION_REFERENCE,
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": source_commit,
        "publication_by_reconstruction": True,
        "allowlist_only_export": True,
        "core_repository_fork": False,
        "git_history_copied": False,
        "private_trial_only": True,
        "public_release_allowed": False,
        "unclassified_export_allowed": False,
        "files": entries,
        "findings": findings,
        "non_claims": [
            "TRIAL_REPOSITORY_NE_CORE_REPOSITORY",
            "TRIAL_ACCESS_NE_SOURCE_LICENSE",
            "CONFORMANCE_NE_ADOPTION",
            "PRIVATE_TRIAL_NE_COMMERCIAL_ADOPTION",
        ],
    })
    manifest_path = output_root / "trial-source-manifest.json"
    manifest_path.write_bytes(pretty_json(manifest))
    os.chmod(manifest_path, 0o644)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    manifest = build(args.output, args.source_commit)
    print(json.dumps({
        "status": "PASS",
        "files": len(manifest["files"]),
        "findings": manifest["findings"],
        "output": str(args.output.resolve()),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
