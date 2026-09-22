# Stage 2 Structural Subset Conformance Run

> **Synthetic research fixture only.** The public GitHub signal is real; the
> Matching Assessment, Approval, reviewer, Action, receipt, and Outcome
> Evidence records are synthetic shapes. No real human decision or external
> action occurred.

## Purpose

This run demonstrates that the current TITMAS Scout Validator Prototype can
execute its five-object `POST_ACTION_CHAIN` structural subset and return
`VALID` without granting authorization.

The result proves machine execution of implemented structural predicates. It
does not establish real-world lifecycle completeness, full Validation Model
conformance, evidentiary sufficiency, human Approval, or production safety.

## Relationship to Stage 1

Stage 1 is preserved at:

```text
examples/validation-runs/2026-08-01-github-agent-hitl-issue-636
```

It used the public signal from
[`openai/openai-agents-python#636`](https://github.com/openai/openai-agents-python/issues/636)
and returned `INVALID` because Matching Assessment and Approval records were
missing.

Stage 2 creates a new synthetic envelope derived from that signal. It does not
modify, supersede, or retroactively repair Stage 1.

## Object Skeleton

```text
Opportunity (public-signal-derived synthetic snapshot)
  -> Matching Assessment (synthetic APPLIED result)
  -> Approval (HUMAN-shaped synthetic record; no real human)
  -> Action (synthetic no-op, COMPLETED/CANCELLED)
  -> Outcome Evidence (synthetic, INSUFFICIENT_EVIDENCE)
```

`lifecycle-input.yaml` marks the Opportunity as `fixture_only: true`. The other
objects use explicit `SYNTHETIC`, `NO_REAL_*`, and `LOCAL_FIXTURE_ONLY`
identifiers and reason codes because the strict envelope grammar does not
allow an additional top-level fixture flag.

## Execution

```bash
ruby src/validator/validate.rb \
  --timestamp 2026-08-01T09:11:04Z \
  examples/validation-runs/2026-08-01-github-agent-hitl-issue-636-stage-2-structural-subset/lifecycle-input.yaml
```

The process returned exit code `0`:

```text
validation_status=VALID
failed_rules=[]
authorization_granted=false
external_action_allowed=false
```

The supplied evaluation time is unattested local time. `VALID` is scoped to
`TITMAS-SCOUT-VALIDATOR-PROTOTYPE-STRUCTURAL-SUBSET-V0.1` only.

## Critical Research Findings

The result exposes two high-risk omissions in the prototype:

1. A HUMAN-shaped synthetic Approval passes even though no real human identity,
   authority, or attestation exists.
2. Outcome Evidence marked `INSUFFICIENT_EVIDENCE` with no ground-truth source
   does not prevent structural `VALID`.

These are documented as semantic-spoofing and state-awareness gaps in
`transition-report.md`. They are reasons to prohibit real action, not reasons
to infer successful governance.

The Action is a synthetic no-op with terminal outcome `CANCELLED`. It records
no real execution and tests no material effect.

## What Changed from INVALID to VALID

- an explicit `POST_ACTION_CHAIN` envelope replaced the plain Opportunity;
- a compatible Matching Assessment shape was added;
- an `APPROVED` synthetic Approval shape was added;
- cross-object lineage and reference values were made consistent;
- ordered Approval, Action, and observation timestamps were supplied;
- a completed/cancelled Action and Outcome Evidence shape were supplied.

See `transition-report.md` for the exact comparison and the semantics that
remain unchecked.

## Conditions That Still Prevent Real Action

- no real human review, Approval, identity, authority, or attestation;
- no real policy, scope, constraint, executor, usage, or replay evaluation;
- no real Action, receipt, external effect, or ground-truth evidence;
- no URI resolution, supporting-object bytes, or Validator-side digest check;
- no cryptographic verification, trusted time, or signed result store;
- no formal schemas or full Validation Model conformance;
- no verified customer demand, current unresolved need, or TITMAS fit.

The Validator hard-codes both permission booleans to `false`. No score,
Approval-shaped input, `VALID` result, or human-readable note can override that
boundary.

## Object Digest Boundary

`object-integrity.yaml` records research-only SHA-256 values for the five
embedded objects using recursively key-sorted compact JSON. These values are
locally recomputable, but the convention is non-normative and the Validator
does not recompute them.

Supporting references have no included object bytes and use synthetic fixture
digests. Their integrity, existence, and semantics are not established.

## Artifact Graph

```text
run-manifest.yaml
  -> Stage 1 manifest/result/tree references
  -> lifecycle-input.yaml
       -> five embedded synthetic object shapes
  -> object-integrity.yaml
  -> execution-receipt.yaml
       -> validation-result.json
  -> transition-report.md
```

## Replay

```bash
stage2_run_dir=examples/validation-runs/2026-08-01-github-agent-hitl-issue-636-stage-2-structural-subset
diff -u "$stage2_run_dir/validation-result.json" \
  <(ruby src/validator/validate.rb \
    --timestamp 2026-08-01T09:11:04Z \
    "$stage2_run_dir/lifecycle-input.yaml")
```

Replay is local and offline. The Validator performs no GitHub API call or
external action.

## Truth Boundary

```text
REAL_PUBLIC_SIGNAL_REFERENCE=true
SYNTHETIC_RESEARCH_FIXTURE=true
FIVE_OBJECT_SHAPES_PRESENT=true
STRUCTURAL_SUBSET_STATUS=VALID
FULL_VALIDATION_MODEL_CONFORMANCE=false
REAL_HUMAN_APPROVAL_PRESENT=false
REAL_ACTION_EXECUTED=false
EVIDENCE_SUFFICIENT=false
AUTHORIZATION_GRANTED=false
EXTERNAL_ACTION_ALLOWED=false
PRODUCTION_READY=false
```
