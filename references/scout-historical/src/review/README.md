# TITMAS Scout Agent Review Aggregator v0.1

This directory contains a deterministic research prototype for aggregating
already-produced Agent Review results. It does not call an LLM, invent a
reviewer conclusion, execute an authorized action, or establish upstream
acceptance.

## Components

- `review_result.rb` strictly parses reviewer JSON, rejects duplicate keys,
  validates closed enums and verifies a digest over the review payload;
- `review_input.rb` strictly loads the review input, validates required
  evidence-envelope and content-reference shapes, recomputes its file digest,
  and exposes the one requested action;
- `policy_loader.rb` loads the fixed v0.1 reviewer quorum and action classes;
- `quorum_aggregator.rb` applies all-or-nothing, fail-closed aggregation;
- `cli.rb` emits one deterministic decision JSON.

## Review Result Contract

Each result records the exact `agent_identifier`,
`model_runtime_identifier`, `review_role`, `input_digest`, `output_digest`,
`decision`, `timestamp`, and `ruleset_version`. `output_digest` is SHA-256 over
the deep-key-sorted compact JSON payload after removing `output_digest` itself.
It is an integrity check, not a cryptographic identity or independence proof.

Reviewer decisions are closed to `PASS` and `BLOCKING_FAIL`. Aggregate
decisions are closed to `ALLOW`, `DENY`, `BLOCKED_BY_MISSING_EVIDENCE`, and
`BLOCKED_BY_CONFLICT`.

## Usage

```text
ruby src/review/cli.rb \
  --policy config/agent-review-policy.yaml \
  --input reports/review-runs/2026-08-02-ca2a-pr-76-ready/input.json \
  --action MARK_PR_READY_FOR_REVIEW \
  REVIEW-1.json REVIEW-2.json REVIEW-3.json REVIEW-4.json REVIEW-5.json
```

Exit status is `0` only for `ALLOW`, `1` for a valid non-allow decision, and
`2` for a load, parse, or policy error. Every error path emits `DENY` JSON.

## Fail-Closed Boundaries

- an unknown action, role, decision, key, or enum denies the request;
- malformed input, duplicate JSON keys, missing required fields, or digest
  mismatch denies the request;
- missing evidence objects/arrays or malformed content-addressed references
  deny the request even if every supplied reviewer result says `PASS`;
- the CLI action must exactly equal the action in the loaded review input, and
  every review must bind the recomputed SHA-256 of that exact input file;
- a missing required reviewer blocks by missing evidence;
- duplicate role or review identifiers, reused agent identifiers, or different
  input digests block by conflict;
- one `BLOCKING_FAIL` denies the request;
- a human-exception action is denied by this aggregator and sets
  `human_review_required=true`;
- v0.1 accepts one exact input-bound action and never issues partial or
  multi-action authorization;
- no timestamp is generated during aggregation, so the same input, action, and
  review set replay to the same output bytes.

This prototype does not verify model identity, runtime isolation, reviewer
independence, signatures, credentials, or external action execution. Those
facts must remain separately evidenced.
