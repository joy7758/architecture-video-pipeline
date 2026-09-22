# ADR-040: Bounded Discovery Self-Healing and Evolution

- Status: Accepted architecture and normative contract
- Decision: `TITMAS-AGENT-NATIVE-DISCOVERY-SELF-HEALING-AND-EVOLUTION-D19-V2-1`
- Decided by: `zhangbin`
- Date: 2026-08-02

## Context

Agent-Native Discovery could identify and report inconsistencies, but it had no
standard route from reproducible evidence to a repair candidate. A report-only
layer cannot demonstrate whether agents can improve infrastructure without
losing provenance, authority boundaries, rollback or failed evidence.

## Decision

Adopt a bounded evolution architecture contract in DBA. It defines seven
transition object Schemas, multi-objective fitness principles, ER-0 through
ER-4 risk classes, isolation requirements, rollback preparation and the
governed Draft PR boundary for eligible ER-1 changes.

DBA remains the normative architecture owner and not a Runtime or executor.
`joy7758/titmac-scout` is the canonical implementation owner.
Canonical child repositories retain their existing object ownership. An agent
may prepare evidence and a Draft PR, but it cannot grant itself authority,
merge, release, deploy, migrate data or modify constitutional constraints.

## Alternatives considered

1. Keep discovery report-only. Rejected because it cannot validate bounded
   repair, reuse or lineage.
2. Create an autonomous production repair service. Rejected because it creates
   new authority and violates the current safety boundary.
3. Allow direct patching without canonical-owner resolution. Rejected because
   it would duplicate ownership and invite cross-project drift.

## Consequences

- AI agents receive a machine-readable repair and evolution path.
- Failed variants and rollbacks become durable evidence.
- ER-1 may reach a Draft PR, but Human Review remains mandatory for merge.
- ER-2 through ER-4 remain proposal-only or prohibited.
- Production, database, credential and P0-10 state remain unchanged.

## Non-authorizations

This ADR does not authorize merge, release, deployment, public community
launch, certification, production self-modification or self-granted authority.
