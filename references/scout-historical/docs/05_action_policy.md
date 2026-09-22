---
artifact_id: titmas-scout-action-policy
contract_id: TITMAS-SCOUT-ACTION-POLICY-V0
title: TITMAS Scout Action Policy
status: RESEARCH_POLICY_CONTRACT
version: 0.1.0
normative: false
---

# TITMAS Scout Action Policy

## Purpose

Define the fail-closed boundary between evidence review and any external or
local action. Discovery, matching, ranking, validation, or one reviewer result
does not itself authorize execution. A complete Agent Review Quorum may
authorize bounded ordinary open-source actions; human exception approval
remains mandatory for legal, financial, identity, privacy, deletion, account
security, and protected-branch merge actions.

## Candidate policy record

| Field | Intended meaning | Current definition |
| --- | --- | --- |
| `policy_id` | Stable policy identifier and version | UNDEFINED |
| `scope` | Actors, systems, targets, and environments governed | UNDEFINED |
| `trigger_condition` | Evidence-linked condition requesting evaluation | UNDEFINED |
| `action_type` | Bounded action under consideration | UNDEFINED |
| `required_authority` | `AGENT_QUORUM` or `HUMAN_EXCEPTION` selected by exact action type | DEFINED_V0.1 |
| `safety_constraints` | Preconditions, prohibitions, limits, and stop rules | UNDEFINED |
| `audit_evidence_ref` | Evidence target for decision and execution records | UNDEFINED |
| `expiry` | Time or state after which a decision is invalid | UNDEFINED |

## Fail-closed decision

```text
default_decision=DENY
if policy_missing_or_expired:
  decision=DENY
  reason_code=POLICY_UNAVAILABLE
if authority_or_audit_target_missing:
  decision=DENY
  reason_code=AUTHORITY_OR_EVIDENCE_MISSING
if safety_constraint_unknown_or_failed:
  decision=DENY
  reason_code=SAFETY_CONSTRAINT_NOT_SATISFIED
```

A policy decision must preserve its policy version, input evidence, decision
actor, timestamp, rationale, and resulting status. A future implementation must
not reinterpret `DENY` or `UNKNOWN` as permission.

## Agent-Authorizable Actions

The following bounded actions default to `AGENT_QUORUM` authority:

- public read-only scanning;
- fork of a public repository;
- push to a personal fork branch;
- open a Draft PR;
- mark a quorum-approved Draft PR ready for review;
- post a scope-bounded technical Issue or PR comment;
- update Scout's own status record.

These actions require the exact target, input digest, action parameters,
ruleset, five required reviewer results, and aggregate `ALLOW`. No wildcard,
implicit permission, partial authorization, or stale fallback is valid.

## Human-Exception Actions

The following actions require a separate human exception decision and cannot
be authorized by Agent Review Quorum v0.1:

- sign a CLA, contract, or legal declaration;
- make a payment, purchase, or binding bid;
- make an irrevocable commitment using a person's identity;
- submit private, restricted, or regulated data;
- merge into a protected production branch;
- delete a remote asset;
- disclose a key or change account-security settings.

## Maintainer Acceptance Boundary

An upstream maintainer's review controls external acceptance and merge under
the upstream repository's policy. It is not a prerequisite for Scout's
internal authorization to submit an ordinary contribution or mark a verified
Draft PR ready for review. `ALLOW` does not predict or claim acceptance.

## Truth boundary

```text
ACTION_POLICY_SCAFFOLD_DEFINED=true
AGENT_REVIEW_POLICY_DEFINED=true
AGENT_QUORUM_AGGREGATOR_IMPLEMENTED=true
ACTION_POLICY_SCHEMA_DEFINED=false
ACTION_POLICY_ENGINE_IMPLEMENTED=PROTOTYPE_SUBSET
ACTION_POLICY_VALIDATED=RESEARCH_TESTS_ONLY
HUMAN_EXCEPTION_ENGINE_IMPLEMENTED=false
UNBOUND_EXTERNAL_ACTION_AUTHORIZED=false
EXTERNAL_ACTION_EXECUTOR_IMPLEMENTED=false
```
