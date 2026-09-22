---
document_id: DBA-MASTER-ROADMAP-0.1
title: Digital Biosphere Master Roadmap v0.1
title_zh: 数字生物圈总路线图 v0.1
status: program-sequencing-baseline
current_milestone: P0-10-UNKNOWN-AGENT-ONBOARDING-CLOSURE
roadmap_is_authorization: false
roadmap_is_implementation: false
last_reviewed: 2026-08-02
---

# Digital Biosphere Master Roadmap v0.1（数字生物圈总路线图 v0.1）

## 1. Roadmap Rule（路线图规则）

本路线图定义跨项目推进顺序和进入条件，不授权代码修改、Runtime、Agent、实验、部署、发布或外部采用。里程碑只有在对应 gate evidence（闸门证据）存在时才能升级状态。

合法状态：

```text
NOT_STARTED
PLANNED
IN_PROGRESS
BASELINE_DEFINED
GATE_PASSED
BLOCKED
DEFERRED
SUPERSEDED
```

## 2. Program Milestones（项目群里程碑）

Developer Preview 是已完成的历史发布阶段；当前执行主线是有界的商业私有基础设施
验证与客户进入准备。原 `M0` 至 `M8` 继续保留为长期项目群路线，不因阶段切换被删除。

| preview milestone | 目标 | primary repository | 当前状态 | 完成证据 | 下一步 |
|---|---|---|---|---|---|
| `DP-1` | 建立 Digital Biosphere 统一公开入口 | DBA | `GATE_PASSED` | Public Overview、Developer Preview Plan、Release Plan、ADR-017、链接与边界验证 | 保持未发布边界 |
| `DP-2` | 建立可复制、可回归测试的 DBOS Developer Preview | DBOS | `GATE_PASSED` | `main@cd3f867`、local editable install、334/334 tests、34/34 validators、public-safe wheel clean install；历史 Evidence 未改写 | 由 `DQ-016` 决定是否公开 exact wheel |
| `DP-3` | 建立三角色 Multi-Agent Trust Demo 和跨项目 fixture | Demo + DBOS | `GATE_PASSED` | Research/Analysis/Review 角色链、3/3 records、11/11 tests、确定性重放、同一 SAEE envelope | 保持 synthetic/non-Agent 边界 |
| `DP-4` | 建立并测试 SAEE Evaluation Layer v0.1 | SAEE | `GATE_PASSED` | public `main@2173c25` 精确 19/19 blobs、8/8 tests、公共 smoke、跨项目 Clean Clone、无写回 | 保持只读和 advisory-only 边界 |
| `DP-5A` | 冻结 Agent Customer Validation Protocol | DBA | `GATE_PASSED` | `AGENT-CUSTOMER-VALIDATION-PROTOCOL.md`、6 个画像、12 个会话、预冻结阈值与 ADR-021 | 执行受控跨模型基线 |
| `DP-5B` | 执行 Agent Customer Validation baseline | DBA + Human Program Owner | `GATE_PASSED_CONDITIONAL` | 千帆／方舟 12/12 完成；公开识别 6/6；权限安全错误 0；总体 `CONDITIONAL` | 修复 4 个失败阈值，不扩展 DBOS 功能 |
| `DP-5C` | Agent-readable remediation and rerun（智能体可读修复与复测） | DBA | `GATE_PASSED` | `TMAI-ACV-20260722-002`：12/12 sessions、全部阈值、权限安全和负控通过；overall verdict 12/12 `CONDITIONAL` | 保留 API 会话的 `OPEN_WEB_DISCOVERY=NOT_ASSESSED`，由 DP-5D 单独观察自然发现 |
| `DP-5D` | Open-web discovery observation（开放网络发现观察） | DBA | `GATE_PASSED_WITH_ACCEPTED_LIMITATION` | `TMAI-OWD-20260722-001=PARTIAL_METADATA_ONLY`；`ADR-022` 为 v0.1 接受并要求继续披露 | 索引刷新后继续复查，不升级当前发现事实 |
| `DP-R` | Developer Preview Release Decision | DBA + Human Release Authority | `GATE_PASSED` | `ADR-022`、`released_by_ref=zhangbin`、exact wheel、GitHub Release、百度云 formal deployment 与公开复验 | 进入发布后观察；不自动启动新功能或长期 `M2` |

