# TITMAS D29 Private Platform Architecture v1

Status: `ARCHITECTURE_FROZEN_BOUNDED_REFERENCE_IMPLEMENTATION_INCOMPLETE`

Commercial entry is governed by `TITMAS-COMMERCIAL-C01`. The entry sequence is
`TITMAS Observer -> Health Snapshot -> Monitor -> separately authorized
Enforce -> Receipt/Audit -> optional private deployment`. Observer is an entry
layer over this platform, not a new service, product, Trace backend or Evidence
owner.

## Repository decision

The existing private repository `joy7758/titmas-sandbox-gateway` is the
canonical composition candidate. Its current commercial surface already owns
the bounded API entry, tenant-bound credentials, quota, Receipt metadata,
verification and audit metadata. Creating `joy7758/titmas-private-platform`
would duplicate composition and tenant/key surfaces.

```text
PRIVATE_PLATFORM_REPOSITORY=joy7758/titmas-sandbox-gateway
OBSERVED_MAIN_HEAD=c02926397563940feeba54b1efbe8d62e406e0e8
REUSE_EXISTING_REPOSITORY=true
CREATE_NEW_PRIVATE_PLATFORM_REPOSITORY=false
DUPLICATION_AUDIT=PASS_REUSE_REQUIRED
```

This observation is point-in-time and must be refreshed before merge or
deployment.

## Plane model

```text
Customer Agent / Application
        |
        v
TITMAS Observer Entry Layer (no authority / no enforcement)
        |
        v
Customer Data Plane Adapter
        |
        v
TITMAS Gate API
        |
        +--> Policy + Authorization References
        +--> Monitor Shadow Decision
        +--> Enforce Decision after customer-specific authorization
        |
        v
Customer Action Boundary
        |
        v
Receipt -> Independent Verification -> Audit / Health
```

### Customer Data Plane

- customer action and raw data;
- customer raw Trace;
- local adapter, optional local policy cache and customer KMS/HSM;
- optional local Receipt storage;
- customer-side enforcement and rollback.

### TITMAS Private Platform Plane

- tenant and workspace metadata;
- Agent registration reference;
- scoped-key verifier and lifecycle;
- policy and authorization references;
- Gate decision, Receipt, verification and audit metadata;
- usage, retention, support and console views.

### Management Plane

- manual customer/workspace provisioning;
- plan and quota configuration;
- deployment record and version;
- support, security notice and commercial status.

The first version keeps management offline or Human-operated. A normal Agent
cannot create credentials, change plan/quota, alter owner maps or deploy.

## Canonical implementation status

| Capability | Current evidence at observed head | D29 status |
|---|---|---|
| separate `/sandbox/v0.1` and `/api/v1` realms | repository layout and AGENTS contract | `PRESENT` |
| tenant-bound credential and scope | commercial service/store/tests | `PRESENT_REVERIFY_REQUIRED` |
| PostgreSQL RLS | migrations and integration tests | `PRESENT_REVERIFY_REQUIRED` |
| quota and idempotency | store and regression tests | `PRESENT_REVERIFY_REQUIRED` |
| signed Receipt and verify endpoint | receipt/service/API tests | `PRESENT_REVERIFY_REQUIRED` |
| audit metadata | database audit insertions | `PARTIAL` |
| formal Workspace object | reference store and PostgreSQL continuity exist; no network control plane is created | `REFERENCE_PRESENT_CONTROL_PLANE_OFFLINE` |
| Monitor shadow vocabulary and no-effect proof | Observer/FirstValue and CE-5 reuse the existing Gate | `IMPLEMENTED_REFERENCE_NOT_DEPLOYED` |
| bounded Enforce pre-side-effect contract | customer-specific authorization structure is exercised only in a synthetic non-binding proof | `TESTED_SYNTHETIC_ONLY_NOT_CUSTOMER_AUTHORIZED` |
| offline Audit Bundle export | metadata-only Bundle and replay verification reused by the reference flows | `IMPLEMENTED_REFERENCE_NOT_EXTERNALLY_ANCHORED` |
| Health Snapshot | existing D29 builder is exposed through the read-only Console projection | `IMPLEMENTED_REFERENCE_NOT_DEPLOYED` |
| data deletion workflow | reference request/session cleanup exists; commercial customer deletion is not deployed | `REFERENCE_ONLY` |
| commercial console | Agent-readable navigation and fourteen read-only pages exist | `IMPLEMENTED_REFERENCE_NOT_DEPLOYED` |

