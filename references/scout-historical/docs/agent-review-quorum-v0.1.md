---
artifact_id: titmas-scout-agent-review-quorum-v0.1
contract_id: TITMAS-SCOUT-AGENT-REVIEW-QUORUM-V0.1
title: TITMAS Scout Agent Review Quorum v0.1
version: "0.1"
status: RESEARCH_PROTOTYPE_CONTRACT
default_mode: AGENT_QUORUM
policy_reference: config/agent-review-policy.yaml
aggregator_reference: src/review/quorum_aggregator.rb
external_action_executor_implemented: false
---

# TITMAS Scout Agent Review Quorum v0.1

## Purpose

Agent Review Quorum provides fail-closed internal release authorization for
bounded TITMAS Scout actions without making a human review the default final
gate for ordinary open-source contributions.

The model separates three different decisions:

1. discovery and validation establish attributable facts and structural
   confidence, but do not themselves authorize action;
2. an independent Agent Review Quorum may issue internal `ALLOW` for an exact
   agent-authorizable action and exact input digest;
3. an upstream maintainer decides external acceptance, review, merge, or
   adoption under the upstream project's own policy.

Maintainer approval is not a prerequisite for Scout to mark a verified Draft
PR ready for review. It remains a prerequisite wherever the upstream project
requires it for merge or acceptance.

## Scope and Non-Goals

This contract covers deterministic aggregation of review results for ordinary,
bounded open-source activity. It does not:

- call an LLM or create reviewer conclusions;
- execute GitHub, email, payment, contract, identity, deletion, or merge actions;
- replace upstream contribution policy or maintainer judgment;
- turn a high score, source state, test result, or Validator `VALID` into
  authorization by itself;
- establish model identity, runtime isolation, legal authority, production
  safety, adoption, customer acquisition, or revenue.

## Closed Reviewer Roles

### `DISCOVERY_REVIEWER`

This reviewer verifies that:

- the opportunity and public source are real and attributable;
- the Issue or participation entry is currently open, unlocked, and actionable;
- the selected task remains outstanding;
- current upstream code and open contribution searches show no duplicate
  implementation;
- a public action entry still exists.

Stale, closed, locked, fabricated, duplicate, or non-participatory entries are
blocking failures.

### `EVIDENCE_REVIEWER`

This reviewer verifies that source, Issue, commit, tree, diff, tests, check
logs, run records, PR body, and digests are reproducible and consistently
described. Missing evidence must remain missing; it cannot be replaced with a
model inference or an unsupported claim.

### `SCOPE_REVIEWER`

This reviewer verifies that the change is limited to the discovered task, adds
no unrelated feature, dependency, protocol, or architecture change, and that
the proposed external text accurately states both completed and uncompleted
scope.

### `QUALITY_REVIEWER`

This reviewer verifies applicable tests, static checks, formatting rules,
security checks, and mutation or negative-control evidence. It must establish
that the new test constrains the intended behavior rather than passing without
asserting it. Unavailable checks are not silently treated as passing.

### `RISK_REVIEWER`

This reviewer verifies that the input contains no secret, personal sensitive
data, license conflict, fabricated claim, impersonation, spam, mass marketing,
unbounded permission, protected-branch write, or irreversible action. It also
checks that the requested action belongs to the exact policy allowlist.

## Reviewer Result Contract

Every reviewer result is bound to one immutable review input and records:

```yaml
schema_version: "0.1"
review_id: <unique-review-id>
agent_identifier: <exact-agent-instance-id>
model_runtime_identifier: <exact-model-or-runtime-id>
review_role: <one-required-role>
input_digest: sha256:<64-lowercase-hex>
output_digest: sha256:<digest-of-result-excluding-output-digest>
decision: PASS | BLOCKING_FAIL
timestamp: <utc-rfc3339-seconds>
ruleset_version: "0.1"
reason_codes: []
findings: []
blocking_reasons: []
evidence_references: []
```

`PASS` requires at least one evidence-backed finding and no blocking reason.
`BLOCKING_FAIL` requires at least one blocking reason. Unknown fields, missing
required fields, duplicate JSON keys, unknown enums, invalid time, or digest
mismatch invalidate the result and cause aggregate `DENY`.

The output digest is an integrity and replay mechanism. It is not a signature,
credential, identity proof, or proof that two runtimes were genuinely
independent.

## Independence Requirements

- every required role must have exactly one applicable result;
- every applicable role must use a distinct `agent_identifier`;
- all results must bind the same `input_digest` and ruleset version;
- a reviewer must not treat another reviewer's conclusion as evidence;
- the agent preparing or executing an action cannot be the sole authorizer;
- duplicate roles, reused agent identifiers, or different input digests are
  conflicts and cannot be combined into permission.

Runtime independence is recorded but not cryptographically proven by v0.1.
Unverifiable independence is a limitation, not a basis for an expanded claim.

## `RELEASE_DECISION_AGENT`

The aggregator consumes existing result JSON only. Its output decision enum is
closed to:

```text
ALLOW
DENY
BLOCKED_BY_MISSING_EVIDENCE
BLOCKED_BY_CONFLICT
```

`MAYBE`, warning-only permission, partial permission, and inferred permission
do not exist.

