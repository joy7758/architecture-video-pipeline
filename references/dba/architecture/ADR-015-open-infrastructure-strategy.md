# ADR-015: Open Infrastructure Strategy

Status: `ACCEPTED`

Date: 2026-07-20

Decision scope: Strategic architecture positioning

Implementation authorization: `NONE`

## Context

Digital Biosphere Stack 已形成身份、治理、证据、验证和演化等长期方向。随着 DBOS 基础设施工作增多，项目存在四类战略漂移风险：

1. 变成与通用 Agent framework 竞争的普通 Agent 平台；
2. 被单一 enterprise audit 产品定义；
3. 用不可验证的数字生命宏大叙事替代可落地基础设施；
4. 通过封闭产品路线削弱协议、开发者和多方生态价值。

如果没有最高战略边界，局部功能、商业机会或行业需求可能反向改变 DBOS 和 SAEE 的架构职责。

## Decision

选择 Open Infrastructure Strategy（开放基础设施战略）：

- DBOS 定位为 Open Digital Entity Infrastructure；
- SAEE 定位为 Evolution Intelligence Layer；
- Developer Ecosystem First；
- 基础协议、数据结构、接口标准和开发工具优先开放；
- 企业部署、行业解决方案、技术服务、认证和高级治理形成可选商业生态；
- Application 建立在 DBOS 之上，不进入 DBOS 核心身份；
- 每项新提案通过 Strategic Proposal Gate 和 Architecture Review。

规范入口为 [Digital Biosphere Open Infrastructure Strategy Constitution v0.1](open-infrastructure-strategy-constitution.md)。

## Why This Decision

开放基础设施路线能够：

- 保持 DBOS 与 Foundation Model、Agent application、行业产品的差异；
- 让多个 Agent framework、模型、Runtime 和行业实现共享治理基础；
- 通过协议、验证工具和 reference implementation 降低开发者采用成本；
- 允许多方在共同基础之上形成商业服务，而不是由一个封闭产品垄断架构；
- 保持 DBOS governs existence / SAEE governs evolution 的职责分离。

“Linux-like”只借鉴开放标准、开发者采用、社区和企业生态的增长机制，不声称复制 Linux 或 Kubernetes 的治理、规模、许可证或成功。

## Alternatives Considered

### Generic Agent Platform

Rejected as the DBOS core strategy。该路线会让 DBOS 与 LangChain、CrewAI、OpenAI Agent 等应用/编排生态竞争，并把身份和治理基础设施从属为 Agent 功能。

Agent development tools 可以作为生态入口，但 DBOS 本身不成为通用 Agent builder。

### Enterprise Audit Product

Rejected as the whole-system identity。Audit 可以成为 Governance Service，但单一审计产品无法代表 Identity、Lifecycle、Capability Boundary、Execution Context、Evidence Integration 和 Federation 的完整基础设施职责。

### Closed SaaS Platform

Rejected as the strategic center。封闭 SaaS 可以是部署方式，但不能成为协议事实的唯一来源，也不能通过供应商锁定替代开放互操作。

### Digital-life-first Product

Rejected as the near-term commercial framing。Digital Biosphere 和长期演化研究可以保留为架构/研究方向，但面向开发者和客户的入口必须从可验证、可复用的 Agent infrastructure 开始。

### Merge DBOS and SAEE

Rejected。存在治理和演化评价具有不同 authority boundary；合并会造成评价、决策、执行和事实所有权混淆。

## Consequences

Positive consequences：

- 新功能拥有明确 Core / Application / Governance Service 归属；
- 开发者工具、协议和验证优先级提高；
- 行业应用和商业服务可以增长而不改写 DBOS 核心；
- 战略漂移可以通过 ADR 和 constitution review 被显式拒绝。

Trade-offs：

- 短期产品叙事必须克制，不能以“大而全 Agent 平台”换取表面功能完整；
- 开放协议需要兼容性、版本和社区治理成本；
- 商业能力必须证明其不破坏开放核心；
- 行业解决方案需要在独立项目或应用层维护边界。

## Non-decisions

本 ADR 不决定：

- 具体 SDK、API、Marketplace 或 Enterprise Edition 的实现；
- 未来仓库许可证、公司结构、价格或 SLA；
- 认证机构、认证标准或合规结论；
- Agent、Runtime、Digital Entity 或 Digital Organism 的创建；
- DBOS 或 SAEE 的实现 roadmap、发布或部署。

## Review Trigger

出现以下情况时必须复核本 ADR：

- DBOS core proposal 只服务一个 Agent 或行业；
- 关键协议变为单一供应商私有格式；
- 商业产品要求改变开放协议语义；
- DBOS 开始实现模型智能或 SAEE 演化算法；
- SAEE 被赋予身份、Permission、Execution 或 Evidence mutation 权限；
- “Marketplace listing”“validator pass”或“付费服务”被表达为官方认证。
