---
document_id: DBA-INTEGRATION-GATES-0.1
title: Digital Biosphere Program Integration Gates v0.1
title_zh: 数字生物圈项目群集成闸门 v0.1
status: fail-closed-gate-baseline
automatic_approval: false
runtime_effect: none
last_reviewed: 2026-08-02
---

# Digital Biosphere Program Integration Gates v0.1（数字生物圈项目群集成闸门 v0.1）

## 1. Gate Principle（闸门原则）

所有跨项目推进默认 fail closed（失败关闭）。`NOT_ASSESSED`、`UNKNOWN`、`STALE`、`PARTIAL`、`PREPARED_ONLY` 和 `BLOCKED` 均不等于 `PASS`。

```text
PLAN_NE_AUTHORIZATION=true
SPECIFICATION_NE_IMPLEMENTATION=true
REFERENCE_NE_INTEGRATION=true
PASS_REQUIRES_SCOPED_EVIDENCE=true
DOWNSTREAM_GATE_CANNOT_BYPASS_UPSTREAM_GATE=true
TRUST_CONCLUSION_REQUIRES_EXECUTION_CONTEXT_BINDING=true
EXECUTION_CONTEXT_CHANGE_REQUIRES_REASSESSMENT=true
MISSING_CONTEXT_COMPARISON_FAILS_CLOSED=true
```

## 2. Standard Gates（标准闸门）

| gate_id | 名称 | 必须证明 | 最小证据 | 失败时 |
|---|---|---|---|---|
| `G0` | Portfolio Admission（项目组合准入） | 项目目的、角色、Owner、范围和非目标明确 | Project Charter、canonical source、准入决定 | 保持 `ADJACENT_CANDIDATE` 或范围外 |
| `G1` | Source Truth（事实来源） | 状态、Capability、Evidence 和 Release 有规范来源 | source path、branch、commit/version、freshness、冲突规则 | 状态保持 `UNKNOWN` / `NOT_ASSESSED` |
| `G2` | Architecture Contract（架构契约） | Owner、对象、方向、权限和失败边界明确 | DBA specification、ADR、data contract、negative rules | 不得创建跨项目实施任务 |
| `G3` | Implementation Mapping（实现映射） | 规范字段能映射到现有实现且没有重复权威 | 实现位置、版本、mapping、unsupported fields | 不得宣称集成可用 |
| `G4` | Conformance（符合性） | 正例、负例、兼容性和 fail-closed 行为在精确执行上下文中通过 | scoped test/validator result、fixture provenance、execution-context manifest、failure retention | 停止推进并保留失败；上下文变化时重评 |
| `G5` | Authorization（授权） | 具体变化有明确 decision 和 authorization reference | approved decision、scope、issuer、expiry/revocation | 不得执行、注册、激活或授予 Permission |
| `G6` | Execution Evidence（执行证据） | 实际执行形成连续、有来源且不可静默删除的记录 | execution、evidence、verification、failure records | 不得进入评价或采用结论 |
| `G7` | Evaluation and Adoption（评价与采纳） | SAEE 评价与人工决定分离且可追溯 | Fitness/Risk/Recommendation + Human Decision | 不得把 Recommendation 当作状态变化 |
| `G8` | Release and Adoption（发布与采用） | 发布、部署、采用和商业状态分别有证据 | release record、adoption decision、deployment evidence | 只能称为本地或未发布状态 |

## 3. Current Gate Matrix（当前闸门矩阵）

