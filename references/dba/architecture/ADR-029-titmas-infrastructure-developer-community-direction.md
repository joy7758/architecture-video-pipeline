---
adr_id: ADR-029
title: Adopt the TITMAS Infrastructure Developer Community Direction
title_zh: 采纳 TITMAS 可信多智能体基础设施开发者社区方向
status: accepted-strategic-direction-contributor-entry-prepared-community-not-established
maturity: Development
maturity_scope: entire-document
owner_ref: NOT_ASSIGNED
decision_reference: ADR-029
supersedes: NONE
superseded_by: NONE
compatibility_statement: "Development document; no implementation compatibility claim."
implementation_feedback_refs: []
conformance_refs: []
known_limitations: [SEE_DOCUMENT_BODY]
decided_by_ref: zhangbin
decided_at: 2026-07-23
primary_repository: digital-biosphere-architecture
implementation_authorized: false
external_action_authorized: false
community_established: false
contributor_entry_prepared: true
public_contribution_surface_authorized: false
code_of_conduct_adopted: false
foundation_in_scope: false
authority_effect: none
---

# ADR-029: Adopt the TITMAS Infrastructure Developer Community Direction

> Historical decision. ADR-034 and
> [`titmas-canonical-community-integration-plan-v1.0.md`](titmas-canonical-community-integration-plan-v1.0.md)
> define the canonical successor name and current integration candidate.

中文：ADR-029——采纳 TITMAS 可信多智能体基础设施开发者社区方向。

## Context（背景）

TITMAS 已被提出为 DBA 下的可信多智能体互操作架构域，但当前仍处于
`AUTHORITY_FREEZE_CANDIDATE`，Interface v0.1、实现、独立仓库和外部生态动作均未获授权。

后继讨论提出建立开发者社区。仅使用 `TITMAS Community` 容易让首次接触者误解为普通
Agent 社区；加入 Foundation（基金会）又会错误暗示法律实体、组织治理和独立 Authority。
Human Program Owner 要求把“基础设施开发者社区”方向写入 DBA 主框架，防止后续开发
偏移。

OpenTelemetry 为规范优先、跨实现版本声明、document-level maturity、公开贡献入口、
SIG/workstream、Contrib 与符合性矩阵提供了适合重度参考的成熟模式。但 Reference
Adoption（参考采纳）不表示 TITMAS 拥有 OpenTelemetry 的品牌、组织地位、CNCF 身份、
社区规模或成熟度。

## Decision（决定）

采纳：

```text
English: TITMAS Infrastructure Developer Community
Chinese: TITMAS 可信多智能体基础设施开发者社区
Subtitle: Developer Community for Trusted Multi-Agent Infrastructure
```

并采纳以下长期约束：

1. TITMAS 社区方向聚焦可信多智能体基础设施的 Specification、Adapter contract、
   Conformance 和 Reference Implementation boundary；
2. 面向首次接触者的名称必须包含 Infrastructure／基础设施；
3. 重度参考 OpenTelemetry 的规范与实现分离、文档级成熟度、贡献入口、工作流组织、
   实现版本声明和符合性矩阵；
4. 正式 SIG 必须在真实工作、参与者、Maintainer/Reviewer 和公开流程形成后单独批准；
5. Community Review 不等于 Architecture Decision，Maintainer 不自动拥有 DBA、DBOS
   或 SAEE Authority；
6. Foundation、法律实体和独立组织不属于当前范围；
7. 当前只采纳社区战略方向，不宣布社区已经建立；
8. 后续外部入口、招募、组织账号、仓库、Issue、PR、实现和发布分别需要明确授权。

C1 允许在 DBA 内准备非执行 Contributor Guide、Proposal/Maturity/Workstream 模板、
行为规范候选、首次贡献候选和机器可读发现文件。这些文件不构成公共入口授权或社区事实。

规范入口：

- [TITMAS Infrastructure Developer Community Strategy v0.1](titmas-infrastructure-developer-community-strategy-v0.1.md)；
- [Contributor Guide](../CONTRIBUTING.md)；
- [Agent-readable Contributor Entry](../TITMAS-CONTRIBUTOR-ENTRY-v0.1.json)；
- [TITMAS Document Maturity Policy v0.1](titmas-document-maturity-policy-v0.1.md)；
- [TITMAS Architecture Charter v1.0](titmas-architecture-charter-v1.0.md)；
- [Open Infrastructure Strategy Constitution](open-infrastructure-strategy-constitution.md)。

## Alternatives Considered（备选方案）

### A. 只称 `TITMAS Community`

拒绝。首次接触者无法立即判断社区面向基础设施而不是 Agent 应用或普通讨论社区。

### B. 同时规划 Community and Foundation

拒绝。Foundation 不是当前目标，会制造法律实体、资金、组织权力和成熟度误读。

### C. 立即复制 OpenTelemetry 的 GC、TC 和 SIG 组织

拒绝。当前没有相应参与者、授权、项目规模或运行事实。只采纳机制，不复制组织事实。

### D. 继续只维护架构文档，不定义社区路径

拒绝。缺乏明确贡献入口会使 TITMAS 难以获得外部实现反馈，并增加后续开发漂移。

## Consequences（影响）

正面影响：

- 第一次接触者能快速理解 TITMAS 的基础设施定位；
- 社区贡献围绕规范、Adapter、Conformance 和参考实现，而不是扩张 Agent 功能；
- OpenTelemetry 参考机制进入可审查的 DBA 战略基线；
- 后续 Roadmap、Risk、Gate 和 Agent-readable entry 有统一检查依据。

代价与限制：

- 当前仍不能宣称社区已建立；
- Contributor Guide 已在 DBA 本地准备，但正式 Code of Conduct、安全接收路径、SIG、
  公开渠道和 Maintainer 仍需后续决定；
- Authority Freeze 和 Interface Readiness blocker 不因本决定关闭；
- OpenTelemetry 上游变化需要 exact-source refresh，不得自动跟随 `latest`。

## Explicit Non-authorizations（明确不授权）

```text
TITMAS_DEVELOPER_COMMUNITY_ESTABLISHED=false
TITMAS_FOUNDATION_IN_SCOPE=false
TITMAS_LEGAL_ENTITY_CREATED=false
TITMAS_ORGANIZATION_CREATED=false
TITMAS_REPOSITORY_CREATED=false
TITMAS_SIG_CREATED=false
TITMAS_MAINTAINER_ASSIGNED=false
TITMAS_CONTRIBUTOR_ENTRY_PREPARED=true
TITMAS_PUBLIC_CONTRIBUTION_SURFACE_AUTHORIZED=false
TITMAS_CODE_OF_CONDUCT_ADOPTED_FOR_INTEGRATION_CANDIDATE=true
TITMAS_INTERFACE_V0_1_AUTHORIZED=false
TITMAS_IMPLEMENTATION_AUTHORIZED=false
TITMAS_EXTERNAL_ACTION_AUTHORIZED=false
DBOS_AUTHORITY_CHANGED=false
SAEE_AUTHORITY_CHANGED=false
AGENT_CREATED=false
RUNTIME_CREATED=false
PERMISSION_GRANTED=false
```
