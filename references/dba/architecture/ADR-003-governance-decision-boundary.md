---
adr_id: ADR-003
title: Establish an Independent Governance Decision Boundary
title_zh: 建立独立治理决策边界
status: accepted-for-architecture-specification-v0.1
decision_scope: architecture-governance-record-and-state-boundary-only
implementation_status: not-authorized
runtime_effect: none
entity_effect: none
capability_effect: none
permission_effect: none
evidence_effect: none
---

# ADR-003: Establish an Independent Governance Decision Boundary

## Problem（问题）

现有 Digital Biosphere Stack 已经分离 DBOS Existence Governance（存在治理）与 SAEE Evolution Governance（演化治理），并规定 SAEE → DBOS 输出是 Recommendation，不是 Command 或 Authorization。

但是，仅有接口边界仍不能回答：

- 谁记录 Review、Decision 和 Adoption；
- `Approved`、`Rejected`、`Adopted` 与 `Executed` 如何区分；
- 显式授权如何进入 Decision Object；
- Recommendation 如何在不获得执行权的情况下影响 DBOS；
- 执行证据与 Verification 如何关闭治理回路；
- 撤销如何保留历史并阻止静默回滚。

如果没有独立决策边界，SAEE Recommendation 可能被直接执行，或 DBOS 可能为了执行而自行产生演化判断。

## Decision（选择）

增加 Governance Decision Layer（治理决策层），其角色为 Architecture Governance（架构治理）。

该层：

1. 规范 Governance Decision Object；
2. 记录 Review、Decision 与 Adoption 状态；
3. 要求 `APPROVED` 具有显式 `approved_by`；
4. 保持 Recommendation、Decision、Adoption、Execution 与 Verification 分离；
5. 将已批准且已采纳的变化交回 DBOS lifecycle control；
6. 不成为 DBOS 模块、SAEE 模块、Runtime、Entity、授权主体或执行主体。

责任保持：

```text
SAEE: produces Recommendation
Architecture Governance: records Decision and Adoption
DBOS: executes authorized change and produces Evidence/Verification
```

## Alternatives（替代方案）

### A. SAEE 直接执行 Recommendation

拒绝。Evaluation 会被升级为 Authority，SAEE 将同时拥有演化判断和运行状态写权。

### B. DBOS 自行决定演化结论

拒绝。DBOS 会吞并 SAEE 的 Fitness、Risk、Evolution Modeling 和 Governance Evolution 责任。

### C. 将 Decision 与 Execution 合并为一个状态

拒绝。批准记录会被误报为执行事实，无法表达采纳失败、执行拒绝、部分执行或执行后验证失败。

### D. 只依赖未结构化人工讨论

拒绝。未结构化讨论不能稳定表达 `approved_by`、范围、状态、撤销、执行引用和 Evidence 链。

### E. 建立新的治理 Runtime 或 Agent

拒绝。本任务只需要 architecture record boundary（架构记录边界），不需要新运行系统或主体。

## Impact（影响）

### Positive（正面影响）

- SAEE 不拥有执行权；
- DBOS 不拥有演化判断权；
- Decision 不再被误当作 Execution；
- 授权、采纳、执行和验证获得独立可追溯状态；
- 撤销不会删除历史或自动回滚；
- 执行必须产生 Evidence 并接受 Verification。

### Costs and unresolved issues（代价与未决问题）

- 最终 decision authority、reviewer 和 adoption authority 尚未指定；
- Decision Object 当前使用 `approved_by`，拒绝者、采纳者和撤销者需通过通用 provenance 表达；未来可能需要更对称的 authority fields（授权字段）；
- Decision Object 没有独立 `verification_reference`；v0.1 只能通过 `execution_reference → Evidence → Verification` 引用链追溯，是否增加直接引用需后续版本决定；
- `EXECUTING` 状态承载 `execution_completed` 里程碑，未来是否增加独立 `EXECUTED_PENDING_VERIFICATION` 状态需要实际用例验证；
- Verification 是否需要与 DBOS Execution 进一步 separation of duties（职责分离）尚未决定；
- 授权过期、并发 Decision、冲突 Adoption 和补偿语义尚需后续规范；
- ADR-001 位于嵌套目录，ADR-002/003 位于 `architecture/`；目录规范化仍待单独决定。

## Consequence boundaries（后果边界）

```text
GOVERNANCE_DECISION_BOUNDARY_DEFINED=true
GOVERNANCE_DECISION_RUNTIME_CREATED=false
GOVERNANCE_DECISION_ENTITY_CREATED=false
SAEE_EXECUTION_AUTHORITY_CREATED=false
DBOS_EVOLUTION_AUTHORITY_CREATED=false
CAPABILITY_CREATED=false
API_CREATED=false
CODE_CHANGED=false
```
