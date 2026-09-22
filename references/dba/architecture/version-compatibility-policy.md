---
spec_id: DBA-VERSION-COMPATIBILITY-POLICY-0.1
title: Digital Biosphere Version Compatibility Policy v0.1
title_zh: 数字生物圈版本兼容策略 v0.1
status: non-executable-compatibility-policy
default_compatibility: unknown
automatic_migration_allowed: false
implementation_effect: none
runtime_effect: none
---

# Digital Biosphere Version Compatibility Policy v0.1

本策略定义 Architecture、Interface、Data Contract 和 Lifecycle Model Version 之间如何声明 compatibility（兼容性）、识别 Breaking Change（破坏性变更）并记录 Migration Requirement（迁移要求）。

## 1. Compatibility Declaration（兼容声明）

每个非 Editorial 的候选版本必须相对于明确的 prior version（先前版本）声明：

```text
SOURCE_VERSION=
TARGET_VERSION=
SCOPE=
BACKWARD_COMPATIBILITY=full|conditional|none|unknown
FORWARD_COMPATIBILITY=full|conditional|none|unknown
BREAKING_CHANGE=true|false|unknown
MIGRATION_REQUIREMENT=none|optional|required|undefined
CONDITIONS=
KNOWN_LIMITATIONS=
ADR_REFS=
```

`unknown` 不得被解释为兼容。没有共同可接受的版本或无法判断权限语义时，未来实现必须 fail closed（保守失败）；本策略不实现该检查。

## 2. Backward Compatibility（向后兼容）

目标版本只有在声明 scope 内满足以下条件时，才能声明向后兼容：

- 符合旧版本的记录、引用或规范解释在新版本下仍可被正确理解；
- 既有字段、状态、Owner、权力和不变量不被重新解释；
- 新增内容是 additive and optional（增量且可选），或缺失时具有明确的保守语义；
- 旧版本的 Recommendation 不会在新版本中变成 Command、Authorization 或 Execution；
- 历史引用继续可解析，且来源和限制不丢失。

Backward Compatible 不表示旧实现已经支持新版本，也不表示新版本已部署。

## 3. Forward Compatibility（向前兼容）

只有较旧的 consumer（消费者）可以安全处理较新版本材料时，才能声明向前兼容：

- 未知字段或受控值可以保持 `unknown`，而不是被错误默认；
- 较旧消费者可以忽略不理解的可选信息而不扩大权限或改变核心语义；
- 新增状态不会被映射为更高权限、成功、验证或采用状态；
- 无法理解的新语义会产生明确诊断或保守拒绝。

Forward Compatibility 默认不成立，必须独立于 Backward Compatibility 声明。文档可理解性不证明 Runtime interoperability（运行互操作性）。

## 4. Breaking Change（破坏性变更）

出现以下任一变化，默认视为 Breaking Change，除非 ADR 在严格限定 scope 内证明不是：

- 改变 SAEE、DBOS、Architecture Governance 或 Governance Decision 的责任 Owner；
- 改变 Architecture、Operational 或 Evolution Authority 的边界；
- 把 Recommendation、Decision、Adoption、Execution 或 Verification 合并或提升；
- 删除或重定义必需字段、状态、对象、标识符或来源语义；
- 改变 Lifecycle transition（生命周期转换）顺序、gate 或状态含义；
- 改变事实、证据、评价、权限或采用的 truth surface；
- 删除旧版本仍需要解析的受控值；
- 将可选字段改为必需字段且没有迁移路径；
- 将 `unknown`、`partial` 或 `conflicted` 默认升级为成功、兼容或已授权；
- 改变 Version/Release/Adoption 与 Implementation/Deployment 的分离。

Breaking Change 必须使用 Major Version、ADR、显式 Architecture Decision 和 Migration Requirement。版本号不能使未经审查的变化自动合法。

## 5. Migration Requirement（迁移要求）

Migration Requirement 是对未来采用或实现所需变化的规范说明，不是迁移授权，也不证明迁移已执行。`required` 声明至少应包含：

| 字段 | 语义 |
|---|---|
| `source_version` / `target_version` | 迁移起点和目标版本 |
| `affected_scope` | 受影响的对象、接口、状态或规范 |
| `required_transformations` | 必须发生的语义转换；不得隐含执行 |
| `state_mapping` | 生命周期或状态映射，未知项保持未知 |
| `provenance_preservation` | 历史、来源、Decision、Evidence 和 ADR 如何保留 |
| `defaults_policy` | 禁止用默认值伪造事实、权限或兼容性 |
| `parallel_support` | 是否允许并行兼容线及限制 |
| `rollback_or_exit` | 失败时的回退或退出语义 |
| `adoption_decision_ref` | 采用该迁移要求的显式决定 |
| `validation_requirements` | 完成后需要的有界验证；不表示已通过 |

迁移计划不得修改历史版本内容。实际代码、数据、Runtime 或状态迁移需要独立项目、权限和验证，本规范不授权。

## 6. Version Type Rules（按版本类型的规则）

| 版本类型 | Compatible change 示例 | Breaking change 示例 |
|---|---|---|
| Architecture | 增加不改变责任的解释或检索入口 | 改变 Stack layering、Owner、Authority 或核心不变量 |
| Interface | 新增有保守缺失语义的可选字段 | 删除字段、改变方向、Recommendation 变 Command |
| Data Contract | 新增可选字段或有界受控值 | 改变对象 Owner、必需字段语义或标识连续性 |
| Lifecycle Model | 增加不改变既有转换的可选说明 | 删除状态、改变 gate、把未验证状态映射为已授权 |

Interface 的详细版本协商继续遵循 [`interface-specification.md`](interface-specification.md)；本策略提供跨版本类型的共同治理规则。

## 7. Patch / Minor / Major Policy

- Patch：只允许无语义变化的修订；若语义、约束或兼容性改变，就不能使用 Patch。
- Minor：只允许经审查且明确声明向后兼容的增量变化。
- Major：用于 Breaking Change；必须有 ADR、Migration Requirement 和显式接受决定。
- `v0.x`：所有兼容性均需显式声明，不能从 Minor 数字推断。

该规则扩展 [`evolution-policy.md`](evolution-policy.md) 的版本摘要，不替代 Architecture Change Process。

## 8. Deprecation Compatibility（废弃兼容）

Deprecated 项目或版本必须说明：

- 哪些旧输入、状态和引用仍可解析；
- 新版本是否接受旧版本材料；
- 旧消费者如何处理新版本材料；
- 迁移是否 required、optional 或 undefined；
- 何时可以停止新采用；
- 归档后如何解析历史记录。

废弃不允许静默删除字段、状态或版本，也不产生 implementation support commitment（实现支持承诺）。若没有替代项，应显式使用 `no_replacement`。

## 9. 兼容性非声明

```text
COMPATIBILITY_POLICY_DEFINED=true
DEFAULT_COMPATIBILITY=unknown
BACKWARD_COMPATIBILITY_AUTOMATIC=false
FORWARD_COMPATIBILITY_AUTOMATIC=false
MIGRATION_AUTHORIZED=false
MIGRATION_EXECUTED=false
IMPLEMENTATION_SUPPORT_PROVEN=false
RUNTIME_INTEROPERABILITY_PROVEN=false
HISTORICAL_VERSION_DELETED=false
```
