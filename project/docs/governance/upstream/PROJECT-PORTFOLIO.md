---
document_id: DBA-PROJECT-PORTFOLIO-0.1
title: Digital Biosphere Project Portfolio v0.1
title_zh: 数字生物圈项目组合 v0.1
status: initial-observed-portfolio-baseline
as_of_date: 2026-08-02
source_policy: reference-only
changes_project_ownership: false
changes_project_status: false
---

# Digital Biosphere Project Portfolio v0.1（数字生物圈项目组合 v0.1）

## 1. Portfolio Tiers（项目组合层级）

| tier | 中文含义 | 准入含义 |
|---|---|---|
| `CORE` | 核心项目 | Digital Biosphere 总目标不可缺少的责任域；不表示仓库被 DBA 所有 |
| `PILOT` | 试验项目 | 用于验证架构契约的受控应用或研究工作流；不表示已实现或已授权执行 |
| `LOGICAL_LAYER` | 逻辑层 | 架构中需要但尚不一定有独立软件仓库的责任边界 |
| `ADJACENT_CANDIDATE` | 相邻候选项目 | 经显式边界审查可纳入组合观察；不表示进入核心、完成 DBOS 映射、跨项目符合性或采用 |
| `OUT_OF_SCOPE` | 当前范围外 | 当前项目群不管理；若未来接入必须重新审查 |

## 2. Core Portfolio（核心项目组合）

| project_id | tier | 项目 | DBA 中的职责 | canonical project source（项目规范来源） | 当前组合状态 | 下一 gate |
|---|---|---|---|---|---|---|
| `DBA` | `CORE` | Digital Biosphere Architecture | Program Governance Hub（项目群治理中心）+ Architecture Specification Hub（架构规范中心）+ Public Entry Governance（公开入口治理） | 本仓库 `README.md`、`PUBLIC-PROJECT-OVERVIEW.md`、`PROGRAM-CHARTER.md`、`architecture/`、ADR | `EXTERNAL_TRIAL_PLAN_DEFINED_NOT_AUTHORIZED` | 处理 `B-007` 与 `DQ-010`；试用计划不等于试用执行或发布 |
| `DBOS` | `CORE` | Digital Biosphere Operating System | Existence Infrastructure（存在基础设施）和 Developer Infrastructure（开发者基础设施） | `/Users/zhangbin/GitHub/digital-biosphere-os/README.md`、`STRATEGIC_ALIGNMENT.md`、`docs/developer-quickstart.md`、registry 与证据文件 | `LOCAL_PREVIEW_CONFORMANCE_PASS_NOT_RELEASED` | 隔离 source changes 并做 clean-clone 复验 |
| `SAEE` | `CORE` | Digital Biosphere Evolution Engine | Evolution Intelligence Layer（演化智能层） | `/Users/zhangbin/GitHub/SAEE/STRATEGIC_ALIGNMENT.md`、`PROJECT_STATUS.md`、Capability inventory（能力清单）及其证据文件 | `LOCAL_READ_ONLY_DBOS_PREVIEW_ADAPTER_PASS_NOT_RELEASED` | 隔离受限 adapter 变更；保持 canonical capability truth 不变 |
| `GOVERNANCE-DECISION` | `LOGICAL_LAYER` | Governance Decision Layer（治理决策层） | Recommendation 到 Decision、Adoption 的记录边界 | DBA 的 `governance-decision-model.md`、状态机与 ADR | `MODEL_DEFINED_IMPLEMENTATION_NOT_ASSESSED` | 指定 deployment-specific decision authority（部署特定决策责任） |
| `TITMAS-DISCOVERY-EVOLUTION` | `LOGICAL_LAYER` | Agent-Native Discovery Evolution Layer（智能体原生发现进化层） | 有界发现、变体、适应度、选择、回滚和谱系规范 | `architecture/titmas-agent-native-discovery-self-healing-evolution-amendment-v2.1.md`、`TITMAS/agent-native/evolution/` | `BOUNDED_REFERENCE_IMPLEMENTED_DRAFT_PR_ONLY` | 验证首个 ER-1 确定性 Demo；任何 merge、release、deployment 仍需人工决定 |
| `RESEARCH-AGENT-PILOT` | `PILOT` | Research Agent Pilot（科研智能体试验） | 第一个 Operational Digital Entity（运行型数字主体）参考试验 | `/Users/zhangbin/GitHub/digital-biosphere-research-agent-pilot/README.md`、`CONSTITUTION.md`、readiness gate（就绪闸门） | `SPECIFICATION_ONLY_NOT_READY` | 完成人工复核、来源批准和原型授权前置条件 |

