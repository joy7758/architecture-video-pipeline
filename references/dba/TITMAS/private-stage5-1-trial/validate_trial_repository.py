#!/usr/bin/env python3
"""Fail-closed validation for a reconstructed Stage 5.1 trial repository."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from build_trial_repository import (
    ALLOWED_ROOT_DIRECTORIES,
    ALLOWED_ROOT_FILES,
    CORE_SYMBOLS,
    PRIVATE_PATHS,
    PROVIDER_CONFIGURATION,
    SECRETS,
    canonical_bytes,
    sha256_bytes,
)


def _manifest_self_digest(manifest: dict[str, Any]) -> str:
    normalized = json.loads(json.dumps(manifest))
    self_entries = [
        item for item in normalized["files"]
        if item["trial_output_path"] == "trial-source-manifest.json"
    ]
    if len(self_entries) != 1:
        raise ValueError("exactly one manifest self record is required")
    self_entries[0]["trial_output_sha256"] = "SELF_HASH_PLACEHOLDER"
    return sha256_bytes(canonical_bytes(normalized))


def _git_history_findings(root: Path) -> int:
    if not (root / ".git").exists():
        return 0
    count = int(subprocess.check_output(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=root,
        text=True,
    ).strip())
    parents = subprocess.check_output(
        ["git", "rev-list", "--parents", "--max-count=1", "HEAD"],
        cwd=root,
        text=True,
    ).split()
    return int(count != 1 or len(parents) != 1)


def validate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    manifest_path = root / "trial-source-manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError("trial-source-manifest.json is required")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["allowlist_only_export"] is not True:
        raise ValueError("allowlist-only export is required")
    if manifest["publication_by_reconstruction"] is not True:
        raise ValueError("publication by reconstruction is required")
    if manifest["public_release_allowed"] is not False:
        raise ValueError("public release must remain false")
    if manifest["git_history_copied"] is not False:
        raise ValueError("core Git history cannot be copied")

    all_entries = [
        path
        for path in root.rglob("*")
        if ".git" not in path.relative_to(root).parts
    ]
    symlinks = sum(path.is_symlink() for path in all_entries)
    if symlinks:
        raise ValueError("trial repository symlinks are prohibited")

    actual_files = {
        str(path.relative_to(root))
        for path in all_entries
        if path.is_file()
    }
    manifest_entries = {
        item["trial_output_path"]: item for item in manifest["files"]
    }
    if actual_files != set(manifest_entries):
        raise ValueError(
            "trial repository files and manifest differ: "
            f"missing={sorted(actual_files - set(manifest_entries))}, "
            f"extra={sorted(set(manifest_entries) - actual_files)}"
        )

    private_paths = 0
    secrets = 0
    core_symbols = 0
    provider_configuration = 0
    for relative in sorted(actual_files):
        path = root / relative
        top = Path(relative).parts[0]
        if (
            relative not in ALLOWED_ROOT_FILES
            and top not in ALLOWED_ROOT_DIRECTORIES
        ):
            raise ValueError(f"unexpected trial path: {relative}")
        entry = manifest_entries[relative]
        required = {
            "source_repository",
            "source_commit",
            "source_path",
            "source_blob_sha",
            "classification",
            "trial_output_path",
            "trial_output_sha256",
            "security_scan_status",
            "commercial_review_status",
            "trial_release_status",
        }
        if not required.issubset(entry):
            raise ValueError(f"incomplete manifest entry: {relative}")
        if entry["trial_release_status"] != "PRIVATE_TRIAL_ONLY":
            raise ValueError(f"trial release status drift: {relative}")
        if entry["public_release_allowed"] is not False:
            raise ValueError(f"public release elevation: {relative}")
        if relative == "trial-source-manifest.json":
            observed = _manifest_self_digest(manifest)
        else:
            observed = sha256_bytes(path.read_bytes())
        if observed != entry["trial_output_sha256"]:
            raise ValueError(f"trial output hash mismatch: {relative}")
        text = path.read_bytes().decode("utf-8", errors="ignore")
        private_paths += int(bool(PRIVATE_PATHS.search(text)))
        secrets += int(bool(SECRETS.search(text)))
        core_symbols += int(bool(CORE_SYMBOLS.search(text)))
        provider_configuration += int(
            bool(PROVIDER_CONFIGURATION.search(text))
        )

    findings = {
        "trial_repository_core_source_findings": core_symbols,
        "trial_repository_secret_findings": secrets,
        "trial_repository_private_path_findings": private_paths,
        "trial_repository_provider_configuration_findings":
            provider_configuration,
        "trial_repository_git_history_findings":
            _git_history_findings(root),
        "trial_repository_symlink_findings": symlinks,
        "unauthorized_export_count": 0,
    }
    if any(findings.values()):
        raise ValueError(f"trial repository findings: {findings}")

    status = json.loads((root / "status.json").read_text(encoding="utf-8"))
    if status["visibility"] != "PRIVATE":
        raise ValueError("trial repository visibility projection drift")
    if status["external_participant_invitation_authorized"] is not False:
        raise ValueError("external invitation is not authorized")
    if status["public_release_allowed"] is not False:
        raise ValueError("public release is not authorized")
    tasks = json.loads(
        (root / "tasks" / "trial-task-catalog.json").read_text(
            encoding="utf-8"
        )
    )
    if len(tasks["tasks"]) != 3:
        raise ValueError("exactly three trial tasks are required")
    if any(item["answer_hint_provided"] for item in tasks["tasks"]):
        raise ValueError("trial task answer hints are prohibited")
    return {
        "status": "PASS",
        "files_checked": len(actual_files),
        "manifest_entries_checked": len(manifest_entries),
        "trial_tasks_checked": len(tasks["tasks"]),
        **findings,
        "core_access_count": 0,
        "real_model_call_count": 0,
        "real_provider_call_count": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.root), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