| integration_track | G0 | G1 | G2 | G3 | G4 | G5-G8 | 结论 |
|---|---|---|---|---|---|---|---|
| DBA Program Governance Cockpit | `PASS` | `PASS_REMOTE_BASELINE` | `PASS` | `NOT_APPLICABLE` | `PASS_CLEAN_CLONE_DOCUMENTATION` | `NOT_APPLICABLE` | 远端文档基线与干净检出已验证；不表示正式发布或子项目采用 |
| DBOS ↔ SAEE Contract | `PASS_CORE_ROLE` | `PASS_FROZEN_REMOTE_SOURCES` | `SPECIFICATION_DEFINED` | `PASS_SCOPED_CLEAN_CLONE` | `PASS_SCOPED_CLEAN_CLONE` | `G6_SYNTHETIC_RECORD_CHAIN_G7_RECOMMENDATION_ONLY` | 只可称为冻结源码上的合成契约符合性；不得称为生产集成或受治理演化闭环 |
| Research Agent Pilot ↔ DBOS / SAEE | `PASS_PILOT_ROLE` | `PARTIAL` | `SPECIFICATION_DEFINED` | `PREPARED_ONLY` | `NOT_ASSESSED` | `BLOCKED_NOT_READY` | 不得创建 Prototype、Agent、Runtime 或实验 |
| TITMAS Agent Action Gate | `REVIEW_REQUIRED_READY_FOR_HUMAN_DECISION` | `PASS_PUBLIC_MAIN_REFERENCE_SOURCE_PINNED` | `PARTIAL_SPECIFIED_CROSS_PROJECT_OWNER_REVIEW_REQUIRED` | `EXPERIMENTAL_REFERENCE_IMPLEMENTATION_MERGED_TO_MAIN` | `PASS_LOCAL_AND_CI_REFERENCE_CONFORMANCE_NOT_INDEPENDENT` | `G5_OWNER_FULL_MANAGEMENT_POLICY_NO_RUNTIME_PERMISSION_G6_SANDBOX_DRAFT_PR_AND_NATIVE_OPERATOR_SUPERVISED_SMOKE_NO_EXTERNAL_ACTION_G7_NOT_ASSESSED_ADVISORY_REVIEW_ONLY_NO_HUMAN_ADOPTION_DECISION_PRODUCT_NOT_RECOMMENDED_G8_NOT_RELEASED_NOT_ADOPTED_NOT_SUBMITTED` | public `main@6f1c83b`、两项 contract check、44 tests、sandbox Draft PR `#3` 与一次已销毁的官方 AgentTeams v1.2.0 本地 smoke 已验证；smoke 未完成自治链、未实施 per-Worker MCP ACL 或 Skill materialization，也未执行 provider action；G0 准入、G7 Human Adoption Decision、生产审查、release 和比赛提交仍未完成 |
| Adjacent components other than Media Evidence | `NOT_PASSED` | `NOT_ASSESSED` | `REVIEW_REQUIRED` | `NOT_ASSESSED` | `NOT_ASSESSED` | `NOT_ASSESSED` | 仅保留候选映射 |
| TITMAS Media Evidence v0.1.0 | `PASS_ADMITTED_AS_ADJACENT_CANDIDATE` | `PASS` | `PASS_BOUNDARY_ONLY_MAPPING_NOT_AUTHORIZED` | `NOT_ASSESSED` | `NOT_ASSESSED` | `G5_NOT_AUTHORIZED_G6_NOT_EXECUTED_G7_NOT_ASSESSED_G8_NOT_RELEASED_NOT_ADOPTED` | 只完成有界项目组合准入和对象边界；DBOS mapping、跨项目符合性、标准、核心、生产和采用均未建立 |
| Trusted Multi-Agent Infrastructure Developer Preview | `PASS_CORE_SCOPE` | `PASS_FROZEN_REMOTE_BASELINE` | `PASS` | `PASS_SCOPED_CLEAN_CLONE` | `AGENT_CUSTOMER_RERUN_PASS` | `G6_SYNTHETIC_G7_PASS_G8_RELEASED_BY_ADR_022` | exact wheel 匿名分发、GitHub Release、百度云 formal deployment 和人工发布决定通过；不是生产采用 |
| P0-10 Unknown-Agent Technical Onboarding | `PASS_UNIQUE_MAINLINE_FROZEN_BY_D16` | `PASS_MACHINE_TRUTH_AND_FROZEN_CONTRACTS` | `PASS_API_V1_SDK_MCP_BOUNDARIES` | `PASS_RUNTIME_ALIGNMENT` | `FAIL_CLOSED_AFTER_RUNTIME_ALIGNMENT` | `G5_D15_ONLY_G6_FAILURE_RETAINED_G7_NOT_ASSESSED_G8_NOT_AUTHORIZED` | discovery、MCP/SDK、preflight call 和 Receipt fetch 已到达；Schema-valid PASS、VALID verification 和 second-task reuse 未达，不能以 CI/HTTP/fixture/human-guided success 替代 |
| D19 Discovery Evolution | `PASS_EXPLICIT_HUMAN_DECISION` | `PASS_DBA_OWNER_ROUTING` | `PASS_SEVEN_SCHEMAS_AND_POLICY` | `PASS_LOCAL_REFERENCE_25_TESTS` | `PENDING_DRAFT_PR_DEMO` | `G5_DRAFT_PR_ONLY_G6_G8_NOT_AUTHORIZED` | ER-1 只允许隔离实现、确定性评价、回滚与 Draft PR；不授权 merge、release、deployment、生产 Runtime 或 P0-10 重开 |
| TITMAS Agent-Native Commercial Maturity | `PASS_PROGRAM_ROLE` | `PASS_VERIFIED_SOURCE_BASELINE` | `PASS_ADR_036` | `NOT_STARTED` | `NOT_ASSESSED` | `G5_BOUNDED_TECHNICAL_AUTHORIZATION_G6_G8_NOT_ASSESSED` | 只授权可逆技术建设；商业技术、Paid Beta、Production 和成熟度全部保持 false |
| D29 Customer Entry Reference Implementation | `PASS_EXISTING_PRIVATE_PLATFORM` | `PASS_SOURCE_PINNED_GATEWAY_MAIN_C029263` | `PASS_C01_AND_D29_BOUNDARIES` | `PASS_BOUNDED_REFERENCE_CE1_CE5` | `PASS_SOURCE_TESTS_AND_CLEAN_CLONE_SYNTHETIC_SCOPE` | `G5_NO_REAL_CUSTOMER_AUTHORIZATION_G6_SYNTHETIC_ONLY_G7_G8_NOT_AUTHORIZED` | PostgreSQL 应用接线、Observer/FirstValue、只读 Console 和软件交付 Proof 已形成有界参考实现；未部署、不可购买、无真实客户或外部动作 |
| TITMAS Commercial Private Infrastructure Direction | `PASS_HUMAN_OWNER_DECISION` | `PASS_DBA_CANONICAL_DOCUMENTS` | `PASS_ADR_042_AND_CONSTITUTION` | `NOT_APPLICABLE_STRATEGY_ONLY` | `PASS_ENTRY_AND_SCHEMA_CONSISTENCY` | `G5_G8_NOT_AUTHORIZED` | 私有核心与有界公共互操作表面已成为当前战略；不授权实现、公开核心、社区、客户、Release 或 Deployment |

