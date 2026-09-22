from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class CommercialPrivateConstitutionTests(unittest.TestCase):
    def test_repository_homepage_uses_current_commercial_identity(self):
        homepage = (ROOT.parent / "README.md").read_text(encoding="utf-8")
        self.assertTrue(homepage.startswith("# TITMAS Commercial Agent Infrastructure"))
        self.assertIn("CURRENT_STRATEGY=COMMERCIAL_PRIVATE_INFRASTRUCTURE", homepage)
        self.assertIn("PUBLIC_SURFACE_NE_OPEN_SOURCE_CORE=true", homepage)
        self.assertIn("PUBLIC_CONTRIBUTION_ROUTE_ACTIVE=false", homepage)
        self.assertNotIn("COMMUNITY_STATUS=LIMITED_REPOSITORY_CONTRIBUTION_PREVIEW", homepage)
        self.assertNotIn("PUBLIC_CONTRIBUTION_SURFACE_ACTIVE=true", homepage)

    def test_current_constitution_and_decision_are_present(self):
        constitution = (ROOT / "architecture/commercial-private-infrastructure-strategy-constitution.md").read_text(encoding="utf-8")
        decision = (ROOT / "architecture/ADR-042-commercial-private-infrastructure-direction.md").read_text(encoding="utf-8")
        self.assertIn("COMMERCIAL_PRIVATE_INFRASTRUCTURE_FIRST=true", constitution)
        self.assertIn("PRIVATE_CORE_IS_CANONICAL=true", constitution)
        self.assertIn("PUBLIC_SURFACE_NE_OPEN_SOURCE_CORE=true", constitution)
        self.assertIn("Status: `ACCEPTED`", decision)

    def test_agent_entry_uses_current_commercial_identity(self):
        index = load_json("agent-index.json")
        self.assertEqual("3.1.0", index["format_version"])
        self.assertEqual("TITMAS Commercial Agent Infrastructure", index["canonical_program_name"])
        self.assertEqual("COMMERCIAL_PRIVATE_AGENT_INFRASTRUCTURE", index["product_category"])
        self.assertNotIn("canonical_community_name", index)
        self.assertEqual("NONE", index["historical_community_identity"]["current_authority_effect"])

    def test_historical_community_paths_are_not_active_entry_commands(self):
        index = load_json("agent-index.json")
        active_commands = index["commands"]
        active_surfaces = index["machine_surfaces"]
        archive = index["historical_community_archive"]

        self.assertFalse(any("community_cli.py" in command for command in active_commands.values()))
        self.assertNotIn("community_status", active_surfaces)
        self.assertNotIn("contribution_activation_package", active_surfaces)
        self.assertEqual("NONE", archive["current_authority_effect"])
        self.assertFalse(archive["invocation_authorized"])
        self.assertFalse(archive["customer_entry"])
        self.assertIn("community_status", archive["surfaces"])
        self.assertTrue(any("community_cli.py" in command for command in archive["commands"].values()))

    def test_human_start_here_separates_historical_contribution_links(self):
        readme = (ROOT / "TITMAS/README.md").read_text(encoding="utf-8")
        active_entry, historical_archive = readme.split("## Historical archive — not an active entry", maxsplit=1)
        self.assertNotIn("FIRST_CONTRIBUTION.md", active_entry)
        self.assertNotIn("community/CONTRIBUTING.md", active_entry)
        self.assertNotIn("github-activation-templates", active_entry)
        self.assertIn("HISTORICAL_COMMUNITY_INVOCATION_AUTHORIZED=false", historical_archive)

    def test_llms_entry_uses_current_commercial_route(self):
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("TITMAS is commercial, private-core infrastructure", llms)
        self.assertIn("Current commercial machine status: ./COMMERCIAL-READINESS-MACHINE-STATUS.json", llms)
        self.assertIn("D29 status: IN_PROGRESS_BLOCKED", llms)
        self.assertNotIn("Agent community CLI:", llms)
        self.assertNotIn("TITMAS is the Agent-Native Standards Community", llms)

    def test_public_surface_does_not_imply_open_core_or_community(self):
        constitution = (ROOT / "architecture/commercial-private-infrastructure-strategy-constitution.md").read_text(encoding="utf-8")
        for invariant in (
            "PUBLIC_SURFACE_NE_OPEN_SOURCE_CORE=true",
            "PUBLIC_SDK_NE_PUBLIC_COMMUNITY=true",
            "CURRENT_IDENTITY_NE_DEVELOPER_COMMUNITY=true",
            "CURRENT_IDENTITY_NE_OPEN_SOURCE_COMMUNITY=true",
            "CURRENT_STRATEGY_NE_OPEN_CORE=true",
            "PUBLIC_ASSET_NE_PUBLIC_CONTRIBUTION_ROUTE=true",
            "PUBLIC_CONTRIBUTION_ROUTE_ACTIVE=false",
            "COMMUNITY_ESTABLISHED=false",
        ):
            self.assertIn(invariant, constitution)

    def test_historical_agent_native_readme_is_not_an_active_entry(self):
        readme = (ROOT / "TITMAS/agent-native/README.md").read_text(encoding="utf-8")
        self.assertTrue(readme.startswith("# TITMAS Agent-Native Architecture — Historical Community Archive"))
        self.assertIn("COMMUNITY_STATUS=SUPERSEDED_HISTORICAL_ARCHIVE", readme)
        self.assertIn("COMMUNITY_CURRENT_AUTHORITY_EFFECT=NONE", readme)
        self.assertIn("COMMUNITY_INVOCATION_AUTHORIZED=false", readme)
        self.assertNotIn("## Agent in 60 seconds", readme)

    def test_current_public_projection_has_no_active_community_identity(self):
        public_llms = (ROOT / "site/public/llms.txt").read_text(encoding="utf-8")
        platform = (ROOT / "docs/TITMAS_PRIVATE_PLATFORM_ARCHITECTURE_v0.1.md").read_text(encoding="utf-8")
        site_content = (ROOT / "site/app/site-content.ts").read_text(encoding="utf-8")

        self.assertNotIn("## What the community works on", public_llms)
        self.assertNotIn("TITMAS Infrastructure Developer Community improves", public_llms)
        self.assertNotIn("The public community repository is", platform)
        self.assertNotIn("社区仍处于准备状态", site_content)
        self.assertNotIn("the community remains in preparation", site_content)

    def test_historical_community_record_is_fail_closed(self):
        status = load_json("TITMAS/community/community-status.json")
        self.assertTrue(status["historical_record"])
        self.assertFalse(status["current_route_active"])
        self.assertEqual("NONE", status["current_authority_effect"])
        self.assertFalse(status["public_contribution_surface"]["active"])
        self.assertFalse(status["public_contribution_surface"]["authorized"])
        self.assertFalse(status["community_established"])

    def test_historical_open_constitution_has_no_current_authority(self):
        historical = (ROOT / "architecture/open-infrastructure-strategy-constitution.md").read_text(encoding="utf-8")
        self.assertIn("Status: `SUPERSEDED_HISTORICAL_STRATEGY`", historical)
        self.assertIn("Current authority effect: `NONE`", historical)
        self.assertIn("ADR-042", historical)

    def test_strategy_change_creates_no_operational_authority(self):
        decision = (ROOT / "architecture/ADR-042-commercial-private-infrastructure-direction.md").read_text(encoding="utf-8")
        for boundary in (
            "IMPLEMENTATION_AUTHORIZED=false",
            "RELEASE_AUTHORIZED=false",
            "DEPLOYMENT_AUTHORIZED=false",
            "COMMERCIAL_OFFER_AUTHORIZED=false",
            "CORE_SOURCE_PUBLICATION_AUTHORIZED=false",
            "PUBLIC_CONTRIBUTION_AUTHORIZED=false",
        ):
            self.assertIn(boundary, decision)

    def test_current_roadmap_uses_commercial_customer_route(self):
        roadmap = (ROOT / "MASTER-ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("CURRENT_FOCUS=D29_COMMERCIAL_PRIVATE_PLATFORM_AND_BOUNDED_CUSTOMER_ENTRY", roadmap)
        self.assertIn("CURRENT_STRATEGY=COMMERCIAL_PRIVATE_INFRASTRUCTURE", roadmap)
        self.assertIn("受控客户接入、商业交付与支持服务", roadmap)
        self.assertNotIn("CURRENT_FOCUS=DEVELOPER_PREVIEW_V0_1_POST_RELEASE_OBSERVATION", roadmap)


if __name__ == "__main__":
    unittest.main()
