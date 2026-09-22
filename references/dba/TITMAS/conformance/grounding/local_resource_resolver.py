#!/usr/bin/env python3
"""Deterministic, read-only resource resolution for community contributions.

The resolver binds a candidate reference to one exact frozen Git tree or to an
 explicit isolated candidate copy. It never uses the network, guesses a path,
or turns a local resolution into DBOS Verification, Evidence Truth, adoption,
or authority.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any


ALLOWED_REFERENCE_TYPES = {
    "CURRENT_SNAPSHOT_RESOURCE",
    "CANDIDATE_CREATED_RESOURCE",
    "CANDIDATE_MODIFIED_RESOURCE",
    "REGISTRY_REFERENCE",
    "SCHEMA_REFERENCE",
    "MACHINE_SURFACE_REFERENCE",
}
RESOLUTION_STATUSES = {
    "RESOLVED",
    "NOT_FOUND",
    "AMBIGUOUS",
    "OUT_OF_SCOPE",
    "INVALID_REFERENCE",
    "NOT_ASSESSED",
}
ID_KEYS = {
    "$id",
    "id",
    "document_id",
    "registry_id",
    "schema_id",
    "task_id",
    "role_id",
}
TEXT_SUFFIXES = {".json", ".yaml", ".yml", ".md"}


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def default_created_at() -> str:
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat()


class LocalResourceResolver:
    """Resolve exact references against one frozen repository revision."""

    def __init__(
        self,
        dba_root: Path,
        source_revision: str,
        allowed_source_revision: str,
        allowed_roots: list[str],
        candidate_root: Path | None = None,
        created_at: str | None = None,
    ) -> None:
        self.dba_root = dba_root.resolve()
        self.git_root = self._find_git_root(self.dba_root)
        self.tree_prefix = self.dba_root.relative_to(self.git_root).as_posix()
        self.source_revision = source_revision
        self.allowed_source_revision = allowed_source_revision
        self.allowed_roots = tuple(self._normalize_allowed_root(item) for item in allowed_roots)
        self.candidate_root = candidate_root.resolve() if candidate_root else None
        self.created_at = created_at or default_created_at()
        self._source_valid = self._validate_source_revision()
        self.snapshot_hash = self._snapshot_hash()

    @staticmethod
    def _find_git_root(path: Path) -> Path:
        proc = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(proc.stdout.strip()).resolve()

    @staticmethod
    def _normalize_allowed_root(value: str) -> str:
        normalized, status = LocalResourceResolver.normalize_reference(value)
        if status != "VALID":
            raise ValueError(f"invalid allowed root: {value}")
        return normalized

    @staticmethod
    def normalize_reference(reference: str) -> tuple[str, str]:
        if not isinstance(reference, str) or not reference.strip():
            return "NOT_AVAILABLE", "INVALID_REFERENCE"
        if "\x00" in reference or "\\" in reference:
            return "NOT_AVAILABLE", "INVALID_REFERENCE"
        value = reference.strip()
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", value):
            return value, "VALID"
        pure = PurePosixPath(value)
        if pure.is_absolute() or any(part == ".." for part in pure.parts):
            return "NOT_AVAILABLE", (
                "INVALID_REFERENCE" if pure.is_absolute() else "OUT_OF_SCOPE"
            )
        normalized = pure.as_posix()
        if normalized in {"", "."}:
            return "NOT_AVAILABLE", "INVALID_REFERENCE"
        return normalized, "VALID"

    def _git(self, *args: str, check: bool = False) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.git_root), *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def _validate_source_revision(self) -> bool:
        if self.source_revision != self.allowed_source_revision:
            return False
        proc = self._git("rev-parse", f"{self.source_revision}^{{commit}}")
        return proc.returncode == 0 and proc.stdout.strip() == self.source_revision

    def _snapshot_hash(self) -> str:
        if not self._source_valid:
            return "NOT_ASSESSED"
        proc = self._git("rev-parse", f"{self.source_revision}^{{tree}}")
        if proc.returncode != 0:
            return "NOT_ASSESSED"
        return "git-tree:" + proc.stdout.strip()

    def _is_allowed(self, normalized: str) -> bool:
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", normalized):
            return True
        return any(
            normalized == root or normalized.startswith(root.rstrip("/") + "/")
            for root in self.allowed_roots
        )

    def _tree_path(self, normalized: str) -> str:
        return f"{self.tree_prefix}/{normalized}" if self.tree_prefix else normalized

    def _source_entry(self, normalized: str) -> tuple[bool, str]:
        tree_path = self._tree_path(normalized)
        proc = self._git("ls-tree", self.source_revision, "--", tree_path)
        if proc.returncode != 0 or not proc.stdout.strip():
            return False, "NOT_FOUND"
        line = proc.stdout.strip().splitlines()[0]
        mode = line.split(maxsplit=1)[0]
        if mode == "120000":
            return False, "SYMLINK_PROHIBITED"
        parts = PurePosixPath(tree_path).parts
        for index in range(1, len(parts)):
            parent = PurePosixPath(*parts[:index]).as_posix()
            parent_proc = self._git("ls-tree", self.source_revision, "--", parent)
            if parent_proc.returncode == 0 and parent_proc.stdout.startswith("120000 "):
                return False, "SYMLINK_PROHIBITED"
        return True, "SOURCE_TREE_ENTRY"

    def _candidate_entry(self, normalized: str) -> tuple[bool, str]:
        if self.candidate_root is None:
            return False, "CANDIDATE_ROOT_NOT_PROVIDED"
        candidate = self.candidate_root / normalized
        try:
            resolved = candidate.resolve(strict=False)
            resolved.relative_to(self.candidate_root)
        except (OSError, ValueError):
            return False, "CANDIDATE_PATH_ESCAPE"
        current = self.candidate_root
        for part in PurePosixPath(normalized).parts:
            current = current / part
            if current.is_symlink():
                try:
                    current.resolve(strict=False).relative_to(self.candidate_root)
                except (OSError, ValueError):
                    return False, "CANDIDATE_SYMLINK_ESCAPE"
        return candidate.exists(), (
            "CANDIDATE_ENTRY" if candidate.exists() else "CANDIDATE_ENTRY_NOT_FOUND"
        )

    @staticmethod
    def _json_contains_identifier(value: Any, reference: str) -> bool:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ID_KEYS and child == reference:
                    return True
                if LocalResourceResolver._json_contains_identifier(child, reference):
                    return True
        elif isinstance(value, list):
            return any(
                LocalResourceResolver._json_contains_identifier(item, reference)
                for item in value
            )
        return False

    @staticmethod
    def _text_contains_identifier(text: str, reference: str) -> bool:
        escaped = re.escape(reference)
        pattern = re.compile(
            rf"^\s*(?:-\s*)?(?:\$id|id|document_id|registry_id|schema_id|task_id|role_id)"
            rf"\s*:\s*[\"']?{escaped}[\"']?\s*$",
            re.MULTILINE,
        )
        return bool(pattern.search(text))

    def _source_text_paths(self) -> list[str]:
        paths: list[str] = []
        for root in self.allowed_roots:
            proc = self._git(
                "ls-tree",
                "-r",
                "--name-only",
                self.source_revision,
                "--",
                self._tree_path(root),
            )
            if proc.returncode != 0:
                continue
            for raw in proc.stdout.splitlines():
                rel = raw
                if self.tree_prefix and raw.startswith(self.tree_prefix + "/"):
                    rel = raw[len(self.tree_prefix) + 1 :]
                if Path(rel).suffix.lower() in TEXT_SUFFIXES:
                    paths.append(rel)
        return sorted(set(paths))

    def _read_source_text(self, relative: str) -> str | None:
        proc = self._git(
            "show",
            f"{self.source_revision}:{self._tree_path(relative)}",
        )
        return proc.stdout if proc.returncode == 0 else None

    def _logical_matches(self, reference: str) -> list[str]:
        matches: list[str] = []
        for relative in self._source_text_paths():
            text = self._read_source_text(relative)
            if text is None:
                continue
            found = False
            if relative.endswith(".json"):
                try:
                    found = self._json_contains_identifier(json.loads(text), reference)
                except json.JSONDecodeError:
                    found = False
            if not found:
                found = self._text_contains_identifier(text, reference)
            if found:
                matches.append(relative)
        if self.candidate_root and self.candidate_root.exists():
            for path in sorted(self.candidate_root.rglob("*")):
                if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                    continue
                try:
                    path.resolve().relative_to(self.candidate_root)
                except (OSError, ValueError):
                    continue
                text = path.read_text(encoding="utf-8")
                found = False
                if path.suffix.lower() == ".json":
                    try:
                        found = self._json_contains_identifier(json.loads(text), reference)
                    except json.JSONDecodeError:
                        found = False
                if not found:
                    found = self._text_contains_identifier(text, reference)
                if found:
                    matches.append(
                        "candidate:" + path.relative_to(self.candidate_root).as_posix()
                    )
        return sorted(set(matches))

    def _receipt(
        self,
        reference: str,
        normalized: str,
        reference_type: str,
        required: bool,
        status: str,
        resolved_path: str,
        checks: list[str],
        limitations: list[str],
        reason_code: str,
    ) -> dict[str, Any]:
        if status not in RESOLUTION_STATUSES:
            raise ValueError(f"unsupported status {status}")
        identity = {
            "reference": reference,
            "normalized_reference": normalized,
            "reference_type": reference_type,
            "status": status,
            "source_revision": self.source_revision,
            "snapshot_hash": self.snapshot_hash,
        }
        return {
            "resolution_id": "RR-" + sha256_text(canonical(identity)).split(":", 1)[1][:20],
            **identity,
            "required_for_candidate": required,
            "resolved_path": resolved_path,
            "checks_performed": checks,
            "limitations": limitations,
            "reason_code": reason_code,
            "created_at": self.created_at,
            "dbos_verification": False,
            "evidence_truth": False,
            "canonical_existence_authority": False,
        }

    def resolve(
        self,
        reference: str,
        reference_type: str,
        required_for_candidate: bool,
    ) -> dict[str, Any]:
        checks = [
            "SOURCE_REVISION_EXACT_MATCH",
            "REFERENCE_NORMALIZATION",
            "ALLOWED_ROOT_CHECK",
            "SYMLINK_ESCAPE_CHECK",
            "EXACT_EXISTENCE_CHECK",
        ]
        limitations = [
            "LOCAL_FROZEN_SNAPSHOT_ONLY",
            "NO_NETWORK_OR_PRIVATE_REPOSITORY_LOOKUP",
            "RESOURCE_RESOLUTION_RECEIPT_NE_DBOS_VERIFICATION",
            "RESOURCE_RESOLUTION_RECEIPT_NE_EVIDENCE_TRUTH",
            "LOCAL_SNAPSHOT_RESOLUTION_NE_CANONICAL_EXISTENCE_AUTHORITY",
        ]
        normalized, normalized_status = self.normalize_reference(reference)
        if reference_type not in ALLOWED_REFERENCE_TYPES:
            return self._receipt(
                reference, normalized, reference_type, required_for_candidate,
                "INVALID_REFERENCE", "NOT_AVAILABLE", checks, limitations,
                "REFERENCE_TYPE_UNSUPPORTED",
            )
        if normalized_status != "VALID":
            return self._receipt(
                reference, normalized, reference_type, required_for_candidate,
                normalized_status, "NOT_AVAILABLE", checks, limitations,
                "REFERENCE_NORMALIZATION_FAILED",
            )
        if not self._source_valid:
            return self._receipt(
                reference, normalized, reference_type, required_for_candidate,
                "NOT_ASSESSED", "NOT_AVAILABLE", checks, limitations,
                "SOURCE_REVISION_MISMATCH",
            )
        is_logical = bool(
            re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", normalized)
        ) or (
            reference_type in {"REGISTRY_REFERENCE", "SCHEMA_REFERENCE"}
            and "/" not in normalized
        )
        if is_logical:
            matches = self._logical_matches(normalized)
            if len(matches) == 1:
                return self._receipt(
                    reference, normalized, reference_type, required_for_candidate,
                    "RESOLVED", matches[0], checks + ["EXACT_IDENTIFIER_LOOKUP"],
                    limitations, "EXACT_IDENTIFIER_RESOLVED",
                )
            if len(matches) > 1:
                return self._receipt(
                    reference, normalized, reference_type, required_for_candidate,
                    "AMBIGUOUS", "NOT_AVAILABLE", checks + ["EXACT_IDENTIFIER_LOOKUP"],
                    limitations, "MULTIPLE_EXACT_IDENTIFIER_MATCHES",
                )
            return self._receipt(
                reference, normalized, reference_type, required_for_candidate,
                "NOT_FOUND", "NOT_AVAILABLE", checks + ["EXACT_IDENTIFIER_LOOKUP"],
                limitations, "EXACT_IDENTIFIER_NOT_FOUND",
            )
        if not self._is_allowed(normalized):
            return self._receipt(
                reference, normalized, reference_type, required_for_candidate,
                "OUT_OF_SCOPE", "NOT_AVAILABLE", checks, limitations,
                "REFERENCE_OUTSIDE_ALLOWED_ROOTS",
            )
        source_exists, source_reason = self._source_entry(normalized)
        candidate_exists, candidate_reason = self._candidate_entry(normalized)
        if "SYMLINK" in source_reason or "ESCAPE" in candidate_reason:
            return self._receipt(
                reference, normalized, reference_type, required_for_candidate,
                "OUT_OF_SCOPE", "NOT_AVAILABLE", checks, limitations,
                source_reason if "SYMLINK" in source_reason else candidate_reason,
            )
        resolved = False
        reason = "REFERENCE_NOT_FOUND"
        resolved_path = "NOT_AVAILABLE"
        if reference_type == "CURRENT_SNAPSHOT_RESOURCE":
            resolved = source_exists
            reason = source_reason
        elif reference_type == "CANDIDATE_CREATED_RESOURCE":
            resolved = candidate_exists and not source_exists
            reason = (
                "CANDIDATE_CREATED_RESOURCE_RESOLVED"
                if resolved else "CANDIDATE_CREATED_RESOURCE_CONDITION_FAILED"
            )
        elif reference_type == "CANDIDATE_MODIFIED_RESOURCE":
            resolved = candidate_exists and source_exists
            reason = (
                "CANDIDATE_MODIFIED_RESOURCE_RESOLVED"
                if resolved else "CANDIDATE_MODIFIED_RESOURCE_CONDITION_FAILED"
            )
        else:
            resolved = candidate_exists or source_exists
            reason = candidate_reason if candidate_exists else source_reason
        if resolved:
            resolved_path = (
                "candidate:" + normalized
                if candidate_exists and reference_type != "CURRENT_SNAPSHOT_RESOURCE"
                else normalized
            )
        return self._receipt(
            reference,
            normalized,
            reference_type,
            required_for_candidate,
            "RESOLVED" if resolved else "NOT_FOUND",
            resolved_path,
            checks,
            limitations,
            reason,
        )


__all__ = [
    "ALLOWED_REFERENCE_TYPES",
    "LocalResourceResolver",
    "RESOLUTION_STATUSES",
]
