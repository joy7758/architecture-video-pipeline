# TITMAS Stage 5 Programmatic Pilot

This private, deterministic gate exercises five synthetic scenarios before any
real model call is permitted. It reuses the existing loopback Gateway,
Conformance harness, Response Capture boundary and the minimal Stage 5 SDK.

The persisted output contains sanitized audit facts only. It contains no
Sandbox Key, provider credential, raw provider response, customer data,
standard adoption or release authorization.

```text
PROGRAMMATIC_PILOT_NE_AGENT_PILOT=true
PILOT_ACCEPTANCE_NE_STANDARD_ADOPTION=true
REAL_MODEL_CALLS_REQUIRE_PROGRAMMATIC_PASS=true
```

## Private Agent pilot audit

- Sanitized audit:
  [`agent-audit/sanitized-agent-pilot-audit.json`](agent-audit/sanitized-agent-pilot-audit.json)
- Sanitized durable plan:
  [`agent-audit/sanitized-contributor-plan.json`](agent-audit/sanitized-contributor-plan.json)
- Sanitized durable contribution:
  [`agent-audit/sanitized-standard-contribution.json`](agent-audit/sanitized-standard-contribution.json)
- Sanitized durable independent review:
  [`agent-audit/sanitized-standard-review.json`](agent-audit/sanitized-standard-review.json)
- Agent pilot registry:
  [`agent-pilot-contribution-registry.json`](agent-pilot-contribution-registry.json)
- Fail-closed validator: [`validate_agent_audit.py`](validate_agent_audit.py)
- Requirement completion audit:
  [`stage5-completion-audit.json`](stage5-completion-audit.json)
- Independent review recovery decision packet:
  [`../../TITMAS-STAGE-5-INDEPENDENT-REVIEW-RECOVERY-HUMAN-DECISION-PACKET-v1.0.md`](../../TITMAS-STAGE-5-INDEPENDENT-REVIEW-RECOVERY-HUMAN-DECISION-PACKET-v1.0.md)
- Post-A02 fail-closed decision:
  [`../../TITMAS-STAGE-5-POST-A02-REVIEW-RECOVERY-DECISION-v1.0.md`](../../TITMAS-STAGE-5-POST-A02-REVIEW-RECOVERY-DECISION-v1.0.md)
- A04 transport remediation decision:
  [`../../TITMAS-STAGE-5-INDEPENDENT-REVIEW-TRANSPORT-REMEDIATION-DECISION-v1.0.md`](../../TITMAS-STAGE-5-INDEPENDENT-REVIEW-TRANSPORT-REMEDIATION-DECISION-v1.0.md)

A01 and A02 Reviewer attempts ended with unknown post-dispatch outcomes and
remain preserved. A03 isolated the local 120-second transport boundary. A04
used one explicitly authorized `BAIDU_QIANFAN/deepseek-v3.2` call, returned the
exact model, passed Review Schema validation and created a durable
`STANDARD_REVIEW` checkpoint. No automatic retry occurred.

```text
STAGE5_PRIVATE_AGENT_PILOT_COMPLETE=true
STAGE5_PRIVATE_PREVIEW_OPERATIONAL=true
INDEPENDENT_REVIEW_OUTCOME=PASS
AUTHORIZED_REVIEW_ATTEMPTS=3
CONFIRMED_REVIEW_RESPONSES=1
TOTAL_MODEL_CALLS=5
AUTOMATIC_RETRY_COUNT=0
A04_REVIEW_AUTHORIZED=true
A04_REVIEW_EXECUTED=true
FORMAL_STANDARD_CHANGE_AUTHORIZED=false
PUBLIC_EXPORT_AUTHORIZED=false
```
