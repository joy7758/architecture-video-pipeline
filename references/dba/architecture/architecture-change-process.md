---
spec_id: DBA-ARCHITECTURE-CHANGE-PROCESS-0.1
title: Digital Biosphere Architecture Change Process v0.1
title_zh: 数字生物圈架构变更流程 v0.1
status: non-executable-change-control-specification
core_spec_direct_change_allowed: false
implementation_meaning: documentation-change-only
runtime_effect: none
authority_effect: none
---

# Digital Biosphere Architecture Change Process v0.1

本流程把架构变更从“提议”推进到“已验证的规范更新”，并防止 DBOS、SAEE、维护者或当前实现绕过 Review 与 Decision 直接改写核心规则。

## 1. 规范状态机

```text
PROPOSED
   ↓
REVIEWED
   ↓
ACCEPTED
   ↓
IMPLEMENTED
   ↓
VALIDATED

Terminal / side states:
REJECTED
WITHDRAWN
SUPERSEDED
```

这里的 `IMPLEMENTED` 只表示“已采纳的架构决定已经反映到文档、ADR、版本和交叉引用”，不表示代码、API、Runtime、DBOS 状态或 SAEE 算法已经实现或改变。

## 2. Architecture Change Record（架构变更记录）

每个语义性变更至少应记录：

| 字段 | 语义 |
|---|---|
| `change_id` | 稳定、不透明的变更引用 |
| `proposer_ref` | 提议来源，不自动成为决策者 |
| `problem` | 要解决的架构问题 |
| `current_rule` | 当前规范基线及精确引用 |
| `proposed_change` | 候选规则变化 |
| `scope` | 受影响职责、对象、接口、权力和文档 |
| `compatibility` | editorial、compatible 或 boundary-breaking |
| `domain_positions` | 相关 DBOS/SAEE Domain Owner 的独立意见 |
| `alternatives` | 被考虑和拒绝的替代方案 |
| `risks_and_unknowns` | 重复建设、事实升级、权限、兼容性及未知项 |
| `adr_reference` | 重大或边界变更对应的 ADR 引用 |
| `decision_result` | pending、accepted、rejected、deferred、withdrawn 或 superseded |
| `decided_by_ref` | 外部治理制度明确指定的决策来源 |
| `adoption_record` | 决策进入目标规范基线的记录 |
| `documentation_refs` | 实际更新的规范与 ADR 引用 |
| `validation_result` | 一致性、边界和范围验证结果 |

该对象是文档契约，不是已实现 schema，也不创建数据库、API 或 Change Service。

## 3. 状态与转换 gate（闸门）

### 3.1 PROPOSED

进入条件：

- 问题、当前规则、候选变化和受影响范围已记录；
- 已搜索现有规范、ADR 和项目映射；
- 尚未把候选语义写成已生效的核心规范。

允许转换：`REVIEWED`、`WITHDRAWN`。

### 3.2 REVIEWED

进入条件：

- Architecture Maintainer 已检查记录完整性；
- Architecture Reviewer 已检查职责重叠、权力越界、兼容性、重复建设和 truth promotion（事实升级）风险；
- 受影响的 DBOS/SAEE Domain Owner 意见分别保留；
- Boundary Change 已有 ADR 草案。

Review 不表示接受。允许转换：`ACCEPTED`、`REJECTED`、`WITHDRAWN`。

### 3.3 ACCEPTED

进入条件：

- 决策结果、理由、接受范围和 `decided_by_ref` 已显式记录；
- 所有未决问题和拒绝的替代方案仍可追溯；
- ADR-required 变更已有 accepted decision（已接受决定）；
- Adoption 已明确目标版本或目标规范基线。

Accepted 不表示文档已更新，更不表示 Runtime 已执行。允许转换：`IMPLEMENTED`、`SUPERSEDED`。

### 3.4 IMPLEMENTED

进入条件：

- Architecture Maintainer 只在 accepted scope（已接受范围）内更新规范；
- ADR、README、交叉引用、状态常量和版本语义保持一致；
- 更新没有声称代码、Capability、Evidence、Permission、Entity 或 Runtime 状态改变。