The current statuses above are source-pinned to private Gateway canonical
`main@c02926397563940feeba54b1efbe8d62e406e0e8` through
[`d29-reference-implementation.json`](../commercial/discovery/d29-reference-implementation.json).
They do not upgrade a reference implementation to a deployed or available
commercial offering. Approval, Support, commercial Billing/Quota,
Deployment-health and Security-incident sources remain partly or wholly
`NOT_ASSESSED` in the Console projections.

## First-value data and permission boundary

```text
SYNTHETIC_FIRST_VALUE_CUSTOMER_DATA_REQUIRED=false
SYNTHETIC_FIRST_VALUE_PRODUCTION_PERMISSION_REQUIRED=false
MONITOR_FIRST_VALUE_PRODUCTION_WRITE_PERMISSION_REQUIRED=false
MONITOR_FIRST_VALUE_AUTOMATIC_ENFORCEMENT=false
RAW_TRACE_UPLOAD_DEFAULT=false
METADATA_ONLY_ENTRY_AVAILABLE=true
CUSTOMER_EXIT_PATH_REQUIRED=true
KEY_REVOCATION_PATH_REQUIRED=true
DELETION_REQUEST_PATH_REQUIRED=true
```

The Human console and Agent entry are derived views over these contracts. They
must not bypass identity binding, workspace isolation, scope, reason codes,
high-risk confirmation, Receipt/Audit limitations or separate Human Enforce
authorization.

`PRESENT` does not mean production ready. Current security/runbook records
retain a failed historical D04/CR-01 ledger-integrity condition and prohibit
reopening or rewriting it.

## Deployment profiles

| Profile | D29 target |
|---|---|
| `LOCAL_DEVELOPER_SANDBOX` | retain current public-safe/stateless route |
| `CHINA_MANAGED_PRIVATE_PILOT` | Pilot architecture and packaging; no automatic deployment |
| `CUSTOMER_VPC` | reference deployment and customer-data-local adapter |
| `CUSTOMER_ON_PREMISES` | reproducible guide and demo-level packaging |
| `AIR_GAPPED_FUTURE_PROFILE` | architecture reservation only |

The existing Baidu Cloud host is the primary China infrastructure candidate
because it is an already-owned resource. Vendor selection does not prove legal
or production readiness and does not authorize deployment.

## Non-negotiable invariants

```text
CUSTOMER_RAW_DATA_STAYS_IN_CUSTOMER_ENVIRONMENT=true
MANAGEMENT_PLANE_RECEIVES_METADATA_ONLY=true
CHAIN_OF_THOUGHT_CAPTURED=false
NORMAL_AGENT_CAN_CREATE_CREDENTIAL=false
NORMAL_AGENT_CAN_CHANGE_PLAN=false
NORMAL_AGENT_CAN_CHANGE_QUOTA=false
UNKNOWN_TO_ALLOW=false
OBSERVER_IS_PRODUCT=false
PUBLIC_PRODUCT_COUNT=4
MONITOR_AUTHORITY_EFFECT=NONE
MONITOR_ENFORCEMENT_EFFECT=NONE
ENFORCE_REQUIRES_SEPARATE_HUMAN_AUTHORIZATION=true
P0_10_REOPENED=false
D04_REOPENED=false
PUBLIC_CORE_SOURCE=false
```
