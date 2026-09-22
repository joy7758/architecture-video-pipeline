# ADR-041: Adopt low-friction entry and progressive value as the first TITMAS commercial principle

中文：将低门槛进入与渐进式价值采纳为TITMAS商业第一原则。

## Status

```text
decision_id=TITMAS-COMMERCIAL-CONSTITUTION-C01-LOW-FRICTION-ENTRY-D29-INTEGRATION
decision=AUTHORIZE-COMMERCIAL-CONSTITUTION-FREEZE-AND-D29-ARCHITECTURE-INTEGRATION
decided_by_ref=zhangbin
accepted_at=2026-08-03
status=accepted
```

`ADR-041` is the next unused number after the two pre-existing `ADR-040`
records. It does not renumber, replace or silently reconcile that historical
duplicate.

## Context

D28/D29 already freeze one private platform, one shared core, four products,
Monitor before Enforce and closed-core/open-discovery/open-proof boundaries.
They did not define a constitutional first-value rule, Observer as a non-product
entry layer, a dual Human/Agent entry, reversible entry contracts or a machine
customer-entry acceptance gate. Without those rules, the architecture could be
correct but still require theory, raw data, production permission, complex
deployment or purchase risk before customers see value.

## Decision

Adopt `TITMAS-COMMERCIAL-C01` as display order one and freeze the sentence:

> 先让客户看见价值，再要求客户承担集成和控制成本。

TITMAS must return an explained and verifiable prior-stage result before asking
for the next stage. The progression is:

```text
DISCOVER -> CONNECT -> OBSERVE -> UNDERSTAND -> MONITOR
  -> ENFORCE -> PROVE -> AUDIT -> EXPAND
```

Observer is `CUSTOMER_ENTRY_LAYER`, not a fifth product. Monitor has authority
and enforcement effect `NONE`. Enforce requires a separate, explicit Human
authorization. First value defaults to minimum necessary data, no raw private
Trace, no production write permission, no automatic enforcement, reversibility
and a deletion path.

## Alternatives

1. Lead with Gate policy configuration: rejected because it imposes control and
   cognitive cost before value.
2. Add Observer as a fifth product: rejected because it breaks the frozen
   four-product portfolio and creates pressure for a second observability core.
3. Require full Trace ingestion: rejected because it raises data exposure and
   duplicates general observability platforms.
4. Start with Enforce: rejected because control risk precedes understanding and
   independent authorization.
5. Publish the core to reduce integration cost: rejected because commercial
   access is not source licensing and public interfaces do not require private
   implementation disclosure.

## Consequences

- D29 prioritizes Observer, synthetic/redacted/read-only first value, Health
  Snapshot and Monitor before customer-specific Enforce.
- Product catalogs declare entry path, permissions, data, reversibility,
  deletion and non-recommendation conditions.
- Console and website plans begin with Agent Overview and customer results.
- Agent discovery exposes applicability, offerings, deployment options,
  limitations and abstention.
- Time-to-first-value values are unmeasured design targets, not achievements.

## Machine contract

The canonical machine surfaces are:

- `commercial/constitution/commercial-constitution-index.json`;
- `commercial/constitution/c01-low-friction-entry.json`;
- `commercial/entry/entry-layer.json`;
- `commercial/entry/customer-path.json`;
- `commercial/entry/first-value-contract.schema.json`;
- `commercial/entry/first-value-examples.json`;
- `commercial/entry/customer-entry-check.json`;
- `commercial/entry/customer-entry-reason-codes.json`;
- `commercial/entry/entry-metrics.json`.

## D29 integration and product-count protection

The existing canonical D29 direction is amended in place. Gate, Receipt, Audit
and Health remain the only four products. Observer maps across them as a shared
entry layer and has `PUBLIC_PRODUCT_COUNT_EFFECT=0`.

## Canonical repository audit

The canonical specification remote is
`joy7758/digital-biosphere-architecture-specification`; the current site source
and public community source are paths in that repository. The D29 private
platform repository is `joy7758/titmas-sandbox-gateway`. The Repository Map
does not declare separate website-deployment or public-community repositories,
so those possible repositories remain explicitly unresolved and were not
inferred from local directory names. The machine audit is
`commercial/discovery/canonical-repositories.json`.

## Human and Agent entry

Human entry answers inventory, activity, attention, shadow outcome, permission,
data location and exit questions. Agent entry supports discovery, applicability,
non-claims, access/data requirements, synthetic evaluation, Monitor request,
result interpretation, proof verification and abstention.

## Reversibility, data minimization and security

Key revocation, connection removal and deletion requests must be available.
Immutable historical Evidence is not rewritten by deletion. Lower friction does
not weaken identity binding, workspace isolation, scope, data classification,
reason codes, Receipt/Audit limits, high-risk confirmation, key expiry/revocation
or Human authorization.

## Non-effects

```text
IMPLEMENTATION_AUTHORIZED=false
CONSOLE_IMPLEMENTATION_AUTHORIZED=false
WEBSITE_IMPLEMENTATION_AUTHORIZED=false
OBSERVER_RUNTIME_IMPLEMENTED=false
TRACE_BACKEND_CREATED=false
HEALTH_ENGINE_CREATED=false
GATE_ENGINE_CREATED=false
PUBLIC_LAUNCH_AUTHORIZED=false
CUSTOMER_CREATED=false
CONTRACT_SIGNED=false
PAYMENT_COLLECTED=false
PUBLIC_CORE_SOURCE=false
OWNER_MAP_CHANGED=false
OWNER_RESOLVER_CHANGED=false
PR_113_CHANGED=false
SIMPLICITY_DOES_NOT_WEAKEN_AUTHORITY=true
SIMPLICITY_DOES_NOT_WEAKEN_EVIDENCE=true
SIMPLICITY_DOES_NOT_HIDE_LIMITATIONS=true
SIMPLICITY_DOES_NOT_REMOVE_HUMAN_AUTHORIZATION=true
NO_NEW_TRACE_PLATFORM=true
NO_NEW_RUNTIME=true
NO_NEW_CONTROL_PLANE=true
NO_NEW_TRUTH_SOURCE=true
NO_DUPLICATE_VERIFICATION=true
NO_P0_10_REOPEN=true
NO_D04_REOPEN=true
```
