#!/usr/bin/env python3
"""Fail-closed, read-only canonical status projection for the DBA cockpit."""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "cockpit" / "source-registry.json"

STATUS_VALUES = {
    "PLANNED", "INITIALIZING", "IMPLEMENTING", "VALIDATING", "BLOCKED",
    "NOT_ASSESSED", "CANDIDATE", "READY_FOR_HUMAN_REVIEW", "MERGED",
    "RELEASED", "DEPLOYED", "MAINTENANCE",
}

REQUIRED_STATUS_FIELDS = {
    "status_contract_version", "project_id", "project_name",
    "conversation_aliases", "repository", "repository_visibility",
    "canonical_branch", "source_revision", "source_tree_digest",
    "architecture_owner", "implementation_owner", "evidence_semantics_owner",
    "lifecycle_status", "development_phase", "implementation_status",
    "discovery_layer_status", "self_observation_status",
    "problem_evidence_status", "canonical_owner_resolution_status",
    "patch_variant_status", "sandbox_implementation_status",
    "fitness_evaluation_status", "selection_status", "rollback_status",
    "lineage_status", "self_healing_status", "self_evolution_status",
    "autonomous_risk_classes", "human_authorization_risk_classes",
    "latest_evolution_run", "latest_run_result", "latest_run_digest",
    "latest_outcome_evidence", "latest_rollback_evidence", "test_summary",
    "ci_summary", "pull_request_observation", "declared_work_items",
    "dynamic_observation_boundaries", "blocking_issues", "blocking_decisions",
    "next_human_decision", "known_limitations", "authority_boundaries",
    "security_boundaries", "evolution_progress", "p0_10_reopened",
    "production_runtime_changed", "database_changed",
    "production_credential_created", "generated_at", "fresh_until",
}

STATUS_FIELDS = {
    "lifecycle_status", "discovery_layer_status", "self_observation_status",
    "problem_evidence_status", "canonical_owner_resolution_status",
    "patch_variant_status", "sandbox_implementation_status",
    "fitness_evaluation_status", "selection_status", "rollback_status",
    "lineage_status", "self_healing_status", "self_evolution_status",
}


class CockpitSourceError(RuntimeError):
    """A fail-closed source error with a stable machine reason code."""

    def __init__(self, code: str, detail: str | None = None) -> None:
        self.code = code
        self.detail = detail
        super().__init__(code if detail is None else f"{code}:{detail}")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def parse_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise CockpitSourceError("SOURCE_INVALID", "INVALID_TIMESTAMP") from exc
    if parsed.tzinfo is None:
        raise CockpitSourceError("SOURCE_INVALID", "TIMESTAMP_MISSING_TIMEZONE")
    return parsed.astimezone(timezone.utc)