允许转换：`VALIDATED`；发现偏差时必须修正文档或创建后续变更，不得静默扩大范围。

### 3.5 VALIDATED

进入条件：

- 文档路径与链接可解析；
- 关键术语、Owner、Lifecycle 和 authority invariants（权力不变量）一致；
- 验证明确区分 `specification defined` 与 `implementation not assessed/not authorized`；
- DBOS、SAEE 和 Architecture Authority 均未获得越界权力；
- 变更记录指向最终文档和验证结果。

Validated 只关闭架构文档变更回路，不验证运行系统、算法效果或部署采用。

## 4. 禁止直接修改核心规范

以下 semantic core（语义核心）不得在没有对应 Change Record、Review、Decision 和 Adoption 的情况下直接改变：

- Stack layering 与 SAEE/DBOS responsibility boundary；
- SAEE–DBOS contract、interface direction 与 data ownership；
- Recommendation、Decision、Authorization、Execution 和 Verification 的分离；
- Digital Entity 定义、最低要求与 Lifecycle ownership；
- Architecture Authority、Operational Authority 与 Evolution Authority 的边界；
- 本流程本身的 gate、不变量与变更分类。

禁止行为包括：

- 先修改核心语义，再补写一个事后 ADR 使其看似获批；
- 由 DBOS 当前实现反推并覆盖规范责任；
- 由 SAEE 评价或 Recommendation 直接改写架构规则；
- 由 Architecture Maintainer 单方面接受自己提出的重大边界变化；
- 用编辑性修订标签隐藏职责、权力或接口语义变化。

紧急性不能取消 gate。若具体制度允许 expedited review（加速审查），仍必须保留 Proposal、Review、Decision、Adoption 和 Documentation Update 的记录。

## 5. 变更级别

| 级别 | 例子 | 最小治理要求 |
|---|---|---|
| Editorial | 拼写、格式、失效链接且语义不变 | Change Record、维护者确认、验证 |
| Compatible | 增加向后兼容说明、可选字段或检索入口 | Proposal、Review、Decision、Adoption、Documentation Update |
| Boundary-breaking | 改变 Owner、权力、层级、不变量或不兼容接口 | 完整流程、ADR、显式决定、跨域审查 |

Patch、Minor、Major 的规范语义以 [`version-compatibility-policy.md`](version-compatibility-policy.md) 为版本治理入口；[`evolution-policy.md`](evolution-policy.md) 第 7 节保留其摘要。版本号本身不能替代本流程、显式 Decision 或 ADR。

## 6. Agent-readable review checklist（智能体可读审查清单）

```text
CHANGE_ID=
CURRENT_RULE_REFERENCED=true|false
EXISTING_ADRS_REVIEWED=true|false
AFFECTED_AUTHORITY_DOMAINS=
DBOS_DOMAIN_POSITION_RECORDED=true|false|not-applicable
SAEE_DOMAIN_POSITION_RECORDED=true|false|not-applicable
ARCHITECTURE_REVIEW_RECORDED=true|false
DECISION_SOURCE_EXPLICIT=true|false
ADOPTION_RECORDED=true|false
DOCUMENTATION_SCOPE_MATCHES_DECISION=true|false
RUNTIME_CHANGE_CLAIMED=false
CAPABILITY_CHANGE_CLAIMED=false
EVIDENCE_CHANGE_CLAIMED=false
PERMISSION_CHANGE_CLAIMED=false
STATUS=proposed|reviewed|accepted|implemented|validated|rejected|withdrawn|superseded
```

## 7. 非实现状态

```text
ARCHITECTURE_CHANGE_PROCESS_DEFINED=true
CHANGE_SERVICE_CREATED=false
CHANGE_API_CREATED=false
ARCHITECTURE_AUTHORITY_ASSIGNED=false
CORE_SPEC_DIRECT_CHANGE_ALLOWED=false
RUNTIME_CHANGED=false
ENTITY_CREATED=false
CAPABILITY_CREATED=false
PERMISSION_GRANTED=false
```
