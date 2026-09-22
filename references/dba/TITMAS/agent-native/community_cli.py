#!/usr/bin/env python3
"""Deterministic, read-only CLI for the TITMAS controlled agent-native pilot.

The CLI emits candidate protocol objects. It never writes state, contacts a
network service, grants Authority, or performs a GitHub action.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DBA_ROOT = ROOT.parents[1]
TASKS = ROOT / "tasks" / "task-registry.json"
PARTICIPANTS = ROOT / "participants" / "participant-registry.json"
AUTHORITIES = ROOT / "participants" / "authority-registry.json"
CALIBRATION_CASES = ROOT / "recommendations" / "calibration-cases.json"
AUTHORITY_REF = "TITMAS-AGENT-NATIVE-COMMUNITY-D01"

ADVERSARIAL_REJECTION_POLICY = {
    "PROMPT_INJECTION": "UNTRUSTED_INSTRUCTION",
    "MALICIOUS_TASK_DESCRIPTION": "FORBIDDEN_ACTION",
    "FORGED_PARTICIPANT_IDENTITY": "IDENTITY_UNVERIFIED",
    "SELF_AUTHORIZATION": "SELF_AUTHORIZATION",
    "SELF_APPROVAL": "SELF_APPROVAL",
    "AUTHORITY_ELEVATION": "AUTHORITY_ELEVATION",
    "TASK_SCOPE_EXPANSION": "SCOPE_EXPANSION",
    "REVIEW_COLLUSION": "INDEPENDENCE_INSUFFICIENT",
    "SYBIL_SESSION_AS_INDEPENDENT_LINEAGE": "LINEAGE_MISREPRESENTATION",
    "INFINITE_TASK_LOOP": "LEASE_OR_STOP_CONDITION_REQUIRED",
    "AUTOMATIC_ISSUE_PR_NOISE": "PUBLIC_GITHUB_WRITE_NOT_AUTHORIZED",
    "DUPLICATE_CONTRIBUTION": "DUPLICATE_ACTIVE_CONTRIBUTION",
    "MALICIOUS_SCHEMA": "SCHEMA_FAIL_CLOSED",
    "PATH_TRAVERSAL": "PATH_TRAVERSAL",
    "HIDDEN_NETWORK_CALL": "UNDECLARED_NETWORK_ACCESS",
    "SUPPLY_CHAIN_DEPENDENCY": "UNAUTHORIZED_DEPENDENCY",
    "FAKE_ADOPTION": "MAPPING_AS_ADOPTION",
    "FAKE_CERTIFICATION": "CERTIFICATION_NOT_AUTHORIZED",
    "DELETE_FAILURE_RECORD": "HISTORY_DELETION",
    "NOT_ASSESSED_TO_PASS": "NOT_ASSESSED_AS_PASS",
    "RECOMMENDATION_TO_COMMAND": "RECOMMENDATION_AS_COMMAND",
    "EVIDENCE_TO_TRUTH": "EVIDENCE_AS_TRUTH",
}


class ProtocolRejected(ValueError):
    """Fail-closed protocol rejection with a stable reason code."""

    def __init__(self, reason_code: str, detail: str):
        super().__init__(f"{reason_code}: {detail}")
        self.reason_code = reason_code


def _load(path: Path) -> dict[str, Any]:
    resolved = path.resolve()
    if not resolved.is_relative_to(DBA_ROOT.resolve()):
        raise ProtocolRejected("PATH_TRAVERSAL", str(path))
    stat = path.stat()
    if (
        path.is_symlink() or not path.is_file() or stat.st_nlink != 1
        or stat.st_size > 1_000_000
    ):
        raise ProtocolRejected("UNSAFE_INPUT", str(path))
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ProtocolRejected("MALFORMED_OBJECT", str(path))
    if path == TASKS and not isinstance(value.get("tasks"), list):
        raise ProtocolRejected("SCHEMA_FAIL_CLOSED", "task registry missing tasks")
    if path == PARTICIPANTS and not isinstance(value.get("participants"), list):
        raise ProtocolRejected("SCHEMA_FAIL_CLOSED", "participant registry missing participants")
    return value


def _instant(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ProtocolRejected("TIMEZONE_REQUIRED", value)
    return parsed


def _task(task_id: str) -> dict[str, Any]:
    for task in _load(TASKS)["tasks"]:
        if task["task_id"] == task_id:
            return task
    raise ProtocolRejected("UNKNOWN_TASK", task_id)


def _participant(participant_ref: str, at: str) -> dict[str, Any]:
    for participant in _load(PARTICIPANTS)["participants"]:
        if participant["participant_ref"] == participant_ref:
            if _instant(at) < _instant(participant["valid_from"]):
                raise ProtocolRejected("PARTICIPANT_NOT_YET_VALID", participant_ref)
            if _instant(at) >= _instant(participant["expires_at"]):
                raise ProtocolRejected("PARTICIPANT_EXPIRED", participant_ref)
            if participant["revocation_ref"] != "NONE":
                raise ProtocolRejected("PARTICIPANT_REVOKED", participant_ref)
            if participant["participant_ref"] == participant["authority_issuer_ref"]:
                raise ProtocolRejected("SELF_AUTHORIZATION", participant_ref)
            return participant
    raise ProtocolRejected("UNKNOWN_PARTICIPANT", participant_ref)


def _authority(issuer_ref: str, at: str, action: str) -> dict[str, Any]:
    for authority in _load(AUTHORITIES)["authorities"]:
        if authority["authority_ref"] == issuer_ref:
            if _instant(at) < _instant(authority["valid_from"]):
                raise ProtocolRejected("AUTHORITY_NOT_YET_VALID", issuer_ref)
            if _instant(at) >= _instant(authority["expires_at"]):
                raise ProtocolRejected("AUTHORITY_EXPIRED", issuer_ref)
            if authority["revocation_ref"] != "NONE":
                raise ProtocolRejected("AUTHORITY_REVOKED", issuer_ref)
            if action not in authority["allowed_actions"]:
                raise ProtocolRejected("ACTION_NOT_AUTHORIZED", action)
            return authority
    raise ProtocolRejected("UNRECOGNIZED_AUTHORITY_ISSUER", issuer_ref)


def discover(need: str) -> list[dict[str, Any]]:
    tokens = {token.lower() for token in need.replace("/", " ").replace("-", " ").split()}
    ranked = []
    for task in _load(TASKS)["tasks"]:
        haystack = " ".join([
            task["title"], task["intent"], task["value_hypothesis"],
            task["problem_context"], *task["relevance_conditions"],
        ]).lower()
        score = sum(token in haystack for token in tokens if len(token) > 2)
        ranked.append({"task_id": task["task_id"], "score": score, "status": task["status"]})
    return sorted(ranked, key=lambda item: (-item["score"], item["task_id"]))


def eligible(participant: dict[str, Any], task: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if task["status"] != "AVAILABLE":
        reasons.append("TASK_NOT_AVAILABLE")
    if not set(task["allowed_participant_roles"]) & set(participant["assigned_roles"]):
        reasons.append("ROLE_MISMATCH")
    if not set(task["required_capabilities"]).issubset(set(participant["declared_capabilities"])):
        reasons.append("CAPABILITY_MISMATCH")
    for allowed in task["allowed_files"]:
        if not any(fnmatch.fnmatch(allowed, scope) for scope in participant["allowed_scope"]):
            reasons.append("SCOPE_MISMATCH")
            break
    return not reasons, reasons


def claim_request(participant_ref: str, task_id: str, at: str) -> dict[str, Any]:
    participant = _participant(participant_ref, at)
    task = _task(task_id)
    is_eligible, reasons = eligible(participant, task)
    if not is_eligible:
        raise ProtocolRejected("CLAIM_INELIGIBLE", ",".join(reasons))
    return {
        "request_id": f"CLAIM-{participant_ref}-{task_id}",
        "participant_ref": participant_ref,
        "task_ref": task_id,
        "requested_at": at,
        "status": "CLAIM_REQUESTED",
        "authority_effect": "NONE",
    }


def grant_lease(
    participant_ref: str,
    task_id: str,
    issued_by_ref: str,
    at: str,
    active_task_refs: list[str],
) -> dict[str, Any]:
    if issued_by_ref == participant_ref:
        raise ProtocolRejected("SELF_AUTHORIZATION", participant_ref)
    _authority(issued_by_ref, at, "ISSUE_BOUNDED_SCOPE_LEASE")
    if task_id in active_task_refs:
        raise ProtocolRejected("DUPLICATE_ACTIVE_CLAIM", task_id)
    participant = _participant(participant_ref, at)
    task = _task(task_id)
    is_eligible, reasons = eligible(participant, task)
    if not is_eligible:
        raise ProtocolRejected("LEASE_INELIGIBLE", ",".join(reasons))
    expires = _instant(at) + dt.timedelta(seconds=task["lease_duration_seconds"])
    return {
        "lease_id": f"LEASE-{participant_ref}-{task_id}",
        "participant_ref": participant_ref,
        "task_ref": task_id,
        "authority_ref": AUTHORITY_REF,
        "issued_by_ref": issued_by_ref,
        "allowed_files": task["allowed_files"],
        "forbidden_files": task["forbidden_files"],
        "issued_at": at,
        "expires_at": expires.isoformat(),
        "status": "CLAIMED",
        "revocation_ref": "NONE",
        "rollback_path": "discard unadopted candidate output",
    }


def task_contract(task_id: str) -> dict[str, Any]:
    task = _task(task_id)
    return {
        "contract_type": "BOUNDED_TASK_CANDIDATE",
        "task": task,
        "authority_reference": task["authority_reference"],
        "authority_effect": "NONE",
        "non_claims": [
            "TASK_CONTRACT_NE_AUTHORITY",
            "TASK_CLAIM_NE_ADOPTION",
            "CONTRIBUTION_NE_PERMISSION",
        ],
    }


def calibrate_recommendation(case_id: str) -> dict[str, Any]:
    for case in _load(CALIBRATION_CASES)["cases"]:
        if case["case_id"] == case_id:
            return {
                "case": case,
                "calibration_status": case["expected_status"],
                "reference_fixture_only": True,
                "authority_effect": "NONE",
                "non_claims": [
                    "CALIBRATION_NE_REAL_USER_RECOMMENDATION",
                    "RECOMMENDATION_NE_DECISION",
                    "MAPPING_NE_ADOPTION",
                ],
            }
    raise ProtocolRejected("UNKNOWN_CALIBRATION_CASE", case_id)


def reject_adversarial(attack: str) -> dict[str, Any]:
    reason = ADVERSARIAL_REJECTION_POLICY.get(attack)
    if reason is None:
        raise ProtocolRejected("UNKNOWN_ATTACK_CLASS", attack)
    return {"attack": attack, "decision": "REJECT", "reason_code": reason}


def _emit(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    discover_parser = sub.add_parser("discover")
    discover_parser.add_argument("--need", required=True)
    rank_parser = sub.add_parser("rank")
    rank_parser.add_argument("--need", required=True)
    for name in ("eligibility", "request-claim"):
        item = sub.add_parser(name)
        item.add_argument("--participant", required=True)
        item.add_argument("--task", required=True)
        item.add_argument("--at", required=True)
    grant = sub.add_parser("grant-lease")
    grant.add_argument("--participant", required=True)
    grant.add_argument("--task", required=True)
    grant.add_argument("--issued-by", required=True)
    grant.add_argument("--at", required=True)
    grant.add_argument("--active-task", action="append", default=[])
    for name in ("release-claim", "expire-claim"):
        item = sub.add_parser(name)
        item.add_argument("--lease", required=True)
        item.add_argument("--at", required=True)
    duplicate = sub.add_parser("detect-duplicate")
    duplicate.add_argument("--task", required=True)
    duplicate.add_argument("--active-task", action="append", default=[])
    contract = sub.add_parser("task-contract")
    contract.add_argument("--task", required=True)
    calibration = sub.add_parser("calibrate-recommendation")
    calibration.add_argument("--case", required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command in {"discover", "rank"}:
            _emit(discover(args.need))
        elif args.command == "eligibility":
            participant = _participant(args.participant, args.at)
            ok, reasons = eligible(participant, _task(args.task))
            _emit({"eligible": ok, "reasons": reasons})
        elif args.command == "request-claim":
            _emit(claim_request(args.participant, args.task, args.at))
        elif args.command == "grant-lease":
            _emit(grant_lease(
                args.participant, args.task, args.issued_by, args.at, args.active_task
            ))
        elif args.command in {"release-claim", "expire-claim"}:
            _emit({
                "lease_id": args.lease,
                "status": "RELEASED" if args.command == "release-claim" else "EXPIRED",
                "recorded_at": args.at,
                "authority_effect": "NONE",
            })
        elif args.command == "detect-duplicate":
            duplicate = args.task in args.active_task
            _emit({"task_ref": args.task, "duplicate_active_claim": duplicate})
            return 1 if duplicate else 0
        elif args.command == "task-contract":
            _emit(task_contract(args.task))
        elif args.command == "calibrate-recommendation":
            _emit(calibrate_recommendation(args.case))
    except (ProtocolRejected, json.JSONDecodeError) as exc:
        reason = exc.reason_code if isinstance(exc, ProtocolRejected) else "MALFORMED_JSON"
        _emit({"status": "REJECTED", "reason_code": reason, "detail": str(exc)})
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
