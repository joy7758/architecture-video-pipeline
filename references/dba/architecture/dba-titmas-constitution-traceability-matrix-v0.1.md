# DBA / TITMAS Constitution Traceability Matrix v0.1

中文：DBA / TITMAS 宪法追踪矩阵 v0.1

Status: `ACCEPTED_EFFECTIVE_ON_CANONICAL_MERGE`

| Stable ID / clause | Existing source | Parent amendment | TITMAS / DCell projection | Machine assertion | Test |
|---|---|---|---|---|---|
| `ADR-032` | ADR-032 | §2 | logical entry is not a physical center | `COMPOSITION_NE_AUTHORITY_AGGREGATION=true` | `test_parent_principle_ids_are_unique_and_traceable` |
| `ADR-033` | ADR-033 | §2 | module selection is a proposal, not activation | `NATURAL_LANGUAGE_NE_DIRECT_ACTIVATION=true` | `test_dcell_activation_fails_closed` |
| `DBA-P-COMPATIBILITY-BEFORE-INNOVATION` | reuse audit | §3 | adapters before new runtime | `NEW_RUNTIME_CREATED=false` | `test_nonclaims_and_no_implementation_authority` |
| `DBA-P-HUMAN-CONSTITUTIONAL-SOVEREIGNTY` | Program Charter / current constitution | §3 | parent cannot be overridden | `TITMAS_MAY_OVERRIDE_DBA=false` | `test_parent_child_inheritance_is_explicit` |
| Applicable constraint intersection | capability boundary / governance decision | §5 | Human approval applies only when policy, risk, action class or escalation requires it | `APPLICABLE_CONSTRAINT_INTERSECTION_REQUIRED=true`; `HUMAN_APPROVAL_ALWAYS_REQUIRED=false` | `test_conditional_human_approval_semantics` |
| Unknown applicability | capability boundary / fail-closed governance | §5 | not applicable is distinct from missing; unknown fails closed | `NOT_APPLICABLE_CONSTRAINT_NE_MISSING_CONSTRAINT=true`; `UNKNOWN_APPLICABILITY_FAILS_CLOSED=true` | `test_not_applicable_and_unknown_semantics` |
| Bound approval | governance decision / parent-child authority | §5 | approval binds principal, Agent/version, task, action/resource, constitution, composition, scope and expiry | `one_time_approval_can_expand_parent_constitution=false` | `test_approval_bindings_and_non_overridable_deny` |
| `DBA-P-COMPOSITION-ACCOUNTABILITY` | ADR-032 / entity lifecycle | §3 | DCell dependency lineage and composition re-evaluation | `COMPOSITION_NE_AUTHORITY_AGGREGATION=true` | `test_dcell_minimum_contract_and_composition_rules` |
| `ADR-039` | ADR-039 | §2 | changed module invalidates inherited conclusion | `automatic_pass_inheritance=false` | `test_dcell_minimum_contract_and_composition_rules` |
| `DBA-P-SHARED-PROTOCOL-NOT-CONTROLLER` | stack and DBOS/SAEE contract | §3 | distributed owned enforcement points | `UNIFIED_ENTRY_NE_GLOBAL_MANDATORY_GATEWAY=true` | `test_titmas_is_not_a_global_controller` |
| `DBA-P-REAL-ENVIRONMENT-FEEDBACK` | customer entry validation | §3 | explicit capability nonclaims | `CROSS_PLATFORM_ENFORCEMENT_PROVEN` is a non-claim | `test_nonclaims_and_retained_failures` |
| C-01 four products | ADR-041 / product catalog | §5 | Gate, Receipt, Audit, Health only | `product_count=4` | `test_product_portfolio_remains_four` |
| Observer entry | ADR-041 / entry layer | §5 | non-product entry | `observer_is_product=false` | `test_product_portfolio_remains_four` |
| DCell module layer | new profile | non-effect | not a fifth product | `public_product_count_effect=0` | `test_product_portfolio_remains_four` |
| Global locale layering | Human interface contract | non-effect | declared principal/market locale; no global `zh-CN` hardcode | `GLOBAL_HARDCODED_HUMAN_LOCALE=false` | `test_base_locale_policy_is_declared_and_not_hardcoded` |
| China market locale | C-01 Human entry surface | non-effect | `CHINA` profile defaults to `zh-CN` and Chinese explanations | `CHINA_MARKET_UI_DEFAULT=SIMPLIFIED_CHINESE` | `test_china_market_profile_preserves_chinese_first` |
| Human adoption decision | ADR-043 | Human Owner authority | adoption approved; candidate branch has no authority effect; effect activates when PR #142 becomes reachable from canonical `main` | `human_adoption_decision=APPROVED`; `effective_trigger=REACHABLE_FROM_CANONICAL_MAIN`; `implementation_authorized=false` | `test_human_adoption_decision_and_canonical_trigger_are_recorded` |
| D04 failure retention | ADR-038 / program state | §5 | no reopen or rewrite | `D04_CLOSED_FAILED_RETAINED=true` | `test_nonclaims_and_retained_failures` |
| P0-10 failure retention | TITMAS README / integration evidence | §5 | no result rewrite | `P0_10_FAIL_CLOSED_RETAINED=true` | `test_nonclaims_and_retained_failures` |

## Conflict semantics

```text
MISSING_PARENT_REFERENCE=PARENT_CONSTITUTION_REVIEW_REQUIRED
UNKNOWN_PRINCIPLE_ID=CONSTITUTION_TRACEABILITY_FAILURE
PRODUCT_COUNT_DRIFT=PRODUCT_BOUNDARY_FAILURE
UNCONDITIONAL_AUTHORITY_EFFECT_BEFORE_CANONICAL_REACHABILITY=AUTHORITY_ELEVATION_FAILURE
IMPLEMENTATION_AUTHORIZED_TRUE=IMPLEMENTATION_BOUNDARY_FAILURE
HISTORICAL_FAILURE_REMOVED=EVIDENCE_RETENTION_FAILURE
```

该矩阵追踪已获 Human Owner 采纳、并以 canonical merge 为生效条件的 contract。测试通过或
候选分支存在不等于规范已生效；只有决定可从 canonical `main` 到达时才正式生效。采纳仍
不等于实现、发布或生产正确性。

## Current implementation status and non-claims

| Candidate surface | Current implementation status | Required non-claim |
|---|---|---|
| Logical unified Agent entry | `NOT_IMPLEMENTED` | `UNIFIED_AGENT_ENTRY_IMPLEMENTED=false` |
| Distributed cross-platform enforcement | `NOT_PROVEN` | `CROSS_PLATFORM_ENFORCEMENT_PROVEN=false` |
| Selectable DCell module library | `NOT_IMPLEMENTED` | `SELECTABLE_DCELL_LIBRARY_IMPLEMENTED=false` |
| Ecological DCell qualification | `NOT_VALIDATED` | Manifest or classification does not prove ecological status |
| 80-Agent scale | `NOT_PROVEN` | `EIGHTY_AGENT_SCALE_PROVEN=false` |
| Production and commercial availability | `NOT_AUTHORIZED` | `PRODUCTION_READY=false`; `COMMERCIAL_OFFERING_AVAILABLE=false` |
| Real customer adoption | `NOT_PROVEN` | `REAL_CUSTOMER_ADOPTION_PROVEN=false` |
