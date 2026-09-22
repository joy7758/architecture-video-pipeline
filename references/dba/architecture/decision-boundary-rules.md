---
spec_id: DBA-DECISION-BOUNDARY-RULES-0.1
title: Governance Decision Boundary Rules v0.1
status: normative-architecture-boundary-rules
implementation_authorized: false
runtime_created: false
entity_created: false
capability_effect: none
authority_effect: none
---

# Governance Decision Boundary Rules v0.1（治理决策边界规则 v0.1）

## 1. 适用范围

这些规则约束 Recommendation → Review → Decision → Adoption → Execution → Verification 的治理路径。它们只建立文档型 architecture invariants（架构不变量），不创建审批系统、工作流 Runtime、执行器或授权主体。

## 2. 五条强制规则

### `DBR-001`: SAEE cannot execute its own recommendations

SAEE 不能执行自己的 Recommendation。SAEE 只能产生 Evaluation、Risk Assessment、Evolution Recommendation 与 Governance Suggestion；它不得把这些对象转成 DBOS 命令、直接状态变更或隐式授权。

### `DBR-002`: DBOS cannot invent evolution conclusions

DBOS 不能发明 Evolution Conclusion（演化结论），不能修改 SAEE Fitness 模型、风险评价、演化建议或治理建议后继续声称为原始 SAEE 输出。DBOS 可以检查自身是否允许执行，但该检查不等于演化判断。

### `DBR-003`: Recommendation cannot directly modify entity state

Recommendation 不能直接修改 Entity Object、Capability record、Lifecycle state、Execution record 或 Evidence。Recommendation 的接收、审查、批准、采纳与执行必须是不同状态。

### `DBR-004`: Decision requires explicit authorization

Decision 必须有显式授权。进入 `APPROVED` 必须具有可追溯的 `approved_by` 和授权范围；缺失、过期、撤销、冲突或无法解析的授权必须 fail closed（保守失败）。Decision Object 和本规范本身都不是授权来源。

### `DBR-005`: Execution must generate evidence

Execution 必须产生或关联 DBOS 管理的 Evidence，并形成有界 Verification Result。没有 Evidence 的执行不能进入 `VERIFIED`；有 Evidence 也不自动证明执行正确或建议有效。

## 3. 附加边界规则

### `DBR-006`: Approval is not adoption

`APPROVED` 只记录授权决策；只有独立的 adoption record（采纳记录）才能进入 `ADOPTED`。

### `DBR-007`: Adoption is not execution

`ADOPTED` 不表示 DBOS 已开始、完成或验证执行。执行必须通过 DBOS lifecycle control（生命周期控制）。

### `DBR-008`: Decision Object cannot mutate source objects

Decision Object 只能引用 Recommendation、Evaluation 和 DBOS 对象，不能覆盖或追溯性修改这些对象。

### `DBR-009`: Revocation does not erase history

`REVOKED` 不删除 Recommendation、Decision、Adoption、Execution 或 Evidence 历史。若执行已经开始，撤销不自动回滚；任何停止、补偿或恢复动作都需要新的 DBOS 受控记录。

### `DBR-010`: Verification is bounded

`VERIFIED` 只表示指定执行、Evidence、规则和版本通过了声明的验证，不表示演化结论正确、能力永久成立、治理策略有效或全局安全。

## 4. 禁止的权限提升

| 禁止模式 | 违反规则 | 正确处理 |
|---|---|---|
| SAEE 写入 `lifecycle_state` | `DBR-001/003` | SAEE 只产生 Recommendation；DBOS 在授权后另行执行 |
| SAEE 自己批准自己的建议 | `DBR-001/004` | 由明确的外部 decision authority 形成批准记录 |
| DBOS 根据运行记录自行生成演化结论 | `DBR-002` | 将记录交给 SAEE Evaluation，再进入决策路径 |
| `decision_result=approved` 直接触发执行 | `DBR-006/007` | 先形成 Adoption，再通过 DBOS 执行前检查 |
| 执行完成直接标记 `VERIFIED` | `DBR-005/010` | 生成 Evidence 并执行有界 Verification |
| 撤销后删除历史 | `DBR-009` | 保留 append-only（仅追加）状态和后续补偿记录 |

## 5. 进入执行的最小条件

DBOS 只有在下列条件同时满足时才可以进入执行处理；本规范不声明当前已有实现：

1. `source_recommendation` 可解析且未被替换或伪造；
2. Decision Object 处于 `ADOPTED`；
3. `decision_result=approved`；
4. `approved_by` 和授权范围可验证且未撤销；
5. Decision 类型与 DBOS 生命周期目标一致；
6. DBOS 当前能力、权限、资源和安全约束允许处理；
7. Evidence 与 Verification 计划已经明确。

任一条件不满足时必须拒绝执行或保持待处理状态，不得通过默认值补造授权。

## 6. 边界状态常量

```text
SAEE_CAN_EXECUTE_RECOMMENDATION=false
DBOS_CAN_INVENT_EVOLUTION_CONCLUSION=false
RECOMMENDATION_CAN_MODIFY_ENTITY_STATE=false
DECISION_REQUIRES_EXPLICIT_AUTHORIZATION=true
EXECUTION_REQUIRES_EVIDENCE=true
APPROVAL_IS_ADOPTION=false
ADOPTION_IS_EXECUTION=false
```

