import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
PORTFOLIO_RECORD = (
    REPOSITORY_ROOT
    / "TITMAS"
    / "specifications"
    / "portfolio"
    / "media-evidence.json"
)
PORTFOLIO_DOCUMENT = REPOSITORY_ROOT / "PROJECT-PORTFOLIO.md"
PROGRAM_STATUS = REPOSITORY_ROOT / "PROGRAM-STATUS.md"
DECISION_QUEUE = REPOSITORY_ROOT / "DECISION-QUEUE.md"
PROPOSAL = (
    REPOSITORY_ROOT
    / "TITMAS"
    / "specifications"
    / "proposals"
    / "titmas-media-evidence-profile-admission-v0.1.md"
)
DECISION = (
    REPOSITORY_ROOT
    / "TITMAS"
    / "specifications"
    / "decisions"
    / "titmas-media-evidence-portfolio-admission-decision-v0.1.md"
)


class MediaEvidencePortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(PORTFOLIO_RECORD.read_text(encoding="utf-8"))

    def test_portfolio_admission_is_explicit_and_bounded(self):
        self.assertTrue(self.record["portfolio_admission"])
        self.assertEqual("ADJACENT_CANDIDATE", self.record["portfolio_classification"])
        self.assertEqual(
            "APPLICATION_PROFILE_AND_REFERENCE_IMPLEMENTATION_CANDIDATE",
            self.record["architecture_classification"],
        )
        self.assertEqual("ACCEPTED_BOUNDED", self.record["architecture_admission"])

    def test_canonical_implementation_snapshot_is_pinned(self):
        self.assertEqual("v0.1.0", self.record["implementation_version"])
        self.assertEqual(
            "7eac452f66a2b7de525543f80b9a7cf1465ef9a1",
            self.record["implementation_tag_commit"],
        )
        self.assertEqual(
            "6ded0dd0d81f8a9fc0fe029f96906cc7bc43f446",
            self.record["governance_source_revision"],
        )
        self.assertEqual(
            "joy7758/titmas-media-guard", self.record["canonical_repository"]
        )
        self.assertEqual(14, self.record["freshness_maximum_age_days"])

    def test_no_silent_authority_or_maturity_elevation(self):
        for field in (
            "dbos_mapping_authorized",
            "core_component",
            "standard",
            "production_ready",
            "external_adoption",
        ):
            self.assertIs(self.record[field], False, field)

    def test_human_and_machine_surfaces_agree_on_admission(self):
        portfolio_text = PORTFOLIO_DOCUMENT.read_text(encoding="utf-8")
        status_text = PROGRAM_STATUS.read_text(encoding="utf-8")
        queue_text = DECISION_QUEUE.read_text(encoding="utf-8")
        proposal_text = PROPOSAL.read_text(encoding="utf-8")

        self.assertIn("`ADMITTED_ADJACENT_CANDIDATE`", portfolio_text)
        self.assertIn("MEDIA_EVIDENCE_PORTFOLIO_ADMISSION_GRANTED=true", status_text)
        self.assertIn("MEDIA_EVIDENCE_DBOS_MAPPING_AUTHORIZED=false", status_text)
        self.assertIn("CLOSED_ACCEPTED_AS_ADJACENT_CANDIDATE", queue_text)
        self.assertIn("review_result: ACCEPTED_BOUNDED", proposal_text)
        self.assertIn(
            "decision_result: ADMITTED_AS_ADJACENT_CANDIDATE", proposal_text
        )
        self.assertTrue(DECISION.is_file())

    def test_gate_states_preserve_unassessed_and_unauthorized_work(self):
        self.assertEqual(
            {
                "G0": "PASS_ADMITTED_AS_ADJACENT_CANDIDATE",
                "G1": "PASS",
                "G2": "PASS_BOUNDARY_ONLY_MAPPING_NOT_AUTHORIZED",
                "G3": "NOT_ASSESSED",
                "G4": "NOT_ASSESSED",
                "G5": "NOT_AUTHORIZED",
                "G6": "NOT_EXECUTED",
                "G7": "NOT_ASSESSED",
                "G8": "NOT_RELEASED_NOT_ADOPTED",
            },
            self.record["gates"],
        )


if __name__ == "__main__":
    unittest.main()
