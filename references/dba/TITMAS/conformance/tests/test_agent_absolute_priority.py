import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class AgentAbsolutePriorityTests(unittest.TestCase):
    def test_machine_priority_preserves_human_authority(self):
        status = json.loads(
            (ROOT / "TITMAS/community/community-status.json").read_text(
                encoding="utf-8"
            )
        )
        priority = status["program_priority"]
        self.assertEqual(priority["primary_operational_customer"], "AI_AGENT")
        self.assertTrue(priority["agent_absolute_priority"])
        self.assertTrue(priority["machine_interface_precedes_human_interface"])
        self.assertFalse(priority["agent_priority_grants_authority"])
        self.assertTrue(priority["human_irreversible_authority_retained"])

    def test_e01_is_history_not_a_stage5_7_gate(self):
        status = json.loads(
            (ROOT / "TITMAS/community/community-status.json").read_text(
                encoding="utf-8"
            )
        )
        validation = status["current_validation"]
        self.assertEqual(
            validation["stage"],
            "TITMAS_STAGE_5_7_AGENT_NATIVE_SELECTION_AND_ROI_BENCHMARK",
        )
        self.assertEqual(
            validation["e01_classification"],
            "LEGACY_OPTIONAL_HUMAN_COMPATIBILITY_OBSERVATION",
        )
        self.assertFalse(validation["e01_is_primary_validation"])
        self.assertFalse(validation["e01_is_program_gate"])
        self.assertFalse(validation["human_trial_required_for_next_stage"])

    def test_constitution_keeps_agent_priority_separate_from_authority(self):
        charter = (
            ROOT / "architecture/titmas-architecture-charter-v1.0.md"
        ).read_text(encoding="utf-8")
        decision = (
            ROOT / "architecture/ADR-035-titmas-agent-absolute-priority.md"
        ).read_text(encoding="utf-8")
        for document in (charter, decision):
            self.assertIn("TITMAS_AGENT_ABSOLUTE_PRIORITY=true", document)
            self.assertIn("AGENT_PRIORITY_NE_AGENT_AUTHORITY=true", document)
        self.assertIn("HUMAN_ACCOUNTABILITY_REMOVED=false", decision)


if __name__ == "__main__":
    unittest.main()
