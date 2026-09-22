"""Load an R1 Enterprise Evaluation Profile from the frozen R0 schema.

This module is dependency-free.  It consumes the canonical JSON Schema instead
of restating EEP fields in Python, and it fails closed on unsupported input.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


DBA_ROOT = Path(__file__).resolve().parents[4]
EEP_SCHEMA_PATH = (
    DBA_ROOT
    / "docs"
    / "enterprise-agent-evaluation"
    / "02_ENTERPRISE_EVALUATION_PROFILE.schema.json"
)
MAX_JSON_BYTES = 1_000_000


class ContractValidationError(ValueError):
    """The supplied contract or instance failed closed."""


def canonical_json_bytes(value: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes for hashing and comparison."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def document_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def load_json_object(path: Path) -> dict[str, Any]:
    resolved = path.resolve()
    if path.is_symlink() or not path.is_file():
        raise ContractValidationError(f"{path}: expected a regular non-symlink file")
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ContractValidationError(f"{path}: exceeds {MAX_JSON_BYTES} bytes")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractValidationError(f"{resolved}: invalid JSON") from exc
    if not isinstance(value, dict):
        raise ContractValidationError(f"{resolved}: top-level JSON must be an object")
    return value


def _matches_type(value: Any, expected: str) -> bool:
    mapping = {
        "object": dict,
        "array": list,
        "string": str,
        "boolean": bool,
        "integer": int,
        "number": (int, float),
        "null": type(None),
    }
    if expected not in mapping:
        raise ContractValidationError(f"unsupported schema type {expected!r}")
    if expected in {"integer", "number"} and isinstance(value, bool):
        return False
    return isinstance(value, mapping[expected])


def _resolve_local_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ContractValidationError(f"external schema reference is not allowed: {reference}")
    node: Any = root_schema
    for part in reference[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            raise ContractValidationError(f"unresolved schema reference: {reference}")
        node = node[part]
    if not isinstance(node, dict):
        raise ContractValidationError(f"schema reference is not an object: {reference}")
    return node


def validate_document(
    value: Any,
    schema: dict[str, Any],
    *,
    root_schema: dict[str, Any] | None = None,
    location: str = "$",
) -> None:
    """Validate the subset of Draft 2020-12 used by the frozen EEP/ESP schemas."""

    root_schema = root_schema or schema
    if "$ref" in schema:
        validate_document(
            value,
            _resolve_local_ref(root_schema, schema["$ref"]),
            root_schema=root_schema,
            location=location,
        )
        return

    expected = schema.get("type")
    if isinstance(expected, str) and not _matches_type(value, expected):
        raise ContractValidationError(f"{location}: expected {expected}")
    if isinstance(expected, list) and not any(_matches_type(value, item) for item in expected):
        raise ContractValidationError(f"{location}: expected one of {expected}")
    if "enum" in schema and value not in schema["enum"]:
        raise ContractValidationError(f"{location}: value is outside enum")
    if "const" in schema and value != schema["const"]:
        raise ContractValidationError(f"{location}: value does not match const")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ContractValidationError(f"{location}: shorter than minLength")
        if len(value) > schema.get("maxLength", MAX_JSON_BYTES):
            raise ContractValidationError(f"{location}: longer than maxLength")
        if schema.get("pattern") and re.fullmatch(schema["pattern"], value) is None:
            raise ContractValidationError(f"{location}: does not match pattern")
        if schema.get("format") == "date-time":
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as exc:
                raise ContractValidationError(f"{location}: invalid date-time") from exc

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", value):
            raise ContractValidationError(f"{location}: below minimum")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ContractValidationError(f"{location}: fewer than minItems")
        if len(value) > schema.get("maxItems", MAX_JSON_BYTES):
            raise ContractValidationError(f"{location}: more than maxItems")
        if schema.get("uniqueItems"):
            encoded = [canonical_json_bytes(item) for item in value]
            if len(encoded) != len(set(encoded)):
                raise ContractValidationError(f"{location}: items are not unique")
        if "items" in schema:
            for index, item in enumerate(value):
                validate_document(
                    item,
                    schema["items"],
                    root_schema=root_schema,
                    location=f"{location}[{index}]",
                )
        if "contains" in schema:
            matched = False
            for item in value:
                try:
                    validate_document(item, schema["contains"], root_schema=root_schema)
                except ContractValidationError:
                    continue
                matched = True
                break
            if not matched:
                raise ContractValidationError(f"{location}: contains condition not met")

    if isinstance(value, dict):
        missing = sorted(set(schema.get("required", [])) - set(value))
        if missing:
            raise ContractValidationError(f"{location}: missing required fields {missing}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise ContractValidationError(f"{location}: additional properties {extra}")
        for key, child_schema in properties.items():
            if key in value:
                validate_document(
                    value[key],
                    child_schema,
                    root_schema=root_schema,
                    location=f"{location}.{key}",
                )

    for child_schema in schema.get("allOf", []):
        validate_document(
            value,
            child_schema,
            root_schema=root_schema,
            location=location,
        )


def load_profile(path: Path, schema_path: Path = EEP_SCHEMA_PATH) -> dict[str, Any]:
    schema = load_json_object(schema_path)
    document = load_json_object(path)
    validate_document(document, schema)
    weights = document["evaluation_weights"]
    if sum(weights.values()) != 100:
        raise ContractValidationError("$.evaluation_weights: weights must total 100")
    return {
        "document": document,
        "profile_id": document["profile_id"],
        "profile_version": document["profile_version"],
        "profile_digest": document_digest(document),
        "schema_ref": "docs/enterprise-agent-evaluation/02_ENTERPRISE_EVALUATION_PROFILE.schema.json",
        "schema_digest": document_digest(schema),
    }
