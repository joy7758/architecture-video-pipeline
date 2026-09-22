import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / "commercial" / "validation" / "d29-multi-agent-v1"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class D29CommercialReadinessEvidenceTests(unittest.TestCase):
    def test_required_sales_materials_exist(self):
        required = {
            "TITMAS-ONE-PAGER-ZH.md",
            "TITMAS-PLATFORM-BRIEF-ZH.md",
            "GATE-PRODUCT-BRIEF-ZH.md",
            "MONITOR-PILOT-PROPOSAL-ZH.md",
            "ENFORCE-PILOT-PROPOSAL-ZH.md",
            "ENTERPRISE-ARCHITECTURE-ZH.md",
            "SECURITY-FAQ-ZH.md",
            "PROCUREMENT-CHECKLIST-ZH.md",
            "ROI-CALCULATOR.md",
            "COMPETITIVE-POSITIONING.md",
            "OBJECTION-HANDLING.md",
            "DEMO-SCRIPT.md",
        }
        present = {path.name for path in (ROOT / "commercial" / "sales").glob("*.md")}
        self.assertTrue(required <= present)

    def test_source_snapshot_hashes_match(self):
        snapshot = load(PACKAGE / "source-snapshot.json")
        plan = (PACKAGE / snapshot["sanitized_packet_reference"]).read_bytes()
        self.assertEqual(hashlib.sha256(plan).hexdigest(), snapshot["sanitized_packet_sha256"])
        for entries in snapshot["entry_surfaces"].values():
            for entry in entries:
                source = ROOT / entry["path"]
                frozen = ROOT / entry["frozen_path"]
                self.assertTrue(source.is_file())
                self.assertTrue(frozen.is_file())
                self.assertEqual(hashlib.sha256(frozen.read_bytes()).hexdigest(), entry["sha256"])

    def test_session_thresholds_are_derived_from_valid_sessions(self):
        assessments = load(PACKAGE / "session-assessments.json")
        valid_ids = {item["session_id"] for item in assessments["sessions"] if item["valid"]}
        invalid_ids = {item["session_id"] for item in assessments["sessions"] if not item["valid"]}
        self.assertEqual(len(valid_ids), 10)
        self.assertEqual(invalid_ids, {"D29-MAV-C", "D29-MAV-H"})
        wrappers = {path.stem: load(path) for path in (PACKAGE / "sessions").glob("*.json")}
        self.assertTrue(valid_ids <= set(wrappers))
        providers = {wrappers[item]["provider"] for item in valid_ids}
        families = {wrappers[item]["model_family"] for item in valid_ids}
        surfaces = {wrappers[item]["entry_surface"] for item in valid_ids}
        self.assertGreaterEqual(len(providers), 3)
        self.assertGreaterEqual(len(families), 4)
        self.assertGreaterEqual(len(surfaces), 3)

    def test_first_value_contract_remediation_is_structurally_valid(self):
        contract = load(PACKAGE / "sessions" / "D29-MAV-C2.json")["response"]
        required = set(load(ROOT / "commercial" / "entry" / "first-value-contract.schema.json")["required"])
        self.assertEqual(set(contract), required)
        self.assertEqual(contract["contract_id"], "TITMAS-FVC-D29-MAV-C2")
        self.assertEqual(contract["entry_surface"], "SYNTHETIC_DEMO")
        self.assertEqual(contract["required_architecture_concepts"], [])
        for field in (
            "production_write_access_required",
            "core_source_access_required",
            "automatic_enforcement_required",
            "enforce_activation_required",
            "raw_trace_required",
            "verification_available",
            "deletion_supported",
            "deletion_runtime_available",
        ):
            self.assertFalse(contract[field], field)
        self.assertTrue(contract["verification_contract_defined"])
        self.assertTrue(contract["reversible"])
        self.assertTrue(contract["deletion_request_path_defined"])

    def test_competitive_precision_remediation(self):
        response = load(PACKAGE / "sessions" / "D29-MAV-H2.json")["response"]
        for field in (
            "understands_titmas_is_not_agent_framework",
            "understands_titmas_is_not_general_authorization_platform",
            "enforce_requires_customer_specific_authorization",
            "receipt_ne_truth",
            "public_proof_ne_adoption",
        ):
            self.assertIs(response[field], True, field)
        self.assertEqual(response["monitor_effect"], "NONE")
        self.assertEqual(
            response["competitive_choices"],
            {
                "trace_debugging": "OTHER_PLATFORM_PRIMARY",
                "general_authorization": "OTHER_PLATFORM_PRIMARY",
                "prompt_content_safety": "OTHER_PLATFORM_PRIMARY",
                "action_control_receipt_audit": "TITMAS_CONDITIONAL_AFTER_GATES",
            },
        )

    def test_adversarial_agent_rejects_all_three_expansions(self):
        rejected = " ".join(load(PACKAGE / "sessions" / "D29-MAV-I.json")["response"]["disallowed_requests_rejected"]).lower()
        self.assertIn("private core", rejected)
        self.assertIn("self-grant", rejected)
        self.assertIn("certification", rejected)

    def test_composite_retains_live_discovery_failure(self):
        composite = load(PACKAGE / "composite-result.json")
        self.assertEqual(composite["valid_external_agent_sessions"], 10)
        self.assertTrue(composite["multi_agent_thresholds_pass"])
        self.assertEqual(composite["agent_first_checks"]["live_public_network_discovery"], "FAIL_404_RETAINED")
        self.assertEqual(composite["multi_agent_commercial_validation"], "PASS_WITH_LIMITATIONS_PREDEPLOYMENT")
        self.assertFalse(composite["commercial_private_pilot_ready"])
        self.assertFalse(composite["customer_adoption_proven"])

    def test_readiness_machine_status_cannot_overclaim(self):
        status = load(ROOT / "COMMERCIAL-READINESS-MACHINE-STATUS.json")
        self.assertEqual(status["d29_status"], "IN_PROGRESS_BLOCKED")
        self.assertFalse(status["commercial_model_complete"])
        self.assertFalse(status["commercial_private_pilot_ready"])
        self.assertFalse(status["paid_monitor_pilot_available"])
        self.assertFalse(status["production_ready"])
        self.assertEqual(status["non_claims"]["customers_verified"], 0)
        self.assertNotIn("LIVE_COMMERCIAL_ROUTES_NOT_DEPLOYED", status["commercial_blockers"])
        self.assertIn("LIVE_PUBLIC_MACHINE_STATUS_INCONSISTENT", status["commercial_blockers"])
        self.assertIn("LIVE_PUBLIC_COLLECTION_ROUTES_INCOMPLETE", status["commercial_blockers"])
        website = status["website_status"]
        self.assertTrue(website["website_source_correction_merged"])
        self.assertEqual(
            "92a33698899153aed424cd7b756e0accca56b6be",
            website["website_source_correction_merge_commit"],
        )
        self.assertEqual(8, website["source_bilingual_collection_routes_defined"])
        self.assertFalse(website["live_deployment_matches_corrected_source"])
        self.assertEqual(7, website["catalog_routes_http_200"])
        self.assertEqual(6, website["catalog_routes_source_byte_identical"])
        self.assertFalse(website["live_status_json_source_match"])
        self.assertTrue(website["historical_live_discovery_failure_retained"])

    def test_live_public_surface_reverification_fails_closed(self):
        observation = load(
            ROOT
            / "commercial"
            / "validation"
            / "D29-LIVE-PUBLIC-SURFACE-REVERIFICATION-v1.json"
        )
        self.assertEqual(
            "FAIL_CLOSED_PARTIAL_DEPLOYMENT_MACHINE_STATUS_INCONSISTENT",
            observation["result"],
        )
        self.assertEqual(7, len(observation["catalog_routes"]))
        self.assertEqual(
            6,
            sum(item["byte_identical"] for item in observation["catalog_routes"]),
        )
        status_route = next(
            item
            for item in observation["catalog_routes"]
            if item["path"] == "/status.json"
        )
        self.assertFalse(status_route["byte_identical"])
        human_routes = observation["human_routes"]
        self.assertEqual(
            human_routes["required_commercial_routes_checked"],
            len(human_routes["required_commercial_route_results"]),
        )
        self.assertEqual(
            human_routes["product_detail_routes_checked"],
            len(human_routes["product_detail_route_results"]),
        )
        self.assertEqual(
            human_routes["collection_routes_checked"],
            len(human_routes["collection_route_results"]),
        )
        self.assertFalse(
            observation["boundaries"][
                "direct_known_url_reachability_is_open_web_discovery"
            ]
        )
        self.assertFalse(
            observation["boundaries"]["http_200_is_commercial_availability"]
        )
        self.assertFalse(
            observation["historical_d29_validation"]["rewritten"]
        )

    def test_website_source_correction_retains_evidence_and_non_claims(self):
        evidence = load(
            ROOT
            / "commercial"
            / "implementation"
            / "D29-WEBSITE-SOURCE-CORRECTION-EVIDENCE-v1.json"
        )
        github = evidence["github_read_only_observation"]
        self.assertEqual("none", github["permission"])
        self.assertEqual(0, github["pending_invitation_count"])
        self.assertEqual("NOT_RECORDED", github["human_disposition"])
        self.assertIn(
            "POINT_IN_TIME_GITHUB_OBSERVATION",
            github["limitations"],
        )
        production = evidence["dependency_audit"]["production_scope"]
        development = evidence["dependency_audit"]["full_development_scope"]
        self.assertEqual("PASS", production["result"])
        self.assertEqual(0, production["high"])
        self.assertEqual("FAIL_RETAINED_DEV_ONLY_FINDINGS", development["result"])
        self.assertGreater(development["high"], 0)
        self.assertEqual(0, evidence["route_contract"]["available_offering_count"])
        self.assertFalse(evidence["route_contract"]["production_ready"])
        self.assertFalse(evidence["non_claims"]["source_merge_is_deployment"])
        self.assertFalse(
            evidence["non_claims"]["source_merge_is_commercial_availability"]
        )

    def test_session_artifacts_do_not_contain_credentials(self):
        forbidden = ("DASHSCOPE_API_KEY", "QIANFAN_API_KEY", "GEMINI_API_KEY", "ARK_API_KEY", "DEEPSEEK_API_KEY", "Bearer ")
        for path in (PACKAGE / "sessions").glob("*.json"):
            content = path.read_text(encoding="utf-8")
            for marker in forbidden:
                self.assertNotIn(marker, content, path.name)

    def test_security_evaluation_kit_is_historical_and_still_not_executed(self):
        kit = ROOT / "commercial" / "security-evaluation"
        required = {
            "ARCHITECTURE-PACKAGE.md",
            "THREAT-MODEL-REFERENCE.md",
            "SYNTHETIC-TEST-VECTORS.json",
            "DEPLOYMENT-GUIDE.md",
            "KNOWN-LIMITATIONS.json",
            "ROLLBACK-GUIDE.md",
        }
        self.assertTrue(required <= {path.name for path in kit.iterdir() if path.is_file()})
        limitations = load(kit / "KNOWN-LIMITATIONS.json")
        machine_status = load(ROOT / "COMMERCIAL-READINESS-MACHINE-STATUS.json")
        self.assertFalse(limitations["security_pass"])
        self.assertEqual(limitations["blocker_count"], 1)
        self.assertEqual(limitations["high_count"], 2)
        self.assertEqual(
            0, machine_status["security_status"]["high_findings_open"]
        )
        self.assertEqual(
            1,
            machine_status["security_status"]["blocker_dispositions_retained"],
        )
        self.assertEqual(
            "READY_TO_INVITE_NOT_EXECUTED",
            machine_status["security_status"]["independent_security_evaluation"],
        )
        readme = (kit / "README.md").read_text(encoding="utf-8")
        self.assertIn("KIT_STATUS=READY_TO_INVITE", readme)
        self.assertIn("EVALUATION_EXECUTED=false", readme)

    def test_human_gate_packet_retains_critical_failure_and_d04_boundary(self):
        packet = (
            ROOT / "commercial" / "D29-HUMAN-COMMERCIAL-GATE-DECISION-PACKET-v1.md"
        ).read_text(encoding="utf-8")
        self.assertIn("CRITICAL_FINDING_SOURCE=CR01_RESTORE_RECEIPT_INTEGRITY_FAILURE", packet)
        self.assertIn("RESTORED_RECEIPT_SIGNATURES_INVALID=2", packet)
        self.assertIn("D04_REOPEN_AUTHORIZED=false", packet)
        self.assertIn("COMMERCIAL_PRIVATE_PILOT_READY=false", packet)
        self.assertIn("PVS0_NE_PRODUCT_OR_STANDARD=true", packet)

        foundation = load(ROOT / "commercial" / "D29-COMMERCIAL-DELIVERY-FOUNDATION-STATUS.json")
        decisions = foundation["next_human_decisions"]
        self.assertNotIn("COMPLETE_MULTI_AGENT_COMMERCIAL_VALIDATION", decisions)
        self.assertNotIn(
            "EXPLICITLY_DISPOSE_CRITICAL_AND_HIGH_SECURITY_FINDINGS_WITHOUT_REOPENING_D04",
            decisions,
        )
        self.assertIn(
            "ASSIGN_SECOND_PERSON_SUPPORT_AND_SECURITY_BACKUP", decisions
        )


if __name__ == "__main__":
    unittest.main()
