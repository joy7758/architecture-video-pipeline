---
spec_id: DBA-PROGRAM-GOVERNANCE-0.1
title: Digital Biosphere Program Governance Specification v0.1
title_zh: 数字生物圈项目群治理规范 v0.1
status: non-executable-program-governance-specification
program_governance_defined: true
program_authority_assigned: true
program_owner_ref: zhangbin
program_owner_assignment_reference: ADR-020
architecture_authority_changed: false
operational_authority_changed: false
evolution_authority_changed: false
runtime_effect: none
permission_effect: none
---

# Digital Biosphere Program Governance Specification v0.1（数字生物圈项目群治理规范 v0.1）

## 1. Definition（定义）

Program Governance（项目群治理）是对 Digital Biosphere 多项目组合的使命、优先级、推进顺序、依赖、决策、风险、集成 gate 和状态沟通进行治理的规则层。

DBA 同时承载：

- Program Governance Hub（项目群治理中心）；
- Architecture Specification Hub（架构规范中心）。

两者都属于 non-executable governance surface（非执行治理表面）。Program Governance 管“整体先做什么、谁负责、缺什么证据、何时允许进入下一阶段”；Architecture Governance 管“规则和边界是什么”。

## 2. Core Invariants（核心不变量）

```text
PROGRAM_GOVERNANCE_NE_ARCHITECTURE_GOVERNANCE=true
PROGRAM_GOVERNANCE_NE_RUNTIME_GOVERNANCE=true
PROGRAM_AUTHORITY_NE_OPERATIONAL_AUTHORITY=true
PROGRAM_AUTHORITY_NE_EVOLUTION_AUTHORITY=true
PROGRAM_PRIORITY_NE_IMPLEMENTATION_AUTHORIZATION=true
PROGRAM_GATE_NE_EXECUTION_PERMISSION=true
PROGRAM_STATUS_NE_CHILD_PROJECT_TRUTH=true
DBA_NE_DBOS=true
DBA_NE_SAEE=true
DBOS_NE_SAEE=true
```

Program Governance 与 Architecture Governance 可以由同一 DBA 仓库承载，但职责不可合并：改变项目优先级不自动改变架构规则；接受架构规则不自动批准项目实施。

## 3. Program Governance Responsibilities（项目群治理职责）

- Program Charter：使命、范围、治理原则和权力分离；
- Project Portfolio：核心、Pilot、逻辑层和相邻候选项目；
- Master Roadmap：跨项目阶段、关键路径和进入条件；
- Program Status：带来源和时间的只读状态快照；
- Cross-project Dependencies：契约、数据、治理和状态依赖；
- Decision Queue：需要人工决定的开放事项；
- Integration Gates：推进所需的最小证据；
- Risk and Blocker Register：风险、阻塞、Owner 和解除条件；
- Program Review：确定下一优先级并保留未知和冲突。

## 4. Program Governance Roles（项目群治理角色）

| 角色 | 负责 | 不负责 |
|---|---|---|
| Human Program Owner（人工项目群负责人） | 使命、优先级、组合准入、重大 gate 和资源方向的最终人工决定 | 因角色自动获得子仓库权限、DBOS Permission 或 SAEE 算法控制 |
| Program Maintainer（项目群维护者） | 更新驾驶舱入口、状态引用、依赖、风险和决策队列 | 不能批准自己的重大提案或改变子项目事实 |
| Architecture Maintainer（架构维护者） | 规范、ADR、版本和一致性 | 不决定 Runtime 操作或 SAEE 结论 |
| Domain Owner（领域负责人） | 提供子项目的 canonical source、现状和领域约束 | 不单方面决定跨域规则或整体优先级 |
| Program Reviewer（项目群审查者） | 检查来源、依赖、重复建设、gate 证据和状态升级风险 | 不自动成为最终 Decision Authority |

`ADR-020` 已把 Human Program Owner 角色指派给 `zhangbin`。该指派只关闭 Program
Governance（项目群治理）层的决定来源缺口，不创建组织、账号、仓库权限、运行权、
演化权或发布权；其他角色仍未由本规范自动指派。

## 5. Program Work Item Lifecycle（项目群工作项生命周期）

```text
PROPOSED
  → CLASSIFIED
  → SOURCE_VERIFIED
  → REVIEWED
  → DECIDED
  → ASSIGNED
  → IN_PROGRESS
  → GATE_REVIEW
  → COMPLETED | REJECTED | DEFERRED | BLOCKED
```

状态规则：

- `CLASSIFIED` 必须只有一个 primary repository；
- `SOURCE_VERIFIED` 必须有 canonical source 和时间点；
- `DECIDED` 必须有 `decided_by_ref`；
- `ASSIGNED` 不等于实现授权；
- `IN_PROGRESS` 不等于结果已验证；
- `COMPLETED` 必须引用满足目标范围的直接证据；
- `BLOCKED` 必须记录阻塞条件和解除条件；
- 被拒绝、延期或失败的工作项不得删除。

## 6. Source and Status Contract（来源与状态契约）

每个核心项目至少登记：

```text
project_id=
canonical_repository=
canonical_status_source=
domain_owner_ref=
observed_branch=
observed_commit_or_version=
observed_at=
freshness_window=
conflict_policy=
status_summary=
unknowns=
```

DBA 可以读取并汇总这些字段，但不能写回或替代子项目的 canonical record。无法确认时使用 `UNKNOWN`；多个来源冲突时使用 `CONFLICTED` 并进入 Decision Queue。

## 7. Program Decision Boundary（项目群决策边界）

Program Decision 可以：

- 确定项目优先级；
- 准入、延期或移出 Portfolio；
- 选择跨项目里程碑；
- 接受风险或要求缓解；
- 决定是否进入下一 Integration Gate；
- 要求创建独立的子项目实施提案。

Program Decision 不能自动：

- 修改 DBOS Identity、Lifecycle、Capability、Execution、Evidence 或 Verification；
- 修改 SAEE 算法、Fitness、Risk 或 Evolution conclusions；
- 创建 Agent、Runtime、Digital Entity、Permission 或实验；
- 产生 release、deployment、adoption 或 commercial availability；
- 取代 Architecture Change、Governance Decision 或 Registration Authorization。

## 8. Cockpit Consistency Rule（驾驶舱一致性规则）

根目录驾驶舱工件与 `architecture/` 规范必须满足：

1. Project ID、角色和 Owner 语义一致；
2. Roadmap 状态不能高于 gate evidence；
3. Program Status 必须带时间，过期不得伪装为当前；
4. Decision Queue 与 ADR 结果可互相追溯；
5. Risk/Blocker 关闭必须引用解除证据；
6. 子项目的 unknown、failure 和 dirty worktree 不能被驾驶舱隐藏；
7. 所有 agent-readable 常量不得声明未实现能力。

## 9. Non-implementation State（非实现状态）

```text
PROGRAM_GOVERNANCE_SPECIFICATION_DEFINED=true
PROGRAM_GOVERNANCE_COCKPIT_DEFINED=true
PROGRAM_AUTHORITY_ASSIGNED=true
PROGRAM_OWNER_REF=zhangbin
PROGRAM_OWNER_ASSIGNMENT_REFERENCE=ADR-020
PROGRAM_GOVERNANCE_RUNTIME_CREATED=false
PROGRAM_STATUS_ADAPTER_CREATED=false
CHILD_PROJECT_WRITE_ACCESS_CREATED=false
IMPLEMENTATION_AUTHORIZED=false
RUNTIME_CREATED=false
AGENT_CREATED=false
ENTITY_CREATED=false
PERMISSION_GRANTED=false
```
