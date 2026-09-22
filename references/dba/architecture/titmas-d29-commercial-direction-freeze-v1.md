# TITMAS D29 Commercial Direction Freeze v1

Decision reference:
`TITMAS-CHINA-COMMERCIAL-PRIVATE-PLATFORM-AND-PAID-PILOT-D29`

Status: `ACCEPTED_FOR_D29_IMPLEMENTATION_WITH_GATES`

The existing D29 status does not authorize implementation under this C-01
change. The current decision is architecture-only:

```text
C01_CUSTOMER_ENTRY_IMPLEMENTATION_AUTHORIZED=false
C01_ENFORCE_IMPLEMENTATION_AUTHORIZED=false
```

## Positioning

```text
TITMAS_POSITIONING=
AGENT_ACTION_CONTROL_AND_VERIFIABLE_ACCOUNTABILITY_PLATFORM

TITMAS_PLATFORM_MODEL=
CLOSED_CORE_OPEN_DISCOVERY_AND_PROOF

AI_AGENT_IS_OPERATIONAL_CUSTOMER=true
HUMAN_OR_ORGANIZATION_IS_CONTRACTING_PRINCIPAL=true
```

## Commercial Constitution C-01

D29 is subordinate to
[`TITMAS-COMMERCIAL-C01`](../docs/commercial/TITMAS_CUSTOMER_ENTRY_PRINCIPLE_C01.md):

```text
LOW_FRICTION_ENTRY_IS_COMMERCIAL_FIRST_PRINCIPLE=true
FIRST_VALUE_BEFORE_ENFORCEMENT=true
MONITOR_BEFORE_ENFORCE=true
MINIMUM_NECESSARY_DATA=true
REVERSIBLE_ENTRY=true
EXPLANATION_BEFORE_CONFIGURATION=true
PROOF_BEFORE_PURCHASE_EXPANSION=true
```

TITMAS must return an explained and verifiable initial result before asking a
customer for full architecture understanding, private-core source access,
production write permission, automatic enforcement, unnecessary raw data,
complex deployment or a high-cost commitment.

TITMAS is one private platform with one shared core. It exposes four public
product contracts:

1. `TITMAS Gate` — pre-action Monitor or Enforce decision;
2. `TITMAS Receipt` — portable technical execution record;
3. `TITMAS Audit` — evidence, authority and decision replay;
4. `TITMAS Health` — bounded completeness and longitudinal evidence view.

Industry solutions configure adapters, policies and views. They do not create
new identity, evidence, policy, receipt, audit, tenant, key or verification
cores.

## Commercial progression

```text
Observer
  -> Health Snapshot
  -> Monitor Pilot
  -> Gate Enforce Pilot
  -> Receipt + Audit
  -> Enterprise Private Deployment
```

```text
HEALTH_IS_ACQUISITION_ENTRY=true
GATE_IS_PRIMARY_PAID_PRODUCT=true
RECEIPT_IS_PORTABLE_PROOF_LAYER=true
AUDIT_IS_ENTERPRISE_EXPANSION=true
```

`TITMAS Observer` is the shared customer entry layer. It contributes zero to
the public product count, has no authority or enforcement effect, and does not
own Trace or Evidence semantics.

The primary first market is software, AI SaaS and enterprise-automation teams
using coding Agents for merge, release, configuration, data write, external
communication and other measurable high-impact actions.

Monitor computes and records `WOULD_ALLOW`, `WOULD_BLOCK`,
`WOULD_NEED_APPROVAL` or `NOT_ASSESSED` and has no enforcement effect. Enforce
uses `ALLOW`, `BLOCK`, `NEEDS_APPROVAL` or `NOT_ASSESSED`; `NOT_ASSESSED` never
becomes allow.

## First-value routes and dual entry

D29 supports three architecture-level first-value routes:

1. zero-customer-data synthetic Observer → Shadow Gate → Receipt → Audit;
2. public, synthetic or authorized redacted Trace import with read-only action
   classification and evidence-gap output;
3. read-only/event-copy Monitor with `WOULD_*` or `NOT_ASSESSED` output.

The Human entry begins with Agent inventory, activity, attention, shadow
outcome, permission, data and exit questions. The Agent entry exposes products,
non-claims, access modes, required inputs, data boundaries, synthetic examples,
Monitor request semantics, verification and abstention. Both views derive from
the same machine contracts.

Design targets of ten minutes for a synthetic demonstration and thirty minutes
for a Monitor sandbox are unmeasured targets, not current product claims.

The normative `FirstValueContract` schema and examples are
[`first-value-contract.schema.json`](../commercial/entry/first-value-contract.schema.json)
and [`first-value-examples.json`](../commercial/entry/first-value-examples.json).
They distinguish architecture requirements from current runtime availability.
The machine `TITMAS_CUSTOMER_ENTRY_CHECK` is
[`customer-entry-check.json`](../commercial/entry/customer-entry-check.json).
If it returns `FAIL`, then `CUSTOMER_ENTRY_TOO_HIGH=true` and
`REDESIGN_REQUIRED=true`; no later-stage implementation may be inferred.

Exit must support connection removal, key revocation and a deletion request.
Deletion cannot rewrite immutable retained Evidence or the D04 failure history.

