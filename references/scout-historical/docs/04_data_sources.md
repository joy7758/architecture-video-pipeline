---
artifact_id: titmas-scout-data-sources
contract_id: TITMAS-SCOUT-SOURCE-V0
title: TITMAS Scout Data Sources
status: DRAFT_SCAFFOLD
version: 0.1.0-draft
normative: false
---

# TITMAS Scout Data Sources

## Purpose

Define the provenance and admission surface for future source observations.
This scaffold does not register, ingest, verify, or authorize any external data
source.

## Candidate source record

| Field | Intended meaning | Current definition |
| --- | --- | --- |
| `source_id` | Stable identifier for the declared source | UNDEFINED |
| `source_type` | Repository, standard, issue, publication, customer declaration, or other type | UNDEFINED |
| `source_reference` | Resolvable location or evidence reference | UNDEFINED |
| `observed_at` | Time represented by the source observation | UNDEFINED |
| `retrieved_at` | Time the observation was collected | UNDEFINED |
| `content_digest` | Digest binding the record to observed content | UNDEFINED |
| `freshness_policy_id` | Versioned rule for acceptable observation age | UNDEFINED |
| `trust_level` | Explicit evidence-backed trust classification | UNKNOWN |
| `usage_constraints` | License, privacy, policy, and customer-use limits | UNDEFINED |

## Fail-closed admission

```text
if provenance_missing:
  admission_status=REJECTED_FOR_MATCHING
if freshness_unknown_or_failed:
  admission_status=STALE_OR_UNKNOWN
if usage_authority_missing:
  admission_status=NOT_AUTHORIZED_FOR_USE
```

An admitted observation is evidence for a bounded claim only. It is not proof
of customer demand, truth, product fit, permission to contact a party, or
permission to act.

## Truth boundary

```text
DATA_SOURCE_RECORD_SCAFFOLD_DEFINED=true
DATA_SOURCE_REGISTRY_DEFINED=false
DATA_SOURCE_ADAPTER_IMPLEMENTED=false
FRESHNESS_POLICY_DEFINED=false
EXTERNAL_SOURCE_VERIFIED=false
SOURCE_USE_AUTHORIZED=false
```