### Developer Preview Gate Detail（开发者预览闸门明细）

| preview milestone | required gate | 当前结果 | 直接证据 | 下一状态条件 |
|---|---|---|---|---|
| `DP-1` | `G1/G2` | `PASS_CLEAN_CLONE` | DBA `91928e3` 已推送；99 个 Markdown 文件、317 个本地链接、0 缺失 | 保持同一公开入口 |
| `DP-2` | `G3/G4` | `PASS_CLEAN_CLONE_WHEEL_CANDIDATE` | DBOS `cd3f867` fresh install；334/334 tests；34/34 validators；public-safe wheel clean install PASS | 保持 exact commit；未获准前不得上传 wheel |
| `DP-3` | `G4/G6` | `PASS_SYNTHETIC_SCOPE` | 11/11 tests；3 角色、3 execution records、3 Evidence References、9 Validation results | 不外推为真实 Agent/Execution |
| `DP-4` | `G3/G4/G7` | `PASS_CLEAN_CLONE_ADVISORY_ONLY` | SAEE `2173c25` public main；8/8 adapter tests；pipeline 输出 `HOLD` 且无 Authority | 不外推为 SAEE 决策权或生产集成 |
| `DP-5A` | `G8_PREPARATION` | `PASS_AGENT_PROTOCOL_FROZEN` | `TMAI-ACV-20260721-001`、Protocol、12-session plan、ADR-021 | 不表示 Agent instance、客户采用或发布 |
| `DP-5B` | `G1/G4/G8_AGENT_VALIDATION` | `CONDITIONAL` | 2 Providers、4 models、12/12 parsed；公开识别 6/6；权限错误 0；4 个阈值失败 | 修复 agent-readable package，并以相同阈值复测 |
| `DP-5C` | `G1/G4/G8_AGENT_RERUN` | `PASS` | `TMAI-ACV-20260722-002`：2 Providers、4 models、12/12 parsed、全部阈值通过、权限错误 0 | 保留原 `001=CONDITIONAL`；开放网络由独立观察处理 |
| `DP-5D` | `G1/G8_OPEN_WEB_OBSERVATION` | `PARTIAL_METADATA_ONLY` | `TMAI-OWD-20260722-001`：GitHub 完整新 description 已命中；规范英文名、中文名和 4 个公开搜索仍无命中 | 规范名称索引刷新后复查，或 Human Owner 显式接受限制 |
| `DP-R` | `G8` | `PASS_RELEASED_WITH_DISCLOSED_LIMITATIONS` | `ADR-022`；exact wheel URL/hash/clean install；GitHub `v0.1-developer-preview`；百度云 formal artifact；`R-015` 与 `PARTIAL_METADATA_ONLY` 继续披露 | 发布后观察；任何生产、Runtime、Permission 或新实现需独立 gate |