## 3. Adjacent Candidate Portfolio（相邻候选项目组合）

这些项目已在架构映射或本地发现中出现，但 v0.1 不把它们自动纳入核心治理、依赖或发布计划。

| candidate_id | 本地发现路径 | 候选角色 | 当前准入状态 | 必须回答的问题 |
|---|---|---|---|---|
| `POP` | `/Users/zhangbin/GitHub/persona-object-protocol` | Identity / Persona adjacent component（身份／人格相邻组件） | `MAPPING_ONLY_REVIEW_REQUIRED` | 与 DBOS canonical identity 的 Owner 和映射边界是什么？ |
| `ARO` | `/Users/zhangbin/GitHub/aro-audit` | Audit / Verification adjacent component（审计／验证相邻组件） | `MAPPING_ONLY_REVIEW_REQUIRED` | 与 DBOS Verification、Agent Evidence 的阶段和数据所有权如何分离？ |
| `AGENT-EVIDENCE` | `/Users/zhangbin/GitHub/agent-evidence` | Execution-to-evidence component（执行到证据组件） | `MAPPING_ONLY_REVIEW_REQUIRED` | 哪些记录是 canonical Evidence，哪些只是 receipt（回执）或 transport（传输）？ |
| `TITMAS-AGENT-ACTION-GATE` | public `joy7758/titmas-agent-action-gate`；`main@6f1c83bf87e6ee96a0eda281e1fa91b8f80a32e1`；status `governance/project-declaration.json` | Agent-proposed action 的 fail-closed Governance Service / Application boundary（治理服务／应用边界）候选 | `REFERENCE_IMPLEMENTED_ON_MAIN_G0_READY_FOR_REVIEW_NOT_ADMITTED` | 已实现 action decision、approval、canonical evidence verification、一次性 execution binding、真实 sandbox Draft PR 与已销毁的官方 AgentTeams v1.2.0 operator-supervised 本地 smoke；仍须审查 per-Worker MCP ACL、Skill materialization、自治链、DBOS Permission、Runtime policy enforcement、TITMAS conformance／gateway 重复和 audit record Owner |
| `titmac-scout` | private `joy7758/titmac-scout`；canonical `main@7cfcde4c22daa8ea3fd2b48a15ba6ab78463c907`；status source `governance/project-status.json` | Discovery self-healing and evolution implementation（发现、自愈与演化实现）候选 | `CANONICAL_STATUS_SOURCE_MERGED_READ_ONLY_COCKPIT_BRIDGE_READY_FOR_HUMAN_REVIEW` | D21 只激活规范状态源和动态只读观察；D19 等价实现、测试与保留 Demo 尚未证明，PR #105/#106 ownership/migration review 仍待决定 |
| `MEDIA-EVIDENCE` | private `joy7758/titmas-media-guard`；`v0.1.0@7eac452f66a2b7de525543f80b9a7cf1465ef9a1`；status `governance/project-status.json` | AIGC media-review Application Profile / Reference Implementation candidate（人工智能生成内容媒体审核应用场景配置／参考实现候选） | `ADMITTED_ADJACENT_CANDIDATE` | G0、G1 和边界限定的 G2 已通过；DBOS Evidence Admission mapping 未授权，G3-G8 未评估、未授权或未执行 |
| `TOKEN-GOVERNOR` | `/Users/zhangbin/GitHub/token-governor` | Resource governance adjacent component（资源治理相邻组件） | `MAPPING_ONLY_REVIEW_REQUIRED` | DBOS 运行约束与 SAEE 资源评价之间的责任边界是什么？ |
| `ACP` | `/Users/zhangbin/GitHub/海洋/autonomous-cell-protocol` | Physical Cell protocol（物理单元协议） | `MAPPING_ONLY_REVIEW_REQUIRED` | Physical Cell Identity 与 DBOS Entity Identity 如何保持不等同？ |

本地路径只证明在 2026-07-21 的工作区发现了候选目录，不证明其当前能力、维护状态、发布状态、项目所有权或已接入 Digital Biosphere。

## 4. Portfolio Admission Rules（项目组合准入规则）

