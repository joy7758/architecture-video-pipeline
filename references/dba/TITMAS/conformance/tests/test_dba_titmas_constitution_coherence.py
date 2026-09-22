from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def load_harness():
    path = ROOT / "TITMAS/conformance/harness.py"
    spec = importlib.util.spec_from_file_location("titmas_constitution_harness", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("conformance harness unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class DbaTitmasConstitutionCoherenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.harness = load_harness()
        cls.schema = load("architecture/schemas/constitution-machine-contract-v0.1.schema.json")
        cls.main = load("architecture/main-constitution-principles.json")
        cls.titmas = load("architecture/titmas-project-constitution.json")
        cls.dcell = load("architecture/dcell-module-governance-profile.json")
        cls.entry_surfaces = load("commercial/entry/entry-surfaces.json")
        cls.contracts = (cls.main, cls.titmas, cls.dcell)

    def test_machine_contracts_validate_against_shared_schema(self):
        for contract in self.contracts:
            self.harness.validate_schema(contract, self.schema)
            self.assertEqual("ACCEPTED_EFFECTIVE_ON_CANONICAL_MERGE", contract["status"])
            self.assertEqual("EFFECTIVE_WHEN_REACHABLE_FROM_CANONICAL_MAIN", contract["authority_effect"])
            self.assertEqual("APPROVED", contract["human_adoption_decision"])
            self.assertEqual("REACHABLE_FROM_CANONICAL_MAIN", contract["effective_trigger"])
            self.assertEqual("refs/heads/main", contract["canonical_ref"])
            self.assertEqual("440d0163aea1577437a2a9c6737a37e0af47663a", contract["authorized_content_head"])
            self.assertEqual("NONE", contract["candidate_branch_authority_effect"])
            self.assertEqual("ADOPTED_AND_EFFECTIVE", contract["post_merge_authority_effect"])
            self.assertTrue(contract["merge_authorized"])
            self.assertFalse(contract["implementation_authorized"])

    def test_parent_principle_ids_are_unique_and_traceable(self):
        ids = [item["stable_id"] for item in self.main["principles"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(8, len(ids))
        self.assertTrue({"ADR-032", "ADR-033", "ADR-039"} <= set(ids))
        for principle in self.main["principles"]:
            for ref in principle["source_refs"]:
                self.assertTrue((ROOT / ref).is_file(), ref)

    def test_parent_child_inheritance_is_explicit(self):
        self.assertEqual(self.main["contract_id"], self.titmas["parent_constitution_ref"])
        self.assertEqual(self.titmas["contract_id"], self.dcell["parent_constitution_ref"])
        self.assertIn("TITMAS_INHERITS_DBA=true", self.titmas["invariants"])
        self.assertIn("TITMAS_MAY_OVERRIDE_DBA=false", self.titmas["invariants"])

    def test_all_source_refs_resolve(self):
        for contract in self.contracts:
            for ref in contract["source_refs"]:
                self.assertTrue((ROOT / ref).is_file(), ref)
            for principle in contract["principles"]:
                for ref in principle["source_refs"]:
                    self.assertTrue((ROOT / ref).is_file(), ref)

    def test_product_portfolio_remains_four(self):
        portfolio = self.titmas["public_product_portfolio"]
        self.assertEqual(4, portfolio["product_count"])
        self.assertEqual(
            {"TITMAS_GATE", "TITMAS_RECEIPT", "TITMAS_AUDIT", "TITMAS_HEALTH"},
            set(portfolio["product_ids"]),
        )
        self.assertFalse(portfolio["observer_is_product"])
        self.assertFalse(portfolio["dcell_layer_is_product"])
        self.assertEqual(0, self.dcell["portfolio_effect"]["public_product_count_effect"])
        self.assertFalse(self.dcell["portfolio_effect"]["is_fifth_product"])

    def test_titmas_is_not_a_global_controller(self):
        role = self.titmas["role"]
        for key in (
            "is_runtime",
            "is_model",
            "is_truth_source",
            "is_final_authority",
            "is_global_mandatory_gateway",
            "is_physical_single_gateway",
        ):
            self.assertFalse(role[key])
        self.assertIn("UNIFIED_ENTRY_NE_GLOBAL_MANDATORY_GATEWAY=true", self.titmas["invariants"])
        goal = self.titmas["unified_entry_goal"]
        self.assertTrue(goal["default_unified_entry_goal"])
        self.assertTrue(goal["logical_unified_entry"])
        self.assertTrue(goal["distributed_enforcement_required"])
        self.assertFalse(goal["global_mandatory_entry_claim"])
        self.assertFalse(goal["physical_single_gateway_required"])
        self.assertFalse(goal["sovereign_central_runtime"])

    def test_parent_machine_assertions_cover_required_principles(self):
        assertions = self.main["constitutional_assertions"]
        expected_true = {
            "distributed_complexity_generation", "centers_may_emerge",
            "bootstrap_center_allowed", "center_must_be_replaceable",
            "center_must_be_auditable", "center_is_not_immune_from_evolution",
            "existing_standard_review_required", "duplicate_core_forbidden",
            "profile_before_core_expansion", "adapter_before_new_runtime",
            "gap_evidence_required_for_new_definition",
            "human_or_organization_is_final_authority",
            "applicable_constraint_intersection_required",
            "unknown_applicability_fails_closed",
            "composition_requires_reevaluation",
            "composition_graph_required_for_consequential_action",
            "composite_authority_escalation_forbidden", "change_event_required",
            "high_risk_permission_revalidation_required",
            "evidence_required_for_trust_restoration", "identity_pluralism",
            "multiple_discovery_paths", "direct_invocation_allowed_where_policy_permits",
            "registry_portability_required", "verifier_replaceability_required",
            "real_goal_and_deadline_evidence_required",
            "capability_claim_requires_execution_evidence",
        }
        expected_false = {
            "permanent_absolute_center", "agent_recommendation_is_authority",
            "agent_can_self_authorize", "cell_can_self_authorize",
            "agent_can_amend_parent_constitution", "cell_can_amend_parent_constitution",
            "component_conformance_is_composition_conformance",
            "silent_authority_inheritance", "shared_protocol_is_shared_controller",
            "documented_capability_is_operational_capability",
            "synthetic_test_is_external_adoption",
            "human_approval_always_required",
            "not_applicable_constraint_is_missing_constraint",
        }
        self.assertTrue(all(assertions[key] is True for key in expected_true))
        self.assertTrue(all(assertions[key] is False for key in expected_false))

    def test_dcell_minimum_contract_and_composition_rules(self):
        required = {
            "cell_id", "logical_identity", "version", "provider_or_operator",
            "capability_contract", "input_contract", "output_contract",
            "allowed_actions", "forbidden_actions", "required_data", "data_retention",
            "external_side_effects", "evidence_obligations", "lifecycle_state",
            "upgrade_path", "rollback_path", "replacement_semantics",
            "revocation_path", "known_limitations",
        }
        self.assertEqual(required, set(self.dcell["minimum_contract_fields"]))
        composition = self.dcell["composition_rules"]
        self.assertTrue(composition["re_evaluation_required"])
        self.assertTrue(composition["change_revalidation_required"])
        self.assertFalse(composition["automatic_pass_inheritance"])
        self.assertFalse(composition["safe_cell_a_plus_safe_cell_b_is_safe_composition"])
        self.assertEqual(
            {"COMPOSITION_GRAPH", "AUTHORITY_GRAPH", "DATA_FLOW_GRAPH", "EVIDENCE_GRAPH"},
            set(composition["required_high_impact_graphs"]),
        )

    def test_dcell_activation_fails_closed(self):
        model = self.dcell["permission_model"]
        self.assertFalse(model["capability_implies_permission"])
        self.assertFalse(model["composition_aggregates_authority"])
        self.assertFalse(model["natural_language_direct_activation"])
        self.assertTrue(model["activation_requires_explicit_authorization"])
        self.assertTrue(model["permission_intersection_required"])
        self.assertTrue(model["cell_can_only_reduce_or_preserve_authority"])
        self.assertFalse(model["cell_can_expand_authority"])
        self.assertFalse(model["lower_level_policy_can_override_higher_level_deny"])
        self.assertFalse(model["human_approval_always_required"])
        self.assertTrue(model["applicable_constraint_intersection_required"])
        self.assertFalse(model["not_applicable_constraint_is_missing_constraint"])
        self.assertTrue(model["unknown_applicability_fails_closed"])
        self.assertEqual(
            {"MANDATORY", "POLICY_REQUIRED", "USER_SELECTABLE", "EXPERIMENTAL"},
            set(self.dcell["activation_classes"]),
        )

    def test_dcell_categories_change_and_language_rules_are_complete(self):
        mandatory = self.dcell["module_categories"]["mandatory_constitutional_cells"]
        self.assertEqual(
            {"CONSTITUTION_GATE", "IDENTITY_AND_VERSION_BINDING", "MINIMUM_RECEIPT", "AUTHORIZATION_REFERENCE"},
            set(mandatory["logical_capabilities"]),
        )
        self.assertFalse(mandatory["can_be_disabled_by_ordinary_user"])
        experimental = self.dcell["module_categories"]["experimental_cells"]
        self.assertEqual({"SANDBOX", "SHADOW", "MONITOR", "CANARY"}, set(experimental["allowed_modes"]))
        self.assertFalse(experimental["production_default"])
        change = self.dcell["change_revalidation"]
        self.assertEqual(12, len(change["triggers"]))
        self.assertTrue(change["dcell_change_requires_revalidation"])
        self.assertFalse(change["new_dcell_version_automatic_high_risk_inheritance"])
        language = self.dcell["natural_language_rule_pipeline"]
        self.assertFalse(language["natural_language_rule_direct_activation"])
        self.assertTrue(language["human_readback_required"])
        self.assertTrue(language["conflict_detection_required"])
        self.assertTrue(language["synthetic_test_required"])
        self.assertTrue(language["signed_human_approval_required"])
        entry = self.dcell["entry_defaults"]
        self.assertNotIn("default_human_language", entry)
        self.assertFalse(entry["global_hardcoded_human_locale"])
        self.assertTrue(entry["usability_is_constitutional_requirement"])
        self.assertTrue(entry["usability_is_safety_property"])

    def test_low_risk_standing_authorization_does_not_require_per_action_approval(self):
        model = self.dcell["permission_model"]
        cases = {item["case_id"]: item for item in model["conformance_examples"]}
        case = cases["LOW_RISK_VALID_STANDING_AUTH"]
        self.assertFalse(model["human_approval_always_required"])
        self.assertFalse(case["approval_applicable"])
        self.assertTrue(case["standing_authorization_valid"])
        self.assertEqual("ALLOW_OR_READY", case["expected_outcome"])

    def test_missing_expired_and_scope_mismatch_require_approval(self):
        cases = {item["case_id"]: item for item in self.dcell["permission_model"]["conformance_examples"]}
        for case_id in (
            "REQUIRED_APPROVAL_MISSING",
            "REQUIRED_APPROVAL_EXPIRED",
            "REQUIRED_APPROVAL_SCOPE_MISMATCH",
        ):
            self.assertTrue(cases[case_id]["approval_applicable"])
            self.assertEqual("NEEDS_APPROVAL", cases[case_id]["expected_outcome"])

    def test_non_overridable_deny_survives_approval(self):
        model = self.dcell["permission_model"]
        cases = {item["case_id"]: item for item in model["conformance_examples"]}
        self.assertFalse(model["one_time_approval_can_override_non_overridable_rule"])
        self.assertFalse(model["one_time_approval_can_expand_parent_constitution"])
        for case_id in ("NON_OVERRIDABLE_DENY_WITHOUT_APPROVAL", "NON_OVERRIDABLE_DENY_WITH_APPROVAL"):
            self.assertTrue(cases[case_id]["non_overridable_deny"])
            self.assertEqual("BLOCK", cases[case_id]["expected_outcome"])

    def test_not_applicable_and_unknown_semantics(self):
        model = self.dcell["permission_model"]
        cases = {item["case_id"]: item for item in model["conformance_examples"]}
        not_applicable = cases["HUMAN_APPROVAL_NOT_APPLICABLE"]
        unknown = cases["UNKNOWN_CONSTRAINT_APPLICABILITY"]
        self.assertFalse(model["not_applicable_constraint_is_missing_constraint"])
        self.assertEqual("ALLOW_OR_READY", not_applicable["expected_outcome"])
        self.assertFalse(unknown["applicability_known"])
        self.assertEqual("NOT_ASSESSED_AND_FAIL_CLOSED", unknown["expected_outcome"])

    def test_approval_bindings_are_complete(self):
        bindings = set(self.dcell["permission_model"]["approval_binding_required"])
        self.assertEqual(
            {
                "PRINCIPAL", "AGENT_ID_AND_VERSION", "TASK", "ACTION_AND_RESOURCE",
                "CONSTITUTION_VERSION", "COMPOSITION_DIGEST_WHEN_APPLICABLE", "SCOPE", "EXPIRY",
            },
            bindings,
        )

    def test_base_locale_policy_is_declared_and_not_hardcoded(self):
        base = self.titmas["human_interface_contract"]
        self.assertTrue(base["human_readback_must_be_comprehensible"])
        self.assertTrue(base["human_readback_must_use_declared_principal_or_market_locale"])
        self.assertTrue(base["locale_must_be_explicitly_declared"])
        self.assertTrue(base["critical_status_must_not_be_machine_code_only"])
        self.assertTrue(base["machine_contract_and_localized_explanation_must_coexist"])
        self.assertFalse(base["global_hardcoded_human_locale"])
        self.assertNotIn("default_human_language", self.dcell["entry_defaults"])

    def test_china_market_profile_preserves_chinese_first(self):
        profile = self.entry_surfaces["surfaces"]["HUMAN"]["locale_profile"]
        self.assertEqual("CHINA", profile["market_profile"])
        self.assertEqual("zh-CN", profile["default_human_locale"])
        self.assertEqual("SIMPLIFIED_CHINESE", profile["china_market_ui_default"])
        self.assertTrue(profile["critical_status_requires_chinese_explanation"])
        self.assertTrue(profile["english_reason_code_may_be_retained"])
        self.assertTrue(profile["english_reason_code_requires_chinese_explanation"])
        self.assertFalse(profile["global_multilingual_expansion_implemented"])
        self.assertEqual("NONE", profile["authority_effect"])

    def test_human_adoption_decision_and_canonical_trigger_are_recorded(self):
        record = (ROOT / "architecture/ADR-043-dba-titmas-constitution-coherent-upgrade.md").read_text(encoding="utf-8")
        for assertion in (
            "HUMAN_DECISION_RECORDED=true",
            "HUMAN_DECIDED_BY_REF=zhangbin",
            "HUMAN_CONTENT_APPROVAL_RECORDED=true",
            "HUMAN_FINAL_DECISION_RECORDED=true",
            "CANDIDATE_APPROVED_BY_HUMAN=true",
            "ADOPTION_AUTHORIZED=true",
            "AUTHORIZED_CONTENT_HEAD=440d0163aea1577437a2a9c6737a37e0af47663a",
            "ADOPTION_EFFECT_TRIGGER=CANONICAL_MAIN_MERGE_OF_PR_142",
            "CANONICAL_REF=refs/heads/main",
            "PRE_MERGE_AUTHORITY_EFFECT=PENDING_CANONICAL_MERGE",
            "POST_MERGE_AUTHORITY_EFFECT=ADOPTED_AND_EFFECTIVE",
            "CONSTITUTION_EFFECTIVE_WHEN_REACHABLE_FROM_CANONICAL_MAIN=true",
            "MERGE_AUTHORIZED=true",
            "IMPLEMENTATION_AUTHORIZED=false",
        ):
            self.assertIn(assertion, record)

    def test_c01_stable_identity_and_meaning_are_preserved(self):
        index = load("commercial/constitution/commercial-constitution-index.json")
        first = index["principles"][0]
        self.assertEqual("TITMAS-COMMERCIAL-C01", first["principle_id"])
        self.assertEqual("FROZEN_COMMERCIAL_CONSTITUTION", first["normative_status"])
        amendment = (ROOT / "architecture/titmas-project-constitution-unified-entry-dcell-amendment-v0.1.md").read_text(encoding="utf-8")
        for invariant in (
            "C01_STABLE_ID_PRESERVED=true",
            "C01_MEANING_PRESERVED=true",
            "FIRST_VALUE_BEFORE_ENFORCEMENT=true",
            "MONITOR_BEFORE_ENFORCE=true",
        ):
            self.assertIn(invariant, amendment)

    def test_bilingual_titles_and_statements_are_present(self):
        chinese = re.compile(r"[\u4e00-\u9fff]")
        for contract in self.contracts:
            self.assertRegex(contract["title_zh"], chinese)
            for principle in contract["principles"]:
                self.assertRegex(principle["title_zh"], chinese)
                self.assertRegex(principle["statement_zh"], chinese)

    def test_nonclaims_and_retained_failures(self):
        required_nonclaims = {
            "UNIFIED_ENTRY_IMPLEMENTED",
            "UNIFIED_AGENT_ENTRY_IMPLEMENTED",
            "SELECTABLE_DCELL_LIBRARY_IMPLEMENTED",
            "CROSS_PLATFORM_ENFORCEMENT_PROVEN",
            "EIGHTY_AGENT_SCALE_PROVEN",
            "PRODUCTION_READY",
            "COMMERCIAL_OFFER_AVAILABLE",
            "EXTERNAL_ADOPTION_PROVEN",
        }
        self.assertTrue(required_nonclaims <= set(self.titmas["non_claims"]))
        status = (ROOT / "PROGRAM-STATUS.md").read_text(encoding="utf-8")
        d04 = (ROOT / "architecture/ADR-038-d04-final-closure-and-adopt-before-build.md").read_text(encoding="utf-8")
        amendment = (ROOT / "architecture/titmas-project-constitution-unified-entry-dcell-amendment-v0.1.md").read_text(encoding="utf-8")
        self.assertIn("P0_10_RESULT=FAIL_CLOSED_AFTER_RUNTIME_ALIGNMENT", status)
        self.assertIn("D04_FINAL_STATUS=CLOSED_FAILED_RETAINED", d04)
        self.assertIn("HISTORICAL_RECEIPT_FAILURES_RETAINED=true", amendment)

    def test_document_and_machine_contract_semantics_are_aligned(self):
        parent_doc = (ROOT / "architecture/dba-main-constitution-coherence-amendment-v0.1.md").read_text(encoding="utf-8")
        child_doc = (ROOT / "architecture/titmas-project-constitution-unified-entry-dcell-amendment-v0.1.md").read_text(encoding="utf-8")
        for assertion in (
            "DISTRIBUTED_COMPLEXITY_GENERATION=true",
            "PERMANENT_ABSOLUTE_CENTER=false",
            "EXISTING_STANDARD_REVIEW_REQUIRED=true",
            "HUMAN_OR_ORGANIZATION_IS_FINAL_AUTHORITY=true",
            "SHARED_PROTOCOL_NE_SHARED_CONTROLLER=true",
            "SYNTHETIC_TEST_NE_EXTERNAL_ADOPTION=true",
        ):
            self.assertIn(assertion, parent_doc)
        for assertion in (
            "TITMAS_IS_AGENT_RUNTIME=false",
            "GLOBAL_MANDATORY_ENTRY_CLAIM=false",
            "DISTRIBUTED_ENFORCEMENT_REQUIRED=true",
            "CELL_SELECTION_NE_AUTHORIZATION=true",
            "DCELL_CHANGE_REQUIRES_REVALIDATION=true",
            "USABILITY_IS_CONSTITUTIONAL_REQUIREMENT=true",
            "NATURAL_LANGUAGE_RULE_DIRECT_ACTIVATION=false",
            "PUBLIC_PRODUCT_COUNT=4",
        ):
            self.assertIn(assertion, child_doc)

    def test_forbidden_capability_claims_remain_false(self):
        child_doc = (ROOT / "architecture/titmas-project-constitution-unified-entry-dcell-amendment-v0.1.md").read_text(encoding="utf-8")
        for claim in (
            "UNIFIED_AGENT_ENTRY_IMPLEMENTED",
            "SELECTABLE_DCELL_LIBRARY_IMPLEMENTED",
            "CROSS_PLATFORM_ENFORCEMENT_PROVEN",
            "EIGHTY_AGENT_SCALE_PROVEN",
            "PRODUCTION_READY",
            "COMMERCIAL_OFFERING_AVAILABLE",
            "REAL_CUSTOMER_ADOPTION_PROVEN",
        ):
            self.assertIn(f"{claim}=false", child_doc)
            self.assertNotIn(f"{claim}=true", child_doc)

    def test_no_private_path_or_secret_material_in_new_artifacts(self):
        paths = [
            "architecture/dba-main-constitution-coherence-amendment-v0.1.md",
            "architecture/titmas-project-constitution-unified-entry-dcell-amendment-v0.1.md",
            "architecture/ADR-043-dba-titmas-constitution-coherent-upgrade.md",
            "architecture/dba-titmas-constitution-reuse-compatibility-audit-v0.1.md",
            "architecture/dba-titmas-constitution-traceability-matrix-v0.1.md",
            "architecture/main-constitution-principles.json",
            "architecture/titmas-project-constitution.json",
            "architecture/dcell-module-governance-profile.json",
            "commercial/entry/entry-surfaces.json",
            "DBA-TITMAS-CONSTITUTION-COHERENT-UPGRADE-COMPLETION-REPORT-v0.1.md",
        ]
        forbidden = (
            "/" + "Users/",
            "/private" + "/tmp/",
            "s" + "k-",
            "API" + "_KEY=",
            "BEGIN" + " PRIVATE KEY",
        )
        for relative in paths:
            text = (ROOT / relative).read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, f"{relative}: {token}")


if __name__ == "__main__":
    unittest.main()
