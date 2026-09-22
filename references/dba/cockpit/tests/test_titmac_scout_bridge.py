from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


COCKPIT = Path(__file__).resolve().parents[1]

import sys

sys.path.insert(0, str(COCKPIT))
from read_only_status_adapter import CockpitSourceError, ReadOnlyStatusAdapter, canonical_json


class TitmacScoutBridgeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.scout = Path(self.temporary_directory.name) / "titmac-scout-fixture"
        (self.scout / "governance").mkdir(parents=True)
        status = self.fixture_status()
        status_bytes = canonical_json(status).encode("utf-8")
        (self.scout / "governance" / "project-status.json").write_bytes(status_bytes)
        schema = {
            "type": "object",
            "required": sorted(status.keys()),
            "properties": {key: {} for key in status},
        }
        (self.scout / "governance" / "project-status.schema.json").write_text(
            canonical_json(schema), encoding="utf-8"
        )
        self.git("init", "-b", "main")
        self.git("config", "user.name", "D21 Test Fixture")
        self.git("config", "user.email", "d21-fixture@example.invalid")
        self.git("add", "governance")
        self.git("commit", "-m", "fixture")
        self.expected_revision = self.git("rev-parse", "HEAD")
        self.expected_tree = self.git("rev-parse", "HEAD^{tree}")
        self.expected_digest = hashlib.sha256(status_bytes).hexdigest()

        registry = json.loads((COCKPIT / "source-registry.json").read_text(encoding="utf-8"))
        entry = registry["sources"][0]
        entry["source_revision"] = self.expected_revision
        entry["source_tree_digest"] = self.expected_tree
        entry["status_digest"] = self.expected_digest
        self.registry_path = Path(self.temporary_directory.name) / "source-registry.json"
        self.registry_path.write_text(canonical_json(registry), encoding="utf-8")
        self.at = datetime(2026, 8, 2, 8, 30, tzinfo=timezone.utc)
        self.adapter = ReadOnlyStatusAdapter(
            self.registry_path, observation_provider=self.observations
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    # D20 bridge regression tests: retained after canonical activation.
    def test_sc_d20_t06_source_revision_verified(self) -> None:
        projection = self.fetch()
        self.assertEqual(self.expected_revision, projection["source_revision"])
        self.assertTrue(projection["source_revision_match"])
        mismatched = self.adapter_with_registry_override(source_revision="0" * 40)
        with self.assertRaisesRegex(CockpitSourceError, "SOURCE_DRIFT:REVISION_MISMATCH"):
            mismatched.fetch_local_git("titmac-scout", self.scout, retrieved_at=self.at)

    def test_sc_d20_t07_source_digest_verified(self) -> None:
        projection = self.fetch()
        self.assertEqual(self.expected_digest, projection["status_source_digest"])
        self.assertEqual("PASS", projection["source_integrity"])
        mismatched = self.adapter_with_registry_override(status_digest="0" * 64)
        with self.assertRaisesRegex(CockpitSourceError, "SOURCE_INVALID:DIGEST_MISMATCH"):
            mismatched.fetch_local_git("titmac-scout", self.scout, retrieved_at=self.at)

    def test_sc_d20_t08_stale_status_fails_closed(self) -> None:
        with self.assertRaisesRegex(CockpitSourceError, "SOURCE_STALE"):
            self.adapter.fetch_local_git(
                "titmac-scout", self.scout,
                retrieved_at=datetime(2026, 8, 6, tzinfo=timezone.utc),
            )

    def test_sc_d20_t09_unavailable_source_fails_closed(self) -> None:
        with self.assertRaisesRegex(CockpitSourceError, "SOURCE_UNAVAILABLE"):
            self.adapter.fetch_local_git(
                "titmac-scout", Path("/definitely/not/a/repository"), retrieved_at=self.at
            )

    def test_sc_d20_t12_cockpit_adapter_is_read_only(self) -> None:
        public_methods = {name for name in dir(self.adapter) if not name.startswith("_")}
        forbidden = {"write", "push", "merge", "open_pr", "trigger_repair", "issue_credential", "activate_mutation"}
        self.assertTrue(forbidden.isdisjoint(public_methods))
        self.assertEqual("READ_ONLY", self.adapter.source("titmac-scout")["access_mode"])

    def test_sc_d20_t13_no_raw_run_is_copied_to_dba(self) -> None:
        projection = self.fetch()
        serialized = canonical_json(projection).lower()
        for forbidden in ("raw evolution run", "raw patch variant", "raw sandbox output", "raw model output", "credential"):
            self.assertNotIn(forbidden, serialized)
        self.assertFalse(projection["projection_boundaries"]["raw_run_copied"])
        self.assertFalse(projection["projection_boundaries"]["cockpit_stores_canonical_run"])

    def test_sc_d20_t16_p0_10_remains_closed(self) -> None:
        self.assertFalse(self.fetch()["summary"]["p0_10_reopened"])

    def test_sc_d20_t17_pr105_remains_draft(self) -> None:
        snapshot = json.loads((COCKPIT / "external-pr-boundaries.json").read_text(encoding="utf-8"))
        item = next(item for item in snapshot["pull_requests"] if item["number"] == 105)
        self.assertEqual("OPEN", item["state"])
        self.assertTrue(item["is_draft"])
        self.assertEqual("PENDING", item["ownership_review"])

    def test_sc_d20_t18_pr106_remains_draft(self) -> None:
        snapshot = json.loads((COCKPIT / "external-pr-boundaries.json").read_text(encoding="utf-8"))
        item = next(item for item in snapshot["pull_requests"] if item["number"] == 106)
        self.assertEqual("OPEN", item["state"])
        self.assertTrue(item["is_draft"])
        self.assertEqual("PENDING", item["migration_review"])

    def test_sc_d20_t20_clean_refresh_replay(self) -> None:
        self.assertEqual(canonical_json(self.fetch()), canonical_json(self.fetch()))

    # D21 canonical-main and dynamic-observation tests.
    def test_cb_d21_t01_canonical_main_fetch_succeeds(self) -> None:
        projection = self.fetch()
        self.assertEqual("main", projection["source_reference"]["branch"])
        self.assertEqual("PASS", projection["cockpit_status"])

    def test_cb_d21_t02_candidate_branch_is_no_longer_canonical(self) -> None:
        source = self.adapter.source("titmac-scout")
        self.assertEqual("CANONICAL_MAIN_EXACT_REVISION", source["source_mode"])
        self.assertFalse(any(key.startswith("candidate_") for key in source))

    def test_cb_d21_t03_exact_main_revision_is_verified(self) -> None:
        projection = self.fetch()
        self.assertEqual(self.expected_revision, projection["source_revision"])
        self.assertTrue(projection["remote_head_observation"]["revision_match"])

    def test_cb_d21_t04_exact_main_tree_is_verified(self) -> None:
        projection = self.fetch()
        self.assertEqual(self.expected_tree, projection["source_tree_digest"])
        self.assertTrue(projection["remote_head_observation"]["tree_match"])
        self.assertTrue(projection["source_tree_match"])

    def test_cb_d21_t05_live_ci_observation_is_separated(self) -> None:
        projection = self.fetch()
        self.assertEqual("EXTERNAL_OBSERVATION_REQUIRED", projection["source_declarations"]["ci_observation_request"]["status"])
        self.assertEqual("PASS", projection["ci_observation"]["status"])
        self.assertEqual("FRESH", projection["ci_observation_freshness"])

    def test_cb_d21_t06_live_pr_observation_is_separated(self) -> None:
        projection = self.fetch()
        request = projection["source_declarations"]["pull_request_observation_request"]
        self.assertFalse(request["items_declared_here"])
        self.assertEqual([1], [item["number"] for item in projection["pull_request_observation"]["merged_pull_requests"]])

    def test_cb_d21_t07_unavailable_github_observation_fails_partially_closed(self) -> None:
        def unavailable(*_args: object) -> dict[str, object]:
            raise CockpitSourceError("GITHUB_OBSERVATION_UNAVAILABLE", "fixture")

        adapter = ReadOnlyStatusAdapter(self.registry_path, observation_provider=unavailable)
        projection = adapter.fetch_local_git("titmac-scout", self.scout, retrieved_at=self.at)
        self.assertEqual("SOURCE_STALE_OR_PARTIALLY_STALE", projection["cockpit_status"])
        self.assertEqual("PASS", projection["source_integrity"])
        self.assertEqual("NOT_ASSESSED", projection["ci_observation"]["status"])

    def test_cb_d21_t08_cockpit_remains_read_only(self) -> None:
        self.assertFalse(self.fetch()["projection_boundaries"]["cockpit_push"])
        self.assertEqual("GITHUB_API_READ_ONLY", self.adapter.source("titmac-scout")["dynamic_observation_mode"])

    def test_cb_d21_t09_source_status_remains_owner_controlled(self) -> None:
        projection = self.fetch()
        self.assertEqual("IMPLEMENTING", projection["summary"]["lifecycle_status"])
        self.assertFalse(projection["projection_boundaries"]["status_owner_is_observer"])
        self.assertEqual("joy7758/titmac-scout", projection["summary"]["implementation_owner"])

    def test_cb_d21_t10_no_raw_scout_evidence_is_copied(self) -> None:
        projection = self.fetch()
        self.assertFalse(projection["projection_boundaries"]["raw_run_copied"])
        self.assertNotIn("latest_run_digest", canonical_json(projection))

    def test_d27_stored_projection_records_negative_discovery_without_elevation(self) -> None:
        projection = json.loads(
            (COCKPIT / "projections" / "titmac-scout.json").read_text(
                encoding="utf-8"
            )
        )
        summary = projection["summary"]
        self.assertEqual(
            "e4adbbbbb149871f108fcf384369182d8c5765f4",
            projection["source_revision"],
        )
        self.assertEqual("PASS", projection["cockpit_status"])
        self.assertEqual("CANDIDATE", summary["discovery_status"])
        self.assertEqual("CANDIDATE", summary["self_healing_status"])
        self.assertEqual("CANDIDATE", summary["self_evolution_status"])
        self.assertEqual(
            "evolution-runs/D26-SECOND-INDEPENDENT-ER1",
            summary["latest_evolution_run"],
        )
        self.assertEqual(
            "NO_ELIGIBLE_INDEPENDENT_ER1_FOUND",
            summary["latest_evolution_result"],
        )
        self.assertIn(
            4,
            [item["number"] for item in summary["merged_pull_requests"]],
        )
        self.assertTrue(
            any(
                "D24-DBA-ER1-001 remains the last retained self-healing run" in item
                for item in summary["known_limitations"]
            )
        )
        self.assertTrue(
            any(
                "REAL_SELF_HEALING_OPERATION_COUNT=1" in item
                for item in summary["known_limitations"]
            )
        )
        self.assertIsNone(summary["latest_rollback_evidence"])
        self.assertFalse(projection["projection_boundaries"]["raw_run_copied"])
        self.assertFalse(summary["ci"]["production_readiness_implied"])
        self.assertNotIn(
            "PRODUCTION_READY",
            {
                summary["implementation_status"],
                summary["discovery_status"],
                summary["self_healing_status"],
                summary["self_evolution_status"],
            },
        )

    def fetch(self) -> dict[str, object]:
        return self.adapter.fetch_local_git("titmac-scout", self.scout, retrieved_at=self.at)

    def observations(
        self, _entry: dict[str, object], revision: str, tree: str, observed_at: datetime
    ) -> dict[str, object]:
        timestamp = observed_at.isoformat().replace("+00:00", "Z")
        return {
            "remote_head_observation": {
                "status": "PASS", "observed_at": timestamp,
                "revision": revision, "tree_digest": tree,
                "revision_match": True, "tree_match": True,
            },
            "ci_observation": {
                "status": "PASS", "observed_at": timestamp,
                "target_revision": revision, "checks": [{"name": "test", "conclusion": "success"}],
            },
            "pull_request_observation": {
                "status": "PASS", "observed_at": timestamp,
                "open_pull_requests": [],
                "merged_pull_requests": [{"number": 1, "state": "MERGED"}],
                "closed_pull_requests": [],
            },
        }

    def git(self, *arguments: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.scout), *arguments], check=True,
            capture_output=True, text=True,
        )
        return result.stdout.strip()

    def adapter_with_registry_override(self, **overrides: object) -> ReadOnlyStatusAdapter:
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        registry["sources"][0].update(overrides)
        path = Path(self.temporary_directory.name) / f"registry-{next(iter(overrides))}.json"
        path.write_text(canonical_json(registry), encoding="utf-8")
        return ReadOnlyStatusAdapter(path, observation_provider=self.observations)

    @staticmethod
    def fixture_status() -> dict[str, object]:
        progress = {
            stage: {
                "status": "NOT_ASSESSED", "updated_at": None,
                "evidence_reference": None, "source_revision": "SELF",
                "limitations": ["Synthetic adapter test fixture only."],
            }
            for stage in (
                "OBSERVE DISCOVER EVIDENCE REPRODUCE CLASSIFY_RISK RESOLVE_OWNER "
                "GENERATE_VARIANTS IMPLEMENT_IN_SANDBOX EVALUATE_FITNESS SELECT "
                "AWAIT_AUTHORIZATION APPLY OBSERVE_OUTCOME RETAIN_OR_ROLLBACK RECORD_LINEAGE"
            ).split()
        }
        return {
            "status_contract_version": "0.1", "project_id": "titmac-scout",
            "project_name": "titmac-scout", "conversation_aliases": ["tiamas-scout"],
            "repository": "joy7758/titmac-scout", "repository_visibility": "PRIVATE",
            "canonical_branch": "main", "source_revision": "SELF",
            "source_tree_digest": "SELF_TREE",
            "architecture_owner": "joy7758/digital-biosphere-architecture-specification",
            "implementation_owner": "joy7758/titmac-scout",
            "evidence_semantics_owner": "TITMAS_EVIDENCE_ARCHITECTURE",
            "lifecycle_status": "IMPLEMENTING", "development_phase": "D21_CANONICAL_STATUS_ACTIVATION",
            "implementation_status": "STATUS_CONTRACT_READY_FOR_CANONICAL_MAIN",
            "discovery_layer_status": "CANDIDATE", "self_observation_status": "CANDIDATE",
            "problem_evidence_status": "CANDIDATE", "canonical_owner_resolution_status": "NOT_ASSESSED",
            "patch_variant_status": "NOT_ASSESSED", "sandbox_implementation_status": "NOT_ASSESSED",
            "fitness_evaluation_status": "NOT_ASSESSED", "selection_status": "NOT_ASSESSED",
            "rollback_status": "NOT_ASSESSED", "lineage_status": "NOT_ASSESSED",
            "self_healing_status": "NOT_ASSESSED", "self_evolution_status": "NOT_ASSESSED",
            "autonomous_risk_classes": [], "human_authorization_risk_classes": [],
            "latest_evolution_run": None, "latest_run_result": None, "latest_run_digest": None,
            "latest_outcome_evidence": None, "latest_rollback_evidence": None,
            "test_summary": {"status": "PASS", "source_revision": "SELF"},
            "ci_summary": {
                "status": "EXTERNAL_OBSERVATION_REQUIRED", "target_revision": "SELF"
            },
            "pull_request_observation": {
                "status": "EXTERNAL_GITHUB_QUERY_REQUIRED", "target_revision": "SELF",
                "items_declared_here": False,
            },
            "declared_work_items": [{
                "reference": "joy7758/titmac-scout#1", "purpose": "D20_STATUS_CONTRACT",
                "dynamic_state": "EXTERNAL_OBSERVATION_REQUIRED",
            }],
            "dynamic_observation_boundaries": {"freshness_scope": "DECLARED_PROJECT_STATUS_ONLY"},
            "blocking_issues": [],
            "blocking_decisions": ["PR105_OWNERSHIP_REVIEW_PENDING", "PR106_MIGRATION_REVIEW_PENDING"],
            "next_human_decision": "TITMAC_SCOUT_EVOLUTION_IMPLEMENTATION_OWNERSHIP_MIGRATION",
            "known_limitations": ["Synthetic adapter test fixture only."],
            "authority_boundaries": ["COCKPIT_PULL_ONLY"],
            "security_boundaries": ["P0_10_CLOSED", "D04_CLOSED"],
            "evolution_progress": progress, "progress_percent": 0,
            "p0_10_reopened": False, "production_runtime_changed": False,
            "database_changed": False, "production_credential_created": False,
            "generated_at": "2026-08-02T08:23:46Z", "fresh_until": "2026-08-05T08:23:46Z",
        }


if __name__ == "__main__":
    unittest.main()
