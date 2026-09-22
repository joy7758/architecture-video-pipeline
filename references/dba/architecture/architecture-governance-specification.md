---
spec_id: DBA-ARCHITECTURE-GOVERNANCE-0.1
title: Digital Biosphere Architecture Governance Specification v0.1
title_zh: 数字生物圈架构治理规范 v0.1
status: non-executable-architecture-governance-specification
architecture_authority_scope: normative-rules-and-records-only
architecture_authority_assigned: false
program_governance_defined: true
program_authority_assigned: true
program_owner_ref: zhangbin
program_owner_assignment_reference: ADR-020
version_governance_defined: true
version_authority_assigned: false
runtime_effect: none
entity_effect: none
capability_effect: none
permission_effect: none
evidence_effect: none
---

# Digital Biosphere Architecture Governance Specification v0.1

本规范定义“治理架构本身的治理”：谁维护 Digital Biosphere Architecture（数字生物圈架构）的规范语义、如何审查边界变化、如何记录决策，以及何时可以更新规范文档。

Architecture Governance（架构治理）是 rule governance（规则治理），不是 Runtime Governance（运行治理）。Architecture Authority（架构权力）是对规范解释、维护和变更记录承担责任的有限角色边界，不是新建组织、Runtime、Agent、Digital Entity 或自动权限。

## 1. 核心不变量

```text
ARCHITECTURE_GOVERNANCE_NE_RUNTIME_GOVERNANCE=true
ARCHITECTURE_AUTHORITY_NE_EXECUTION_AUTHORITY=true
ARCHITECTURE_AUTHORITY_NE_DBOS=true
ARCHITECTURE_AUTHORITY_NE_SAEE=true
DBOS_NE_SAEE=true
ARCHITECTURE_CHANGE_REQUIRES_EXPLICIT_DECISION=true
ARCHITECTURE_GOVERNANCE_CREATES_RUNTIME=false
ARCHITECTURE_GOVERNANCE_GRANTS_PERMISSION=false
PROGRAM_GOVERNANCE_NE_ARCHITECTURE_GOVERNANCE=true
PROGRAM_AUTHORITY_NE_EXECUTION_AUTHORITY=true
```

1. Architecture Governance ≠ Runtime Governance：架构治理定义规则，DBOS 在有效授权与生命周期边界内负责运行。
2. Architecture Authority ≠ Execution Authority：能够解释或维护规范，不表示能够执行规范。
3. SAEE ≠ Architecture Authority：SAEE 可以提出评价或建议，不能单方面修改其生态规则。
4. DBOS ≠ Architecture Authority：DBOS 可以提出运行约束，不能用当前实现或运行状态单方面改写架构定义。
5. Architecture Change requires explicit decision process：语义性架构变化必须有可追溯的 Proposal、Review、Decision、Adoption 和 Documentation Update。

## 2. Architecture Authority（架构权力）

Architecture Authority 是 Digital Biosphere Architecture normative layer（规范层）的解释和维护责任，由经过明确指定的治理角色与受控变更流程共同实现。v0.1 只定义角色和记录要求，不指定个人、组织、账号或最终授权者，也不授予仓库写权限。

### 2.1 职责

- 维护架构规范、术语、交叉引用、版本、发布清单和 agent-readable（智能体可读）入口；
- 审查涉及 SAEE、DBOS、Governance Decision 或 Digital Entity 的重大边界变化；
- 创建、维护和索引 ADR（Architecture Decision Record，架构决策记录）；
- 检查规范之间的职责、权力、对象 Owner 和 truth surface（事实表面）是否一致；
- 保留被拒绝、撤销或替代的变更记录，不追溯性改写历史决策；
- 在变更被明确采纳后，使文档更新严格对应已接受范围。

### 2.2 限制

Architecture Authority：

- 不直接运行、部署或控制 DBOS；
- 不控制、重写或选择 SAEE 内部算法、Fitness 模型或演化结论；
- 不形成 DBOS 的 Identity、Capability、Execution、Evidence、Verification 或 Lifecycle 事实；
- 不替 SAEE 产生 Evaluation、Fitness、Risk 或 Evolution Recommendation；
- 不因接受架构变更而授予 Capability、Permission、Authorization 或 Execution 权限；
- 不把 Architecture Decision 自动升级为 Runtime Decision、Governance Decision Object 或已执行状态。

Architecture Authority 对规则的规范作用不外溢为运行权。DBOS 和 SAEE 也不会因成为 Domain Owner（领域所有者）而获得单方面修改规范的权力。

## 3. Architecture Change Lifecycle（架构变更生命周期）

```text
Proposal
   ↓
Review
   ↓
Decision
  ↙     ↘
Rejected  Accepted
             ↓
          Adoption
             ↓
     Documentation Update
```

