---
adr_id: ADR-002
title: Establish the SAEE-DBOS Interface Contract
title_zh: 建立 SAEE-DBOS 接口契约
status: accepted-for-architecture-specification-v0.1
decision_scope: data-contract-and-authority-boundary-only
implementation_status: not-authorized
api_effect: none
capability_effect: none
permission_effect: none
evidence_effect: none
---

# ADR-002: Establish the SAEE–DBOS Interface Contract（建立 SAEE–DBOS 接口契约）

## Background（背景）

ADR-001 已确定 `SAEE ≠ DBOS`、`DBOS ≠ SAEE`：DBOS governs existence（DBOS 治理存在），SAEE governs evolution（SAEE 治理演化）。现有 `saee-dbos-contract.md` 已定义交换方向和非授权语义，但尚缺少稳定的字段级 interface profile（接口配置）、核心对象 Owner、版本兼容规则和禁止重复建设规则。

缺少这些内容会导致：

- 同一运行事实在 DBOS 和 SAEE 中形成两个规范版本；
- Verification Result 与 Fitness Assessment 被同一 `status` 或 `score` 混用；
- SAEE 的 Recommendation 被误读为 DBOS Command；
- Evidence、Evaluation 或 Recommendation 的 Owner 不明确；
- 各项目独立设计不兼容字段或重复对象；
- 文档接口被误报为已实现 API 或集成能力。

## Decision（决策）

1. 建立 `interface-specification.md`，定义 DBOS → SAEE 与 SAEE → DBOS 的 v0.1 字段语义。
2. 建立 `data-contracts.md`，确定以下对象 Owner：
   - Entity、Execution、Evidence Object：DBOS；
   - Evaluation、Recommendation Object：SAEE。
3. 建立 `interface-boundary-rules.md`，固定“DBOS 负责有界运行记录，SAEE 负责派生评价”的边界。
4. 所有 SAEE → DBOS 输出的 authority class 为 `Recommendation`，不是 `Command`。
5. SAEE 不得创建身份、修改能力或 Evidence、授予权限、删除历史或直接改变 DBOS 状态。
6. DBOS 不得修改 SAEE 算法、Fitness 模型或演化结论。
7. 版本变化必须显式说明 backward compatibility（向后兼容）、schema evolution（模式演化）和 deprecation（弃用）。
8. 本决策只建立文档数据契约，不创建 API、endpoint、可执行 schema、代码或集成。

## Alternatives（替代方案）

### A. 继续只有概念边界，不定义字段

拒绝。概念边界不足以阻止不同项目为同一对象创建不兼容字段和多个 Owner。

### B. 合并 SAEE 与 DBOS

拒绝。合并会把运行记录、验证、评价、建议与状态权放进同一责任域，违反 ADR-001。

### C. 让 SAEE 输出可直接执行的 Command

拒绝。它会把评价和建议升级为运行权限，绕过独立授权 gate。

### D. 让 DBOS 内建 SAEE Fitness 与演化算法

拒绝。它会使 Existence Governance 吞并 Evolution Governance，并使模型无法独立版本化和审计。

### E. 各组件维护自己的 Entity、Evidence 和 Evaluation schema

拒绝。它会产生重复建设、来源漂移、字段同名异义和多个 canonical Owner。

## Impact（影响）

### Positive（正面影响）

- DBOS 输入和 SAEE 输出获得稳定、智能体可检索的字段语义；
- 核心对象 Owner 和只读消费关系明确；
- Recommendation 与 Command、Verification 与 Evaluation 保持分离；
- 后续 adapter 可以在不合并系统的前提下检查兼容性；
- 重复建设可以在设计阶段被识别。

### Costs and unresolved issues（代价与未决问题）

- 未来仍需单独选择序列化格式、传输机制、认证和隐私处理；
- `v0.x` 版本兼容性必须逐次显式声明；
- 受控值域、数值尺度、单位和 SAEE 模型版本仍由各责任域后续规范；
- 最终 policy and authorization gate 的权威主体仍未定义；
- ADR-001 位于 `architecture/architecture-decision-records/`，ADR-002 按本任务要求位于 `architecture/`；是否统一 ADR 目录需要单独的信息架构决定，本任务不迁移既有文件。

## Consequence boundaries（后果边界）

```text
INTERFACE_CONTRACT_DOCUMENTED=true
INTERFACE_CONTRACT_IMPLEMENTED=false
API_CREATED=false
ENDPOINT_CREATED=false
CODE_CHANGED=false
SAEE_RUNTIME_AUTHORITY_CREATED=false
DBOS_EVOLUTION_AUTHORITY_CREATED=false
```

