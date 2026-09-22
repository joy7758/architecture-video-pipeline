---
adr_id: ADR-040
title: TITMAC Scout Canonical Identity and Read-only Progress Bridge
title_zh: TITMAC Scout 规范身份与只读进度桥接
status: accepted-canonical-status-active-cockpit-rebind-ready-for-review
decision_id: TITMAS-TITMAC-SCOUT-CANONICAL-IDENTITY-AND-COCKPIT-PROGRESS-BRIDGE-D20
amendment_decision_id: TITMAS-TITMAC-SCOUT-CANONICAL-STATUS-ACTIVATION-AND-COCKPIT-REBIND-D21
decided_by_ref: zhangbin
decided_at: 2026-08-02
release_authorized: false
deployment_authorized: false
---

# ADR-040: TITMAC Scout Canonical Identity and Read-only Progress Bridge

## Context

The discovery implementation existed in a local directory labelled
`tiamas-scout`, while D19 architecture and candidate execution work remained in
DBA Draft PR #105 and #106. There was no canonical machine identity, no unique
project-status source, and no source-pinned fail-closed DBA pull path. This
created identity drift, duplicate-implementation risk, and stale cockpit risk.

## Decision

1. Freeze `titmac-scout` as the only machine project ID, repository slug,
   package/import direction, and code project name.
2. Retain `tiamas-scout` only as a conversation label.
3. Make `joy7758/titmac-scout` the implementation and canonical status owner.
4. Keep DBA as architecture/governance owner and read-only status aggregator.
5. Establish `governance/project-status.json` plus its Schema as the sole Scout
   status source.
6. Register the canonical `main` source and the exact Draft candidate source in
   the existing DBA cockpit. Candidate projection is explicitly not adoption.
7. Fail closed on source unavailability, stale status, revision mismatch, tree
   mismatch, digest mismatch, Schema mismatch, or authority-boundary drift.
8. Store only a bounded projection in DBA; canonical run evidence remains with
   `titmac-scout`.

## D21 Amendment: canonical activation and dynamic observation

D21 accepts the corrected Scout contract and activates it on canonical `main`.
The project-owned status source declares durable project state and observation
requests; it does not hardcode current GitHub CI, pull-request, merge,
default-branch Head, workflow-run or availability state.

The DBA bridge is rebound to:

```text
repository=joy7758/titmac-scout
branch=main
mode=CANONICAL_MAIN_EXACT_REVISION
revision=7cfcde4c22daa8ea3fd2b48a15ba6ab78463c907
tree=474e20cca30f89b66638cfaf56d6d147c9e9f1d3
status_digest=84610eb8bc0aed4bb3ed1a12997a140d4fa44b723d5fb5e4cebec2dc7626a4ab
```

DBA observes remote Head, CI and pull requests through a read-only GitHub API
path. It keeps source-status, remote-revision, CI and pull-request freshness
separate. Source integrity failures remain fail-closed; unavailable or stale
dynamic observations produce `SOURCE_STALE_OR_PARTIALLY_STALE`. Neither path
writes to Scout or changes Scout-owned status.

The source uses `SELF` and `SELF_TREE` sentinels because a tracked file cannot
contain the hash of the Git commit or tree that contains itself without a
self-reference cycle. The deterministic renderer resolves those sentinels to
the fetched commit and tree, while the adapter separately verifies the status
file SHA-256 digest.

The pre-development Agent recommendation is `CONDITIONALLY_RECOMMENDED`: use
this bridge when an Agent needs machine-readable project identity, provenance,
freshness and drift diagnostics. Do not recommend it as a discovery Runtime,
control plane, write-back mechanism, production authority, or replacement for
the source repository. The initial non-recommendation reasons were the missing
canonical identity, missing unique status source, and missing fail-closed
cockpit adapter; D20 addresses only those gaps.

## Consequences

- D20 can expose exact identity, provenance, freshness, progress, and blockers
  without turning DBA into a control plane.
- The corrected private status source is canonical on Scout `main`; DBA PR
  #107 remains the bounded review surface until its separately authorized
  merge completes.
- `PR #105` and `PR #106` remain open Drafts. Their ownership and migration
  reviews remain pending until equivalent Scout implementation, tests, and a
  retained demo are proven.
- D20 does not establish self-healing or self-evolution completion, public
  community operation, release, deployment, production readiness, adoption, or
  certification.

## Rejected alternatives

- Rename the machine project to `tiamas-scout` or `titmas-scout`.
- Add another discovery implementation inside DBA.
- Let DBA write back, trigger repair, open/merge PRs, issue credentials, or
  activate mutation.
- Copy raw evolution evidence into DBA.
- Treat a PR or CI result as release or production readiness.

```text
COCKPIT_IS_READ_ONLY_AGGREGATOR=true
TITMAC_SCOUT_IS_STATUS_OWNER=true
TITMAC_SCOUT_IS_IMPLEMENTATION_OWNER=true
DBA_NE_DISCOVERY_RUNTIME=true
COCKPIT_NE_CONTROL_PLANE=true
STATIC_DECLARATION_NE_DYNAMIC_OBSERVATION=true
SOURCE_STATUS_NE_GITHUB_CI_STATUS=true
SOURCE_STATUS_NE_GITHUB_PR_STATUS=true
COCKPIT_SOURCE_MODE=CANONICAL_MAIN_EXACT_REVISION
COCKPIT_DYNAMIC_OBSERVATION=GITHUB_API_READ_ONLY
P0_10_REOPENED=false
D04_REOPENED=false
```
