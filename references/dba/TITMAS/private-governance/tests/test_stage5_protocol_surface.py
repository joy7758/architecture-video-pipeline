#!/usr/bin/env python3
"""Private Stage 5 protocol-surface reconstruction tests."""

from __future__ import annotations

import importlib.util
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "build_stage5_protocol_surface.py"
SPEC = importlib.util.spec_from_file_location("stage5_surface_builder", MODULE_PATH)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = BUILDER
SPEC.loader.exec_module(BUILDER)
CANONICAL_OUTPUT_ROOT = BUILDER.OUTPUT_ROOT


def build_in_isolated_output(test_case_class, build=None):
    """Build the surface without leaking temporary output state.

    ``addClassCleanup`` is intentional: unittest runs these cleanups even when
    ``setUpClass`` raises, whereas ``tearDownClass`` is not guaranteed to run.
    """

    build = build or BUILDER.build
    test_case_class.tracked_output_root = BUILDER.OUTPUT_ROOT
    test_case_class.temporary_directory = tempfile.TemporaryDirectory(
        prefix="titmas-stage5-protocol-surface-"
    )
    test_case_class.temporary_directory_path = Path(
        test_case_class.temporary_directory.name
    )
    test_case_class.addClassCleanup(test_case_class.temporary_directory.cleanup)

    BUILDER.OUTPUT_ROOT = (
        test_case_class.temporary_directory_path
        / "private-stage5-protocol-surface"
    )
    test_case_class.addClassCleanup(
        setattr,
        BUILDER,
        "OUTPUT_ROOT",
        test_case_class.tracked_output_root,
    )
    return build()


class Stage5ProtocolSurfaceCleanupTests(unittest.TestCase):
    @staticmethod
    def run_probe(build):
        class IsolatedBuildProbe(unittest.TestCase):
            @classmethod
            def setUpClass(cls) -> None:
                cls.manifest = build_in_isolated_output(cls, build)

            def test_build_completed(self) -> None:
                self.assertIsInstance(self.manifest, dict)

        result = unittest.TestResult()
        unittest.defaultTestLoader.loadTestsFromTestCase(IsolatedBuildProbe).run(
            result
        )
        return IsolatedBuildProbe, result

    def test_d25_t01_normal_build_restores_output_root(self) -> None:
        _probe, result = self.run_probe(BUILDER.build)
        self.assertTrue(result.wasSuccessful(), result.errors)
        self.assertEqual(CANONICAL_OUTPUT_ROOT, BUILDER.OUTPUT_ROOT)

    def test_d25_t02_build_exception_restores_output_root(self) -> None:
        def controlled_failure():
            raise RuntimeError("D25 controlled build failure")

        _probe, result = self.run_probe(controlled_failure)
        self.assertEqual(1, len(result.errors))
        self.assertIn("D25 controlled build failure", result.errors[0][1])
        self.assertEqual(CANONICAL_OUTPUT_ROOT, BUILDER.OUTPUT_ROOT)

    def test_d25_t03_normal_build_cleans_temporary_directory(self) -> None:
        probe, result = self.run_probe(BUILDER.build)
        self.assertTrue(result.wasSuccessful(), result.errors)
        self.assertFalse(probe.temporary_directory_path.exists())

    def test_d25_t04_build_exception_cleans_temporary_directory(self) -> None:
        def controlled_failure():
            raise RuntimeError("D25 controlled build failure")

        probe, result = self.run_probe(controlled_failure)
        self.assertEqual(1, len(result.errors))
        self.assertIn("D25 controlled build failure", result.errors[0][1])
        self.assertFalse(probe.temporary_directory_path.exists())

    def test_d25_t05_subsequent_test_sees_canonical_output_root(self) -> None:
        self.assertEqual(CANONICAL_OUTPUT_ROOT, BUILDER.OUTPUT_ROOT)


class Stage5ProtocolSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = build_in_isolated_output(cls)

    def test_generated_surface_matches_tracked_expected_bytes(self) -> None:
        generated_files = {
            path.relative_to(BUILDER.OUTPUT_ROOT)
            for path in BUILDER.OUTPUT_ROOT.rglob("*")
            if path.is_file()
        }
        tracked_files = {
            path.relative_to(self.tracked_output_root)
            for path in self.tracked_output_root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(tracked_files, generated_files)
        for relative in sorted(generated_files):
            self.assertEqual(
                (self.tracked_output_root / relative).read_bytes(),
                (BUILDER.OUTPUT_ROOT / relative).read_bytes(),
                str(relative),
            )

    def test_manifest_is_private_and_default_deny(self) -> None:
        self.assertFalse(self.manifest["public_release_allowed"])
        self.assertTrue(self.manifest["private_stage_5_use_allowed"])
        self.assertFalse(self.manifest["git_tracking_default"])

    def test_every_payload_is_hash_and_source_bound(self) -> None:
        for entry in self.manifest["files"]:
            path = BUILDER.OUTPUT_ROOT / entry["path"]
            self.assertEqual(
                entry["output_sha256"], BUILDER.sha256_bytes(path.read_bytes())
            )
            self.assertRegex(entry["source_blob_sha"], r"^[0-9a-f]{40}$")
            self.assertFalse(entry["public_release_allowed"])

    def test_surface_contains_only_allowed_extensions(self) -> None:
        for path in BUILDER.OUTPUT_ROOT.rglob("*"):
            if path.is_file():
                self.assertIn(path.suffix, {".json", ".md"})
                self.assertFalse(path.is_symlink())

    def test_surface_scans_are_zero(self) -> None:
        self.assertEqual(
            {
                "protocol_surface_core_source_findings": 0,
                "protocol_surface_private_path_findings": 0,
                "protocol_surface_secret_findings": 0,
                "protocol_surface_symlink_findings": 0,
            },
            self.manifest["findings"],
        )

    def test_generated_permissions_are_private(self) -> None:
        self.assertEqual(
            0o700, stat.S_IMODE(BUILDER.OUTPUT_ROOT.stat().st_mode)
        )
        for path in BUILDER.OUTPUT_ROOT.rglob("*"):
            expected = 0o700 if path.is_dir() else 0o600
            self.assertEqual(expected, stat.S_IMODE(path.stat().st_mode))

    def test_no_private_implementation_payload(self) -> None:
        names = {
            path.name for path in BUILDER.OUTPUT_ROOT.rglob("*") if path.is_file()
        }
        self.assertNotIn("harness.py", names)
        self.assertNotIn("response_capture.py", names)
        self.assertNotIn("service.py", names)


if __name__ == "__main__":
    unittest.main()
