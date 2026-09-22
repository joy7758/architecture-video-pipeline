import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
COMMERCIAL = ROOT / "commercial"


class D29CommercialDeliveryFoundationTest(unittest.TestCase):
    def test_required_artifact_groups_are_complete(self):
        expected = {
            "offerings": 4,
            "pricing": 6,
            "contracts": 18,  # 17 drafts plus the package index
            "support": 3,
            "design-partner": 6,
            "onboarding": 6,
            "china": 3,
            "sales": 13,
        }
        for folder, minimum in expected.items():
            files = [path for path in (COMMERCIAL / folder).iterdir() if path.is_file()]
            self.assertGreaterEqual(len(files), minimum, folder)

    def test_machine_artifacts_parse(self):
        paths = [
            COMMERCIAL / "D29-COMMERCIAL-DELIVERY-FOUNDATION-STATUS.json",
            COMMERCIAL / "agent-index.json",
            COMMERCIAL / "pricing" / "COST-MODEL.json",
            COMMERCIAL / "pricing" / "UNIT-ECONOMICS.json",
            COMMERCIAL / "design-partner" / "FEEDBACK-SCHEMA.json",
            COMMERCIAL / "reviews" / "D29-AGENT-CUSTOMER-RECOMMENDATION-REVIEW-v0.1.json",
            ROOT / "architecture" / "titmas-fdo-dtr-pvs0-assets-v0.1.json",
        ]
        for path in paths:
            with path.open(encoding="utf-8") as handle:
                json.load(handle)

    def test_no_false_availability_or_authority(self):
        status = json.loads(
            (COMMERCIAL / "D29-COMMERCIAL-DELIVERY-FOUNDATION-STATUS.json").read_text(encoding="utf-8")
        )
        self.assertFalse(status["commercial_private_pilot_ready"])
        self.assertFalse(status["paid_monitor_pilot_available"])
        self.assertFalse(status["enforce_pilot_available"])
        self.assertTrue(all(value is False for value in status["offering_availability"].values()))
        self.assertTrue(all(value is False for value in status["non_effects"].values()))

    def test_contract_drafts_retain_legal_boundary(self):
        drafts = list((COMMERCIAL / "contracts").glob("*-DRAFT.md"))
        self.assertEqual(len(drafts), 17)
        for path in drafts:
            content = path.read_text(encoding="utf-8")
            self.assertIn("DRAFT_NOT_LEGAL_ADVICE=true", content, path.name)
            self.assertIn("CHINESE_COUNSEL_REVIEW_REQUIRED=true", content, path.name)

    def test_pricing_contains_no_approved_amount(self):
        cost = json.loads((COMMERCIAL / "pricing" / "COST-MODEL.json").read_text(encoding="utf-8"))
        units = json.loads((COMMERCIAL / "pricing" / "UNIT-ECONOMICS.json").read_text(encoding="utf-8"))
        self.assertFalse(cost["public_price"])
        self.assertFalse(cost["payment_authorized"])
        self.assertTrue(units["status"].startswith("NOT_ASSESSED"))

    def test_fdo_auxiliary_line_cannot_be_promoted(self):
        data = json.loads(
            (ROOT / "architecture" / "titmas-fdo-dtr-pvs0-assets-v0.1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(data["portfolio_role"], "PUBLIC_EVIDENCE_AUXILIARY_LINE")
        self.assertTrue(all(value is False for value in data["boundaries"].values()))

    def test_agent_customer_review_retains_not_recommended(self):
        review = json.loads(
            (COMMERCIAL / "reviews" / "D29-AGENT-CUSTOMER-RECOMMENDATION-REVIEW-v0.1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(review["recommendation"], "NOT_RECOMMENDED")
        self.assertFalse(review["authority"])
        self.assertEqual(review["decision_effect"], "NONE")


if __name__ == "__main__":
    unittest.main()
