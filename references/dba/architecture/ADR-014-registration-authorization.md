---
adr_id: ADR-014
title: Registration Authorization Boundary
title_zh: 登记授权边界
status: proposed-architecture-decision-record
decision_adopted: false
implementation_authorized: false
registration_authorization_issued: false
registration_executed: false
entity_instance_created: false
---

# ADR-014: Registration Authorization Boundary

## Status（状态）

Proposed（提议）。本 ADR 记录 v0.1 architecture decision（架构决策）内容；尚未形成 adoption record（采纳记录），不授权 DBOS 实现或执行。

## Context（背景）

Digital Entity Admission Specification 已定义 Candidate Submission、Admission Review、Admission Decision、概念性的 Registration Authorization 与 DBOS Registration，但缺少正式 Authorization Object 和 Governance Decision mapping（治理决策映射）。

如果直接使用 `Admission Decision=APPROVED` 触发 DBOS，会混淆三种事实：

1. Candidate 在治理上可被接受；
2. 明确 issuer 是否允许某次、有界的登记操作；
3. DBOS 是否实际形成 canonical registration record。

这种混淆可能使 Approval 被误读为 Registration、Permission、Capability Grant 或 Active transition，也会使 DBOS 看起来既作决定又执行决定。

## Decision（决策）

采用独立 Registration Authorization boundary（登记授权边界）：

```text
Governance Decision Framework
  ↓ decision_type=admission
Admission Decision
  ↓ separate explicit issuance
Registration Authorization
  ↓ DBOS validation
DBOS Registration
```

具体规则：

- Admission Decision 是 Governance Decision framework 的 `admission` 类型；
- Admission `APPROVED` 只允许进入独立授权签发审查；
- 对 admission profile，Registration Authorization 承接特定登记 scope 的显式 Adoption/Authorization 记录，但仍与 Admission Decision 分离；
- Registration Authorization 使用 `authorization_id`、`decision_reference`、`candidate_id`、`target_entity_type`、`authorized_scope`、`issuer_reference`、`status` 和 `timestamp`；
- Authorization 状态为 `PENDING`、`AUTHORIZED`、`REJECTED` 或 `REVOKED`；
- 只有当前有效的 `AUTHORIZED` 才允许 DBOS 进入 pre-registration checks；
- DBOS Registration 是 approved governance result（已批准治理结果）的执行，不是 Admission Decision；
- 最大登记结果是 `REGISTERED`，不产生 Active、Capability Grant、Permission 或 Runtime；
- SAEE 不拥有 Admission、Authorization 或 Registration authority；
- 历史必须保留，撤销不得追溯删除已经发生的事实。

## Alternatives Considered（备选方案）

### A. Admission Approval directly triggers DBOS

拒绝。它把 Decision 与 Execution 合并，无法表达 scope、issuer、有效期、撤销和 DBOS 拒绝执行。

### B. Treat Registration Authorization as Permission

拒绝。Permission 是具体上下文中的执行许可；Registration Authorization 只允许 DBOS 尝试登记，不能授权 Entity 行为。

### C. Let DBOS issue its own Admission Decision

拒绝。DBOS 是 Operational Authority（运行权力）和 Registration executor（登记执行者），不能同时补造治理结论。

### D. Let SAEE approve admission based on fitness

拒绝。Evaluation ≠ Authority；SAEE governs evolution，不拥有初始登记权。

### E. Keep authorization implicit

拒绝。隐式授权无法被可靠验证、撤销、版本化或审计，且容易 fail open。

## Consequences（影响）

正向影响：

- Decision、Authorization 与 Execution 各自具有独立 truth surface；
- DBOS 可验证、拒绝或停止执行，而不改写上游 Decision；
- Candidate、Entity、Capability 与 Permission 继续分离；
- Research Agent 的未来登记路径具有可审计的人工/治理 gate；
- 编码智能体和检索智能体可以通过明确字段与常量识别边界。

代价与限制：

- 登记前增加一层 issuer authority、scope、有效期和 revocation 检查；
- 需要定义 Decision、Authorization 与 Registration Result 的引用完整性；
- v0.1 只定义规范，不选择 schema serialization（模式序列化）、API、存储或签名机制。

## Unresolved Questions（未决问题）

1. 谁可以担任 Authorization issuer，以及 authority assignment 如何记录、撤销和轮换？
2. `issuer_reference` 的真实性、签名或其他 integrity verification 由什么机制证明？
3. 是否需要在后续版本新增显式 `EXPIRED` 状态？
4. Registration Result / Receipt（登记结果/回执）的 canonical data contract 由哪个规范定义？
5. single-use、idempotency、duplicate、partial failure 和 retry 如何统一表达？
6. Candidate reference 到新 `entity_id` 的 continuity proof（连续性证明）如何形成？
7. 本 ADR、mapping 与 data contract 由谁正式 review、accept 和 adopt？

在这些问题解决前，不得把本 ADR 描述为已采纳的运行授权。

## Conformance（符合性）

符合本决策的规范必须维持：

```text
ADMISSION_DECISION_NE_REGISTRATION_AUTHORIZATION=true
REGISTRATION_AUTHORIZATION_NE_DBOS_REGISTRATION=true
REGISTRATION_AUTHORIZATION_NE_PERMISSION=true
REGISTERED_NE_ACTIVE=true
GOVERNANCE_DECISION_NE_EXECUTION=true
SAEE_NE_DBOS=true
ADR_ADOPTED=false
IMPLEMENTATION_AUTHORIZED=false
ENTITY_INSTANCE_CREATED=false
```