| milestone | 目标 | primary repository | 当前状态 | 完成证据 | 下一步 |
|---|---|---|---|---|---|
| `M0` | 建立 DBA、DBOS、SAEE、Digital Entity 和 Governance Decision 的基本边界 | DBA | `GATE_PASSED` | 当前架构规范、接口契约、ADR-001 至 ADR-015 | 保持一致性，不再重复定义 |
| `M1` | 将 DBA 建成项目群治理与架构总驾驶舱 | DBA | `BASELINE_DEFINED` | 本路线图、Portfolio、Status、Decision、Gate、Risk、Program Governance Spec 和 ADR-016 | 完成验证并决定版本发布 |
| `M2` | 为核心项目确认 canonical status source 与刷新规则 | DBA 协调；各项目提供来源 | `PLANNED` | DBOS、SAEE、Research Agent Pilot 的明确状态入口、Owner、freshness 和冲突处理记录 | 处理 `DQ-003` |
| `M3` | 建立 DBOS ↔ SAEE contract conformance baseline（契约符合性基线） | DBA 协调；DBOS/SAEE 分别实施 | `PLANNED` | 字段映射、版本、正负用例、验证结果；不要求真实 Runtime 调用 | 处理 `DQ-004` |
| `M4` | 建立 Digital Entity admission and registration conformance（准入与登记符合性） | DBOS；DBA gate | `NOT_STARTED` | Candidate、Decision、Authorization、Registration 的连续引用和负例证据 | M2、M3 先通过 |
| `M5` | 决定 Research Agent Prototype（科研智能体原型）是否获准创建 | Research Agent Pilot；DBA 协调 | `NOT_STARTED` | Human Review、approved sources、protocol freeze、prototype authorization | 当前保持 `NOT_READY` |
| `M6` | 执行第一个受控 Digital Entity research loop（数字主体研究闭环） | Research Agent Pilot + DBOS + SAEE | `NOT_STARTED` | 显式实验授权、执行记录、Evidence、Verification、Evaluation、Human Decision | 不得由路线图自动启动 |
| `M7` | 建立可重复的多主体接入和联邦符合性 | DBOS + future Digital Entities | `NOT_STARTED` | 至少一个已验证 Pilot 后的通用接入契约和负例 | 不能从单一 Pilot 直接外推 |
| `M8` | 推进受控客户接入、商业交付与支持服务 | 各相应项目 | `IN_PROGRESS` | D29 设计伙伴入口、私有核心边界和交付基础已定义；商业、部署、支持与客户事实仍分别验证 | 不得用战略文档声称已可售、已部署或已采用 |

## 3. Critical Path（关键路径）

```text
DP-1 Public Entry
  → DP-2 DBOS Developer Preview
  → DP-3 Multi-Agent Trust Demo
  → DP-4 SAEE Evaluation Layer
  → DP-5A Agent Customer Protocol
  → DP-5B Agent Customer Baseline
  → DP-5C Agent-readable Remediation and Rerun
  → DP-5D Open-Web Discovery Observation
  → DP-R Human Release Decision

Long-term continuation:
M2 Canonical Status Sources
  → M3 DBOS / SAEE Conformance
  → M4 Entity Admission Conformance
  → M5 Human Prototype Decision
  → M6 Controlled Research Loop
  → M7 Repeatable Multi-entity Onboarding
```

`M8` 不是 `M6` 或 `M7` 的自动结果。Commercial Offering（商业服务）、Certification（认证）和 Marketplace（市场）需要独立决策与证据。

## 4. Current Program Focus（当前项目群焦点）

```text
CURRENT_FOCUS=D29_COMMERCIAL_PRIVATE_PLATFORM_AND_BOUNDED_CUSTOMER_ENTRY
CURRENT_STRATEGY=COMMERCIAL_PRIVATE_INFRASTRUCTURE
CURRENT_ENTRY=OBSERVER_TO_MONITOR_TO_SEPARATELY_AUTHORIZED_ENFORCE
NEXT_BLOCKER=COMMERCIAL_SECURITY_SUPPORT_PRICING_LEGAL_DEPLOYMENT_AND_CUSTOMER_GATES
NEXT_DECISION=SEPARATE_HUMAN_DECISIONS_REQUIRED_FOR_OFFER_DEPLOYMENT_ACCESS_AND_CUSTOMER_DATA
NEXT_DELIVERY=ZERO_CUSTOMER_DATA_SYNTHETIC_FIRST_VALUE_AND_DURABLE_EVIDENCE_READ_VALIDATION
NEXT_INTEGRATION=NONE_AUTOMATICALLY_AUTHORIZED_BY_PUBLIC_INTEROPERABILITY_SURFACES
DQ_015_AGENT_NATIVE_VALIDATION_ACCEPTED=true
BASELINE_VALIDATION_ID=TMAI-ACV-20260721-001
BASELINE_RESULT=CONDITIONAL
RERUN_VALIDATION_ID=TMAI-ACV-20260722-002
RERUN_RESULT=PASS
OPEN_WEB_DISCOVERY_OBSERVATION_ID=TMAI-OWD-20260722-001
OPEN_WEB_DISCOVERY_RESULT=PARTIAL_METADATA_ONLY
GITHUB_DISCOVERY_METADATA_REMEDIATED=true
GITHUB_METADATA_DESCRIPTION_MATCH=true
OPEN_WEB_CANONICAL_NAME_MATCH=false
CROSS_PROJECT_CLEAN_CLONE_PASS=true
HUMAN_PARTICIPANT_SOURCE_REQUIRED=false
RESEARCH_AGENT_PROTOTYPE_AUTHORIZED=false
```