## Competitive correction

Signed receipts, offline verification and action-control vendors already
exist. Receipt novelty is not the moat.

```text
RECEIPT_CATEGORY_EXISTS=true
RECEIPT_IS_NOT_UNIQUE_MOAT=true
TITMAS_DIFFERENTIATION=
CROSS_AGENT_ACTION_CONTROL_AND_EVIDENCE_INTEROPERABILITY
```

TITMAS is not the primary recommendation when a buyer only needs Trace and
debugging, general RBAC/ABAC, or prompt/content security.

## Source boundaries

```text
AGENT_EVIDENCE_IS_UNIQUE_EXECUTION_EVIDENCE_SEMANTIC_SOURCE=true
TITMAS_NE_GENERAL_AUTHORIZATION_PLATFORM=true
TITMAS_NE_OBSERVABILITY_PLATFORM=true
TITMAS_NE_AI_FIREWALL=true
TITMAS_NE_CERTIFICATION_AUTHORITY=true
```

DBA owns the commercial architecture and gate definitions. The private
implementation remains in its canonical child repository. Public discovery
contains contracts, SDK/Sandbox entry and synthetic proof only, never private
core or attack material.

## China defaults

```text
CHINESE_COMMERCIAL_LANGUAGE_PRIMARY=true
CUSTOMER_RAW_DATA_LOCAL_BY_DEFAULT=true
MANAGEMENT_PLANE_METADATA_ONLY=true
CUSTOMER_DATA_TO_FOREIGN_MODEL_DEFAULT=false
PUBLIC_SELF_SERVICE_SALES=false
ONLINE_PAYMENT=false
MANUAL_COMMERCIAL_PROVISIONING=true
HUMAN_LEGAL_REVIEW_REQUIRED=true
```

The first proposed design-partner offer architecture is a B2B, manually
provisioned, bounded private Monitor Pilot. `AVAILABLE_OFFERING=false`; this is
not a currently purchasable or deployed offer.
No legal, filing, licensing, production, customer adoption or certification
claim follows from this architecture freeze.

## Direction check

```text
ONE_PRIVATE_PLATFORM=true
ONE_SHARED_CORE=true
FOUR_PUBLIC_PRODUCTS=true
PUBLIC_PRODUCT_COUNT=4
PUBLIC_PRODUCTS=GATE_RECEIPT_AUDIT_HEALTH
MULTIPLE_INDUSTRY_CONFIGURATIONS=true
OBSERVER_IS_ENTRY_LAYER=true
OBSERVER_IS_FIFTH_PRODUCT=false
FIRST_VALUE_BEFORE_ENFORCEMENT=true
MONITOR_BEFORE_ENFORCE=true
CLOSED_CORE=true
OPEN_DISCOVERY=true
OPEN_PROOF=true
PUBLIC_INTERFACE_NE_PRIVATE_IMPLEMENTATION=true
COMMERCIAL_ACCESS_NE_SOURCE_LICENSE=true
NEW_IDENTITY_CORE=false
NEW_EVIDENCE_CORE=false
NEW_POLICY_ENGINE=false
NEW_GATE_ENGINE=false
NEW_RECEIPT_ENGINE=false
NEW_AUDIT_ENGINE=false
NEW_TENANT_SYSTEM=false
NEW_TRACE_PLATFORM=false
SECOND_IDENTITY_CORE_CREATED=false
SECOND_EVIDENCE_OBJECT_SYSTEM_CREATED=false
SECOND_POLICY_ENGINE_CREATED=false
SECOND_RECEIPT_ENGINE_CREATED=false
SECOND_AUDIT_CHAIN_CREATED=false
SECOND_TENANT_SYSTEM_CREATED=false
SECOND_KEY_SYSTEM_CREATED=false
SECOND_VERIFICATION_AUTHORITY_CREATED=false
TITMAS_DIRECTION_CHECK_RESULT=PASS
```

At the C-01 freeze, this D29 integration was architecture only. A later,
separately authorized bounded implementation sequence is now source-pinned to
private Gateway canonical
`main@c02926397563940feeba54b1efbe8d62e406e0e8`. The architecture freeze and
its non-effects are not rewritten; current implementation facts are projected
through
[`d29-reference-implementation.json`](../commercial/discovery/d29-reference-implementation.json).

```text
CONSOLE_IMPLEMENTED_REFERENCE=true
CONSOLE_DEPLOYED=false
WEBSITE_IMPLEMENTED=false
OBSERVER_RUNTIME_IMPLEMENTED_REFERENCE=true
OBSERVER_RUNTIME_DEPLOYED=false
SOFTWARE_DELIVERY_PROOF=TESTED_SYNTHETIC_ONLY_NOT_DEPLOYED
COMMERCIAL_OFFERING_AVAILABLE=false
PAID_MONITOR_PILOT_AVAILABLE=false
CUSTOMER_SPECIFIC_ENFORCE_AUTHORIZED=false
PUBLIC_LAUNCH_AUTHORIZED=false
COMMERCIAL_CUSTOMER_CREATED=false
TITMAS_DRIFT_CHECK_RESULT=PASS_WITH_RECORDED_LIMITATIONS
```
