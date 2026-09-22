#!/usr/bin/env python3
"""Deterministic community contribution-grounding matrix."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


DBA_ROOT = Path(__file__).resolve().parents[3]
GROUNDING_ROOT = (
    DBA_ROOT
    / "TITMAS"
    / "conformance"
    / "grounding"
)
sys.path.insert(0, str(GROUNDING_ROOT))


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, GROUNDING_ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


RESOLVER = load_module("local_resource_resolver", "local_resource_resolver.py")
PREFLIGHT = load_module("candidate_preflight", "candidate_preflight.py")
SOURCE = "ba6d51f60c12f1ac954dd67947451821fd5a3eb6"


def produced_candidate(
    reference: str = "architecture/stack-specification.md",
    reference_type: str = "CURRENT_SNAPSHOT_RESOURCE",
    candidate_files: dict | None = None,
) -> dict:
    files = candidate_files or {
        "candidate.json": {
            "maturity": "Development",
            "limitations": ["DETERMINISTIC_FIXTURE_ONLY"],
        }
    }
    return {
        "candidate_status": "CANDIDATE_PRODUCED",
        "finding_disposition": "VALID_RELEVANT_ACTIONABLE",
        "candidate_files": files,
        "reference_claims": [
            {
                "reference": reference,
                "reference_type": reference_type,
                "required_for_candidate": True,
                "expected_resolution_status": "RESOLVED",
                "justification": "Exact deterministic fixture reference.",
            }
        ],
        "created_resources": sorted(files),
        "modified_resources": [],
        "abstention_reason": "NOT_APPLICABLE",
        "rationale": "Deterministic fixture candidate.",
        "limitations": ["DETERMINISTIC_FIXTURE_ONLY"],
        "validation_plan": ["RUN_PREFLIGHT", "RUN_FINAL_CONFORMANCE"],
    }


def run_preflight(candidate: dict, source: str = SOURCE) -> dict:
    return PREFLIGHT.run_candidate_preflight(
        candidate=candidate,
        dba_root=DBA_ROOT,
        source_revision=source,
        allowed_source_revision=SOURCE,
        allowed_roots=[
            "agent-index.json",
            "architecture/stack-specification.md",
            "TITMAS",
            "architecture",
            "generated",
        ],
        allowed_candidate_files={
            "candidate.json",
            "other.json",
            "generated/new.json",
            "community-surface.variant-b.json",
        },
    )


def passing_reviewer(preflight: dict) -> dict:
    receipt_ids = [
        item["resolution_id"]
        for item in preflight["resolution_receipts"]
        if item["resolution_phase"] == "AFTER_CANDIDATE_APPLY"
        and item["required_for_candidate"]
    ]
    verified = [
        item["reference"]
        for item in preflight["resolution_receipts"]
        if item["resolution_phase"] == "AFTER_CANDIDATE_APPLY"
        and item["status"] == "RESOLVED"
    ]
    return {
        "verdict": "PASS",
        "caught_issues": [],
        "semantic_elevation_detected": False,
        "harmful_candidate": False,
        "required_corrections": [],
        "limitations": ["REVIEW_NE_DECISION"],
        "reviewed_artifact_refs": [preflight["candidate_ref"]],
        "preflight_result_ref": preflight["preflight_id"],
        "checks_performed": [
            "READ_PREFLIGHT_RESULT",
            "CHECK_REQUIRED_RESOLUTION_RECEIPTS",
        ],
        "verified_resource_refs": verified,
        "resolution_receipt_refs": receipt_ids,
        "unverified_claims": [],
        "abstention_reason": "NOT_APPLICABLE",
    }


class CandidateGroundingMatrix(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_root = Path(tempfile.mkdtemp(prefix="titmas-cg-tests-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_root)

    def resolver(self, candidate_root: Path | None = None, source: str = SOURCE):
        return RESOLVER.LocalResourceResolver(
            dba_root=DBA_ROOT,
            source_revision=source,
            allowed_source_revision=SOURCE,
            allowed_roots=[
                "agent-index.json",
                "architecture/stack-specification.md",
                "TITMAS",
                "architecture",
                "generated",
            ],
            candidate_root=candidate_root,
            created_at="2026-07-29T00:00:00+08:00",
        )

    def test_cg01_existing_resource_resolved(self):
        receipt = self.resolver().resolve(
            "architecture/stack-specification.md",
            "CURRENT_SNAPSHOT_RESOURCE",
            True,
        )
        self.assertEqual("RESOLVED", receipt["status"])

    def test_cg02_missing_resource_not_found(self):
        receipt = self.resolver().resolve(
            "TITMAS/does-not-exist.json", "MACHINE_SURFACE_REFERENCE", True
        )
        self.assertEqual("NOT_FOUND", receipt["status"])

    def test_cg03_path_escape_out_of_scope(self):
        receipt = self.resolver().resolve(
            "../private.txt", "CURRENT_SNAPSHOT_RESOURCE", True
        )
        self.assertEqual("OUT_OF_SCOPE", receipt["status"])

    def test_cg04_absolute_path_invalid(self):
        receipt = self.resolver().resolve(
            "/etc/passwd", "CURRENT_SNAPSHOT_RESOURCE", True
        )
        self.assertEqual("INVALID_REFERENCE", receipt["status"])

    def test_cg05_multiple_exact_identifiers_ambiguous(self):
        for index in (1, 2):
            path = self.temp_root / f"registry-{index}.json"
            path.write_text(
                json.dumps({"registry_id": "CG-AMBIGUOUS-ID"}),
                encoding="utf-8",
            )
        receipt = self.resolver(self.temp_root).resolve(
            "CG-AMBIGUOUS-ID", "REGISTRY_REFERENCE", True
        )
        self.assertEqual("AMBIGUOUS", receipt["status"])

    def test_cg06_candidate_created_resource_resolved_after_apply(self):
        candidate = produced_candidate(
            "generated/new.json",
            "CANDIDATE_CREATED_RESOURCE",
            {"generated/new.json": {"id": "CG-06"}},
        )
        result = run_preflight(candidate)
        self.assertEqual("PASS", result["status"])
        self.assertEqual(
            ["NOT_FOUND", "RESOLVED"],
            [
                item["status"]
                for item in result["resolution_receipts"]
                if item["reference"] == "generated/new.json"
            ],
        )

    def test_cg07_claimed_creation_without_patch_not_found(self):
        candidate = produced_candidate(
            "generated/new.json",
            "CANDIDATE_CREATED_RESOURCE",
            {"other.json": {"id": "CG-07"}},
        )
        result = run_preflight(candidate)
        self.assertEqual("REVISION_REQUIRED", result["status"])
        self.assertIn(
            "generated/new.json", result["unresolved_required_references"]
        )

    def test_cg08_missing_schema_reference_not_found(self):
        receipt = self.resolver().resolve(
            "TITMAS/agent-native/schemas/missing.schema.json",
            "SCHEMA_REFERENCE",
            True,
        )
        self.assertEqual("NOT_FOUND", receipt["status"])

    def test_cg09_missing_registry_id_not_found(self):
        receipt = self.resolver().resolve(
            "CG-REGISTRY-ID-DOES-NOT-EXIST", "REGISTRY_REFERENCE", True
        )
        self.assertEqual("NOT_FOUND", receipt["status"])

    def test_cg10_contributor_abstention_passes(self):
        candidate = {
            "candidate_status": "ABSTAINED_NO_VALID_TARGET",
            "finding_disposition": "INSUFFICIENT_CONTEXT",
            "candidate_files": {},
            "reference_claims": [],
            "created_resources": [],
            "modified_resources": [],
            "abstention_reason": "NO_VALID_TARGET_RESOLVED",
            "rationale": "No exact target can be grounded.",
            "limitations": ["NO_CANDIDATE_CREATED"],
            "validation_plan": [],
        }
        result = run_preflight(candidate)
        self.assertEqual("PASS", result["status"])
        self.assertEqual("NOT_APPLICABLE", result["candidate_apply_status"])

    def test_cg11_guessed_candidate_path_rejected(self):
        result = run_preflight(
            produced_candidate(
                "TITMAS/community/does-not-exist.json",
                "MACHINE_SURFACE_REFERENCE",
            )
        )
        self.assertEqual("REVISION_REQUIRED", result["status"])
        self.assertIn("REQUIRED_REFERENCE_UNRESOLVED", result["errors"])

    def test_cg12_reviewer_pass_with_failed_preflight_rejected(self):
        preflight = run_preflight(
            produced_candidate(
                "TITMAS/community/does-not-exist.json",
                "MACHINE_SURFACE_REFERENCE",
            )
        )
        with self.assertRaisesRegex(
            PREFLIGHT.GroundingContractError,
            "REVIEW_PASS_WITH_PREFLIGHT_NOT_PASS",
        ):
            PREFLIGHT.validate_reviewer_assessment_v11(
                passing_reviewer(preflight), preflight
            )

    def test_cg13_reviewer_pass_with_unresolved_reference_rejected(self):
        preflight = run_preflight(produced_candidate())
        preflight["unresolved_required_references"] = ["still-missing"]
        with self.assertRaisesRegex(
            PREFLIGHT.GroundingContractError,
            "REVIEW_PASS_WITH_UNRESOLVED_REFERENCE",
        ):
            PREFLIGHT.validate_reviewer_assessment_v11(
                passing_reviewer(preflight), preflight
            )

    def test_cg14_reviewer_abstention_passes(self):
        preflight = run_preflight(produced_candidate())
        review = passing_reviewer(preflight)
        review.update(
            {
                "verdict": "ABSTAIN_INSUFFICIENT_EVIDENCE",
                "abstention_reason": "INDEPENDENT_RESOURCE_CHECK_UNAVAILABLE",
            }
        )
        PREFLIGHT.validate_reviewer_assessment_v11(review, preflight)

    def test_cg15_reviewer_pass_references_resolution_receipt(self):
        preflight = run_preflight(produced_candidate())
        review = passing_reviewer(preflight)
        PREFLIGHT.validate_reviewer_assessment_v11(review, preflight)
        self.assertTrue(review["resolution_receipt_refs"])

    def test_cg17_revision_repairs_path_and_repasses_full_preflight(self):
        sequence = PREFLIGHT.run_preflight_with_single_revision(
            initial_candidate=produced_candidate(
                "TITMAS/community/does-not-exist.json",
                "MACHINE_SURFACE_REFERENCE",
            ),
            revision_candidate=produced_candidate(),
            dba_root=DBA_ROOT,
            source_revision=SOURCE,
            allowed_source_revision=SOURCE,
            allowed_roots=[
                "agent-index.json",
                "TITMAS",
                "architecture",
                "generated",
            ],
            allowed_candidate_files={
                "candidate.json",
                "other.json",
                "generated/new.json",
                "community-surface.variant-b.json",
            },
        )
        self.assertEqual("PASS", sequence["status"])
        self.assertEqual(1, sequence["revision_count"])
        self.assertEqual(
            ["REVISION_REQUIRED", "PASS"],
            [item["status"] for item in sequence["attempts"]],
        )
        self.assertTrue(sequence["review_stage_allowed"])

    def test_cg18_final_conformance_failure_remains_fail_closed(self):
        preflight = run_preflight(produced_candidate())
        review = passing_reviewer(preflight)
        result = PREFLIGHT.complete_candidate_validation(
            preflight,
            review,
            {"status": "FAIL", "errors": ["LATE_INCONSISTENCY"]},
        )
        self.assertEqual("FAIL_CLOSED", result["status"])
        self.assertEqual(
            "FINAL_CONFORMANCE_FAILED_AFTER_INCREMENTAL_PASS",
            result["reason_code"],
        )

    def test_cg19_source_revision_drift_not_assessed(self):
        receipt = self.resolver(source="0" * 40).resolve(
            "agent-index.json", "CURRENT_SNAPSHOT_RESOURCE", True
        )
        self.assertEqual("NOT_ASSESSED", receipt["status"])
        result = run_preflight(produced_candidate(), source="0" * 40)
        self.assertEqual("REJECTED", result["status"])

    def test_cg20_resource_receipt_truth_or_authority_claim_rejected(self):
        candidate = produced_candidate()
        candidate["rationale"] = "RESOURCE_RESOLUTION_RECEIPT_IS_TRUTH=true"
        result = run_preflight(candidate)
        self.assertEqual("REJECTED", result["status"])
        self.assertIn("SEMANTIC_ELEVATION_PROHIBITED", result["errors"])


if __name__ == "__main__":
    unittest.main()
