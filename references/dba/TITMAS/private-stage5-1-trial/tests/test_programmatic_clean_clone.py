#!/usr/bin/env python3

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
TRIAL_ROOT = PROJECT_ROOT / "TITMAS" / "private-stage5-1-trial"
sys.path.insert(0, str(TRIAL_ROOT))

import build_trial_repository
import run_clean_clone_trial


class ProgrammaticCleanCloneTests(unittest.TestCase):
    def test_clean_clone_sdk_and_sandbox_cycle(self):
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=PROJECT_ROOT,
            text=True,
        ).strip()
        with tempfile.TemporaryDirectory(
            prefix="titmas-stage51-program-"
        ) as raw:
            root = Path(raw)
            repository = root / "repository"
            build_trial_repository.build(repository, revision)
            subprocess.run(["git", "init", "-b", "main"], cwd=repository, check=True)
            subprocess.run(
                ["git", "config", "user.name", "TITMAS Test"],
                cwd=repository,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@invalid.example"],
                cwd=repository,
                check=True,
            )
            subprocess.run(["git", "add", "."], cwd=repository, check=True)
            subprocess.run(
                ["git", "commit", "-m", "initial private trial package"],
                cwd=repository,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            trial_revision = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=repository,
                text=True,
            ).strip()
            report = run_clean_clone_trial.run(
                PROJECT_ROOT,
                str(repository),
                root / "report.json",
                expected_revision=trial_revision,
            )
            self.assertEqual("PASS", report["private_trial_clean_clone"])
            self.assertEqual("PASS", report["trial_sdk_install"])
            self.assertEqual("PASS", report["trial_task_discovery"])
            self.assertEqual("PASS", report["trial_contribution_preflight"])
            self.assertEqual("PASS", report["trial_sandbox_submission"])
            self.assertEqual("PASS", report["trial_conformance_result"])
            self.assertEqual(
                "CONFORMANCE_FAIL", report["invalid_test_vector"]
            )
            self.assertEqual(0, report["core_access_count"])
            self.assertEqual(0, report["real_model_call_count"])


if __name__ == "__main__":
    unittest.main()
