from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GATEWAY_REVISION = "1a065f1702e355d5f5ed566bdfd3e895cdca2540"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class D29CurrentImplementationProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.projection = load("commercial/discovery/d29-reference-implementation.json")
        cls.status = load("commercial/discovery/status.json")
        cls.offerings = load("commercial/discovery/commercial-offerings.json")
        cls.limitations = load("commercial/discovery/known-limitations.json")
        cls.repositories = load("commercial/discovery/canonical-repositories.json")
        cls.program = load("commercial-program-state.json")
        cls.readiness = load("commercial-readiness.json")
        cls.readiness_schema = load(
            "architecture/schemas/commercial-readiness-v1.0.schema.json"
        )
        cls.machine_readiness = load("COMMERCIAL-READINESS-MACHINE-STATUS.json")
        cls.agent_index = load("agent-index.json")
        cls.convergence = load(
            "titmas-commercial-product-convergence-status-v1.0.json"
        )

    def test_conditional_convergence_projection_is_discoverable_and_fail_closed(self):
        surfaces = self.agent_index["machine_surfaces"]
        self.assertEqual(
            "titmas-commercial-product-convergence-status-v1.0.json",
            surfaces["commercial_product_convergence_status"],
        )
        self.assertEqual(
            "TITMAS-COMMERCIAL-PRODUCT-CONVERGENCE-IMPLEMENTATION-PROJECTION-v1.0.md",
            surfaces["commercial_product_convergence_projection"],
        )
        self.assertEqual(
            "ENGINEERING_CANDIDATE_PENDING_ELAPSED_SOAK_TIME",
            self.convergence["status"],
        )
        self.assertEqual(
            "8437b2c1ac860f10953ff60603ddd6814b97393a",
            self.convergence["source_truth"]["gateway"]["base_commit"],
        )
        self.assertEqual(
            "MERGED",
            self.convergence["source_truth"]["integrations"]["pull_request_state"],
        )
        self.assertEqual(
            "MERGED",
            self.convergence["source_truth"]["governance"]["pull_request_state"],
        )
        self.assertTrue(
            self.convergence["authority"]["cockpit_status_projection_merge_executed"]
        )
        self.assertEqual(
            "REMAINING_GATEWAY_CONVERGENCE_CANDIDATE_ONLY",
            self.convergence["authority"]["merge_authority_scope"],
        )
        self.assertFalse(self.convergence["soak"]["complete"])
        self.assertFalse(self.convergence["candidate"]["commercial_private_pilot_ready"])
        self.assertFalse(self.convergence["candidate"]["production_ready"])
        self.assertFalse(self.convergence["candidate"]["commercial_offering_available"])
        for authority in (
            "merge_authorized",
            "release_authorized",
            "deployment_authorized",
            "customer_data_authorized",
            "payment_authorized",
        ):
            with self.subTest(authority=authority):
                self.assertFalse(self.convergence["authority"][authority])

    def test_source_is_exact_canonical_gateway_main(self):
        source = self.projection["source"]
        self.assertEqual("joy7758/titmas-sandbox-gateway", source["repository"])
        self.assertEqual("main", source["branch"])
        self.assertEqual(GATEWAY_REVISION, source["revision"])
        self.assertEqual("MERGED_ON_CANONICAL_MAIN", source["source_status"])
        self.assertEqual(GATEWAY_REVISION, self.repositories["commercial_platform"]["observed_main_head"])
        self.assertEqual(GATEWAY_REVISION, self.program["source_commits"]["data_plane"])

    def test_reference_capabilities_do_not_become_offerings(self):
        self.assertTrue(self.status["observer_runtime_implemented"])
        self.assertTrue(self.status["console_implemented"])
        self.assertTrue(self.status["synthetic_first_value_implemented"])
        self.assertTrue(self.status["software_delivery_proof_implemented"])
        for key in (
            "observer_runtime_status",
            "console_status",
            "synthetic_first_value_status",
        ):
            self.assertEqual("IMPLEMENTED_REFERENCE_NOT_DEPLOYED", self.status[key])
        self.assertEqual(0, self.status["available_offering_count"])
        self.assertFalse(self.status["currently_achieved"])
        self.assertFalse(self.status["deployment_executed"])
        self.assertFalse(self.status["paid_monitor_pilot_available"])
        self.assertFalse(self.status["customer_specific_enforce_authorized"])
        self.assertFalse(self.status["public_launch_authorized"])
        self.assertFalse(self.status["commercial_customer_created"])
        self.assertEqual(0, self.offerings["available_offering_count"])
        self.assertTrue(all(not item.get("currently_available_offering", False) for item in self.offerings["offerings"]))

    def test_durable_read_projections_retain_bounded_audit_boundary(self):
        capabilities = self.projection["capabilities"]
        boundaries = self.projection["retained_fail_closed_boundaries"]
        self.assertEqual(
            "IMPLEMENTED_REFERENCE_NOT_DEPLOYED",
            capabilities["durable_receipt_read_projection"],
        )
        self.assertEqual(
            "PASS_SOURCE_AND_EPHEMERAL_POSTGRES_CI_COMPLETE_DECLARED_WORKSPACE_SCOPE_NOT_DEPLOYED",
            capabilities["durable_audit_export_projection"],
        )
        self.assertEqual(
            "IMPLEMENTED_REFERENCE_AUDIT_COMPLETE_FOR_DECLARED_WORKSPACE_SCOPE_NOT_DEPLOYED",
            capabilities["durable_health_projection"],
        )
        self.assertTrue(
            boundaries[
                "postgres_audit_projection_chain_complete_for_declared_workspace_scope"
            ]
        )
        self.assertEqual(
            "COMMERCIAL_TENANT_WORKSPACE_EXPORT_V1",
            boundaries["postgres_audit_projection_profile"],
        )
        self.assertFalse(boundaries["canonical_tenant_event_content_complete"])
        self.assertFalse(
            boundaries["offline_scope_non_membership_cryptographic_proof"]
        )
        self.assertFalse(boundaries["external_cryptographic_anchor"])
        self.assertFalse(self.projection["availability"]["deployed"])

    def test_security_engineering_gate_fails_closed_with_exact_counts(self):
        gate = self.projection["security_engineering_gate"]
        self.assertEqual("FAIL_CLOSED_RETAINED_CR01_LIMITATION", gate["status"])
        self.assertEqual(20, gate["control_count"])
        self.assertEqual(18, gate["pass"])
        self.assertEqual(0, gate["partial"])
        self.assertEqual(1, gate["fail_retained"])
        self.assertEqual(0, gate["not_assessed"])
        self.assertEqual(1, gate["not_applicable"])
        self.assertEqual(0, gate["blocker_findings_open"])
        self.assertEqual(1, gate["blocker_dispositions_retained"])
        self.assertEqual(0, gate["high_findings_open"])
        self.assertEqual(
            "RECOMMEND_BOUNDED_TECHNICAL_EVALUATION_ONLY",
            gate["agent_recommendation"],
        )
        self.assertFalse(gate["paid_pilot_recommended"])
        self.assertFalse(gate["independent_security_evaluation_executed"])
        self.assertFalse(gate["d04_reopened"])
        self.assertEqual("NONE", gate["commercial_effect"])
        self.assertEqual(
            "FAIL_CLOSED_RETAINED_CR01_LIMITATION",
            self.status["security_engineering_gate"],
        )
        blockers = self.machine_readiness["commercial_blockers"]
        self.assertNotIn("HIGH_SECURITY_FINDINGS_OPEN_2", blockers)
        self.assertIn(
            "SECURITY_GATE_FAIL_CLOSED_RETAINED_CR01_LIMITATION", blockers
        )

    def test_workspace_data_lifecycle_is_source_only_and_not_deployed(self):
        capabilities = self.projection["capabilities"]
        for key in ("workspace_deletion_lifecycle", "workspace_retention_lifecycle"):
            self.assertEqual(
                "PASS_SOURCE_AND_EPHEMERAL_POSTGRES_CI_NOT_DEPLOYED",
                capabilities[key],
            )
            self.assertEqual(capabilities[key], self.status[key])
        self.assertFalse(self.projection["availability"]["deployed"])
        self.assertFalse(self.status["deployment_executed"])

    def test_security_drill_executed_and_temporary_authority_is_closed(self):
        drill = self.projection["security_drill_readiness"]
        self.assertEqual("EXECUTED_PASS_AUTHORITY_CLOSED", drill["status"])
        self.assertTrue(drill["incident_drill_executed"])
        self.assertTrue(drill["formal_rollback_drill_executed"])
        self.assertFalse(drill["incident_drill_authorized"])
        self.assertFalse(drill["rollback_drill_authorized"])
        self.assertEqual(
            "PASS_EXACT_RELEASES_BACKUP_AND_SYNTHETIC_BOUNDARY",
            drill["read_only_preflight_status"],
        )
        self.assertEqual(
            "efdfc84462628abdfbfe111f61253f76569edec0",
            drill["observed_active_symlink_release"],
        )
        self.assertTrue(drill["drill_target_frozen"])
        self.assertTrue(drill["formal_rollback_pointer_found"])
        self.assertEqual(
            "efdfc84462628abdfbfe111f61253f76569edec0",
            drill["candidate_release"],
        )
        self.assertEqual(
            "314cc178ea4f99c1b39e2a6d5ea9706f56d596f9",
            drill["rollback_release"],
        )
        self.assertEqual(2166, drill["incident_recovery_milliseconds"])
        self.assertEqual(2604, drill["formal_rollback_milliseconds"])
        self.assertEqual(2012, drill["forward_recovery_milliseconds"])
        self.assertEqual(2, drill["security_findings_closed"])
        self.assertEqual(1, drill["blocker_dispositions_retained"])
        self.assertEqual(
            "NONE_SECURITY_GATE_REMAINS_FAIL_CLOSED", drill["commercial_effect"]
        )
        self.assertEqual(
            "EXECUTED_PASS_AUTHORITY_CLOSED",
            self.status["security_drill_readiness"],
        )
        self.assertTrue(self.status["incident_drill_executed"])
        self.assertTrue(self.status["formal_rollback_drill_executed"])

    def test_synthetic_measurements_retain_scope_and_non_claims(self):
        measured = self.projection["measured_synthetic_reference"]
        self.assertEqual(0, measured["customer_data_count"])
        self.assertEqual(0, measured["real_external_action_count"])
        self.assertEqual(0, measured["production_permission_count"])
        self.assertEqual("PASS", measured["first_value"]["receipt_verification"])
        self.assertEqual(
            "SYNTHETIC_ZERO_DATA_BENCHMARK_NOT_PRODUCTION_PERFORMANCE",
            measured["measurement_classification"],
        )
        self.assertFalse(measured["latency_is_slo"])
        self.assertFalse(measured["result_is_customer_evidence"])
        self.assertEqual(
            "NON_BINDING_SYNTHETIC_PROOF_ONLY_NO_CUSTOMER_AUTHORIZATION_OR_RELEASE_ACTION",
            measured["software_delivery_proof_disclaimer"],
        )
        self.assertFalse(measured["software_delivery_proof"]["release_or_merge_executed"])
        self.assertEqual(0, measured["software_delivery_proof"]["external_network_call_count"])

    def test_fail_closed_commercial_boundaries_are_retained(self):
        availability = self.projection["availability"]
        boundaries = self.projection["retained_fail_closed_boundaries"]
        self.assertFalse(availability["deployed"])
        self.assertFalse(availability["commercial_offering_available"])
        self.assertFalse(availability["paid_monitor_pilot_available"])
        self.assertFalse(availability["customer_specific_enforce_authorized"])
        self.assertEqual(0, availability["customer_count"])
        self.assertFalse(availability["production_ready"])
        self.assertEqual("CLOSED_FAILED_RETAINED", boundaries["d04_status"])
        self.assertFalse(boundaries["p0_10_agent_first_acceptance"])
        self.assertFalse(boundaries["receipt_pass_is_truth"])
        self.assertFalse(boundaries["verification_is_authorization"])
        self.assertFalse(boundaries["gate_decision_is_execution"])
        self.assertFalse(boundaries["synthetic_authorization_is_customer_authorization"])
        self.assertFalse(self.readiness["commercial_technical_ready"])
        self.assertFalse(self.readiness["paid_beta_ready"])
        self.assertFalse(self.readiness["production_ready"])

    def test_commercial_readiness_matches_its_declared_schema_contract(self):
        allowed_gates = set(
            self.readiness_schema["$defs"]["gateMap"]["additionalProperties"][
                "enum"
            ]
        )
        for gate_map in ("technical_gates", "operational_gates"):
            with self.subTest(gate_map=gate_map):
                self.assertTrue(
                    set(self.readiness[gate_map].values()).issubset(allowed_gates)
                )

        external_schema = self.readiness_schema["properties"]["external_evidence"]
        self.assertTrue(
            set(self.readiness["external_evidence"]).issubset(
                external_schema["properties"]
            )
        )
        self.assertEqual(0, self.readiness["security"]["critical_findings_open"])
        self.assertEqual(
            0, self.readiness["security"]["high_findings_without_mitigation"]
        )
        self.assertEqual(
            "PASS_WITH_LIMITATIONS",
            self.readiness["operational_gates"]["incident_drill"],
        )
        self.assertEqual(
            "PASS_WITH_LIMITATIONS",
            self.readiness["operational_gates"]["formal_rollback_drill"],
        )
        self.assertEqual(
            "PASS_WITH_LIMITATIONS",
            self.readiness["technical_gates"]["d29_security_drill_readiness"],
        )

    def test_agent_only_security_advisory_does_not_become_formal_audit(self):
        advisory = load(
            "commercial/security-evaluation/"
            "D29-AGENT-ONLY-ADVISORY-EVALUATION-v1.0.json"
        )
        self.assertEqual(
            "AGENT_ONLY_ADVISORY_COMPLETE_WITH_CALL_FAILURES", advisory["status"]
        )
        self.assertEqual(3, advisory["structured_consensus"]["eligible_response_count"])
        self.assertEqual(
            "NOT_RECOMMENDED", advisory["structured_consensus"]["recommendation"]
        )
        self.assertEqual(
            "FAIL_CLOSED", advisory["structured_consensus"]["security_gate"]
        )
        self.assertFalse(
            advisory["structured_consensus"]["paid_monitor_pilot_recommended_now"]
        )
        self.assertEqual(0, advisory["structured_consensus"]["security_findings_closed"])
        self.assertFalse(advisory["authority"]["formal_independent_security_audit"])
        self.assertEqual(
            "READY_TO_INVITE_NOT_EXECUTED",
            advisory["retained_boundaries"]["independent_security_evaluation"],
        )
        self.assertFalse(advisory["retained_boundaries"]["paid_monitor_pilot_available"])
        surface = self.agent_index["machine_surfaces"][
            "commercial_d29_agent_only_security_advisory"
        ]
        self.assertEqual(
            "commercial/security-evaluation/"
            "D29-AGENT-ONLY-ADVISORY-EVALUATION-v1.0.json",
            surface,
        )
        self.assertTrue((ROOT / surface).is_file())

    def test_agent_entry_exposes_one_projection_without_copying_child_truth(self):
        surface = self.agent_index["machine_surfaces"]["commercial_d29_reference_implementation"]
        self.assertEqual("commercial/discovery/d29-reference-implementation.json", surface)
        self.assertTrue((ROOT / surface).is_file())
        current = self.agent_index["commercialization_boundary"]["d29_customer_entry_reference"]
        self.assertEqual(GATEWAY_REVISION, current["source_revision"])
        self.assertFalse(current["commercial_offering_available"])
        self.assertFalse(current["production_ready"])
        self.assertEqual(
            "READ_ONLY_DBA_SOURCE_PIN_NO_CHILD_STATUS_WRITE",
            self.projection["projection_effect"],
        )

    def test_current_limitations_replace_stale_missing_claims(self):
        limitations = set(self.limitations["limitations"])
        self.assertIn("D29_REFERENCE_IMPLEMENTATION_NOT_DEPLOYED", limitations)
        self.assertIn("OBSERVER_FIRST_VALUE_SYNTHETIC_ONLY", limitations)
        self.assertIn("CONSOLE_REFERENCE_NOT_DEPLOYED", limitations)
        self.assertIn("PAID_MONITOR_PILOT_NOT_AVAILABLE", limitations)
        self.assertNotIn("OBSERVER_RUNTIME_NOT_IMPLEMENTED", limitations)
        self.assertNotIn("CONSOLE_NOT_IMPLEMENTED", limitations)


if __name__ == "__main__":
    unittest.main()