### P0-10 D16 Closure Detail

| closure gate | current result | exact continuation boundary |
|---|---|---|
| Unique mainline | `FROZEN` | Unknown Agent through second-task reuse; no adjacent replacement |
| D12 history | `FAILURE_RETAINED` | PR `titmas-integrations#5` stays Draft and unmerged |
| Last diagnostic | `D15_AUTHORIZED_NOT_EXECUTED_BY_D16` | one privacy-preserving structural diagnostic only |
| Root-cause threshold | `NOT_ASSESSED` | confidence `>=0.85` and competing layers excluded |
| Remediation | `NOT_AUTHORIZED` | at most one future single-layer PR after a separate Human Decision |
| Final rerun | `NOT_AUTHORIZED_YET` | at most one rerun after the separately authorized fix |
| Non-blocking development | `HOLD` | standards, profiles, Demos, adapters, Portfolio, landing, community and commercial expansion |

```text
DISCOVERY_PASS_NE_ONBOARDING_PASS=true
RECEIPT_FETCH_NE_RECEIPT_VERIFY=true
PREFLIGHT_CALL_NE_PREFLIGHT_PASS=true
MAX_ADDITIONAL_DIAGNOSTIC_ROUNDS=1
MAX_REMEDIATION_PRS_AFTER_D15=1
MAX_FINAL_RERUNS=1
```

## 4. Gate Evidence Record（闸门证据记录）

每次 gate 判断至少记录：

```text
gate_record_id=
gate_id=
integration_track=
scope=
evidence_refs=
observed_version_or_commit=
execution_context_manifest_ref=
prior_context_manifest_digest=
current_context_manifest_digest=
changed_context_dimensions=
conclusion_inheritance=UNCHANGED|REASSESSMENT_REQUIRED|HOLD_MISSING_EVIDENCE|REVIEW_REQUIRED|REVALIDATED_BOUNDED|INVALIDATED_FOR_DECLARED_SCOPE
positive_checks=
negative_checks=
unknowns=
result=PASS|FAIL|BLOCKED|NOT_ASSESSED|NOT_APPLICABLE
reviewed_by_ref=
reviewed_at=
next_gate=
```

