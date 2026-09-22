---
adr_id: ADR-011
title: Establish the Research Agent Implementation Contract
title_zh: 建立科研数字实体实现契约
status: accepted-for-architecture-specification-v0.1
decision_scope: architecture-to-implementation-requirements-only
implementation_status: not-authorized
contract_effect: specification-only
implementation_effect: none
prototype_effect: none
agent_instance_effect: none
runtime_effect: none
capability_effect: none
permission_effect: none
---

# ADR-011: Establish the Research Agent Implementation Contract

## Problem（问题）

Digital Entity、Capability Boundary、Research Agent Pilot、Research Protocol、DBOS/SAEE Interface 和 Governance Decision 已定义架构职责，但 Architecture 与未来实现之间仍缺少一层明确桥梁：

- 实现需要向 DBOS 提供哪些 Entity Registration 和 Execution 语义；
- Research Agent material 如何进入 DBOS canonical Evidence，而不由 Agent 自证；
- 实现如何声明 Capability 而不自动扩大 Capability、Permission 或 Authority；
- Human Oversight gate 如何成为实现约束；
- DBOS input 如何进入 SAEE Evaluation，而不改变 Recommendation 权限类别；
- 失败、冲突、拒绝和 Retry 如何保留；
- 怎样判断 implementation candidate 符合架构，而不把 Contract 当作 Implementation Authorization。

缺少桥梁时，未来代码可能自行创建 Identity、扩大 Capability、把 Agent output 当作 Evidence、让 SAEE Recommendation 直接执行，或把字段存在误报为合规实现。

## Decision（决策）

建立 Research Agent Implementation Contract v0.1：

1. 定义 Entity Registration Contract：`entity_id`、`entity_type`、`owner_reference`、`lifecycle_state`；
2. 定义 Execution Contract：`execution_id`、`task_reference`、`input_reference`、`output_reference`、`context_reference`；
3. 定义 Evidence Contract：`raw_output_reference`、`process_reference`、`tool_usage_reference`、`failure_reference`；
4. Canonical Identity、Execution、Evidence、Verification 和 Lifecycle record 归 DBOS；
5. 定义 Capability Contract：`capability_name`、`scope`、`constraints`、`risk_level`，禁止实现自动扩大能力；
6. Research Conclusion、Publication、External Release 和 Major Capability Change 保留 Human Approval gate；
7. DBOS 向 SAEE 提供 Execution History、Evidence Bundle、Verification Result；
8. SAEE 只输出 Fitness Assessment、Risk Assessment、Evolution Recommendation；
9. 建立概念数据流与 object ownership，保持 Research Agent、DBOS、SAEE、Governance Decision 和 Human responsibility 分离；
10. Execution Failure、Evidence Failure、Verification Failure、Evaluation Conflict 和 Human Rejection 必须保留；
11. Future Research Agent implementation 必须符合本契约，但 Contract adoption 不自动授权实现、Prototype、Runtime 或 Deployment；
12. 本 ADR 不包含代码、API、schema、Agent、Runtime、Capability、Permission、Evidence、Evaluation 或实验执行。

```text
Contract ≠ Implementation
Contract Adoption ≠ Implementation Authorization
Research Agent Specification ≠ Agent Instance
Implementation ≠ Capability Expansion
Implementation ≠ Permission Grant
Evidence ≠ Truth
DBOS ≠ SAEE
```

## Alternatives（替代方案）

### A. 直接从 Pilot Specification 开始编码

拒绝。Pilot 描述角色和边界，但没有实现交付字段、Owner、失败保留和合规检查，容易产生架构漂移。

### B. 让 Research Agent 自行管理 Identity、Execution 和 Evidence

拒绝。会创建与 DBOS 竞争的事实权威，并允许 Agent 自证身份、历史和证据。

### C. 让实现根据可用工具自动生成 Capability

拒绝。技术可调用性不是已声明、Verified、Authorized 或 Permitted Capability。

### D. 让 DBOS 同时形成 SAEE 评价

拒绝。DBOS 提供运行事实和 Verification；Fitness、Risk 与 Evolution Evaluation 属于 SAEE。

### E. 让 SAEE Recommendation 直接修改实现或 DBOS 状态

拒绝。Recommendation 必须经过 Review、Decision、Adoption、独立授权和 DBOS lifecycle-controlled Execution。

### F. 将字段表直接定义为 API schema

拒绝。字段只定义 semantic contract；序列化、认证、transport、endpoint 和版本握手尚未选择，也未授权实现。

## Impact（影响）

### Positive（正面影响）

- Architecture 与 future implementation candidate 之间形成可审查桥梁；
- Entity、Execution、Evidence、Capability、Human gate 和 SAEE evaluation 具有稳定的最低交付语义；
- 数据 Owner、只读和写入边界可由智能体发现；
- 失败与 Retry 不再允许覆盖历史；
- Contract、Implementation、Authorization、Prototype 和 Deployment 保持不同状态；
- 未来 conformance review（合规审查）可以在不创造新权限的情况下进行。

### Costs and unresolved issues（代价与未决问题）

- 实际 contract adopter、implementation authorizer、conformance reviewer 和职责分离尚未指定；
- 字段的 data type、必填条件、controlled vocabulary、schema 和 version line 尚未选择；
- `entity_id`、`execution_id`、reference integrity 和跨系统 correlation 的生成/验证机制尚未定义；
- DBOS evidence collection adapter、SAEE evaluation adapter 和 transport 不存在；
- Capability verification、risk threshold、Permission policy 和 Context validation 仍需实现前规范；
- Human Approval reference 的身份、签名、撤销和有效期语义尚未定义；
- Failure taxonomy 与 DBOS/SAEE 既有错误语义的映射尚未完成；
- Legal data ownership、copyright、dataset license 和 retention 不由 architecture Owner 表自动解决；
- Conformance test、negative fixture 和 independent review evidence 尚未设计；
- Prototype 的最小任务集、隔离策略、停止规则和明确授权仍未形成。

## Consequence Boundaries（后果边界）

```text
RESEARCH_AGENT_IMPLEMENTATION_CONTRACT_DEFINED=true
RESEARCH_AGENT_DATA_FLOW_DEFINED=true
RESEARCH_AGENT_FAILURE_MODEL_DEFINED=true
RESEARCH_AGENT_IMPLEMENTATION_CONTRACT_ADOPTED=false
RESEARCH_AGENT_IMPLEMENTATION_AUTHORIZED=false
RESEARCH_AGENT_IMPLEMENTATION_CREATED=false
PROTOTYPE_CREATED=false
AGENT_INSTANCE_CREATED=false
DIGITAL_ENTITY_INSTANCE_CREATED=false
RUNTIME_CREATED=false
API_CREATED=false
SCHEMA_CREATED=false
CAPABILITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
EVIDENCE_CREATED=false
SAEE_EVALUATION_EXECUTED=false
CODE_CHANGED=false
```
