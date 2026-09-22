# Research-Only Validation Run: Public GitHub Issue Signal

## Purpose

This directory records an offline execution of the TITMAS Scout Validator
Prototype against a local Opportunity derived from a real public Agent
ecosystem signal.

The word **real** applies only to the existence of the referenced public
signal. This is not a real customer record, full real-world object chain,
production validation, market validation, completed human review, or
authorization record.

## Signal

The primary signal is GitHub issue
[`openai/openai-agents-python#636`](https://github.com/openai/openai-agents-python/issues/636).
The page was observed through a read-only browser on 2026-08-01. It displayed
the issue as `Closed` and showed a linked `Merged #2230` item.

The issue author's requests are source-authored claims, not verified customer
facts. The visible merged link is not treated as proof that every request was
implemented or that the signal is currently unresolved.

The secondary signal is a
[commit-pinned tracing document](https://github.com/openai/openai-agents-python/blob/21c88f582cdf7a8cbd96c33398eefe166a791d5c/docs/tracing.md).
It says that the SDK includes built-in tracing. This is relevant counter-scope:
the run must not infer an ecosystem-wide absence of Agent execution evidence.

Neither public page is archived in this record. See
`source-observation.yaml` for observation provenance and limitations.

## Local Input

The Validator consumed:

```text
examples/opportunities/example-github-agent-evidence.yaml
```

Its local SHA-256 digest is bound in `run-manifest.yaml` and
`execution-receipt.yaml`. The run does not modify the Opportunity or recompute
the remote source digests declared inside it.

The Opportunity remains example-only, non-normative, `discovered`,
`NOT_COMPUTABLE`, `NOT_VALIDATED`, and `NOT_AUTHORIZED`.

## Execution

The offline command was:

```bash
ruby src/validator/validate.rb \
  --timestamp 2026-08-01T08:41:24Z \
  examples/opportunities/example-github-agent-evidence.yaml
```

The process returned exit code `1`, meaning the input was evaluated and found
`INVALID`. The supplied evaluation timestamp equals the recorded execution
timestamp but remains an unattested local time value.

## Result

```text
validation_status=INVALID
failed_rule=TVP-AUT-001:APPROVAL_MISSING
failed_rule=TVP-LIF-003:MATCHING_ASSESSMENT_MISSING
authorization_granted=false
external_action_allowed=false
```

The result means only that the plain Opportunity was normalized fail-closed to
the prototype `POST_ACTION_CHAIN` profile and lacks Matching Assessment and
Approval records. Dependent missing Action and Outcome Evidence records are not
reported as cascading failures after the missing Approval.

The result does not mean that the GitHub issue is invalid, unimportant,
resolved, unresolved, commercially valuable, or suitable for TITMAS.

## Artifact Graph

```text
run-manifest.yaml
  -> source-observation.yaml
  -> ../../opportunities/example-github-agent-evidence.yaml
  -> execution-receipt.yaml
       -> validation-result.json
  -> human-review.md (PENDING_HUMAN_REVIEW)
```

The manifest binds local artifacts by SHA-256. External webpages remain
unarchived references and are not cryptographically bound by this run.

## Replay

Replay requires the same repository commit, Ruby runtime, input bytes, and
explicit timestamp. A byte-for-byte result comparison can be performed with:

```bash
validation_run_dir=examples/validation-runs/2026-08-01-github-agent-hitl-issue-636
diff -u "$validation_run_dir/validation-result.json" \
  <(ruby src/validator/validate.rb \
    --timestamp 2026-08-01T08:41:24Z \
    examples/opportunities/example-github-agent-evidence.yaml)
```

The Validator itself performs no network request, GitHub API call, or external
action. Rechecking the public pages is a separate read-only observation and may
produce different page state later.

## Human Review Boundary

`human-review.md` is a machine-prefilled review aid with
`PENDING_HUMAN_REVIEW`. No human reviewer identity, decision, Approval, or
authorization is recorded. Pending review remains fail-closed.

## Truth Boundary

```text
PUBLIC_SIGNAL_EXISTS=true
PUBLIC_SIGNAL_OBSERVATION_ARCHIVED=false
REAL_CUSTOMER_IDENTIFIED=false
CUSTOMER_DEMAND_VALIDATED=false
CURRENT_UNRESOLVED_NEED_VALIDATED=false
ECOSYSTEM_WIDE_ABSENCE_VALIDATED=false
TITMAS_FIT_VALIDATED=false
HUMAN_REVIEW_COMPLETED=false
VALIDATION_STATUS=INVALID
AUTHORIZATION_GRANTED=false
EXTERNAL_ACTION_ALLOWED=false
PRODUCTION_READY=false
```
