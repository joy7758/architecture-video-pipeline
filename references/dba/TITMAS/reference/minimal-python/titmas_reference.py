#!/usr/bin/env python3
"""Minimal synthetic TITMAS Development reference implementation."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


class BoundaryRejected(ValueError):
    pass


def transform(payload: dict[str, Any]) -> dict[str, Any]:
    required = {
        "identity", "boundary", "event", "existing_evidence_ref",
        "existing_verification_ref", "limitations",
    }
    missing = sorted(required - payload.keys())
    if missing:
        raise ValueError(f"missing required input fields: {missing}")

    boundary = payload["boundary"]
    event = payload["event"]
    action = event.get("action")
    if action in boundary.get("forbidden_actions", []):
        raise BoundaryRejected(f"action {action!r} is forbidden")
    if action not in boundary.get("allowed_actions", []):
        raise BoundaryRejected(f"action {action!r} is not allowed")

    limitations = list(payload["limitations"])
    for limitation in (
        "NO_DBOS_ADMISSION",
        "NO_SAEE_EXECUTION",
        "REFERENCE_IMPLEMENTATION_NE_STANDARD",
    ):
        if limitation not in limitations:
            limitations.append(limitation)

    evidence_ref = payload["existing_evidence_ref"]
    verification_ref = payload["existing_verification_ref"]
    return {
        "profile_version": "0.1.0",
        "profile_status": "DEVELOPMENT_DRAFT",
        "identity_ref": payload["identity"],
        "boundary": boundary,
        "event": event,
        "evidence_binding": {
            "evidence_ref": evidence_ref,
            "source": "CALLER_SUPPLIED_EXISTING_REFERENCE",
            "source_kind": "EVIDENCE_REFERENCE",
            "admission_status": "REFERENCE_ONLY_NOT_DBOS_ADMITTED",
        },
        "verification_result": {
            "verification_ref": verification_ref,
            "status": "STRUCTURE_PASS",
            "verifier_ref": "TITMAS_LOCAL_REFERENCE",
        },
        "evaluation_handoff": {
            "status": "READY_FOR_OPTIONAL_READ_ONLY_EVALUATION",
            "input_refs": [event["event_id"], evidence_ref, verification_ref],
        },
        "limitations": limitations,
        "claims": ["STRUCTURE_VALIDATED"],
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: titmas_reference.py INPUT.json", file=sys.stderr)
        return 2
    try:
        input_path = Path(argv[1])
        resolved = input_path.resolve()
        if input_path.suffix.lower() != ".json":
            raise ValueError("input must use a .json suffix")
        if input_path.is_symlink() or not input_path.is_file():
            raise ValueError("input must be a regular non-symlink file")
        if not resolved.is_relative_to(Path.cwd().resolve()):
            raise ValueError("input must remain inside the current working directory")
        if input_path.stat().st_size > 1_000_000:
            raise ValueError("input exceeds the 1000000-byte local limit")
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        output = transform(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "error": str(exc)}))
        return 1
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
