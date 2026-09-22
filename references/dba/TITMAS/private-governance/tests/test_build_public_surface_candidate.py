import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "build_public_surface_candidate.py"
SPEC = importlib.util.spec_from_file_location("public_surface_builder", MODULE_PATH)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


def registry_for(path: str, classification: str = "PUBLIC_DOCUMENTATION") -> dict:
    return {
        "default_classification": "UNCLASSIFIED",
        "unclassified_export_allowed": False,
        "publication_policy": {
            "allowlist_only_export": True,
            "publication_by_reconstruction": True,
            "full_repository_copy_prohibited": True,
            "git_history_export_prohibited": True,
        },
        "entries": [{
            "path": path,
            "classification": classification,
            "legal_review_status": "APPROVED",
            "commercial_review_status": "APPROVED",
            "security_review_status": "APPROVED",
            "license_status": "APPROVED",
            "export_allowed": True,
        }],
    }


class PublicSurfaceBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.output = self.root / "candidate"
        self.source.mkdir()
        (self.source / "docs").mkdir()
        (self.source / "docs" / "intro.md").write_text("public candidate\n", encoding="utf-8")
        self.registry = self.root / "registry.json"

    def tearDown(self):
        self.temp.cleanup()

    def write_registry(self, value: dict):
        self.registry.write_text(json.dumps(value), encoding="utf-8")

    def test_builds_only_approved_allowlisted_file(self):
        self.write_registry(registry_for("docs/intro.md"))
        manifest = BUILDER.build_candidate(self.registry, self.source, self.output)
        self.assertEqual(["docs/intro.md"], [item["path"] for item in manifest["files"]])
        self.assertFalse(manifest["published"])

    def test_unclassified_entry_is_rejected(self):
        self.write_registry(registry_for("docs/intro.md", "UNCLASSIFIED"))
        with self.assertRaisesRegex(BUILDER.ExportBoundaryError, "CLASSIFICATION_NOT_PUBLIC"):
            BUILDER.build_candidate(self.registry, self.source, self.output)

    def test_pending_legal_review_is_rejected(self):
        value = registry_for("docs/intro.md")
        value["entries"][0]["legal_review_status"] = "PENDING"
        self.write_registry(value)
        with self.assertRaisesRegex(BUILDER.ExportBoundaryError, "LEGAL_REVIEW_STATUS_NOT_APPROVED"):
            BUILDER.build_candidate(self.registry, self.source, self.output)

    def test_absolute_path_is_rejected(self):
        self.write_registry(registry_for("/tmp/file.md"))
        with self.assertRaisesRegex(BUILDER.ExportBoundaryError, "ABSOLUTE_PATH_PROHIBITED"):
            BUILDER.build_candidate(self.registry, self.source, self.output)

    def test_path_traversal_is_rejected(self):
        self.write_registry(registry_for("../outside.md"))
        with self.assertRaisesRegex(BUILDER.ExportBoundaryError, "PATH_TRAVERSAL_PROHIBITED"):
            BUILDER.build_candidate(self.registry, self.source, self.output)

    def test_internal_test_path_is_rejected(self):
        self.write_registry(registry_for("tests/test_core.py", "PUBLIC_CLIENT_STUB_CANDIDATE"))
        with self.assertRaisesRegex(BUILDER.ExportBoundaryError, "PRIVATE_PATH_PROHIBITED"):
            BUILDER.build_candidate(self.registry, self.source, self.output)

    def test_core_python_is_rejected(self):
        (self.source / "core.py").write_text("pass\n", encoding="utf-8")
        self.write_registry(registry_for("core.py", "PUBLIC_PROTOCOL"))
        with self.assertRaisesRegex(BUILDER.ExportBoundaryError, "CORE_IMPLEMENTATION_CODE_PROHIBITED"):
            BUILDER.build_candidate(self.registry, self.source, self.output)

    def test_symlink_is_rejected(self):
        (self.source / "docs" / "linked.md").symlink_to(self.source / "docs" / "intro.md")
        self.write_registry(registry_for("docs/linked.md"))
        with self.assertRaisesRegex(BUILDER.ExportBoundaryError, "SOURCE_MUST_BE_REGULAR_NON_SYMLINK_FILE"):
            BUILDER.build_candidate(self.registry, self.source, self.output)

    def test_no_approved_entries_fails_closed(self):
        value = registry_for("docs/intro.md")
        value["entries"][0]["export_allowed"] = False
        self.write_registry(value)
        with self.assertRaisesRegex(BUILDER.ExportBoundaryError, "NO_APPROVED_EXPORT_ENTRIES"):
            BUILDER.build_candidate(self.registry, self.source, self.output)

    def test_output_inside_source_is_rejected(self):
        self.write_registry(registry_for("docs/intro.md"))
        with self.assertRaisesRegex(BUILDER.ExportBoundaryError, "OUTPUT_MUST_BE_OUTSIDE_SOURCE"):
            BUILDER.build_candidate(
                self.registry,
                self.source,
                self.source / "public-candidate",
            )


if __name__ == "__main__":
    unittest.main()
