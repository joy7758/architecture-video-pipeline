#!/usr/bin/env python3
"""Build a reviewed public-surface candidate from an explicit allowlist.

This tool is local and deterministic. It does not publish, create a repository,
copy Git history, call a Provider, or make a file public.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path, PurePosixPath
from typing import Any


PUBLIC_CLASSIFICATIONS = {
    "PUBLIC_PROTOCOL",
    "PUBLIC_DOCUMENTATION",
    "PUBLIC_SYNTHETIC_EXAMPLE",
    "PUBLIC_CLIENT_STUB_CANDIDATE",
}
APPROVED = "APPROVED"
BLOCKED_PARTS = {
    ".git",
    ".github",
    "commercialization",
    "private-customer-evaluation",
    "private-governance",
    "tests",
    "__pycache__",
}
BLOCKED_FRAGMENTS = {
    "provider",
    "credential",
    "secret",
    "customer-data",
    "production-evidence",
    "response_capture",
    "conformance/harness",
}


class ExportBoundaryError(ValueError):
    """A stable, fail-closed public export boundary error."""


def _safe_relative_path(raw: str) -> PurePosixPath:
    if not isinstance(raw, str) or not raw:
        raise ExportBoundaryError("PATH_EMPTY")
    path = PurePosixPath(raw)
    if path.is_absolute():
        raise ExportBoundaryError("ABSOLUTE_PATH_PROHIBITED")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ExportBoundaryError("PATH_TRAVERSAL_PROHIBITED")
    if any(part.lower() in BLOCKED_PARTS for part in path.parts):
        raise ExportBoundaryError("PRIVATE_PATH_PROHIBITED")
    lowered = raw.lower()
    if any(fragment in lowered for fragment in BLOCKED_FRAGMENTS):
        raise ExportBoundaryError("CORE_OR_SENSITIVE_PATH_PROHIBITED")
    return path


def _load_registry(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ExportBoundaryError("REGISTRY_NOT_REGULAR_FILE")
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("default_classification") != "UNCLASSIFIED":
        raise ExportBoundaryError("DEFAULT_CLASSIFICATION_MUST_BE_UNCLASSIFIED")
    if value.get("unclassified_export_allowed") is not False:
        raise ExportBoundaryError("UNCLASSIFIED_MUST_NOT_EXPORT")
    policy = value.get("publication_policy", {})
    required = {
        "allowlist_only_export": True,
        "publication_by_reconstruction": True,
        "full_repository_copy_prohibited": True,
        "git_history_export_prohibited": True,
    }
    if any(policy.get(key) is not expected for key, expected in required.items()):
        raise ExportBoundaryError("PUBLICATION_POLICY_INVALID")
    return value


def _approved_entry(entry: dict[str, Any]) -> PurePosixPath:
    classification = entry.get("classification", "UNCLASSIFIED")
    if classification not in PUBLIC_CLASSIFICATIONS:
        raise ExportBoundaryError("CLASSIFICATION_NOT_PUBLIC")
    if entry.get("export_allowed") is not True:
        raise ExportBoundaryError("EXPORT_NOT_ALLOWED")
    for field in (
        "legal_review_status",
        "commercial_review_status",
        "security_review_status",
        "license_status",
    ):
        if entry.get(field) != APPROVED:
            raise ExportBoundaryError(f"{field.upper()}_NOT_APPROVED")
    path = _safe_relative_path(entry.get("path", ""))
    if path.suffix == ".py" and (
        classification != "PUBLIC_CLIENT_STUB_CANDIDATE"
        or path.parts[0] != "public-client-stubs"
    ):
        raise ExportBoundaryError("CORE_IMPLEMENTATION_CODE_PROHIBITED")
    return path


def build_candidate(registry_path: Path, source_root: Path, output_root: Path) -> dict[str, Any]:
    """Build a local candidate or fail closed before copying unauthorized data."""

    source = source_root.resolve()
    output = output_root.resolve()
    if source == output or output.is_relative_to(source):
        raise ExportBoundaryError("OUTPUT_MUST_BE_OUTSIDE_SOURCE")
    if (source / ".git").exists() and output.name == source.name:
        raise ExportBoundaryError("FULL_REPOSITORY_COPY_PROHIBITED")

    registry = _load_registry(registry_path.resolve())
    approved: list[tuple[PurePosixPath, dict[str, Any]]] = []
    for entry in registry.get("entries", []):
        if entry.get("export_allowed") is True:
            approved.append((_approved_entry(entry), entry))
    if not approved:
        raise ExportBoundaryError("NO_APPROVED_EXPORT_ENTRIES")
    if output.exists():
        raise ExportBoundaryError("OUTPUT_ALREADY_EXISTS")

    prepared: list[tuple[Path, Path, str]] = []
    for relative, _entry in approved:
        unresolved_source_path = source / Path(*relative.parts)
        if unresolved_source_path.is_symlink():
            raise ExportBoundaryError("SOURCE_MUST_BE_REGULAR_NON_SYMLINK_FILE")
        source_path = unresolved_source_path.resolve()
        if not source_path.is_relative_to(source):
            raise ExportBoundaryError("SOURCE_PATH_ESCAPES_ROOT")
        if not source_path.is_file():
            raise ExportBoundaryError("SOURCE_MUST_BE_REGULAR_NON_SYMLINK_FILE")
        destination = output / Path(*relative.parts)
        digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
        prepared.append((source_path, destination, digest))

    output.mkdir(parents=True)
    files: list[dict[str, str]] = []
    for source_path, destination, digest in prepared:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination)
        files.append({
            "path": destination.relative_to(output).as_posix(),
            "sha256": digest,
        })
    manifest = {
        "candidate_only": True,
        "published": False,
        "source_registry": registry_path.name,
        "files": files,
    }
    (output / "public-surface-candidate-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    manifest = build_candidate(args.registry, args.source_root, args.output_root)
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
