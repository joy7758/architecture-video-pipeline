# TITMAS Security Policy

Status: `PROCESS_DEFINED_PUBLIC_TRANSPORT_INACTIVE_PRIVATE_REPOSITORY`

## Supported surface

Only a private Development repository and bounded internal review surface are
current. There is no public contribution operation, production release, SLA,
certification or security guarantee.

## Reporting

Do not publish suspected vulnerabilities, secrets, personal data or exploit
details in an Issue. GitHub Private Vulnerability Reporting was historically
enabled and verified on 2026-07-29, but live re-verification after the
repository became private returned HTTP 404. It is not a current public
transport. No private mailbox is invented, and no response SLA is claimed.
`zhangbin` is the temporary, revocable process owner through
2026-09-30T23:59:59+08:00.

Current state:

```text
SECURITY_PROCESS_DEFINED=true
SECURITY_PROCESS_OWNER_ASSIGNED=true
SECURITY_DISCLOSURE_PATH_ACTIVATED=false
SECURITY_TRANSPORT_VERIFIED=false
SECURITY_RESPONSE_TEAM_ASSIGNED=false
PUBLIC_LAUNCH_BLOCKER_SECURITY_TRANSPORT=true
```

Do not send external reports automatically. The private reporting path is a
transport, not a security audit, certification or guarantee.

GitHub Issue and PR templates remain in history after Activation PR #42 but
are not a current public submission surface.

## Review requirements

Schema, validator, adapter and reference changes must assess:

- untrusted input and fail-closed behavior;
- path traversal, unsafe deserialization and command execution;
- secret, PII and customer-data exclusion;
- dependency and supply-chain changes;
- denial-of-service and size limits;
- semantic elevation from Observation, Evidence or Verification;
- rollback and historical record preservation.

Security review does not grant Authorization or Certification.
