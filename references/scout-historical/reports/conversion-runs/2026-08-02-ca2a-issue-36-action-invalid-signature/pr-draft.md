---
artifact_type: UPSTREAM_PULL_REQUEST_DRAFT
status: PREPARED_NOT_SENT
repository: agentrust-io/ca2a
base_branch: main
source_branch: contrib/issue-36-action-invalid-signature
external_action_authorized: false
pull_request_created: false
issue_comment_created: false
---

# PR Draft: Cover Invalid Delegation Signature in Action Evidence

## Proposed Title

```text
test: cover invalid delegation signature in action evidence
```

## Proposed Body

### Summary

Refs agentrust-io/ca2a#36.

Adds the residual ACTION-path invalid-signature conformance case identified
after PR #37. This covers one remaining Issue #36 checklist item and does not
close the full issue.

### What Changed

- Documents `ACTION-008` as a MUST-level conformance case.
- Replaces the signed leaf credential with an otherwise identical credential
  whose signature differs by one byte while retaining valid hexadecimal shape
  and length.
- Verifies the existing Action Evidence path returns
  `provenance_invalid / INVALID_CREDENTIAL` before authorization or controller
  outcome handling.

### Test Evidence

```text
TEST_FILE=tests/conformance/test_profile_conformance.py
ACTION_008=test_action_008_invalid_delegation_signature_is_provenance_invalid
.venv/bin/pytest "${TEST_FILE}::${ACTION_008}" -v
1 passed

.venv/bin/pytest "$TEST_FILE" -k 'action or deleg' -v
16 passed, 15 deselected

.venv/bin/pytest tests/unit/test_delegation.py tests/unit/test_verify.py -v
21 passed

.venv/bin/pytest tests/conformance/ -v
31 passed

.venv/bin/pytest tests/unit/ tests/conformance/ -v --tb=short --cov=src --cov-report=term
252 passed, 3 skipped, 87.01% coverage

.venv/bin/ruff check src/ tests/
All checks passed

.venv/bin/mypy src/ca2a_runtime/ src/ca2a_verify/
Success: no issues found in 36 source files

.venv/bin/bandit -r src/ -c pyproject.toml
No issues identified

.venv/bin/pip-audit
No known vulnerabilities found

git diff --check
Passed
```

The three skips require real SEV-SNP, TDX, and TPM capture fixtures that are
not present in this local environment. Pytest does not report a separate
assertion count.

A disposable mutation check changed the new test's expected classification to
`authorization_invalid`; the test failed because the actual result remained
`provenance_invalid`. This confirms the classification assertion is active.

### Security and Compatibility

- Test and conformance documentation only; no runtime verifier code changes.
- No new dependency, protocol field, credential type, or API surface.
- Uses synthetic test credentials and makes no claim about production keys,
  permissions, authorization, or deployment safety.
- Preserves the existing boundary: invalid credential signatures are
  provenance-invalid; scope or local-policy denials are authorization-invalid;
  controller rejection remains valid negative evidence.

### Remaining Issue #36 Checklist

This PR does not address:

- direct use of the public `agent-manifest` delegation verifier, or revision of
  that acceptance criterion to the current cA2A verifier API;
- credential validity-window fields and expired/not-yet-valid cases;
- delegatee, session, or channel binding mismatch cases;
- longer ACTION-path attenuation and intermediate scope-widening cases;
- external subject identifier or digest representation and verification.

## Potential Maintainer Rejection Reasons

- The maintainer may prefer a serialized fixture instead of an inline
  conformance chain mutation.
- The maintainer may want different `ACTION-008` wording or numbering.
- The maintainer may decide `DELEG-001` is sufficient despite the residual
  checklist, or require the public `agent-manifest` verifier first.
- The maintainer may request additional platform or CI evidence before review.

## External Action Boundary

This draft has not been sent. No branch was pushed, no pull request was
created, and no Issue comment was posted.