当前不应继续增加新的 Entity、生产 Runtime 或无验证接口承诺。优先任务是形成零客户
数据、可验证、可测量首次价值的商业私有基础设施闭环，并保持 Observer、Monitor、Gate、
Receipt、Audit、Health 与私有 canonical core 的边界。公共互操作表面只服务 Agent 发现、
调用和验证，不再承担社区增长或核心开源目标。

## 5. Roadmap Non-claims（路线图非声明）

```text
ROADMAP_DEFINED=true
ROADMAP_APPROVES_IMPLEMENTATION=false
ROADMAP_APPROVES_EXECUTION=false
ROADMAP_APPROVES_EXPERIMENT=false
ROADMAP_PROVES_INTEGRATION=false
ROADMAP_PROVES_ADOPTION=false
```

## 6. Historical TITMAS Open Standards Route（历史开放标准路线）

该路线已由 `ADR-042` 取代，不再是当前产品、社区或增长主线。以下 milestone 只保留
历史追踪，不得自动恢复公共贡献、社区、源码开放或 Release。

| milestone | objective | status | required evidence |
|---|---|---|---|
| `TOS-1` | Selective canonical integration | `HISTORICAL_COMPLETE` | retained historical evidence |
| `TOS-2` | Human merge review | `HISTORICAL_COMPLETE` | retained historical evidence |
| `TOS-3` | Security transport activation decision | `SUPERSEDED_NOT_CURRENT_ROUTE` | no current public transport activation |
| `TOS-4` | Limited public contribution preview | `SUPERSEDED_NOT_CURRENT_ROUTE` | future activation requires a new Human Decision |
| `TOS-5` | Agent-native contribution pilot | `SUPERSEDED_NOT_CURRENT_ROUTE` | future activation requires a new Human Decision |
| `TOS-6` | Community Preview | `SUPERSEDED_NOT_CURRENT_ROUTE` | community is not the current route |

```text
CURRENT_TITMAS_FOCUS=COMMERCIAL_PRIVATE_AGENT_INFRASTRUCTURE
OPEN_STANDARDS_COMMUNITY_IS_MAINLINE=false
OPEN_STANDARDS_COMMUNITY_STATUS=SUPERSEDED_HISTORICAL_NOT_CURRENT_ROUTE
PRIVATE_CORE_IS_CANONICAL=true
PUBLIC_INTEROPERABILITY_SURFACES_RETAINED=true
CALIBRATION_IS_SUPPORTING_VALIDATION_ONLY=true
CALIBRATION_V0_3_AUTHORIZED=false
```

## 7. Stage 5.7 Agent-Native Selection and ROI Benchmark

`ADR-035` 将下一条验证主线修正为：

```text
Anonymous comparable infrastructure options
  → randomized isolated model sessions
    → discovery / repair / composition / reuse scenarios
      → machine metrics and retained failures
        → Agent Selection Auditor
          → bounded conclusion
```

| milestone | objective | status | required evidence |
|---|---|---|---|
| `S5.7-A` | 冻结匿名选项、场景、随机化、ROI 评分和上限 | `COMPLETE` | Sandbox PR `#11`、102 tests、空白报告、无品牌提示检查 |
| `S5.7-B` | 执行多供应商、多模型受控会话 | `COMPLETE` | 3 providers、4 exact models、24 valid runs、失败完整保留 |
| `S5.7-C` | 独立 Agent Selection Auditor 复核 | `PASS` | 随机化、匿名、公平、无事后改分、未知保留全部通过 |
| `S5.7-D` | 提交脱敏结果和有界结论 | `COMPLETE` | Sandbox PR `#14`、manifest、hash chain、aggregate、limitations |

E01 与付费真人试用不再是本路线的前置 gate。Stage 5.7 可以证明选择和相对 ROI，
不能证明客户采用、合同、正式标准、Production 或 Human Authority 已被替代。

