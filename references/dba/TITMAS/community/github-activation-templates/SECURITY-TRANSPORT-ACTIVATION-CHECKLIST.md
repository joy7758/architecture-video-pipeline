# Security Transport Activation Checklist

Status: `HISTORICAL_TRANSPORT_ACTIVATION_CURRENT_LIVE_REVERIFICATION_FAILED`

This checklist records the historical bounded security-setting activation authorized by
`TITMAS-COMMUNITY-CORE-MERGE-AND-OPENING-D01`. No private report content,
token or Authorization header is stored.

| Check | Initial state |
|---|---|
| Human Decision ID recorded | `PASS — TITMAS-COMMUNITY-CORE-MERGE-AND-OPENING-D01` |
| GitHub Private Vulnerability Reporting enabled | `PASS — GET enabled=true after PUT HTTP 204` |
| Security Process Owner term valid | `PASS — zhangbin through 2026-09-30T23:59:59+08:00` |
| Private intake reachable by an authorized reporter | `PASS — GitHub repository security route enabled; no private report content inspected` |
| Synthetic private test report received | `NOT_EXECUTED_NOT_REQUIRED_FOR_LIMITED_PREVIEW` |
| Notification and acknowledgement confirmed | `NOT_ASSESSED_NO_PRIVATE_REPORT_CREATED` |
| Response-time statement reviewed | `NOT_DEFINED_NO_SLA_CLAIM` |
| Data retention and deletion rules approved | `GITHUB_PLATFORM_POLICY_APPLIES_NO_LOCAL_COPY` |
| Emergency disable procedure reviewed | `PASS — repository setting can be disabled by authorized administrator` |
| Public `SECURITY.md` route verified | `PASS` |
| Public-Issue sensitive disclosure warning verified | `PASS` |
| Rollback steps verified | `PASS — deterministic fail-closed configuration rollback test` |

Required evidence must include the decision reference, observer, timestamp,
actual API state, access boundary and rollback result. The enabled GitHub
setting proves only that the transport is available; it does not prove an SLA,
audit, certification or absence of vulnerabilities.

```text
SECURITY_PROCESS_NE_SECURITY_TRANSPORT=true
SECURITY_SETTING_CHANGE_AUTHORIZED=true
HISTORICAL_SECURITY_TRANSPORT_ACTIVE=true
CURRENT_SECURITY_TRANSPORT_ACTIVE=false
CURRENT_SECURITY_TRANSPORT_VERIFIED=false
HISTORICAL_SECURITY_ACTIVATION_HTTP_STATUS=204
SECURITY_CERTIFIED=false
SECURITY_AUDITED=false
```
