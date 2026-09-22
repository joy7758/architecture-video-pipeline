---
document_id: DBA-CROSS-PROJECT-DEPENDENCIES-0.1
title: Digital Biosphere Cross-project Dependency Map v0.1
title_zh: 数字生物圈跨项目依赖图 v0.1
status: architecture-dependency-baseline
dependency_is_implementation: false
dependency_is_runtime_call: false
last_reviewed: 2026-08-02
---

# Digital Biosphere Cross-project Dependency Map v0.1（数字生物圈跨项目依赖图 v0.1）

## 1. Dependency Semantics（依赖语义）

本表的 dependency（依赖）表示推进条件、数据责任、规范约束或治理交接，不表示已经存在代码 import（导入）、API、网络调用、部署关系或所有权。

合法依赖类型：

- `NORMATIVE`：规范约束；
- `DATA_CONTRACT`：数据契约；
- `GOVERNANCE_GATE`：治理闸门；
- `EVIDENCE_INPUT`：证据输入；
- `EVALUATION_INPUT`：评价输入；
- `APPLICATION_SERVICE`：应用使用基础设施的候选关系；
- `STATUS_REFERENCE`：驾驶舱只读状态引用。

## 2. Core Dependency Register（核心依赖登记）

| dependency_id | upstream | downstream | 类型 | 契约或交接 | 当前状态 | 不表示 |
|---|---|---|---|---|---|---|
| `DEP-001` | DBA | DBOS | `NORMATIVE` | DBOS 遵循已采纳的 Identity、Lifecycle、Capability、Evidence 与 Authority 边界 | `SPECIFICATION_DEFINED_ADOPTION_NOT_ASSESSED` | DBA 可以执行或修改 DBOS |
| `DEP-002` | DBA | SAEE | `NORMATIVE` | SAEE 遵循 Evaluation、Recommendation 与非执行边界 | `SPECIFICATION_DEFINED_ADOPTION_NOT_ASSESSED` | DBA 控制 SAEE 算法 |
| `DEP-003` | DBOS | SAEE | `DATA_CONTRACT` | Entity Identity、Execution History、Evidence Bundle、Verification Result、Resource Usage、Behavior Trace | `SPECIFICATION_DEFINED_IMPLEMENTATION_NOT_ASSESSED` | 已有 API 或 Runtime 调用 |
| `DEP-004` | SAEE | Governance Decision | `EVALUATION_INPUT` | Fitness、Risk、Evolution Recommendation、Governance Suggestion | `SPECIFICATION_DEFINED_IMPLEMENTATION_NOT_ASSESSED` | Recommendation 自动获批 |
| `DEP-005` | Governance Decision | DBOS | `GOVERNANCE_GATE` | Approved / Adopted result + separate Authorization reference | `SPECIFICATION_DEFINED_IMPLEMENTATION_NOT_ASSESSED` | Decision 等于 Execution |
| `DEP-006` | DBOS | Digital Entity | `APPLICATION_SERVICE` | Registration、Identity、Capability records、Execution/Evidence/Verification、Lifecycle | `ARCHITECTURE_DEFINED_ENTITY_SPECIFIC_INTEGRATION_NOT_ASSESSED` | Entity 自动 Active 或获得 Permission |
| `DEP-007` | Digital Entity | DBOS | `EVIDENCE_INPUT` | 任务、过程和输出引用进入 DBOS 有界记录 | `ARCHITECTURE_DEFINED_ENTITY_SPECIFIC_INTEGRATION_NOT_ASSESSED` | Agent 自己成为 canonical Evidence authority |
| `DEP-008` | Research Agent Pilot | DBOS | `APPLICATION_SERVICE` | 未来只读/记录接口准备 | `PREPARED_ONLY` | Research Agent 已注册、已连接或已运行 |
| `DEP-009` | Research Agent Pilot | SAEE | `EVALUATION_INPUT` | 未来 Evaluation Profile（评价配置）准备 | `PREPARED_ONLY` | 已形成 Fitness、Risk 或 Recommendation |
| `DEP-010` | Core projects | DBA | `STATUS_REFERENCE` | 项目提供带来源的状态，DBA 只读汇总 | `SOURCE_ALIGNMENT_PENDING` | DBA 状态摘要覆盖子项目事实 |
| `DEP-D19-001` | DBA Discovery Evolution policy | Canonical owner repositories | `NORMATIVE` / `GOVERNANCE_GATE` | Problem Evidence、owner routing、risk class、variant evidence、rollback 与 Draft PR handoff | `BOUNDED_REFERENCE_DEFINED_CROSS_REPO_PROPOSAL_ONLY` | DBA 直接执行子项目变化、Agent 自动 merge 或生产激活 |
| `DEP-011` | titmac-scout | DBA | `STATUS_REFERENCE` | canonical `main` 的 `governance/project-status.json`、Schema、exact revision/tree/file digest，以及分离的 source/remote/CI/PR freshness 只读按需投影 | `CANONICAL_MAIN_SOURCE_PINNED_DYNAMIC_GITHUB_OBSERVATION_PASS` | DBA 拥有 Scout 状态、运行修复、生成 patch、触发 PR、执行 merge/deploy 或复制 canonical run |