本格式是文档契约，不创建 Gate Service（闸门服务）、API、Permission 或自动审批系统。

同一模型名称、版本或工件 digest 不足以继承旧 gate 结论。若上下文 manifest 无法比较、
关键字段为 `UNKNOWN`，或发生 `ADR-039` 所列实质变化，旧 `PASS` 必须 fail closed 到重评
状态。重评状态本身不执行 Runtime 操作，也不撤销 Permission。

## 5. Gate Authority Boundary（闸门权力边界）

- DBA 定义 gate 和记录评审结果；
- 子项目提供自己领域内的实现和证据；
- Human Decision Authority 决定是否采纳或授权；
- DBOS 只在有效授权下执行；
- SAEE 评价 gate 产生的运行材料，但不能批准自己进入下一 gate；
- validator pass（验证器通过）只对声明范围有效，不能代替人工决策、发布或采用。

```text
INTEGRATION_GATES_DEFINED=true
AUTOMATIC_GATE_APPROVAL=false
IMPLEMENTATION_AUTHORIZED=FROZEN_PUBLIC_SAFE_SOURCES_ONLY
EXECUTION_AUTHORIZED=false
RELEASE_AUTHORIZED=true
DEVELOPER_PREVIEW_RELEASED=true
```

## 6. Commercial Maturity Gate Detail

| gate | current result | required evidence |
|---|---|---|
| `CM-G1` Source and state | `PASS_WITH_LIMITATIONS` | exact DBA/Gateway/Integrations commits, server releases, retained Stage 5.8 result |
| `CM-G2` Architecture | `PASS_BASELINE` | ADR-036, commercial architecture, security, operations and data boundaries |
| `CM-G3` Multi-tenant implementation | `PASS_IMPLEMENTED` | Gateway `c319001…` includes PostgreSQL migrations, forced RLS and Tenant/Agent/credential isolation tests |
| `CM-G4` Receipt and metering | `BLOCKED_CR01_LEDGER_INTEGRITY` | current implementation exists, but isolated restore found 2 unverifiable historical synthetic Receipt signatures |
| `CM-G5` Security and operations | `BLOCKED_CR01` | backup integrity and partial rollback pass; complete restore, cross-Tenant restored runtime test, sustained load, headroom and formal incident drill remain incomplete |
| `CM-G6` Agent onboarding | `IN_PROGRESS` | public-safe SDK/Adapter source is hardened at `titmas-integrations@6ed4dad…`; packages remain unpublished and autonomous two-task reuse remains unassessed |
| `CM-G7` External Agent Beta | `NOT_STARTED` | independent providers, frameworks, tenants, identities and calls |
| `CM-G8` Paid/production maturity | `WAITING_FOR_UPSTREAM_GATES` | D04 is closed failed-retained; the final-form P0 implementation decision, external Agent Beta, separate Paid Beta clean-genesis/signer decision, legal/pricing inputs, real payment/use and elapsed reliability evidence remain required |

The Build-versus-Adopt audit passing with limitations is not a runtime gate.
No component may be installed, started, purchased or deployed until
`AUTHORIZE_FINAL_FORM_IMPLEMENTATION_FROM_ACCEPTED_ADOPTION_MATRIX` defines an
exact repository, path, test, rollback and data boundary. P1 and P2 remain
independently closed even if P0 is later accepted.

## 7. C-01 Customer Entry Architecture Gate

