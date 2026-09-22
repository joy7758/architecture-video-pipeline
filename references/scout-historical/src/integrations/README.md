# TITMAS Integration v0.1

This directory connects Scout operations to existing TITMAS sources without
turning Scout into a protocol or evidence-schema repository.

## Canonical boundary

- `titmas_evidence_adapter.rb` calls the pinned local `agent-evidence` CLI via
  `record -> verify --store -> export -> verify-export`.
- The adapter does not copy the Agent Evidence schema or hash-chain logic.
- An unsigned export that verifies successfully is recorded as
  `STRUCTURE_DIGEST_CHAIN_ONLY`; it does not authenticate the actor.
- Evidence verification never creates action authorization.
- `titmas_run_orchestrator.rb` binds a Quorum decision to the exact run,
  repository, target, head SHA, diff digest, review-input digest, ruleset,
  action, and expiry before an executor may act.
- `titmas_feedback_loop.rb` deterministically separates external policy
  blockers, code failures, conflicts, unknown mergeability, and stale reviews.
- `dba_handoff.rb` writes local read-only pointers whose status is always
  `READY_FOR_READ_ONLY_REVIEW_NOT_INTEGRATED`.

The integration is a local research MVP. It does not establish external event
truth, maintainer acceptance, identity authentication, certification,
production safety, adoption, customers, or revenue.