def safe_source_path(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise CockpitSourceError("SOURCE_INVALID", "UNSAFE_SOURCE_PATH")
    return str(path)


class ReadOnlyStatusAdapter:
    """Read-only adapter; intentionally exposes no write or mutation methods."""

    def __init__(
        self,
        registry_path: Path = DEFAULT_REGISTRY,
        command_runner: Callable[[list[str]], subprocess.CompletedProcess[str]] | None = None,
        observation_provider: Callable[[dict[str, Any], str, str, datetime], dict[str, Any]] | None = None,
    ) -> None:
        self.registry_path = Path(registry_path)
        self.command_runner = command_runner or self._run
        self.observation_provider = observation_provider or self._observe_github

    def source(self, project_id: str) -> dict[str, Any]:
        try:
            registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CockpitSourceError("SOURCE_REGISTRY_INVALID") from exc
        matches = [entry for entry in registry.get("sources", []) if entry.get("project_id") == project_id]
        if len(matches) != 1:
            raise CockpitSourceError("SOURCE_REGISTRATION_NOT_UNIQUE")
        entry = matches[0]
        if entry.get("access_mode") != "READ_ONLY" or entry.get("refresh_mode") != "ON_DEMAND":
            raise CockpitSourceError("SOURCE_REGISTRY_AUTHORITY_INVALID")
        if entry.get("source_mode") != "CANONICAL_MAIN_EXACT_REVISION":
            raise CockpitSourceError("SOURCE_REGISTRY_MODE_INVALID")
        if any(key.startswith("candidate_") for key in entry):
            raise CockpitSourceError("SOURCE_REGISTRY_CANDIDATE_FORBIDDEN")
        return entry

    def fetch_local_git(
        self,
        project_id: str,
        repository_path: Path,
        *,
        retrieved_at: datetime | None = None,
    ) -> dict[str, Any]:
        entry = self.source(project_id)
        repository_path = Path(repository_path).resolve()
        ref = entry["source_branch"]
        revision = self._git(repository_path, "rev-parse", ref)
        tree_digest = self._git(repository_path, "rev-parse", f"{ref}^{{tree}}")
        status_bytes = self._git_bytes(
            repository_path, "show", f"{ref}:{safe_source_path(entry['source_status_path'])}"
        )
        schema_bytes = self._git_bytes(
            repository_path, "show", f"{ref}:{safe_source_path(entry['source_schema_path'])}"
        )
        return self._project(
            entry, status_bytes, schema_bytes, revision=revision,
            tree_digest=tree_digest, retrieved_at=retrieved_at,
        )

    def fetch_github(
        self,
        project_id: str,
        *,
        retrieved_at: datetime | None = None,
    ) -> dict[str, Any]:
        entry = self.source(project_id)
        ref = entry["source_branch"]
        repository = entry["source_repository"]
        commit = self._gh_json(f"repos/{repository}/commits/{quote(ref, safe='')}")
        revision = commit.get("sha")
        tree_digest = commit.get("commit", {}).get("tree", {}).get("sha")
        if not revision or not tree_digest:
            raise CockpitSourceError("SOURCE_UNAVAILABLE", "GITHUB_COMMIT_METADATA")
        status_bytes = self._gh_content(repository, entry["source_status_path"], revision)
        schema_bytes = self._gh_content(repository, entry["source_schema_path"], revision)
        return self._project(
            entry, status_bytes, schema_bytes, revision=revision,
            tree_digest=tree_digest, retrieved_at=retrieved_at,
        )

    def _project(
        self,
        entry: dict[str, Any],
        status_bytes: bytes,
        schema_bytes: bytes,
        *,
        revision: str,
        tree_digest: str,
        retrieved_at: datetime | None,
    ) -> dict[str, Any]:
        if revision != entry["source_revision"]:
            raise CockpitSourceError("SOURCE_DRIFT", "REVISION_MISMATCH")
        if tree_digest != entry["source_tree_digest"]:
            raise CockpitSourceError("SOURCE_DRIFT", "TREE_MISMATCH")
        status_digest = hashlib.sha256(status_bytes).hexdigest()
        if status_digest != entry["status_digest"]:
            raise CockpitSourceError("SOURCE_INVALID", "DIGEST_MISMATCH")

        try:
            status = json.loads(status_bytes)
            schema = json.loads(schema_bytes)
        except json.JSONDecodeError as exc:
            raise CockpitSourceError("SOURCE_INVALID", "JSON_PARSE") from exc
        self._validate_status(status, schema, entry)

        resolved = copy.deepcopy(status)
        if resolved["source_revision"] == "SELF":
            resolved["source_revision"] = revision
        if resolved["source_tree_digest"] == "SELF_TREE":
            resolved["source_tree_digest"] = tree_digest
        for stage in resolved["evolution_progress"].values():
            if stage.get("source_revision") == "SELF":
                stage["source_revision"] = revision
        if resolved.get("test_summary", {}).get("source_revision") == "SELF":
            resolved["test_summary"]["source_revision"] = revision
        if resolved.get("ci_summary", {}).get("target_revision") == "SELF":
            resolved["ci_summary"]["target_revision"] = revision
        if resolved.get("pull_request_observation", {}).get("target_revision") == "SELF":
            resolved["pull_request_observation"]["target_revision"] = revision
        if resolved["source_revision"] != revision:
            raise CockpitSourceError("SOURCE_DRIFT", "REVISION_MISMATCH")
        if resolved["source_tree_digest"] != tree_digest:
            raise CockpitSourceError("SOURCE_DRIFT", "TREE_MISMATCH")

        now = (retrieved_at or datetime.now(timezone.utc)).astimezone(timezone.utc)
        if now > parse_timestamp(resolved["fresh_until"]):
            raise CockpitSourceError("SOURCE_STALE")

        projection = {
            "projection_contract_version": "0.2",
            "cockpit_status": "PASS",
            "project_id": entry["project_id"],
            "display_name": entry["display_name"],
            "conversation_alias": entry["conversation_alias"],
            "source_reference": {
                "repository": entry["source_repository"],
                "branch": entry["source_branch"],
                "status_path": entry["source_status_path"],
                "schema_path": entry["source_schema_path"],
                "mode": entry["source_mode"],
            },
            "source_revision": revision,
            "source_tree_digest": tree_digest,
            "status_source_digest": status_digest,
            "source_freshness": "FRESH",
            "source_status_freshness": "FRESH",
            "remote_revision_freshness": "NOT_ASSESSED",
            "ci_observation_freshness": "NOT_ASSESSED",
            "pull_request_observation_freshness": "NOT_ASSESSED",
            "fresh_until": resolved["fresh_until"],
            "retrieved_at": now.isoformat().replace("+00:00", "Z"),
            "source_integrity": "PASS",
            "source_revision_match": True,
            "source_tree_match": True,
            "source_declarations": {
                "ci_observation_request": resolved["ci_summary"],
                "pull_request_observation_request": resolved["pull_request_observation"],
                "declared_work_items": resolved["declared_work_items"],
                "dynamic_observation_boundaries": resolved["dynamic_observation_boundaries"],
            },
            "community_boundaries": {
                "architecture_status": "READY",
                "protocol_status": "CANDIDATE",
                "public_operation_status": "NOT_YET_VERIFIED",
            },
            "projection_boundaries": {
                "cockpit_pull_only": True,
                "cockpit_push": False,
                "cockpit_stores_projection": True,
                "cockpit_stores_canonical_run": False,
                "raw_run_copied": False,
                "status_projection_is_adoption": False,
                "status_owner_is_observer": False,
            },
        }
        return self._attach_observations(projection, entry, resolved, revision, tree_digest, now)

    def _attach_observations(
        self,
        projection: dict[str, Any],
        entry: dict[str, Any],
        status: dict[str, Any],
        revision: str,
        tree_digest: str,
        now: datetime,
    ) -> dict[str, Any]:
        try:
            observations = self.observation_provider(entry, revision, tree_digest, now)
            for key in ("remote_head_observation", "ci_observation", "pull_request_observation"):
                if key not in observations:
                    raise CockpitSourceError("GITHUB_OBSERVATION_UNAVAILABLE", f"MISSING:{key}")
            projection.update(observations)
            max_age = entry["freshness_policy"]["dynamic_observation_max_age_seconds"]
            freshness = {
                "remote_revision_freshness": self._observation_freshness(
                    observations["remote_head_observation"], now, max_age
                ),
                "ci_observation_freshness": self._observation_freshness(
                    observations["ci_observation"], now, max_age
                ),
                "pull_request_observation_freshness": self._observation_freshness(
                    observations["pull_request_observation"], now, max_age
                ),
            }
            projection.update(freshness)
            observation_available = all(value == "FRESH" for value in freshness.values())
            remote_matches = (
                observations["remote_head_observation"].get("revision_match") is True
                and observations["remote_head_observation"].get("tree_match") is True
            )
            if not observation_available or not remote_matches:
                projection["cockpit_status"] = "SOURCE_STALE_OR_PARTIALLY_STALE"
        except (CockpitSourceError, KeyError, TypeError, ValueError) as exc:
            detail = exc.detail if isinstance(exc, CockpitSourceError) else str(exc)
            projection["cockpit_status"] = "SOURCE_STALE_OR_PARTIALLY_STALE"
            projection["remote_head_observation"] = self._unavailable_observation("REMOTE_HEAD", detail)
            projection["ci_observation"] = self._unavailable_observation("CI", detail)
            projection["pull_request_observation"] = self._unavailable_observation("PULL_REQUEST", detail)

        projection["summary"] = self._summary(status, projection)
        return projection

    @staticmethod
    def _observation_freshness(observation: dict[str, Any], now: datetime, max_age_seconds: int) -> str:
        observed_at = parse_timestamp(observation.get("observed_at", ""))
        age = (now - observed_at).total_seconds()
        if -60 <= age <= max_age_seconds and observation.get("status") != "NOT_ASSESSED":
            return "FRESH"
        return "STALE"

    @staticmethod
    def _unavailable_observation(kind: str, detail: str | None) -> dict[str, Any]:
        return {
            "status": "NOT_ASSESSED",
            "observation_kind": kind,
            "observed_at": None,
            "reason": "GITHUB_OBSERVATION_UNAVAILABLE",
            "detail": detail,
            "limitations": ["No dynamic GitHub state is inferred from the static project-status source."],
        }

    def _observe_github(
        self,
        entry: dict[str, Any],
        revision: str,
        tree_digest: str,
        observed_at: datetime,
    ) -> dict[str, Any]:
        repository = entry["source_repository"]
        branch = entry["source_branch"]
        timestamp = observed_at.isoformat().replace("+00:00", "Z")
        remote = self._gh_json(f"repos/{repository}/commits/{quote(branch, safe='')}")
        remote_revision = remote.get("sha")
        remote_tree = remote.get("commit", {}).get("tree", {}).get("sha")
        if not remote_revision or not remote_tree:
            raise CockpitSourceError("GITHUB_OBSERVATION_UNAVAILABLE", "REMOTE_HEAD_METADATA")

        check_payload = self._gh_json(
            f"repos/{repository}/commits/{revision}/check-runs",
            headers=["Accept: application/vnd.github+json"],
        )
        checks = [
            {
                "name": item.get("name"),
                "status": item.get("status"),
                "conclusion": item.get("conclusion"),
                "details_url": item.get("html_url") or item.get("details_url"),
            }
            for item in check_payload.get("check_runs", [])
        ]
        ci_status = self._ci_status(checks)

        pulls = self._gh_json(f"repos/{repository}/pulls?state=all&per_page=100")
        if not isinstance(pulls, list):
            raise CockpitSourceError("GITHUB_OBSERVATION_UNAVAILABLE", "PULL_REQUEST_PAYLOAD")
        normalized = [
            {
                "number": item.get("number"),
                "state": "MERGED" if item.get("merged_at") else item.get("state", "UNKNOWN").upper(),
                "is_draft": bool(item.get("draft")),
                "head_revision": item.get("head", {}).get("sha"),
                "base_branch": item.get("base", {}).get("ref"),
                "url": item.get("html_url"),
            }
            for item in pulls
        ]
        return {
            "remote_head_observation": {
                "status": "PASS" if remote_revision == revision and remote_tree == tree_digest else "FAIL",
                "observation_owner": "DBA_COCKPIT_READ_ONLY_ADAPTER",
                "observed_at": timestamp,
                "repository": repository,
                "branch": branch,
                "revision": remote_revision,
                "tree_digest": remote_tree,
                "revision_match": remote_revision == revision,
                "tree_match": remote_tree == tree_digest,
                "limitations": ["This is a point-in-time GitHub API observation."],
            },
            "ci_observation": {
                "status": ci_status,
                "observation_owner": "DBA_COCKPIT_READ_ONLY_ADAPTER",
                "observed_at": timestamp,
                "target_revision": revision,
                "checks": checks,
                "release_implied": False,
                "deployment_implied": False,
                "production_readiness_implied": False,
                "limitations": ["CI state is dynamic and applies only to the exact target revision."],
            },
            "pull_request_observation": {
                "status": "PASS",
                "observation_owner": "DBA_COCKPIT_READ_ONLY_ADAPTER",
                "observed_at": timestamp,
                "open_pull_requests": [item for item in normalized if item["state"] == "OPEN"],
                "merged_pull_requests": [item for item in normalized if item["state"] == "MERGED"],
                "closed_pull_requests": [item for item in normalized if item["state"] == "CLOSED"],
                "limitations": ["Pull request state is a point-in-time GitHub API observation."],
            },
        }

    @staticmethod
    def _ci_status(checks: list[dict[str, Any]]) -> str:
        if not checks:
            return "NOT_CONFIGURED"
        if any(item.get("status") != "completed" for item in checks):
            return "PENDING"
        accepted = {"success", "neutral", "skipped"}
        return "PASS" if all(item.get("conclusion") in accepted for item in checks) else "FAIL"

    def _validate_status(
        self, status: dict[str, Any], schema: dict[str, Any], entry: dict[str, Any]
    ) -> None:
        missing = sorted(REQUIRED_STATUS_FIELDS - status.keys())
        if missing:
            raise CockpitSourceError("SOURCE_INVALID", f"MISSING_FIELDS:{','.join(missing)}")
        schema_required = set(schema.get("required", []))
        if not REQUIRED_STATUS_FIELDS.issubset(schema_required):
            raise CockpitSourceError("SOURCE_INVALID", "SCHEMA_REQUIRED_FIELDS")
        expected = {
            "project_id": "titmac-scout",
            "project_name": "titmac-scout",
            "conversation_aliases": ["tiamas-scout"],
            "repository": entry["source_repository"],
            "repository_visibility": "PRIVATE",
            "canonical_branch": "main",
            "p0_10_reopened": False,
            "production_runtime_changed": False,
            "database_changed": False,
            "production_credential_created": False,
        }
        for key, value in expected.items():
            if status.get(key) != value:
                raise CockpitSourceError("SOURCE_INVALID", f"BOUNDARY:{key}")
        invalid = sorted(key for key in STATUS_FIELDS if status.get(key) not in STATUS_VALUES)
        if invalid:
            raise CockpitSourceError("SOURCE_INVALID", f"STATUS_ENUM:{','.join(invalid)}")
        if not status.get("known_limitations"):
            raise CockpitSourceError("SOURCE_INVALID", "KNOWN_LIMITATIONS_REQUIRED")
        if status.get("ci_summary", {}).get("status") != "EXTERNAL_OBSERVATION_REQUIRED":
            raise CockpitSourceError("SOURCE_INVALID", "CI_STATE_MUST_BE_EXTERNAL")
        if status.get("pull_request_observation", {}).get("items_declared_here") is not False:
            raise CockpitSourceError("SOURCE_INVALID", "PR_STATE_MUST_BE_EXTERNAL")
        if status.get("dynamic_observation_boundaries", {}).get("freshness_scope") != "DECLARED_PROJECT_STATUS_ONLY":
            raise CockpitSourceError("SOURCE_INVALID", "FRESHNESS_SCOPE_INVALID")

    @staticmethod
    def _summary(status: dict[str, Any], projection: dict[str, Any]) -> dict[str, Any]:
        pr_observation = projection["pull_request_observation"]
        return {
            "implementation_owner": status["implementation_owner"],
            "canonical_repository": status["repository"],
            "lifecycle_status": status["lifecycle_status"],
            "development_phase": status["development_phase"],
            "implementation_status": status["implementation_status"],
            "status_source_state": "MERGED_ON_CANONICAL_MAIN",
            "cockpit_bridge_state": "READY_FOR_HUMAN_REVIEW",
            "discovery_status": status["discovery_layer_status"],
            "self_healing_status": status["self_healing_status"],
            "self_evolution_status": status["self_evolution_status"],
            "latest_evolution_run": status["latest_evolution_run"],
            "latest_evolution_result": status["latest_run_result"],
            "latest_selected_variant": None,
            "latest_outcome_evidence": status["latest_outcome_evidence"],
            "latest_rollback_evidence": status["latest_rollback_evidence"],
            "tests": status["test_summary"],
            "ci": projection["ci_observation"],
            "open_pull_requests": pr_observation.get("open_pull_requests", []),
            "merged_pull_requests": pr_observation.get("merged_pull_requests", []),
            "closed_pull_requests": pr_observation.get("closed_pull_requests", []),
            "blocking_issues": status["blocking_issues"],
            "blocking_decisions": status["blocking_decisions"],
            "next_human_decision": status["next_human_decision"],
            "known_limitations": status["known_limitations"],
            "authority_boundaries": status["authority_boundaries"],
            "evolution_progress": status["evolution_progress"],
            "p0_10_reopened": status["p0_10_reopened"],
        }

    def _git(self, repository_path: Path, *arguments: str) -> str:
        result = self.command_runner(["git", "-C", str(repository_path), *arguments])
        if result.returncode != 0:
            raise CockpitSourceError("SOURCE_UNAVAILABLE", result.stderr.strip())
        return result.stdout.strip()

    def _git_bytes(self, repository_path: Path, *arguments: str) -> bytes:
        result = subprocess.run(
            ["git", "-C", str(repository_path), *arguments],
            check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            raise CockpitSourceError(
                "SOURCE_UNAVAILABLE", result.stderr.decode("utf-8", errors="replace").strip()
            )
        return result.stdout

    def _gh_json(self, endpoint: str, headers: list[str] | None = None) -> Any:
        arguments = ["gh", "api"]
        for header in headers or []:
            arguments.extend(["-H", header])
        arguments.append(endpoint)
        result = self.command_runner(arguments)
        if result.returncode != 0:
            raise CockpitSourceError("SOURCE_UNAVAILABLE", result.stderr.strip())
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise CockpitSourceError("SOURCE_UNAVAILABLE", "GITHUB_JSON_INVALID") from exc

    def _gh_content(self, repository: str, path: str, ref: str) -> bytes:
        payload = self._gh_json(
            f"repos/{repository}/contents/{safe_source_path(path)}?ref={quote(ref, safe='')}"
        )
        if payload.get("encoding") != "base64" or not payload.get("content"):
            raise CockpitSourceError("SOURCE_UNAVAILABLE", "GITHUB_CONTENT_INVALID")
        try:
            return base64.b64decode(payload["content"], validate=False)
        except (ValueError, TypeError) as exc:
            raise CockpitSourceError("SOURCE_UNAVAILABLE", "GITHUB_CONTENT_DECODE") from exc

    @staticmethod
    def _run(arguments: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(arguments, check=False, capture_output=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", default="titmac-scout")
    parser.add_argument("--local-repository", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    adapter = ReadOnlyStatusAdapter()
    try:
        if args.local_repository:
            projection = adapter.fetch_local_git(args.project_id, args.local_repository)
        else:
            projection = adapter.fetch_github(args.project_id)
    except CockpitSourceError as exc:
        print(canonical_json({"ok": False, "cockpit_status": exc.code, "detail": exc.detail}), end="")
        return 1

    output = canonical_json(projection)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