Stage 5.7 的 canonical sanitized evidence 位于
`titmas-sandbox-gateway@ab1d875921d0a68c5b91fa054f692f1284a75949`。
24/24 会话把匿名 Option D 排在第一位，但只有 7/24 独占选择；冻结公式平均
Agent ROI 为 `12.504572`。该结果只适用于合成基准，不是商业采用或生产可靠性证据。

## 8. Agent-Native Commercial Maturity Program

| phase | objective | status | exit evidence |
|---|---|---|---|
| `CM-0` | verify Stage 5.8 and current infrastructure truth | `PASS_WITH_LIMITATIONS` | exact source, retained unknowns/failures, server and public baseline |
| `CM-1` | governance, state machine and architecture freeze | `GATE_PASSED` | ADR-036, state schemas, architecture/security/operations/data contracts |
| `CM-2` | first private multi-tenant vertical slice | `GATE_PASSED` | Gateway `c319001…`: tenant-bound credential, preflight, signed receipt, idempotent usage/quota |
| `CM-3` | security and operational candidate | `BLOCKED_RETAINED_CR01` | 18/20 controls pass and bounded incident/formal rollback drills pass; CR-01 restore remains failed-retained and independent evaluation is not executed |
| `CM-4` | machine onboarding and public-safe integrations | `IMPLEMENTATION_COMPLETE_ACCEPTANCE_FAIL_CLOSED` | machine truth、API v1、Runtime alignment、generated SDK 和 MCP Adapter 已通过；Unknown Agent 完整接入仍未通过 |
| `CM-5` | internal soak and capacity | `BLOCKED` | frozen capacity observations exist; sustained test, headroom and 72-hour soak did not start |
| `CM-6` | external Agent Beta | `NOT_STARTED` | independent tenants, Agents, frameworks, calls and repeat-use evidence |
| `CM-7` | Paid Beta Human Decision | `BLOCKED_INPUT` | technical readiness, Beta, legal/pricing packets and Human authorization |
| `CM-8` | 30-day production/maturity observation | `NOT_STARTED` | real payment, availability, repeat use and maturity thresholds |

Waiting for real elapsed time, external Agent usage or Human commercial
decisions is a valid state and must not be bypassed.

Current stop:

```text
CR01_STATUS=BLOCKED_LEDGER_INTEGRITY_FAILED_RETAINED
PROGRAM_STATUS=WAITING_FOR_HUMAN_DECISION
D04_FINAL_STATUS=CLOSED_FAILED_RETAINED
D04_FURTHER_CANARY_RETRIES_AUTHORIZED=false
LEGACY_LEDGER_CLASSIFICATION=INTERNAL_EXPERIMENTAL_LEDGER
FUTURE_PRODUCTION_LEDGER_MODE=CLEAN_GENESIS
BUILD_VERSUS_ADOPT_AUDIT_COMPLETE=true
FINAL_FORM_IMPLEMENTATION_PLAN_READY=true
FINAL_FORM_CORE_IMPLEMENTATION_COMPLETE=true
AGENT_FIRST_ACCEPTANCE_COMPLETE=false
NEW_FEATURE_DEVELOPMENT_FROZEN=true
D15_REMAINS_AUTHORIZED=true
NEXT_HUMAN_DECISION=AFTER_D15_CHOOSE_ONE_BOUNDED_SINGLE_LAYER_REMEDIATION_OR_FINAL_NOT_ASSESSED_DISPOSITION
```

## 9. D16 Unique Mainline and Closure Budget

The current technical roadmap has one path only:

```text
Unknown Agent
  -> Machine Discovery
  -> Capability and Catalog
  -> Schema Selection
  -> Schema-valid Object Construction
  -> Preflight
  -> Receipt Fetch
  -> Receipt Verification
  -> Second-task Reuse
```

| Step | Current state | Closure evidence |
|---|---|---|
| Machine truth | `PASS` | machine entry and frozen API surfaces remain reachable |
| API v1 Contract | `PASS` | frozen contract is retained |
| Runtime alignment | `PASS` | legacy envelope mismatch is resolved |
| Generated SDK | `PASS` | generated Python and TypeScript surfaces retained |
| MCP Adapter | `PASS` | Adapter reuses the SDK boundary |
| Agent-first acceptance | `FAIL_CLOSED_AFTER_RUNTIME_ALIGNMENT` | PR `titmas-integrations#5`; Receipt fetch reached but valid object/verification/reuse gates not met |