项目进入 `CORE` 或 `PILOT` 前，以及相邻候选获得显式组合接纳时，必须：

1. 有稳定 `project_id`、项目目的和 canonical source；
2. 指定一个 primary responsibility domain（主责任域）；
3. 通过 duplicate construction review（重复建设审查）；
4. 明确 Capability、Authority、Permission、Execution、Evidence、Evaluation 和 Decision 边界；
5. 记录与 DBOS、SAEE、DBA 或应用层的依赖；
6. 指定状态更新来源和 freshness policy（时效策略）；
7. 通过 [`INTEGRATION-GATES.md`](INTEGRATION-GATES.md) 的 `G0` 与 `G1`；
8. 由显式人工决策记录准入结果。

Repository discovery（仓库发现）不等于 Portfolio Admission（项目组合准入）。

当前 Program Governance Cockpit 与既有 Digital Biosphere public meaning layer 的长期 canonical relationship 尚未决定；本仓库是本次明确目标下的项目群驾驶舱基线，但不会据此静默覆盖、删除或合并另一仓库。该问题登记为 `DQ-008`。

## 5. Portfolio Truth Boundary（项目组合事实边界）

```text
PORTFOLIO_BASELINE_DEFINED=true
PORTFOLIO_OWNS_CHILD_REPOSITORIES=false
PORTFOLIO_CHANGES_CHILD_STATUS=false
ADJACENT_PROJECTS_ADMITTED=true
MEDIA_EVIDENCE_PORTFOLIO_ADMISSION_GRANTED=true
MEDIA_EVIDENCE_PORTFOLIO_CLASSIFICATION=ADJACENT_CANDIDATE
MEDIA_EVIDENCE_DBOS_MAPPING_AUTHORIZED=false
AGENT_ACTION_GATE_EXISTENCE_DECLARED=true
AGENT_ACTION_GATE_PORTFOLIO_ADMISSION_GRANTED=false
AGENT_ACTION_GATE_DBA_MANAGEMENT_POLICY_GRANTED=true
AGENT_ACTION_GATE_GITHUB_ACL_CHANGED=false
AGENT_ACTION_GATE_RUNTIME_PERMISSION_CREATED=false
AGENT_ACTION_GATE_NATIVE_SMOKE_FULLY_AUTONOMOUS=false
AGENT_ACTION_GATE_NATIVE_SMOKE_PERSISTENT_OR_PRODUCTION_DEPLOYMENT=false
TITMAC_SCOUT_CANONICAL_IDENTITY_FROZEN=true
TITMAC_SCOUT_PORTFOLIO_ADMISSION_GRANTED=false
TITMAC_SCOUT_STATUS_CONTRACT_MERGED=true
TITMAC_SCOUT_PUBLIC_OPERATION_VERIFIED=false
DISCOVERY_NE_ADOPTION=true
MAPPING_NE_INTEGRATION=true
```

## 6. Commercial Program Implementation Surface

`ADR-036` records a program track, not a new project admission:

| surface | portfolio role | source | state |
|---|---|---|---|
| Commercial governance | DBA responsibility extension | `commercial-program-state.json`, ADR-036, ADR-037, ADR-038 | `D04_CLOSED_FAILED_RETAINED_FINAL_FORM_DECISION_PENDING` |
| Commercial data/control modules | private Gateway bounded extension | `joy7758/titmas-sandbox-gateway@1a065f1702e355d5f5ed566bdfd3e895cdca2540` | `D29_REFERENCE_IMPLEMENTED_SECURITY_DRILLS_PASS_AUTHORITY_CLOSED_CR01_FAIL_RETAINED_GATE_FAIL_CLOSED` |
| Public-safe SDK and adapters | existing integrations repository | `joy7758/titmas-integrations@6ed4dad…` | `PASS_WITH_LIMITATIONS_PACKAGES_UNPUBLISHED` |
| Commercial control-plane repository | optional candidate | none | `NOT_CREATED_NOT_CURRENTLY_JUSTIFIED` |
| FDO DTR migration and PVS-0 | public evidence auxiliary line | `joy7758/titmas-fdo-public-verification@1dcca69…`, Zenodo `10.5281/zenodo.21778954`, five PIDs | `PUBLIC_ARCHIVED_MAINTENANCE_MODE_WAITING_FOR_GWDG_RESPONSE` |

No portfolio Owner, repository visibility or canonical implementation truth is
changed by this entry.
