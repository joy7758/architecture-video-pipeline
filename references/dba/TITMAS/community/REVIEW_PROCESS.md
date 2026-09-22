# TITMAS Review Process

## Review types

- Editorial: clarity, links, terminology and localization.
- Technical: schema, examples, compatibility and tests.
- Domain: DBOS, SAEE, Agent Evidence or external profile boundary.
- Security and Privacy: data, threat and disclosure controls.
- Governance: status, maturity, authority and decision provenance.

## Independence

The author may respond to findings but may not provide the only approval of
their own normative or security-sensitive change. AI reviews are advisory and
must identify model, session and scope.

## Required review output

```text
finding_id:
severity: LOW|MEDIUM|HIGH|CRITICAL
evidence:
required_correction:
deferred_issue:
result: PASS|FAIL|HOLD
```

HIGH or CRITICAL findings require correction and a new review of the affected
scope. Unknown evidence produces `HOLD`, not PASS.

## Bootstrap fail-closed rule

Until a Reviewer or Maintainer is explicitly assigned, an incoming contribution
may be validated and queued but cannot be accepted, merged or given an SLA.
Automated checks may triage completeness only; they cannot approve. The public
surface must disclose `NO_REVIEWER_ASSIGNED` instead of promising response time.

## Appeals

Use the conflict process in [GOVERNANCE.md](GOVERNANCE.md). A review result
cannot modify Authority, Gate state or source facts.
