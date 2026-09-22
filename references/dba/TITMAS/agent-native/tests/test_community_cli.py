import importlib.util
import unittest
from pathlib import Path

CLI_PATH = Path(__file__).resolve().parents[1] / "community_cli.py"
SPEC = importlib.util.spec_from_file_location("community_cli", CLI_PATH)
assert SPEC and SPEC.loader
CLI = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLI)


def participant() -> dict:
    return {
        "participant_ref": "PILOT-A",
        "participant_identity_ref": "LOCAL-PILOT-A",
        "provider_ref": "ALIBABA_CLOUD",
        "model_identity": "qwen3.7-max",
        "runtime_identity": "PYTHON_STDLIB_CLIENT",
        "session_identity": "SESSION-A",
        "owner_or_operator_ref": "zhangbin",
        "authority_issuer_ref": "zhangbin",
        "lineage_ref": "QWEN-3.7-MAX",
        "declared_capabilities": ["LOCAL_CATALOG_REASONING"],
        "declared_limitations": ["ADVISORY_ONLY"],
        "assigned_roles": ["AGENT_EXPLORER"],
        "allowed_scope": ["agent-index.json", "TITMAS/agent-native/**"],
        "prohibited_scope": [".git/**", ".github/**"],
        "valid_from": "2026-07-29T00:00:00+08:00",
        "expires_at": "2026-09-30T23:59:59+08:00",
        "revocation_ref": "NONE",
        "evidence_refs": [],
    }


class CommunityCliTests(unittest.TestCase):
    def test_discover_is_deterministic(self):
        need = "trusted multi agent evidence review"
        self.assertEqual(CLI.discover(need), CLI.discover(need))

    def test_eligibility_matches_capability_role_and_scope(self):
        task = CLI._task("AN-01-BLIND-NEED-DISCOVERY")
        self.assertEqual((True, []), CLI.eligible(participant(), task))

    def test_missing_capability_rejected(self):
        value = participant()
        value["declared_capabilities"] = ["UNRELATED"]
        ok, reasons = CLI.eligible(value, CLI._task("AN-01-BLIND-NEED-DISCOVERY"))
        self.assertFalse(ok)
        self.assertIn("CAPABILITY_MISMATCH", reasons)

    def test_self_authorization_rejected(self):
        with self.assertRaisesRegex(CLI.ProtocolRejected, "SELF_AUTHORIZATION"):
            CLI.grant_lease(
                "zhangbin", "AN-01-BLIND-NEED-DISCOVERY", "zhangbin",
                "2026-07-29T12:00:00+08:00", [],
            )

    def test_duplicate_claim_rejected(self):
        original = CLI._participant
        CLI._participant = lambda _ref, _at: participant()
        try:
            with self.assertRaisesRegex(CLI.ProtocolRejected, "DUPLICATE_ACTIVE_CLAIM"):
                CLI.grant_lease(
                    "PILOT-A", "AN-01-BLIND-NEED-DISCOVERY", "zhangbin",
                    "2026-07-29T12:00:00+08:00",
                    ["AN-01-BLIND-NEED-DISCOVERY"],
                )
        finally:
            CLI._participant = original

    def test_contract_cannot_create_authority(self):
        contract = CLI.task_contract("AN-01-BLIND-NEED-DISCOVERY")
        self.assertEqual("NONE", contract["authority_effect"])
        self.assertIn("TASK_CONTRACT_NE_AUTHORITY", contract["non_claims"])

    def test_valid_human_authority_registry_issues_bounded_candidate(self):
        original = CLI._participant
        CLI._participant = lambda _ref, _at: participant()
        try:
            lease = CLI.grant_lease(
                "PILOT-A", "AN-01-BLIND-NEED-DISCOVERY", "zhangbin",
                "2026-07-29T12:00:00+08:00", [],
            )
            self.assertEqual("CLAIMED", lease["status"])
            self.assertEqual(CLI.AUTHORITY_REF, lease["authority_ref"])
        finally:
            CLI._participant = original

    def test_recommendation_calibration_is_reference_only(self):
        result = CLI.calibrate_recommendation("REC-FIT")
        self.assertTrue(result["reference_fixture_only"])
        self.assertEqual("NONE", result["authority_effect"])

    def test_all_adversarial_classes_fail_closed(self):
        self.assertEqual(22, len(CLI.ADVERSARIAL_REJECTION_POLICY))
        for attack, reason in CLI.ADVERSARIAL_REJECTION_POLICY.items():
            decision = CLI.reject_adversarial(attack)
            self.assertEqual("REJECT", decision["decision"])
            self.assertEqual(reason, decision["reason_code"])


if __name__ == "__main__":
    unittest.main()
