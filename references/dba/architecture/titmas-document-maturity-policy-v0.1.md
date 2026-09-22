---
document_id: DBA-TITMAS-DOCUMENT-MATURITY-POLICY-0.1
title: TITMAS Document Maturity Policy v0.1
title_zh: TITMAS 文档成熟度政策 v0.1
status: policy-defined-no-maturity-promotions-executed
maturity: Development
maturity_scope: entire-document
owner_ref: NOT_ASSIGNED
decision_reference: NOT_DECIDED
supersedes: NONE
superseded_by: NONE
compatibility_statement: "Development document; no implementation compatibility claim."
implementation_feedback_refs: []
conformance_refs: []
known_limitations: [SEE_DOCUMENT_BODY]
document_type: non-executable-document-governance-policy
architecture_domain: TITMAS
default_document_maturity: Development
stable_documents_declared_by_this_policy: 0
release_effect: none
implementation_effect: none
authority_effect: none
---

# TITMAS Document Maturity Policy v0.1

## 1. Principle（原则）

本政策重度参考 OpenTelemetry 的 document-level maturity（文档级成熟度）：状态属于单个
文档或显式 section，不属于整个 TITMAS 品牌，也不自动传播到实现、Community、Release、
Adoption 或 Production。

```text
DOCUMENT_MATURITY_NE_IMPLEMENTATION_STATUS=true
DOCUMENT_MATURITY_NE_COMMUNITY_STATUS=true
DOCUMENT_MATURITY_NE_RELEASE_STATUS=true
DOCUMENT_MATURITY_NE_ADOPTION_STATUS=true
```

无显式 `maturity` 字段的 TITMAS 文档按 `Development` 处理。

## 2. Maturity States（成熟度状态）

| maturity | 含义 | 允许变化 | 最低进入证据 |
|---|---|---|---|
| `Development` | 内容不完整，主要用于问题界定和反馈 | 可移除，可发生 breaking change | purpose、scope、Owner 状态、已知缺口 |
| `Alpha` | 对有限非关键用途可评审；接口仍可能频繁变化 | 可 breaking，但必须记录 | 对象/字段/失败语义、初步负例、来源 |
| `Beta` | 核心接口尽量稳定，已有多个实现或使用反馈 | breaking change 必须最小化并给迁移说明 | 版本、兼容政策、实现反馈、测试设计 |
| `Release Candidate` | 功能范围完整，准备进入 Stable 决策 | 只允许特殊且记录的 breaking change | 完整 review、conformance plan、无未处置关键边界冲突 |
| `Stable` | 对声明范围提供版本和兼容保证 | breaking change 需新版本与迁移/废弃路径 | Architecture Decision、Owner、版本、实现反馈、独立符合性和安全审查 |
| `Deprecated` | 停止新增；保留兼容窗口和替代路径 | 仅关键修正 | deprecation decision、replacement、时间表、历史保留 |
| `Unmaintained` | 没有活动 Owner，状态必须显式暴露 | 不得继续声称受维护 Stable | inactivity evidence、Owner 缺失、寻求维护者路径 |
| `Archived` | 历史保留，不再作为当前规范入口 | 只修正历史元数据或链接 | archive decision、successor/none、immutable history reference |

可使用 `Mixed` 表示一个文档的显式 section 处于不同成熟度；每个 section 必须单独标注。

## 3. Required Metadata（必需元数据）

```yaml
document_id:
title:
version:
maturity: Development|Alpha|Beta|Release Candidate|Stable|Deprecated|Unmaintained|Archived|Mixed
maturity_scope:
owner_ref:
decision_reference:
supersedes:
superseded_by:
compatibility_statement:
implementation_feedback_refs: []
conformance_refs: []
known_limitations: []
```

在 Owner、Decision 或 evidence 不存在时必须写 `NOT_ASSIGNED`、`NOT_DECIDED` 或空数组，
不得用计划替代事实。

## 4. Promotion Rules（升级规则）

每次升级必须：

1. 单独 Proposal；
2. 明确当前与目标 maturity；
3. 证明目标状态的进入条件；
4. 记录正例、负例、失败、unknown 和 unsupported；
5. 检查 backward/forward compatibility；
6. 检查 security、privacy、Authority 和 duplicate ownership；
7. 获得适用 Owner review；
8. 需要时形成 DBA Architecture Decision；
9. 保留原版本和结果。

`Alpha → Beta → Release Candidate → Stable` 不是自动计时器。下载量、Star、PR 数、模型推荐、
一项实现、自报 PASS 或单个文档 Stable 都不能单独升级状态。

## 5. Downgrade, Deprecation and Archive（降级、废弃与归档）

- 发现重大事实错误、安全问题、Owner 缺失或无法维持兼容保证时，可以降级；
- 降级必须记录原因、影响范围、替代路径和下一次复核；
- Deprecated 不等于 Deleted，必须保留历史版本；
- Unmaintained 不得伪装成 Stable；
- Archived 不删除失败、review、Decision 或 compatibility history。

## 6. Separate State Dimensions（独立状态维度）

每个规范及其实现至少分开记录：

```text
document_maturity=
specification_version=
implementation_status=
implementation_version=
conformance_status=
community_status=
release_status=
adoption_status=
production_status=
```

任何缺失项按 `UNKNOWN` 或 `NOT_ASSESSED`，不能从相邻字段推导。

## 7. OpenTelemetry Reference Boundary（参考边界）

参考
[OpenTelemetry Definitions of Document Statuses](https://opentelemetry.io/docs/specs/otel/document-status/)
在 `2026-07-23` 可见的 document-level status 机制。TITMAS 增加 `Archived` 并将各项
进入条件适配到 DBA 权力模型。该参考不表示 TITMAS 采用 OpenTelemetry 的品牌、组件
成熟度、组织治理或运行兼容性。

## 8. Current Result（当前结果）

```text
TITMAS_DOCUMENT_MATURITY_POLICY_DEFINED=true
TITMAS_DEFAULT_DOCUMENT_MATURITY=Development
TITMAS_STABLE_DOCUMENTS_DECLARED_BY_THIS_POLICY=0
TITMAS_MATURITY_PROMOTION_EXECUTED=false
TITMAS_IMPLEMENTATION_STATUS_CHANGED=false
TITMAS_RELEASE_STATUS_CHANGED=false
```
