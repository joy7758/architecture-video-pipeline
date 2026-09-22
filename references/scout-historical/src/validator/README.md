# TITMAS Scout Validator Prototype v0.1

## Purpose

This directory contains a research prototype that tests whether a bounded
subset of the current TITMAS Scout design rules can be executed by a machine.
It is not a production validator, authorization engine, policy engine, action
runner, or proof that the current object chain is valid.

An independent pre-development agent review returned
`CONDITIONAL_RECOMMEND`: the approach is suitable only for structural research
when its omissions are machine-readable, YAML aliases are disabled, outputs
are deterministic, and every result remains non-authorizing. Those conditions
are represented in code, tests, and the Validation Result JSON.

After those conditions were implemented, the second independent gate returned
`RECOMMEND_FOR_RESEARCH_ONLY` with no remaining research-release blocker. The
recommendation does not extend to production, authorization, execution,
cryptographic integrity, trusted time, or evidence admissibility.

## Truth Boundary

```text
RESEARCH_PROTOTYPE_IMPLEMENTED=true
PROTOTYPE_STRUCTURAL_SUBSET_EXECUTABLE=true
FORMAL_SCHEMA_VALIDATION_IMPLEMENTED=false
FULL_VALIDATION_MODEL_CONFORMANCE=false
AUTHORIZATION_ENGINE_IMPLEMENTED=false
EXTERNAL_ACTION_IMPLEMENTED=false
PRODUCTION_READY=false
```

`validation_status: VALID` means only that the input passed this named
prototype subset at the recorded evaluation time. It does not mean that a
formal schema, URI, digest, signature, reviewer, policy, evidence claim, or
external action was verified.

## Modules

- `schema_check.rb`: prototype allowlists, required shapes, closed enums,
  discovery evidence, and selected cross-field invariants.
- `reference_check.rb`: bound-reference components, registered prototype
  types, immutable-looking versions, digest syntax, and lineage equality.
- `lifecycle_check.rb`: chain dependencies, UTC timestamps, Approval interval,
  completed Action state, and post-action evidence ordering.
- `validation_aggregator.rb`: check orchestration, deterministic failure
  aggregation, fail-closed error handling, and result construction.
- `input_loader.rb`: safe YAML loading with aliases disabled.
- `validate.rb`: read-only CLI and deterministic JSON serialization.

The `TVP-*` identifiers are prototype rules. Each failure includes a
`source_design_rule` that identifies the related `TVM-*` design rule. This
mapping does not claim complete implementation of the source rule.

## Input Contract

The prototype evaluates the `POST_ACTION_CHAIN` structural profile:

```yaml
prototype_profile: POST_ACTION_CHAIN
opportunity: {}
assessment: {}
approval: {}
action: {}
outcome_evidence: {}
```

The assessment, Action, and Outcome Evidence records use the minimum
relationship-bearing fields documented by the current design plus the
prototype transport field `schema_version: 0.1-prototype`. They are not new
normative object schemas.

For compatibility with the required repository example, a plain Opportunity
mapping is deterministically normalized to the same profile with the other
objects absent. The normalization grants no implicit relationship or
permission. The current example therefore returns `INVALID` because it has no
assessment or Approval; dependent Action and Outcome Evidence absence is not
reported as a cascade after the missing Approval.

Unknown envelope or object fields outside the hard-coded prototype allowlists
return `INVALID`. Some nested extension semantics in the draft Opportunity are
not formalized; this limitation is declared in `unchecked_capabilities`.

## Validation Result Contract

Every result includes the required fields:

```json
{
  "authorization_granted": false,
  "external_action_allowed": false,
  "failed_rules": [],
  "ruleset_version": "TITMAS-SCOUT-VALIDATOR-PROTOTYPE-STRUCTURAL-SUBSET-V0.1",
  "timestamp": "2026-08-01T12:00:00Z",
  "validation_status": "VALID"
}
```

The complete output also carries `validation_scope`,
`prototype_classification`, `non_authorization_assertion`,
`checked_rule_ids`, `timestamp_trust`, and `unchecked_capabilities`.
`authorization_granted` and `external_action_allowed` are hard-coded JSON
booleans and remain `false` for both `VALID` and `INVALID`.

Keys and failures are emitted in deterministic order. Failure deduplication
uses `rule_id`, `reason_code`, and JSON path, so distinct failures are
preserved while repeated diagnostics are suppressed.

## Run

From the repository root:

```bash
ruby src/validator/validate.rb \
  --timestamp 2026-08-01T12:00:00Z \
  examples/opportunities/example-github-agent-evidence.yaml
```

The optional timestamp exists for reproducible research output. It must be
RFC 3339 UTC at whole-second precision. It is explicitly reported as
unattested and is not a trusted time source.

Exit codes are:

- `0`: the input passed the named prototype subset.
- `1`: the input was evaluated and is `INVALID`.
- `2`: loading, parsing, or CLI usage failed; an `INVALID` fail-closed result is
  still emitted.

The CLI reads one local YAML file and writes JSON to standard output. It has no
network client and performs no external action.

## Test

```bash
ruby -I src tests/validator_test.rb
```

The tests cover missing Approval, missing discovery evidence, missing Outcome
Evidence, invalid lineage references, a structurally valid synthetic chain,
unknown fields, disabled YAML aliases, unresolvable URIs without network
resolution, deterministic failure ordering, and the invariant that validation
never grants authorization.

## Explicitly Unimplemented

- formal JSON Schema or YAML schema validation;
- full `TITMAS-SCOUT-VALIDATION-V0.1` ruleset execution;
- immutable ruleset registry and manifest verification;
- URI resolution or artifact digest recomputation;
- cryptographic signature, receipt, or attestation verification;
- evidence provenance, freshness, admissibility, or ground-truth verification;
- reviewer identity, role, authority, or attestation verification;
- policy, scope, constraint, replay, or use-limit evaluation;
- automatic execution, GitHub API access, or any external action;
- production packaging, deployment, monitoring, or operational hardening.

The same list is included in every result as `unchecked_capabilities`, using
machine-readable identifiers.