| 阶段 | 最小记录 | 主要参与角色 | 不表示 |
|---|---|---|---|
| Proposal（提案） | 问题、当前规则、候选变化、范围、受影响文档与风险 | Proposer；Architecture Maintainer 接收 | 可以直接修改核心规范 |
| Review（审查） | 边界影响、兼容性、替代方案、DBOS/SAEE 领域意见与未决问题 | Architecture Reviewer、相关 Domain Owner | 已接受或已授权 |
| Decision（决策） | `accepted`、`rejected` 或 `deferred`，理由、范围与明确决策来源 | 被外部治理制度明确指定的 decision authority | 已采纳、已更新文档或已执行 |
| Adoption（采纳） | 将已接受决策纳入目标规范基线的记录 | Architecture Authority 的已指定角色 | Runtime 已采用、DBOS 已执行或 SAEE 已改变 |
| Documentation Update（文档更新） | 与已采纳范围一致的规范、ADR、版本和交叉引用更新 | Architecture Maintainer | 代码、API、Capability 或运行状态已改变 |

被拒绝的 Proposal 不得进入 Adoption。若问题重新提出，必须创建新的或明确修订的 Proposal，并保留旧记录。详细状态和 gate（闸门）见 [`architecture-change-process.md`](architecture-change-process.md)。

Documentation Update 只完成已采纳变更的文档落地，不自动产生 Current Version 或 Release。进入 Current 必须另行经过 Version 与 Release Governance。

## 4. Governance Roles（治理角色）

这些是 responsibility roles（责任角色），不是 Entity 类别、账号、权限包或新运行主体。角色指派与任期由本规范之外的治理制度决定。

| 角色 | 负责 | 不负责 |
|---|---|---|
| Architecture Maintainer（架构维护者） | 维护文档结构、版本、ADR 索引和已采纳变更；执行一致性检查 | 不得把未接受提案直接写入核心规范；不因维护角色获得运行权 |
| Architecture Reviewer（架构审查者） | 审查职责、权力、接口、兼容性、重复建设和事实升级风险 | 不运行 DBOS、不修改 SAEE 算法、不自动成为最终决策者 |
| Domain Owner（领域所有者） | 提供本领域的规范语义、约束、现状和影响说明 | 不单方面决定跨域规则，不把仓库事实变成架构授权 |
| DBOS Domain Owner | 说明 Existence Governance、运行约束和 DBOS 事实边界 | 不拥有 SAEE 评价或 Architecture Authority |
| SAEE Domain Owner | 说明 Evolution Governance、评价语义和 SAEE 算法边界 | 不拥有 DBOS 运行状态或 Architecture Authority |

同一参与者可以在具体制度中承担多个角色，但角色不得因此合并。重大边界变化应记录独立审查；v0.1 不定义人数、quorum（法定人数）或组织任命机制。

## 5. Conflict Resolution（冲突解决）

当 DBOS 需求与 SAEE 需求冲突时，必须：

1. 保留双方原始需求、来源、范围和未决事实；
2. 识别冲突影响的是运行事实、演化评价、接口、权力还是规范术语；
3. 由相关 DBOS Domain Owner 与 SAEE Domain Owner 分别说明约束，不允许一方改写另一方领域结论；
4. 由 Architecture Reviewer 检查现有规范、替代方案、兼容性和重复建设风险；
5. 创建或更新 ADR，明确选择、拒绝的替代方案、影响和未知项；
6. 经显式 Architecture Decision 后进入 Adoption 与 Documentation Update；
7. 在新决策完成前，现行 canonical specification（规范基线）继续有效。

Runtime 行为、仓库当前实现或 SAEE 评价结果都不能单独解决架构冲突。它们可以成为审查输入，但不是 Architecture Decision。

## 6. Architecture Governance 与 Governance Decision 的边界

| 边界 | 输入 | 主要记录 | 效力 |
|---|---|---|---|
| Architecture Governance | Architecture Change Proposal（架构变更提案） | ADR、Architecture Change Record、规范版本 | 改变被采纳的规范语义；不改变运行事实 |
| Governance Decision Layer | SAEE Recommendation 或其他治理输入 | Governance Decision Object | 记录 Review、Decision 与 Adoption；不直接执行 |
| DBOS | 已批准、已采纳且另有有效授权的运行变化 | Execution、Evidence、Verification、Lifecycle records | 在其运行边界内形成有界运行记录 |
| SAEE | DBOS 运行材料 | Evaluation 与 Recommendation | 形成演化评价；不改变规范或运行状态 |

Architecture Change Proposal 不自动等于 SAEE Recommendation；Architecture Decision 也不自动等于 Governance Decision Object。两类决策记录的映射、共同授权者或统一 schema 尚未定义。

## 7. 变更分类

- Editorial Change（编辑性变更）：只修正文案、链接或格式，不改变语义；仍需可追溯记录与验证。
- Compatible Architecture Change（兼容性架构变更）：增加不破坏既有责任或接口的说明；需要 Proposal、Review、Decision 和 Adoption。
- Boundary Change（边界变更）：改变层级、职责 Owner、权力、不变量或不兼容接口；必须新增 ADR 并获得显式决定。

