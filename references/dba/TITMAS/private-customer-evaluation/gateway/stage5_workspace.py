#!/usr/bin/env python3
"""Explicit customer copy boundary for Stage 5 protocol and SDK assets."""

from __future__ import annotations

import shutil
from pathlib import Path


FORBIDDEN_MARKERS = (
    "/Users/",
    "/private/tmp/",
    "GatewayService",
    "capture_response",
    "source-classification-registry",
)


def install_stage5_customer_assets(
    project_root: Path,
    customer_root: Path,
) -> dict[str, Path]:
    source_surface = project_root / "TITMAS" / "private-stage5-protocol-surface"
    source_sdk = project_root / "TITMAS" / "private-stage5-sdk" / "python"
    if not source_surface.is_dir() or not source_sdk.is_dir():
        raise ValueError("Stage 5 customer assets are incomplete")
    target_surface = customer_root / "stage5-protocol"
    target_sdk = customer_root / "stage5-sdk-python"
    target_surface.mkdir(mode=0o700)
    target_sdk.mkdir(mode=0o700)

    for source in sorted(source_surface.rglob("*")):
        if source.is_symlink():
            raise ValueError("Stage 5 surface symlink is prohibited")
        relative = source.relative_to(source_surface)
        target = target_surface / relative
        if source.is_dir():
            target.mkdir(exist_ok=True, mode=0o700)
        elif source.is_file():
            if source.suffix not in {".json", ".md"}:
                raise ValueError("Stage 5 surface contains unsupported file")
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            shutil.copyfile(source, target)
            target.chmod(0o600)

    sdk_allowlist = ("titmas_stage5_sdk.py", "README.md")
    for name in sdk_allowlist:
        source = source_sdk / name
        if source.is_symlink() or not source.is_file():
            raise ValueError("Stage 5 SDK allowlist is incomplete")
        target = target_sdk / name
        shutil.copyfile(source, target)
        target.chmod(0o600)

    findings = inspect_stage5_customer_assets(target_surface, target_sdk)
    if any(findings.values()):
        raise ValueError(f"Stage 5 customer asset disclosure: {findings}")
    return {
        "protocol_surface": target_surface,
        "sdk": target_sdk,
    }


def inspect_stage5_customer_assets(
    protocol_surface: Path,
    sdk_root: Path,
) -> dict[str, int]:
    files = [
        path
        for root in (protocol_surface, sdk_root)
        for path in root.rglob("*")
        if path.is_file()
    ]
    private_paths = 0
    core_symbols = 0
    symlinks = 0
    unexpected_python = 0
    for path in files:
        symlinks += int(path.is_symlink())
        if path.suffix == ".py" and path.name != "titmas_stage5_sdk.py":
            unexpected_python += 1
        text = path.read_text(encoding="utf-8")
        private_paths += int(any(marker in text for marker in FORBIDDEN_MARKERS[:2]))
        core_symbols += int(any(marker in text for marker in FORBIDDEN_MARKERS[2:]))
    return {
        "STAGE5_CUSTOMER_PRIVATE_PATH_FINDINGS": private_paths,
        "STAGE5_CUSTOMER_CORE_SYMBOL_FINDINGS": core_symbols,
        "STAGE5_CUSTOMER_SYMLINK_FINDINGS": symlinks,
        "STAGE5_CUSTOMER_UNEXPECTED_PYTHON_FINDINGS": unexpected_python,
    }