| gate | result | bounded evidence |
|---|---|---|
| `C01-G1` Direction | `PASS` | one platform/core, exact four products, Observer non-product, no duplicate cores |
| `C01-G2` Machine contract | `PASS` | JSON parsing, FirstValue schema validation, reason-code and reference closure |
| `C01-G3` Customer entry | `PASS` | T01-T15 baseline and negative-mutation tests |
| `C01-G4` Cross-document consistency | `PASS` | Constitution, D29, private platform, portfolio, console, website and discovery surfaces |
| `C01-G5` Change boundary | `PASS` | no core/runtime/database/site implementation, owner-map/resolver or PR #113 change |

These are the recorded document-and-machine-contract results. At this C-01
architecture gate, implementation evaluation and measured customer experience
were `NOT_ASSESSED`; commercial availability remains unavailable. The later
source-pinned implementation projection below does not rewrite this historical
scope or create deployment or customer authority.

### D29 current implementation projection

The earlier C-01 gate remains the architecture-contract result at its recorded
scope. A later, separately authorized implementation sequence is now observed
from `joy7758/titmas-sandbox-gateway` canonical
`main@1a065f1702e355d5f5ed566bdfd3e895cdca2540`:

| implementation gate | result | retained boundary |
|---|---|---|
| Store wiring | `PASS_REFERENCE_NOT_DEPLOYED` | Memory and PostgreSQL implementations share the bounded Store Protocol; no new table or API v1 change |
| Observer / FirstValue | `PASS_SYNTHETIC_REFERENCE` | zero customer data, no production Permission, no external action |
| Console | `PASS_READ_ONLY_REFERENCE_NOT_DEPLOYED` | missing sources remain `NOT_ASSESSED`; Human view derives from machine projections |
| Monitor / Enforce proof | `PASS_SYNTHETIC_NON_BINDING` | no real customer authorization, release, merge or provider call |
| Durable Receipt read | `PASS_REFERENCE_NOT_DEPLOYED` | Tenant/Workspace/Agent credential binding; no offering or production access |
| Durable Audit / Health projection | `PASS_COMPLETE_DECLARED_WORKSPACE_SCOPE_NOT_DEPLOYED` | PostgreSQL verifies every canonical Tenant link and exports complete declared Workspace content; unrelated content, offline non-membership proof and external anchor remain absent |
| Durable credential lifecycle | `PASS_SOURCE_AND_EPHEMERAL_POSTGRES_CI_NOT_DEPLOYED` | offline rotation/revocation preserves Tenant, Agent, quota, scopes and operation boundary; no customer self-service or deployment |
| Workspace deletion lifecycle | `PASS_SOURCE_AND_EPHEMERAL_POSTGRES_CI_NOT_DEPLOYED` | auditable request/execute/verify path revokes Workspace access and redacts mutable customer references; retained evidence exceptions remain immutable |
| Workspace retention lifecycle | `PASS_SOURCE_AND_EPHEMERAL_POSTGRES_CI_NOT_DEPLOYED` | managed 7/30/90-day policies and bounded private/on-prem days are machine-defined; enforcement is offline and not deployed |
| Security drill execution | `EXECUTED_PASS_AUTHORITY_CLOSED` | PR #58 records the bounded incident and formal rollback drills: 2166 ms incident recovery, 2604 ms rollback and 2012 ms forward recovery; temporary authority is closed |
| Security engineering control mapping | `FAIL_CLOSED_RETAINED_CR01_LIMITATION` | 20 controls mapped: 18 PASS, 0 PARTIAL, 1 FAIL_RETAINED, 0 NOT_ASSESSED, 1 NOT_APPLICABLE; open Blocker/High counts are zero, while one CR01 disposition and `D29-SEC-11=FAIL_RETAINED` remain |
| Commercial availability | `FAIL_CLOSED_NOT_AVAILABLE` | paid Monitor, customer Enforce, deployment, customer, payment and Production remain false |

`PASS` above applies only to the source-pinned reference scope. Receipt
verification is not Truth, Gate decision is not execution, and a synthetic
authorization profile is not customer authorization.
