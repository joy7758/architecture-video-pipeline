#!/usr/bin/env python3
"""Validate the sanitized Stage 5 Agent pilot audit without Provider access."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
AUDIT_ROOT = ROOT / "agent-audit"
SECRET = re.compile(
    r"sk-(?:proj|sp)-[A-Za-z0-9._-]{12,}|"
    r"Authorization\s*:\s*Bearer\s+[A-Za-z0-9._~+/=-]{12,}",
    re.IGNORECASE,
)
PRIVATE_PATH = re.compile(r"/(?:Users|private|home|var|tmp)/|[A-Za-z]:\\")
PROHIBITED_ELEVATION = {
    "STANDARD_ADOPTED",
    "STABLE",
    "CERTIFIED",
    "EXTERNAL_ADOPTION",
}
REGISTRY_FIELDS = {
    "submission_id",
    "type",
    "source",
    "contributor_kind",
    "conformance_status",
    "review_status",
    "human_disposition",
    "pilot_status",
    "hashes",
    "limitations",
}
SANITIZED_PAYLOAD_HASHES = {
    "sanitized-contributor-plan.json":
        "9373f5cb59deb2bd025359985c6e6056e17ab8ce8e893d59d479a6f09e8cbda7",
    "sanitized-standard-contribution.json":
        "193d76e12b6518d9d5ff6c5d5f921d4e48aecb8f165520e78bf515233b4f0c14",
    "sanitized-standard-review.json":
        "bcc73d38ff68b2cee628c57f5b63cdb5dc176e9b6aada88a9b0cd4f2fc80a1dd",
}


def load(name: str) -> dict[str, Any]:
    value = json.loads((AUDIT_ROOT / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{name} must contain an object")
    return value


def sanitized_payload_sha256(value: dict[str, Any]) -> str:
    payload = {
        key: item
        for key, item in value.items()
        if key not in {
            "checkpoint_payload_sha256",
            "sanitized_payload_sha256",
        }
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate() -> dict[str, Any]:
    audit = load("sanitized-agent-pilot-audit.json")
    plan = load("sanitized-contributor-plan.json")
    contribution = load("sanitized-standard-contribution.json")
    review = load("sanitized-standard-review.json")
    registry = json.loads(
        (ROOT / "agent-pilot-contribution-registry.json").read_text(
            encoding="utf-8"
        )
    )
    completion = json.loads(
        (ROOT / "stage5-completion-audit.json").read_text(encoding="utf-8")
    )
    if audit["model_calls"] != 5 or audit["provider_calls"] != 5:
        raise ValueError("bounded A01/A02/A04 call audit required")
    if audit["automatic_retry_count"] != 0:
        raise ValueError("automatic retry is prohibited")
    if audit["independent_agent_review_complete"] is not True:
        raise ValueError("independent Reviewer completion is required")
    if audit["review_result"] != "PASS":
        raise ValueError("durable Reviewer verdict drift")
    if audit["authorized_review_attempts"] != 3:
        raise ValueError("exact three Human-authorized review attempts required")
    if audit["confirmed_review_responses"] != 1:
        raise ValueError("exact one confirmed Reviewer response required")
    reviewer_models = audit["models"][2:]
    if len(reviewer_models) != 3:
        raise ValueError("three bounded Reviewer attempt records required")
    if any(
        item["provider"] != "BAIDU_QIANFAN"
        or item["requested_model"] != "kimi-k2.6"
        or item["returned_model"] != ""
        or item["capture_state"] != "FAILED_AFTER_DISPATCH_OUTCOME_UNKNOWN"
        for item in reviewer_models[:2]
    ):
        raise ValueError("unknown Kimi history drift")
    final_reviewer = reviewer_models[2]
    if (
        final_reviewer["provider"] != "BAIDU_QIANFAN"
        or final_reviewer["requested_model"] != "deepseek-v3.2"
        or final_reviewer["returned_model"] != "deepseek-v3.2"
        or final_reviewer["model_identity_status"] != "MATCH"
        or final_reviewer["capture_state"] != "FINALIZED_SUCCESS"
    ):
        raise ValueError("A04 Reviewer identity or capture state drift")
    if audit["stage5_private_preview_operational"] is not True:
        raise ValueError("completed Stage 5 preview must be operational")
    if audit["stage5_private_agent_pilot_complete"] is not True:
        raise ValueError("Agent pilot completion drift")
    if audit["formal_specification_registry_modified"] is not False:
        raise ValueError("formal registry modification is prohibited")
    if audit["further_review_authorized"] is not False:
        raise ValueError("no further Reviewer call is authorized")
    if plan["checkpoint_state"] != "DURABLE":
        raise ValueError("plan checkpoint is not durable")
    if contribution["checkpoint_state"] != "DURABLE":
        raise ValueError("contribution checkpoint is not durable")
    if review["checkpoint_state"] != "DURABLE":
        raise ValueError("review checkpoint is not durable")
    checkpoints = {
        "sanitized-contributor-plan.json": plan,
        "sanitized-standard-contribution.json": contribution,
        "sanitized-standard-review.json": review,
    }
    observed_sanitized_hashes = []
    for name, checkpoint in checkpoints.items():
        observed = sanitized_payload_sha256(checkpoint)
        if (
            checkpoint.get("sanitized_payload_sha256") != observed
            or observed != SANITIZED_PAYLOAD_HASHES[name]
        ):
            raise ValueError(f"{name} sanitized payload hash drift")
        observed_sanitized_hashes.append(observed)
    if audit["sanitized_payload_hashes"] != observed_sanitized_hashes:
        raise ValueError("Agent audit sanitized payload hash binding drift")
    if audit["checkpoint_hashes"] != [
        checkpoint["checkpoint_payload_sha256"]
        for checkpoint in checkpoints.values()
    ]:
        raise ValueError("Agent audit checkpoint hash binding drift")
    if review["structured_result"]["verdict"] != "PASS":
        raise ValueError("sanitized review verdict drift")
    if contribution["structured_result"]["conformance_status"] != "CONFORMANCE_PASS":
        raise ValueError("captured customer Conformance result drift")
    entries = registry.get("entries")
    if not isinstance(entries, list) or len(entries) != 1:
        raise ValueError("one Agent pilot registry entry required")
    if set(entries[0]) != REGISTRY_FIELDS:
        raise ValueError("pilot registry field boundary drift")
    if entries[0]["pilot_status"] != "PILOT_ACCEPTED":
        raise ValueError("Human Pilot disposition drift")
    if entries[0]["human_disposition"] != "ACCEPT_PILOT":
        raise ValueError("Pilot Registry lacks Human disposition")
    if completion["summary"] != {
        "pass": 24,
        "partial": 0,
        "incomplete": 0,
        "total": 24,
    }:
        raise ValueError("completion audit count drift")
    if completion["completion_proven"] is not True:
        raise ValueError("completed Goal audit drift")
    incomplete_sections = {
        item["section"]
        for item in completion["requirements"]
        if item["status"] == "INCOMPLETE"
    }
    if incomplete_sections:
        raise ValueError("completed audit contains incomplete sections")
    if completion["blocking_condition"] != "NONE":
        raise ValueError("completion audit blocking condition drift")
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(AUDIT_ROOT.glob("*.json"))
    )
    if SECRET.search(text) or PRIVATE_PATH.search(text):
        raise ValueError("sanitized audit contains secret or private path")
    if any(value in text for value in PROHIBITED_ELEVATION):
        raise ValueError("sanitized audit contains semantic elevation")
    return {
        "agent_audit_files_checked": 4,
        "agent_pilot_registry_entries_checked": 1,
        "goal_sections_checked": 24,
        "model_calls": 5,
        "authorized_review_attempts": 3,
        "automatic_retry_count": 0,
        "durable_checkpoints": 3,
        "sanitized_payload_hashes_verified": 3,
        "review_checkpoint_durable": True,
        "stage5_private_preview_operational": True,
        "secret_findings": 0,
        "private_path_findings": 0,
        "semantic_elevation_findings": 0,
        "status": "PASS_COMPLETE_WITH_RECORDED_LIMITATIONS",
    }


def main() -> int:
    print(json.dumps(validate(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
