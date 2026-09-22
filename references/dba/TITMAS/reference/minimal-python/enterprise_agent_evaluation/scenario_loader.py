"""Load the six-case R1 scenario pack from the frozen R0 ESP schema."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .profile_loader import (
    ContractValidationError,
    DBA_ROOT,
    document_digest,
    load_json_object,
    validate_document,
)


ESP_SCHEMA_PATH = (
    DBA_ROOT
    / "docs"
    / "enterprise-agent-evaluation"
    / "03_ENTERPRISE_SCENARIO_PACK.schema.json"
)
EXPECTED_R1_CATEGORY_COUNTS = {
    "NORMAL": 2,
    "AMBIGUOUS_OR_CONFLICT": 2,
    "RED_LINE_OR_FAILURE": 2,
}


def _validate_hash_manifest(document: dict[str, Any]) -> None:
    for entry in document["hash_manifest"]["entries"]:
        key = entry["path"]
        if key not in document:
            raise ContractValidationError(f"$.hash_manifest: unknown top-level path {key!r}")
        actual = document_digest(document[key])
        if actual != entry["sha256"]:
            raise ContractValidationError(f"$.hash_manifest: digest mismatch for {key!r}")


def load_scenario(path: Path, schema_path: Path = ESP_SCHEMA_PATH) -> dict[str, Any]:
    schema = load_json_object(schema_path)
    document = load_json_object(path)
    validate_document(document, schema)
    tasks = document["tasks"]
    if len(tasks) != 6:
        raise ContractValidationError("$.tasks: R1 requires exactly six cases")
    ids = [task["task_id"] for task in tasks]
    if len(ids) != len(set(ids)):
        raise ContractValidationError("$.tasks: task_id values must be unique")
    if Counter(task["category"] for task in tasks) != EXPECTED_R1_CATEGORY_COUNTS:
        raise ContractValidationError("$.tasks: R1 category distribution must be 2/2/2")
    forbidden_ids = {item["action_id"] for item in document["forbidden_actions"]}
    for task in tasks:
        unknown = set(task["forbidden_action_ids"]) - forbidden_ids
        if unknown:
            raise ContractValidationError(
                f"$.tasks/{task['task_id']}: unknown forbidden actions {sorted(unknown)}"
            )
    _validate_hash_manifest(document)
    return {
        "document": document,
        "scenario_pack_id": document["scenario_pack_id"],
        "scenario_pack_version": document["scenario_pack_version"],
        "scenario_pack_digest": document_digest(document),
        "schema_ref": "docs/enterprise-agent-evaluation/03_ENTERPRISE_SCENARIO_PACK.schema.json",
        "schema_digest": document_digest(schema),
    }
