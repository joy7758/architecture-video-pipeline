---
module_id: titmas-scout-opportunity
status: DESIGN_SCAFFOLD
implementation_available: false
schema_defined: false
validator_available: false
---

# Opportunity Module

## Purpose

Future home for building and validating OpportunityObjects under
`TITMAS-SCOUT-OPPORTUNITY-V0`. The current directory contains no executable
implementation.

## Intended responsibility

```text
admitted source observation
-> candidate field mapping
-> provenance-preserving OpportunityObject
-> validation result
```

## Current dependencies

- Candidate field groups: `docs/02_opportunity_object_model.md`
- Source admission boundary: `docs/04_data_sources.md`
- Non-normative shape example: `examples/sample_opportunity.yaml`

## Gaps before implementation

- canonical field names and data types
- required-versus-optional field rules
- identifier and version format
- evidence-reference profile
- lifecycle state machine
- schema and fail-closed validator

Until `OPPORTUNITY_OBJECT_SCHEMA_DEFINED=true`, data shaped like an
OpportunityObject is illustrative input only and must not be treated as valid,
accepted, or customer-derived.

## Truth boundary

```text
OPPORTUNITY_MODULE_SCAFFOLDED=true
OPPORTUNITY_OBJECT_SCHEMA_DEFINED=false
OPPORTUNITY_BUILDER_IMPLEMENTED=false
OPPORTUNITY_VALIDATOR_IMPLEMENTED=false
```
