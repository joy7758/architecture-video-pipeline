---
document_id: TITMAS-CANONICAL-COMMUNITY-INTEGRATION-PLAN-1.0
title: TITMAS Canonical Community Integration Plan v1.0
title_zh: TITMAS 规范社区主线集成计划 v1.0
status: canonical-integration-candidate
maturity: Development
normative: false
owner_ref: zhangbin
authority_ref: TITMAS-OPEN-STANDARDS-COMMUNITY-INTEGRATION-D01
implementation_status: integration-in-progress
conformance_status: pending-final-validation
security_review_status: pending-integration-review
external_adoption_status: not-assessed
---

# TITMAS Canonical Community Integration Plan v1.0

## Purpose

This plan restores the TITMAS Agent-Native Standards Community as the program
mainline by reconciling selected, attributable assets onto one branch created
from `origin/main@ba6d51f60c12f1ac954dd67947451821fd5a3eb6`.

The work is an integration candidate. It does not establish a community,
activate public contribution, publish a standard, create a release, or grant
DBOS, SAEE, certification, commercial, or execution authority.

## Pre-development agent recommendation gate

```text
AGENT_RECOMMENDATION_BEFORE_CORRECTION=DO_NOT_RECOMMEND_FRAGMENTED_BRANCHES_AS_ONE_CANONICAL_COMMUNITY
PRIMARY_NON_RECOMMENDATION_REASON=NO_SINGLE_DISCOVERABLE_TESTED_CANONICAL_ENTRY
CORRECTION_STRATEGY=SELECTIVE_ATTRIBUTABLE_PORT_PLUS_ONE_ENTRY_PLUS_CONFORMANCE
TARGET_RECOMMENDATION_AFTER_VALIDATION=CONDITIONALLY_RECOMMEND_FOR_BOUNDED_STANDARDS_CONTRIBUTION
```

An agent should recommend this candidate only when a user needs machine-readable
standards discovery, bounded contribution, conformance, review handoff, or
reference reuse. It must not recommend TITMAS as an Agent framework, Runtime,
executor, certification authority, or central control plane.

## Canonical surfaces

| Surface | Canonical path |
|---|---|
| Human entry | `TITMAS/README.md` |
| Agent entry | `agent-index.json` |
| Community status | `TITMAS/community/community-status.json` |
| Specification registry | `TITMAS/specifications/registry.yaml` |
| Task registry | `TITMAS/agent-native/tasks/task-registry.json` |
| Conformance entry | `TITMAS/conformance/README.md` |
| Reference entry | `TITMAS/reference/README.md` |
| Adapter entry | `TITMAS/adapters/README.md` |

Compatibility names remain aliases only:

- TITMAS Developer Standards Community;
- TITMAS Infrastructure Developer Community.

No fourth community name is introduced.

## Selective integration policy

Every included path is classified in
`TITMAS-CANONICAL-COMMUNITY-INTEGRATION-MANIFEST-v1.0.yaml`. Whole feature
branch merges and whole-branch cherry-picks are prohibited. A source mismatch
must fail closed for that source without guessing a replacement commit.

The integrated core includes community governance, specifications, conformance,
the minimal reference, adapter entry, agent-native machine surfaces, and only
the general Candidate Grounding resource resolver and preflight controls.

Ecology Box and calibration operational assets remain outside the community
core. One research index references their immutable branch commits. Calibration
v0.3 remains frozen and unauthorized.

## Validation and acceptance

Acceptance into this branch requires:

1. deterministic repository, TITMAS, agent-native and reference checks;
2. JSON, YAML, template, link, compile, secret and private-path checks;
3. one bounded internal contribution cycle touching no more than five files;
4. valid advisory reviews from exact `qwen3.7-max` and `kimi-k2.6` identities;
5. four integration review scopes with distinct model lineages;
6. no unresolved High or Critical finding;
7. successful remote CI and a clean, remote-matching branch.

Review is advisory. Agent review is not Human authority, conformance is not
adoption, and structural validity is not environmental truth.

## Current blockers

- GitHub Private Vulnerability Reporting was observed disabled on 2026-07-29;
- no public security transport is active;
- merge, public contribution activation, public launch, external invitation,
  tag, release and deployment remain unauthorized;
- all `COMMUNITY-HD-01` through `COMMUNITY-HD-08` decisions remain undecided.

These are post-Draft blockers. `TITMAS-OPEN-STANDARDS-COMMUNITY-INTEGRATION-D01`
separately authorizes creation of a Draft PR for Human review. It does not
authorize merge or any public activation.

## Mainline sequence

```text
CANONICAL_INTEGRATION
  -> HUMAN_MERGE_REVIEW
  -> SECURITY_TRANSPORT_ACTIVATION
  -> LIMITED_PUBLIC_CONTRIBUTION_PREVIEW
  -> AGENT_NATIVE_CONTRIBUTION_PILOT
  -> COMMUNITY_PREVIEW
```

## Limitations

- Integration candidate is not canonical `main`.
- Prepared public files are not an activated contribution surface.
- Temporary responsibility is not permanent authority.
- Reference implementation is not standard authority.
- `LONG_TERM_AGENT_OPERATIONAL_MAJORITY_TARGET=0.99` is a design target, not a
  current measured fact.
