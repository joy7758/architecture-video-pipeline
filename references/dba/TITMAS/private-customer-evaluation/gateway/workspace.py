#!/usr/bin/env python3
"""Fail-closed temporary workspace isolation for private customer evaluation."""

from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


CUSTOMER_BUNDLE_FILES = (
    "README.md",
    "agent-service-discovery.json",
    "api-contract.json",
    "black-box-validation.md",
    "error-codes.json",
    "evaluation-task.md",
    "human-accountability.md",
    "synthetic-request.json",
    "synthetic-response.json",
)

PRIVATE_PATH_MARKERS = (
    "/Users/",
    "/private/tmp/",
    "\\Users\\",
)


@dataclass
class IsolatedWorkspaces:
    """Two temporary roots with an explicit one-way customer copy boundary."""

    core_handle: tempfile.TemporaryDirectory[str]
    customer_handle: tempfile.TemporaryDirectory[str]
    core_root: Path
    customer_root: Path
    capture_directory: Path
    customer_bundle: Path
    customer_results: Path

    def cleanup(self) -> None:
        self.customer_handle.cleanup()
        self.core_handle.cleanup()


def create_isolated_workspaces(bundle_source: Path) -> IsolatedWorkspaces:
    """Create isolated roots and copy only the public contract allowlist."""

    source = bundle_source.resolve()
    missing = [name for name in CUSTOMER_BUNDLE_FILES if not (source / name).is_file()]
    if missing:
        raise ValueError("customer bundle allowlist is incomplete")

    core_handle = tempfile.TemporaryDirectory(prefix="titmas-core-service-")
    customer_handle = tempfile.TemporaryDirectory(prefix="titmas-customer-")
    core_root = Path(core_handle.name)
    customer_root = Path(customer_handle.name)
    capture_directory = core_root / "response-capture"
    customer_bundle = customer_root / "bundle"
    customer_results = customer_root / "results"
    capture_directory.mkdir(mode=0o700)
    customer_bundle.mkdir(mode=0o700)
    customer_results.mkdir(mode=0o700)

    for name in CUSTOMER_BUNDLE_FILES:
        shutil.copyfile(source / name, customer_bundle / name)

    return IsolatedWorkspaces(
        core_handle=core_handle,
        customer_handle=customer_handle,
        core_root=core_root,
        customer_root=customer_root,
        capture_directory=capture_directory,
        customer_bundle=customer_bundle,
        customer_results=customer_results,
    )


def inspect_customer_workspace(customer_root: Path) -> dict[str, int]:
    """Return bounded disclosure counts for the customer-visible workspace."""

    root = customer_root.resolve()
    files = [path for path in root.rglob("*") if path.is_file()]
    directories = [path for path in root.rglob("*") if path.is_dir()]
    core_source = sum(path.suffix in {".py", ".pyc", ".so"} for path in files)
    internal_tests = sum(
        "test" in path.name.lower() or "tests" in path.parts
        for path in files
    )
    git_metadata = sum(path.name == ".git" for path in files + directories)
    private_paths = 0
    for path in files:
        try:
            rendered = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(marker in rendered for marker in PRIVATE_PATH_MARKERS):
            private_paths += 1
    return {
        "CUSTOMER_WORKSPACE_CORE_SOURCE_COUNT": core_source,
        "CUSTOMER_WORKSPACE_INTERNAL_TEST_COUNT": internal_tests,
        "CUSTOMER_WORKSPACE_GIT_METADATA_COUNT": git_metadata,
        "CUSTOMER_WORKSPACE_PRIVATE_PATH_COUNT": private_paths,
    }