任何类别都不得用“文档修改”绕过能力事实、证据事实、权限或实现状态边界。

Compatibility（兼容性）必须按照 [`version-compatibility-policy.md`](version-compatibility-policy.md) 显式声明；版本号本身不能替代 Architecture Change Process 或 ADR。

## 8. Version Governance（版本治理）

Architecture Governance 通过 Version Governance 管理已验证规范如何形成版本、发布、采用、废弃和归档记录：

```text
Version: Draft → Reviewed → Accepted → Current → Deprecated → Archived
Release: Release Proposal → Review → Decision → Release → Adoption
```

- Version 表示 normative specification state（规范状态），不是 Implementation；
- Architecture Version 不等于 Runtime Version；
- Current 必须具有明确 scope 和 Release Record；
- Adoption 必须由采用方形成显式 Decision；
- Deprecated 版本继续冻结、保留并可追溯，不得删除历史；
- Architecture Maintainer 可以记录已批准发布，但不能自行批准或替任何项目采用版本；
- Version Authority 属于 Architecture Authority 的有限责任，不扩大 DBOS Operational Authority 或 SAEE Evolution Authority。

规范入口：

| 文档 | 职责 |
|---|---|
| [`version-governance-specification.md`](version-governance-specification.md) | 版本类型、生命周期、冻结、权力和历史保留 |
| [`version-compatibility-policy.md`](version-compatibility-policy.md) | Backward/Forward Compatibility、Breaking Change 与 Migration Requirement |
| [`release-governance-model.md`](release-governance-model.md) | Release Proposal、Decision、Release 与 Adoption 分离 |
| [`ADR-007-version-governance.md`](ADR-007-version-governance.md) | 建立版本和发布治理的架构决策 |

## 9. Architecture Governance 与 Program Governance 的边界

DBA 同时承载 Architecture Governance（架构治理）和 Program Governance（项目群治理），但两者职责不同：

| 维度 | Architecture Governance | Program Governance |
|---|---|---|
| 核心问题 | 规则、边界、接口和版本如何定义与改变？ | 整体现在在哪里、先做什么、谁负责、缺什么证据？ |
| 主要工件 | Specification、ADR、Change Record、Version、Release Record | Charter、Portfolio、Roadmap、Status、Dependency、Decision Queue、Gate、Risk |
| 决策对象 | Architecture Change（架构变化） | 项目优先级、组合准入、推进顺序和 gate |
| 不拥有 | Runtime、DBOS 状态、SAEE 评价 | 子项目实现事实、执行权、算法权或自动授权 |

Program Priority（项目优先级）不能直接改变 architecture truth；Architecture Decision 也不能自动批准项目实施。二者需要分别记录、相互引用，并遵守 [`program-governance-specification.md`](program-governance-specification.md) 与根目录 [`PROGRAM-CHARTER.md`](../PROGRAM-CHARTER.md)。

```text
PROGRAM_GOVERNANCE_DEFINED=true
PROGRAM_AUTHORITY_ASSIGNED=true
PROGRAM_OWNER_REF=zhangbin
PROGRAM_OWNER_ASSIGNMENT_REFERENCE=ADR-020
PROGRAM_GOVERNANCE_RUNTIME_CREATED=false
PROGRAM_STATUS_CHANGES_CHILD_TRUTH=false
```

## 10. 非实现状态

```text
ARCHITECTURE_GOVERNANCE_SPECIFICATION_DEFINED=true
ARCHITECTURE_AUTHORITY_ROLE_MODEL_DEFINED=true
ARCHITECTURE_AUTHORITY_ASSIGNED=false
ARCHITECTURE_CHANGE_PROCESS_DEFINED=true
PROGRAM_GOVERNANCE_SPECIFICATION_DEFINED=true
PROGRAM_GOVERNANCE_COCKPIT_DEFINED=true
PROGRAM_AUTHORITY_ASSIGNED=true
PROGRAM_OWNER_REF=zhangbin
PROGRAM_OWNER_ASSIGNMENT_REFERENCE=ADR-020
VERSION_GOVERNANCE_SPECIFICATION_DEFINED=true
VERSION_AUTHORITY_ASSIGNED=false
ARCHITECTURE_RELEASE_CREATED=false
VERSION_ADOPTION_RECORDED=false
ARCHITECTURE_GOVERNANCE_RUNTIME_CREATED=false
ARCHITECTURE_GOVERNANCE_ENTITY_CREATED=false
DBOS_ARCHITECTURE_CHANGE_AUTHORITY_CREATED=false
SAEE_ARCHITECTURE_CHANGE_AUTHORITY_CREATED=false
EXECUTION_AUTHORITY_CREATED=false
CAPABILITY_CREATED=false
PERMISSION_GRANTED=false
API_CREATED=false
CODE_CHANGED=false
```