### Deterministic Aggregation

1. missing or malformed review input, unknown enum, invalid digest, action/input
   mismatch, unknown action, or invalid policy produces `DENY`;
2. an action classified as a human exception produces `DENY` and
   `human_review_required=true`;
3. any applicable `BLOCKING_FAIL` produces `DENY`, even if another reviewer is
   missing or conflicting;
4. duplicate role results, review identifiers, reused agent identifiers, or different input
   digests produce `BLOCKED_BY_CONFLICT`;
5. a missing required reviewer produces `BLOCKED_BY_MISSING_EVIDENCE`;
6. exactly one valid `PASS` for every required role and only
   the input-bound agent-authorizable requested action produces `ALLOW`.

Aggregation is non-compensatory. Four `PASS` results cannot override one
blocking result. v0.1 accepts exactly one input-bound requested action; it does
not issue partial or multi-action authorization.

## Agent-Authorizable Actions

The policy may authorize only these v0.1 actions:

- `PUBLIC_READ`;
- `CREATE_FORK`;
- `PUSH_PERSONAL_BRANCH`;
- `OPEN_DRAFT_PR`;
- `MARK_PR_READY_FOR_REVIEW`;
- `POST_BOUNDED_TECHNICAL_COMMENT`;
- `UPDATE_SCOUT_STATUS`.

An `ALLOW` binds only the exact requested action, input-file digest, target,
head commit, policy version, and review results. It cannot be generalized to a
different repository, commit, PR body, comment, target, or later state.

## Human-Exception Actions

The Agent Review Quorum cannot authorize:

- `SIGN_LEGAL_AGREEMENT`;
- `MAKE_PAYMENT`;
- `SUBMIT_BINDING_BID`;
- `MAKE_IRREVOCABLE_IDENTITY_COMMITMENT`;
- `DISCLOSE_RESTRICTED_DATA`;
- `DISCLOSE_SECRET_OR_KEY`;
- `DELETE_REMOTE_ASSET`;
- `CHANGE_ACCOUNT_SECURITY`;
- `MERGE_PROTECTED_BRANCH`.

These actions require a separate human exception decision because they create
legal, financial, identity, privacy, deletion, account-security, or protected
production effects.

## Fail-Closed Authorization Rules

An ordinary open-source action can receive internal `ALLOW` only when all of
the following are evidenced:

- source and public participation entry are attributable and current;
- no duplicate implementation or competing equivalent contribution is found;
- action, target, commit, diff, and message scope are exact;
- worktree and diff are clean;
- applicable tests, static checks, format checks, security checks, and negative
  controls pass;
- no secret, restricted data, license conflict, false claim, impersonation,
  spam, or irreversible risk exists;
- no protected upstream branch is directly modified;
- the aggregator loads the actual review-input JSON, rejects duplicate keys,
  requires the evidence-envelope JSON shapes and content-addressed reference
  formats, recomputes the input SHA-256 digest, and matches the requested
  action exactly;
- every required reviewer returns one valid `PASS` over that recomputed input
  digest.

Unknown action defaults to `DENY`. A changed head SHA, diff, PR body, target,
policy, reviewer result, or material external state invalidates the old
decision and requires a new review run.

## Validation and Authorization Separation

Trust Guard validation remains non-authorizing:

```text
VALIDATOR_VALID != QUORUM_ALLOW
QUORUM_ALLOW != UPSTREAM_ACCEPTANCE
UPSTREAM_ACCEPTANCE != MERGE_OR_ADOPTION
```

A Validator result may be evidence consumed by reviewers. Only the separate
Agent Review Quorum aggregator can produce the internal release decision, and
the external executor must still recheck the exact current target and bound
action immediately before acting.

## Agent-Readable Decision Output

```json
{
  "decision": "ALLOW",
  "human_review_required": false,
  "authorized_actions": [
    "MARK_PR_READY_FOR_REVIEW"
  ],
  "blocked_actions": [],
  "reviewers": [],
  "ruleset_version": "0.1"
}
```

The full result also carries deterministic reason codes and digest-bearing
reviewer summaries. It contains no execution instruction or credential.

## Current Limitations

- reviewer identity and runtime independence are declared, not attested;
- no signed policy, review, or aggregate result format exists;
- finding and evidence-reference semantics remain reviewer responsibilities;
  the prototype verifies required envelope types, digest/reference shapes, and
  input binding, not the truth of every referenced assertion;
- no expiry scheduler or automatic revalidation monitor exists;
- no external action executor consumes `ALLOW`;
- no formal legal, license, privacy, or production-risk engine exists;
- no claim is made that upstream maintainers accept this authorization model.

## Truth Boundary

```text
AGENT_REVIEW_QUORUM_POLICY_DEFINED=true
DETERMINISTIC_REVIEW_AGGREGATOR_IMPLEMENTED=true
REVIEWER_CONCLUSIONS_GENERATED_BY_AGGREGATOR=false
EXTERNAL_ACTION_EXECUTOR_IMPLEMENTED=false
UPSTREAM_ACCEPTANCE_ESTABLISHED=false
PRODUCTION_AUTHORIZATION_SYSTEM_ESTABLISHED=false
```
