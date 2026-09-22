---
spec_id: DBA-ENTITY-CLASSIFICATION-0.1
title: Digital Entity Classification v0.1
status: non-executable-architecture-classification
classification_grants_permission: false
entity_instance_created: false
capability_effect: none
authority_effect: none
---

# Digital Entity Classification v0.1（数字实体分类 v0.1）

## 1. 分类目的

分类用于表达一个已满足 Digital Entity 最低要求的生态成员主要承担什么职责。分类是 routing and interpretation metadata（路由与解释元数据），不是权限、能力、身份验证、运行状态或项目归属证明。

Repository、Component、Runtime 或名称不能直接获得 Entity 分类。实际对象必须先满足 [`digital-entity-specification.md`](digital-entity-specification.md) 并进入 DBOS-governed lifecycle（DBOS 治理的生命周期）。

## 2. Primary Classes（主分类）

| `primary_class` | 分类 | 核心职责 | 架构角色示例 | 实例边界 |
|---|---|---|---|---|
| `infrastructure` | Infrastructure Entity（基础设施实体） | 为其他生态成员提供身份、治理、协议、资源或基础服务 | DBOS | DBOS 仓库不是实体；只有满足最低要求的持久主体实例才可被分类 |
| `evolution` | Evolution Entity（演化实体） | 产生适应度、风险、稳定性、演化或治理演化评价 | SAEE | SAEE 仓库不是实体；分类不授予 DBOS 写权或执行权 |
| `operational` | Operational Entity（运行实体） | 在授权边界内执行具体任务并形成行为与结果 | Research Agent reference model | 本规范没有创建 Research Agent、Runtime 或任务权限 |
| `evaluation` | Evaluation Entity（评价实体） | 在明确模型与输入范围内产生有界评价 | Future Evaluation Service | 未来示例；不自动获得 SAEE Evolution Governance 权限 |

表中的 DBOS、SAEE 和 Research Agent 是 architecture role examples（架构角色示例），不是已创建、已注册或已验证的 Digital Entity 实例。Research Agent 的受限参考模型见 [`research-agent-specification.md`](research-agent-specification.md)。

## 3. Role Labels（角色标签）

主分类用于确定首要责任域；角色标签用于描述具体用途。一个实体应有一个主分类，可以有多个无权限效力的角色标签。

| `role_label` | 典型含义 | 常见主分类 | 边界 |
|---|---|---|---|
| `autonomous_agent` | 在受控范围内选择或执行任务路径 | Operational | `Agent` 标签不等于无限自治或权限 |
| `research_agent` | 研究、检索、分析或证据材料生成 | Operational | 参考模型不创建 Research Agent 实例或 Capability |
| `service_entity` | 提供稳定、有边界的服务 | Infrastructure / Operational | endpoint、process 或 repository 本身不是实体 |
| `governance_entity` | 承担明确治理职责的实体角色 | Infrastructure | Governance Decision Layer 不是 Entity |
| `evaluation_entity` | 产生模型范围内评价 | Evaluation / Evolution | 不自动获得 SAEE 的完整职责或模型所有权 |

## 4. 分类判定顺序

1. Qualification（资格）：确认 Identity、Capability Boundary、Execution History、Evidence History 与 Lifecycle State。
2. Boundary（边界）：排除 Repository、Runtime、Component 或未治理 Agent 名称的误分类。
3. Primary responsibility（首要职责）：选择一个主分类。
4. Role labels：添加用途标签，但不改变主分类 Owner 和权限边界。
5. Governance check（治理检查）：确认分类没有绕过 DBOS、SAEE 或 Governance Decision。
6. Record（记录）：由 DBOS 将分类作为 Entity record 的受控元数据；分类变化需要可追溯记录。

分类不明确时必须标记 `unknown` 或保持 Entity Candidate，不得为了进入某条工作流而选择权限更大的类别。

## 5. Classification ≠ Permission（分类不等于权限）

```text
INFRASTRUCTURE_CLASS_GRANTS_GOVERNANCE_AUTHORITY=false
EVOLUTION_CLASS_GRANTS_EXECUTION_AUTHORITY=false
OPERATIONAL_CLASS_GRANTS_TASK_AUTHORIZATION=false
EVALUATION_CLASS_GRANTS_SAEE_AUTHORITY=false
ROLE_LABEL_GRANTS_CAPABILITY=false
```

- Infrastructure Entity 不自动拥有身份、策略或授权管理权；
- Evolution Entity 不自动拥有 SAEE 模型所有权或 DBOS 写权；
- Operational Entity 不自动获准执行任务；
- Evaluation Entity 不自动拥有演化选择或治理建议权；
- 多个标签的并集不形成权限并集。

## 6. 分类变化

分类变化是 Governance Decision 的候选事项，不是 Entity 自行选择：

```text
Evaluation / Recommendation
  ↓
Governance Decision: explicit review and adoption
  ↓
DBOS: update classification record under lifecycle control
  ↓
Evidence and Verification
```

该图是概念责任流，不是已实现 API 或 Runtime。分类变化不得追溯性改写历史分类、执行记录或 Evidence。

## 7. 非实现状态

```text
ENTITY_CLASSIFICATION_DEFINED=true
ENTITY_CLASSIFICATION_RUNTIME_CREATED=false
ENTITY_INSTANCE_CLASSIFIED=false
DBOS_ENTITY_INSTANCE_VERIFIED=false
SAEE_ENTITY_INSTANCE_VERIFIED=false
FUTURE_RESEARCH_AGENT_CREATED=false
```