All other roadmap expansion is `HOLD_NON_BLOCKING`. Existing artifacts remain
available as historical or adjacent candidates, but no new standard alignment,
reference model, application profile, Demo, Portfolio candidate, Adapter,
landing page, community feature or commercial feature may displace P0-10.

## 10. D19 Bounded Discovery Evolution Exception

D19 v2.1 is a Human-authorized, narrow exception to the D16 development freeze.
It does not reopen P0-10 or resume unbounded feature development.

| milestone | objective | status | exit evidence |
|---|---|---|---|
| `D19-E1` | Freeze machine-readable evolution policy and seven missing object schemas | `IMPLEMENTED_CANDIDATE` | JSON parse, schema validation, canonical-owner and authority checks |
| `D19-E2` | Validate bounded ER-1 reference path | `IMPLEMENTED_CANDIDATE` | 25/25 tests, deterministic replay, secret/disclosure scans |
| `D19-E3` | Open first synthetic self-healing Draft PR | `AUTHORIZED_NOT_MERGED` | stale derived registry repaired, rollback and lineage retained, Draft PR only |
| `D19-E4` | Human disposition of candidate | `NOT_AUTHORIZED` | independent review plus new merge/activation decision |

```text
UNBOUNDED_PRODUCT_DEVELOPMENT=FROZEN
EVIDENCE_TRIGGERED_EVOLUTION=OPEN
P0_10_REOPENED=false
PRODUCTION_ACTIVATION_AUTHORIZED=false
```

```text
MAX_ADDITIONAL_DIAGNOSTIC_ROUNDS=1
MAX_REMEDIATION_PRS_AFTER_D15=1
MAX_FINAL_RERUNS=1
INDEFINITE_AGENT_RETRY=false
INDEFINITE_OBSERVABILITY_ADDITION=false
```

If D15 does not establish a single-layer root cause with confidence at least
`0.85` while excluding competing layers, the route terminates as
`NOT_ASSESSED_DIAGNOSTIC_LIMIT_REACHED`. If one separately authorized fix and
the one final rerun fail, the route terminates as `FAIL_CLOSED`. Either terminal
result ends this development round without creating production, commercial,
certification, adoption or conformance claims.

## 11. C-01 and D29 Customer Entry Architecture

| milestone | objective | status | exit evidence |
|---|---|---|---|
| `C01-A1` | Freeze low-friction entry as display-order one | `ARCHITECTURE_FROZEN` | ADR-041, Constitution and C-01 machine contract |
| `C01-A2` | Preserve one platform, one core, four products and classify Observer as entry layer | `CONTRACT_CONFORMANCE_PASS` | catalog and T05/T06/T14/T15 tests |
| `C01-A3` | Define Human/Agent entry, FirstValue routes and reversible exit | `CONTRACT_CONFORMANCE_PASS` | entry surfaces, examples, access modes and exit controls |
| `C01-A4` | Implement Observer and measured first value | `BOUNDED_REFERENCE_COMPLETE_NOT_DEPLOYED` | Gateway CE-1/CE-2 retained on canonical `main@1a065f1702e355d5f5ed566bdfd3e895cdca2540`; zero customer data and no real action |
| `C01-A5` | Expose read-only Agent/Human Console projections | `BOUNDED_REFERENCE_COMPLETE_NOT_DEPLOYED` | Gateway CE-3/CE-4; machine projections are canonical and Human HTML is derived |
| `C01-A6` | Validate one software-delivery Monitor/Enforce comparison | `TESTED_SYNTHETIC_ONLY_NOT_DEPLOYED` | Gateway CE-5; existing Gate, Receipt and Audit reused; real customer authorization and external action count remain zero |
| `C01-A7` | Persist bounded Receipt/Audit/Health read projections | `BOUNDED_REFERENCE_COMPLETE_DECLARED_WORKSPACE_SCOPE_NOT_DEPLOYED` | Gateway CE-6/CE-7; Receipt is credential-bound and Workspace Audit verifies all canonical Tenant links while omitting unrelated event content; offline non-membership proof and external anchor remain false |
| `C01-A8` | Map and incrementally remediate D29 security engineering controls | `FAIL_CLOSED_RETAINED_CR01_LIMITATION` | Gateway PR #52 mapped 20 controls; PR #53–#55 closed bounded source/CI findings; PR #57 fixed backup inputs; PR #58 passed bounded incident/formal rollback drills and disposed CR-01 without rewriting history. Open Blocker/High findings are zero, but `D29-SEC-11=FAIL_RETAINED`; no commercial availability or production claim |

These bounded implementation rows do not reopen P0-10 or D04 and do not
authorize website changes, customer contact, paid access or production
deployment. They do not make the complete D29 commercial program ready.