## 3. Adjacent Dependency Candidates（相邻依赖候选）

| candidate_dependency | 候选关系 | 状态 | 进入核心依赖前的要求 |
|---|---|---|---|
| POP ↔ DBOS | Persona projection 与 canonical identity 映射 | `REVIEW_REQUIRED` | Owner、schema、状态写权与冲突规则 |
| Agent Evidence → DBOS | receipt / evidence reference 交接 | `REVIEW_REQUIRED` | canonical Evidence owner、完整性与版本边界 |
| TITMAS Agent Action Gate → DBA / future execution surfaces | 项目状态汇报与未来 action decision / authorization-reference / refusal 交接候选 | `REFERENCE_IMPLEMENTED_MAPPING_REVIEW_REQUIRED_G0_PENDING_NOT_ADMITTED` | public `main@6f1c83b` 已实现确定性 gate、6-tool MCP、pinned agent-evidence、独立 caller／approver credential、一次性 consumption、真实 sandbox Draft PR 和已销毁的官方 AgentTeams v1.2.0 operator-supervised 本地 smoke；G0 仍待 Human Decision，项目未准入；仍须审查 per-Worker MCP ACL、Skill materialization、自治链、DBOS Permission、Runtime enforcement、Gateway 和 audit-record Owner；无跨项目 API mapping、持久／生产 Runtime 或采用权 |
| Media Evidence → DBA / DBOS | 已接纳相邻候选的 private canonical status 只读引用；未来可能的媒体 evidence-bearing record / reference 交接 | `PORTFOLIO_ADMITTED_BOUNDARY_ONLY_MAPPING_NOT_AUTHORIZED` | Source/owner/freshness 和组合准入已建立；DBOS Evidence Admission contract、mapping 实现、跨项目符合性和 G3-G8 仍须独立决定；网站展示不等于架构采用 |
| ARO → DBOS / SAEE | Audit result 作为 Verification 或 Evaluation 输入 | `REVIEW_REQUIRED` | Audit、Verification、Evaluation 三者分离 |
| Token Governor → DBOS / SAEE | 资源约束记录与资源适应度输入 | `REVIEW_REQUIRED` | 执行约束、评价和最终决策责任分离 |
| ACP ↔ DBOS | Physical Cell identity 与 Entity reference 映射 | `REVIEW_REQUIRED` | `cell_id` 不得自动等于 `entity_id` |

## 4. Dependency Change Rule（依赖变更规则）

新增或升级依赖必须：

1. 有稳定 `dependency_id`；
2. 指定 upstream、downstream 和 dependency type；
3. 引用契约、ADR 或状态来源；
4. 明确 data owner（数据所有者）、write authority（写权）和 failure behavior（失败行为）；
5. 通过 duplicate capability review；
6. 通过 [`INTEGRATION-GATES.md`](INTEGRATION-GATES.md) 的相应 gate；
7. 不把 `PLANNED`、`PREPARED_ONLY` 或 `SPECIFICATION_DEFINED` 写成 `IMPLEMENTED`。

```text
DEPENDENCY_MAP_DEFINED=true
RUNTIME_DEPENDENCIES_CREATED=false
API_DEPENDENCIES_CREATED=false
CHILD_REPOSITORIES_CHANGED=false
```

## 5. Commercial Program Dependencies

| dependency_id | upstream | downstream | type | current state | boundary |
|---|---|---|---|---|---|
| `DEP-CM-001` | DBA commercial contracts | private Gateway | `NORMATIVE` | `D29_SOURCE_PINNED_SECURITY_DRILLS_PASS_CR01_FAIL_RETAINED` | DBA defines objects/gates and projects exact source; Gateway owns implementation and operational evidence truth |
| `DEP-CM-002` | private Gateway | PostgreSQL 16 candidate | `APPLICATION_SERVICE` | `DEPLOYED_SYNTHETIC_METADATA_ONLY` | metadata/ledgers only; no raw payload persistence; restore integrity gate is blocked |
| `DEP-CM-003` | private Gateway | public integrations | `DATA_CONTRACT` | `COMMERCIAL_READINESS_NOT_ASSESSED` | only public-safe OpenAPI, SDK, Adapter and verifier assets |
| `DEP-CM-004` | Gateway execution evidence | SAEE | `EVALUATION_INPUT` | `NOT_STARTED` | read-only future evaluation; SAEE does not authorize or mutate Gateway |
| `DEP-CM-005` | Contracting Principal | Tenant/Agent credential lifecycle | `GOVERNANCE_GATE` | `INTERNAL_SYNTHETIC_ONLY` | Human retains contract/payment/irreversible authority |

The commercial program does not add a second Gateway, Agent Runtime, truth
store or certification authority.
