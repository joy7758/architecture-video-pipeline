import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


PRIVATE_ROOT = Path(__file__).resolve().parents[1]
TITMAS_ROOT = PRIVATE_ROOT.parent
DBA_ROOT = TITMAS_ROOT.parent
MODULE_PATH = PRIVATE_ROOT / "build_public_surface_candidate.py"
SPEC = importlib.util.spec_from_file_location("public_surface_builder_boundary", MODULE_PATH)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class PrivateCommercializationBoundaryTests(unittest.TestCase):
    def test_source_classification_registry_is_default_deny(self):
        registry = json.loads(
            (PRIVATE_ROOT / "source-classification-registry.json").read_text(encoding="utf-8")
        )
        self.assertEqual("UNCLASSIFIED", registry["default_classification"])
        self.assertFalse(registry["unclassified_export_allowed"])
        self.assertTrue(registry["publication_policy"]["allowlist_only_export"])
        self.assertTrue(registry["publication_policy"]["publication_by_reconstruction"])
        self.assertTrue(all(not item["export_allowed"] for item in registry["entries"]))

    def test_public_candidates_are_pending_all_reviews(self):
        registry = json.loads(
            (PRIVATE_ROOT / "source-classification-registry.json").read_text(encoding="utf-8")
        )
        public = {
            "PUBLIC_PROTOCOL",
            "PUBLIC_DOCUMENTATION",
            "PUBLIC_SYNTHETIC_EXAMPLE",
            "PUBLIC_CLIENT_STUB_CANDIDATE",
        }
        candidates = [item for item in registry["entries"] if item["classification"] in public]
        self.assertGreaterEqual(len(candidates), 1)
        for item in candidates:
            self.assertEqual("PENDING", item["legal_review_status"])
            self.assertEqual("PENDING", item["commercial_review_status"])
            self.assertEqual("PENDING", item["security_review_status"])
            self.assertEqual("PENDING", item["license_status"])
            self.assertFalse(item["export_allowed"])

    def test_canonical_registry_cannot_build_an_export(self):
        registry = PRIVATE_ROOT / "source-classification-registry.json"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "candidate"
            with self.assertRaisesRegex(BUILDER.ExportBoundaryError, "NO_APPROVED_EXPORT_ENTRIES"):
                BUILDER.build_candidate(registry, DBA_ROOT, output)
            self.assertFalse(output.exists())

    def test_exposure_inventory_has_no_secret_classification(self):
        inventory = json.loads(
            (PRIVATE_ROOT / "public-exposure-inventory.json").read_text(encoding="utf-8")
        )
        self.assertEqual(0, inventory["secret_findings"])
        self.assertFalse(inventory["secret_rotation_required"])
        self.assertTrue(inventory["assessment_basis"]["prior_public_content_cannot_be_retracted"])
        self.assertTrue(inventory["assessment_basis"]["potentially_public_content_may_have_been_copied"])
        self.assertFalse(inventory["assessment_basis"]["confirmed_third_party_copy"])
        self.assertNotIn(
            "L4_SECRET_NEVER_EXPORT",
            {item["classification"] for item in inventory["entries"]},
        )
        for item in inventory["entries"]:
            self.assertEqual(
                {
                    "path",
                    "blob_sha",
                    "last_potentially_public_commit",
                    "classification",
                    "commercial_impact",
                    "recommended_action",
                },
                set(item),
            )

    def test_private_customer_allowlist_contains_no_core_code_or_tests(self):
        bundle = TITMAS_ROOT / "private-customer-evaluation"
        files = {path.name for path in bundle.iterdir() if path.is_file()}
        self.assertEqual(
            {
                "README.md",
                "agent-service-discovery.json",
                "api-contract.json",
                "synthetic-request.json",
                "synthetic-response.json",
                "error-codes.json",
                "black-box-validation.md",
                "evaluation-task.md",
                "human-accountability.md",
            },
            files,
        )
        self.assertFalse(any(path.endswith(".py") for path in files))
        self.assertFalse(any("test" in Path(path).name.lower() for path in files))
        self.assertTrue((bundle / "gateway" / "service.py").is_file())

    def test_private_customer_bundle_declares_no_endpoint_or_release(self):
        discovery = json.loads(
            (TITMAS_ROOT / "private-customer-evaluation" / "agent-service-discovery.json")
            .read_text(encoding="utf-8")
        )
        contract = json.loads(
            (TITMAS_ROOT / "private-customer-evaluation" / "api-contract.json")
            .read_text(encoding="utf-8")
        )
        self.assertFalse(discovery["real_endpoint_available"])
        self.assertFalse(discovery["real_model_call_authorized"])
        self.assertTrue(discovery["local_ephemeral_gateway_implemented"])
        self.assertTrue(contract["endpoint_implemented"])
        self.assertFalse(contract["endpoint_deployed"])
        self.assertTrue(contract["loopback_only"])
        self.assertFalse(contract["core_source_returned"])

    def test_commercial_drafts_are_nonbinding_and_inactive(self):
        root = TITMAS_ROOT / "commercialization"
        documents = list(root.glob("*.md"))
        self.assertEqual(6, len(documents))
        for path in documents:
            text = path.read_text(encoding="utf-8")
            self.assertIn("DRAFT_FOR_LEGAL_REVIEW=true", text)
            self.assertIn("NON_BINDING=true", text)
            self.assertIn("AGREEMENT_ACTIVE=false", text)

    def test_d02_remains_undecided_and_zero_call(self):
        text = (
            DBA_ROOT
            / "TITMAS-FIRST-PRIVATE-CONTROLLED-AGENT-CUSTOMER-CYCLE-D02-READINESS-v0.1.md"
        ).read_text(encoding="utf-8")
        self.assertIn("DECISION=UNDECIDED", text)
        self.assertIn("D02_PRIVATE_AGENT_CUSTOMER_CYCLE_AUTHORIZED=false", text)
        self.assertIn("REAL_MODEL_CALL_COUNT=0", text)
        self.assertIn("REAL_PROVIDER_CALL_COUNT=0", text)


if __name__ == "__main__":
    unittest.main()
