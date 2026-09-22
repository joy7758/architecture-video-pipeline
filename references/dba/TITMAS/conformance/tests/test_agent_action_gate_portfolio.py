from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
PROJECTION = ROOT / "TITMAS/specifications/portfolio/agent-action-gate.json"
PROPOSAL = ROOT / "TITMAS/specifications/proposals/titmas-agent-action-gate-admission-v0.1.md"
HISTORICAL_CONSTITUTION = ROOT / "architecture/open-infrastructure-strategy-constitution.md"
CURRENT_CONSTITUTION = ROOT / "architecture/commercial-private-infrastructure-strategy-constitution.md"


class AgentActionGatePortfolioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.projection = json.loads(PROJECTION.read_text(encoding="utf-8"))
        self.proposal = PROPOSAL.read_text(encoding="utf-8")

    def test_public_reference_implementation_source_is_exactly_pinned(self) -> None:
        self.assertEqual(
            self.projection["canonical_remote_repository"],
            "https://github.com/joy7758/titmas-agent-action-gate",
        )
        self.assertEqual(self.projection["observed_branch"], "main")
        self.assertEqual(
            self.projection["observed_commit"],
            "6f1c83bf87e6ee96a0eda281e1fa91b8f80a32e1",
        )
        self.assertEqual(
            self.projection["contract_ci"]["head_sha"],
            self.projection["implementation_pull_request"]["head_commit"],
        )
        self.assertEqual(self.projection["contract_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(len(self.projection["contract_ci"]["checks"]), 2)
        self.assertTrue(
            all(
                check["conclusion"] == "SUCCESS"
                for check in self.projection["contract_ci"]["checks"]
            )
        )

    def test_existence_and_management_do_not_elevate_authority(self) -> None:
        self.assertFalse(self.projection["portfolio_admission"])
        self.assertTrue(self.projection["dba_management_policy_granted"])
        self.assertFalse(self.projection["github_principal_mapped"])
        self.assertFalse(self.projection["github_acl_changed"])
        self.assertFalse(self.projection["runtime_permission_created"])
        self.assertTrue(self.projection["implementation_started"])
        self.assertTrue(self.projection["action_gate_implemented"])
        self.assertTrue(self.projection["mcp_server_implemented"])
        smoke = self.projection["native_agentteams_smoke"]
        self.assertTrue(smoke["executed"])
        self.assertFalse(smoke["autonomous_end_to_end_completed"])
        self.assertFalse(smoke["per_worker_mcp_tool_acl_enforced"])
        self.assertFalse(smoke["repository_skills_materialized"])
        self.assertFalse(smoke["external_action_executed"])
        self.assertFalse(smoke["persistent_deployment"])
        self.assertFalse(smoke["production_deployment"])
        self.assertTrue(smoke["temporary_stack_destroyed"])
        self.assertTrue(smoke["temporary_state_removed"])
        self.assertFalse(self.projection["competition_submission"])

    def test_gates_preserve_reference_and_non_release_boundaries(self) -> None:
        gates = self.projection["gates"]
        self.assertEqual(gates["G0"], "REVIEW_REQUIRED_READY_FOR_HUMAN_DECISION")
        self.assertEqual(gates["G1"], "PASS_PUBLIC_MAIN_REFERENCE_SOURCE_PINNED")
        self.assertIn("REFERENCE_IMPLEMENTATION", gates["G3"])
        self.assertIn("NOT_INDEPENDENT", gates["G4"])
        self.assertIn("RUNTIME_PERMISSION_NOT_CREATED", gates["G5"])
        self.assertIn("NO_MERGE", gates["G6"])
        self.assertIn("NO_EXTERNAL_ACTION", gates["G6"])
        self.assertIn("NOT_ASSESSED", gates["G7"])
        self.assertIn("NO_HUMAN_ADOPTION_DECISION", gates["G7"])
        self.assertIn("PRODUCT_NOT_RECOMMENDED", gates["G7"])
        self.assertEqual(gates["G8"], "NOT_RELEASED_NOT_ADOPTED_NOT_SUBMITTED")

    def test_proposal_is_review_ready_but_not_admitted(self) -> None:
        self.assertIn("status: READY_FOR_REVIEW", self.proposal)
        self.assertIn("PORTFOLIO_ADMISSION_GRANTED=false", self.proposal)
        self.assertIn("ACTION_GATE_REFERENCE_IMPLEMENTED=true", self.proposal)
        self.assertIn("AGENTTEAMS_NATIVE_LOCAL_SMOKE_EXECUTED=true", self.proposal)
        self.assertIn("AGENTTEAMS_NATIVE_SMOKE_FULLY_AUTONOMOUS=false", self.proposal)
        self.assertIn(
            "AGENTTEAMS_PERSISTENT_OR_PRODUCTION_DEPLOYMENT=false",
            self.proposal,
        )
        self.assertIn("COMPETITION_SUBMITTED=false", self.proposal)

    def test_agent_assistance_results_do_not_create_authority(self) -> None:
        reviews = self.projection["agent_assistance_results"]
        self.assertEqual(
            {review["agent"] for review in reviews},
            {"Qwen qwen3.8-max-preview", "Gemini 3.6 Flash", "Jules API"},
        )
        self.assertTrue(
            all(review["authorization_effect"] == "NONE" for review in reviews)
        )
        self.assertEqual(
            {review["agent"]: review["executed"] for review in reviews},
            {
                "Qwen qwen3.8-max-preview": True,
                "Gemini 3.6 Flash": True,
                "Jules API": False,
            },
        )
        self.assertEqual(self.projection["product_recommendation"], "NOT_RECOMMENDED")

    def test_constitution_pin_remains_historical_after_strategy_supersession(self) -> None:
        lock = self.projection["constitution_lock"]
        self.assertFalse(lock["content_matches_observed_main"])
        self.assertTrue(lock["candidate_content_matches_current_branch"])
        self.assertEqual(
            lock["candidate_decision_reference"],
            "TITMAS-AGENT-NATIVE-DISCOVERY-SELF-HEALING-AND-EVOLUTION-D19-V2-1",
        )
        self.assertEqual(lock["adoption_status"], "PENDING_D19_DRAFT_PR_REVIEW")
        self.assertFalse(lock["child_second_constitution_created"])
        self.assertEqual("51e7ab5cb03953b46bf9216ee4d6be430637b8c2f6d8d195b3b48909b470eb02", lock["sha256"])
        self.assertNotEqual(hashlib.sha256(HISTORICAL_CONSTITUTION.read_bytes()).hexdigest(), lock["sha256"])
        self.assertNotEqual(hashlib.sha256(CURRENT_CONSTITUTION.read_bytes()).hexdigest(), lock["sha256"])
        self.assertIn("SUPERSEDED_HISTORICAL_STRATEGY", HISTORICAL_CONSTITUTION.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
