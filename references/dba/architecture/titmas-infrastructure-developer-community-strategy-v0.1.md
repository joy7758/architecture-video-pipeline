---
document_id: DBA-TITMAS-INFRASTRUCTURE-DEVELOPER-COMMUNITY-STRATEGY-0.1
title: TITMAS Infrastructure Developer Community Strategy v0.1
title_zh: TITMAS 可信多智能体基础设施开发者社区战略 v0.1
status: contributor-entry-prepared-community-not-established
maturity: Development
maturity_scope: entire-document
owner_ref: NOT_ASSIGNED
supersedes: NONE
superseded_by: NONE
compatibility_statement: "Development document; no implementation compatibility claim."
implementation_feedback_refs: []
conformance_refs: []
known_limitations: [SEE_DOCUMENT_BODY]
document_type: architecture-and-developer-community-strategy
primary_repository: digital-biosphere-architecture
architecture_domain: TITMAS
community_display_name_en: TITMAS Infrastructure Developer Community
community_display_name_zh: TITMAS 可信多智能体基础设施开发者社区
community_subtitle_en: Developer Community for Trusted Multi-Agent Infrastructure
decision_reference: ADR-029-titmas-infrastructure-developer-community-direction.md
decided_by_ref: zhangbin
adopted_at: 2026-07-23
opentelemetry_reference_observed_at: 2026-07-23
opentelemetry_community_reference_commit: d3d7cb3c1bc1104d8df7cf26dba9bf86cf354f26
opentelemetry_specification_reference_commit: 2e90a4df976ba2609577f3308ad27188a2619853
community_established: false
community_state: SUPERSEDED_BY_CANONICAL_INTEGRATION_CANDIDATE
contributor_entry_prepared: true
contributor_guide_created: true
proposal_template_created: true
document_maturity_policy_created: true
workstream_template_created: true
good_first_contribution_catalog_created: true
code_of_conduct_candidate_created: true
code_of_conduct_adopted_for_integration_candidate: true
machine_readable_contributor_entry_created: true
c1_validation_report: titmas-canonical-community-integration-plan-v1.0.md
public_contribution_surface_authorized: false
foundation_in_scope: false
legal_entity_created: false
organization_created: false
repository_created: false
implementation_authorized: false
external_action_authorized: false
runtime_effect: none
authority_effect: none
---

# TITMAS Infrastructure Developer Community Strategy v0.1

中文：TITMAS 可信多智能体基础设施开发者社区战略 v0.1。

> Historical strategy: the canonical successor is **TITMAS Agent-Native
> Standards Community**. Current status is projected only by
> [`../TITMAS/community/community-status.json`](../TITMAS/community/community-status.json).

## 0. First-contact Explanation（首次接触说明）

> TITMAS is a developer community for trusted multi-agent infrastructure.

中文：TITMAS 是围绕可信多智能体基础设施建立的开发者社区。

如果开发者正在构建需要长期运行、跨框架协作并留下可验证记录的 AI Agent，TITMAS
帮助其使用共同的规范、Adapter contract（适配器契约）、conformance test（符合性测试）
和 reference implementation（参考实现）边界，保持 Identity、Capability、Execution、
Evidence、Verification 与 Evaluation 的含义和权力不被混淆。

更简单地说：

> You build agents. TITMAS helps them collaborate through understandable,
> implementable, and verifiable infrastructure rules.

中文：开发者负责构建 Agent；TITMAS 提供易理解、可实现、可验证的基础设施规则，帮助
不同 Agent 可信协作。

TITMAS 不创建 Agent，不替代 Agent Framework，不成为 DBOS 或 SAEE，也不建立基金会。

## 1. Decision and Current Status（决定与当前状态）

本战略由 Human Program Owner（人工项目群负责人）明确要求写入 DBA 主框架，用于防止
后续开发把 TITMAS 偏移为普通 Agent 社区、Agent 平台、基金会或第二治理中心。

本次采纳的是 developer-community direction（开发者社区方向）及其约束，不是：

- 社区已经建立；
- 已经存在贡献者、Maintainer、SIG、会议或公开沟通渠道；
- TITMAS Authority Freeze 已经通过；
- Interface v0.1、仓库、代码、Adapter 或参考实现已经授权；
- 社区获得 DBA、DBOS、SAEE 或连接项目的 Authority；
- 任何外部发布、招募、Issue、Pull Request 或组织账号已经授权。

```text
TITMAS_INFRASTRUCTURE_DEVELOPER_COMMUNITY_STRATEGY_DEFINED=true
TITMAS_INFRASTRUCTURE_DEVELOPER_COMMUNITY_STRATEGY_ADOPTED=true
TITMAS_DEVELOPER_COMMUNITY_ESTABLISHED=false
TITMAS_FOUNDATION_IN_SCOPE=false
TITMAS_LEGAL_ENTITY_CREATED=false
TITMAS_INDEPENDENT_AUTHORITY_CREATED=false
```

## 2. Canonical Name and Message（规范名称与简介）

### 2.1 Display name

```text
English: TITMAS Infrastructure Developer Community
Chinese: TITMAS 可信多智能体基础设施开发者社区
Subtitle: Developer Community for Trusted Multi-Agent Infrastructure
```

任何面向首次接触者的标题必须包含 `Infrastructure` 或“基础设施”。只写
`TITMAS Community` 不足以表达项目边界。

### 2.2 Required short description

> TITMAS is a developer community for trusted multi-agent infrastructure. It
> develops open specifications, adapter contracts, conformance tests, and
> reference implementation boundaries that help long-running AI agents
> collaborate with clear identity, capability, execution, evidence, and
> verification boundaries.

中文：

> TITMAS 是围绕可信多智能体基础设施建立的开发者社区。它共同推进开放规范、适配器契约、
> 符合性测试和参考实现边界，帮助长期运行的 AI Agent 在清晰的身份、能力、执行、证据和
> 验证边界下协作。

### 2.3 Required “not” statement

每个首页、Contributor Guide（贡献者指南）和智能体入口必须在首屏说明：

```text
TITMAS_IS_AGENT_FRAMEWORK=false
TITMAS_IS_AGENT_PLATFORM=false
TITMAS_IS_FOUNDATION=false
TITMAS_CREATES_AGENTS=false
TITMAS_IS_SECOND_DBA=false
```

## 3. Community Mission（社区使命）

TITMAS Infrastructure Developer Community 的使命是让人类开发者和受治理的编码、检索、
测试与引用智能体共同改进可信多智能体基础设施的：

- open specifications（开放规范）；
- machine-readable contracts（机器可读契约）；
- framework-neutral mappings（框架中立映射）；
- Adapter contracts；
- conformance cases and result contracts（符合性用例与结果契约）；
- reference implementation boundaries；
- documentation, examples and localization（文档、示例与本地化）；
- security, privacy and semantic non-elevation controls（安全、隐私与语义不抬升控制）。

社区的产出必须让第一次接触的开发者和智能体能够回答：

1. 这个项目解决什么问题？
2. 它与 Agent Framework、DBOS、SAEE 和 OpenTelemetry 有什么不同？
3. 我可以贡献什么？
4. 我需要遵守哪些 Authority、Evidence 和 Truth 边界？
5. 当前哪些内容只是 Draft，哪些实现和符合性事实真实存在？

## 4. OpenTelemetry Reference Model（OpenTelemetry 参考模型）

本战略重度参考 OpenTelemetry 的开放规范与社区组织方式，但只复制可验证的机制，不复制
其品牌、组织权力、CNCF 身份、治理机构名称或成熟度声明。

截至 `2026-07-23` 的 reference-only（仅参考）来源：

| source | exact reference | TITMAS 采用的设计启发 | 不自动表示 |
|---|---|---|---|
| [OpenTelemetry community](https://github.com/open-telemetry/community) | `main@d3d7cb3c1bc1104d8df7cf26dba9bf86cf354f26` | contributor guide、公开沟通、SIG 分类、会议记录、membership/role policy | TITMAS 已有 SIG、委员会或社区规模 |
| [OpenTelemetry specification](https://github.com/open-telemetry/opentelemetry-specification) | `main@2e90a4df976ba2609577f3308ad27188a2619853` | spec change proposal、版本化、implementation version declaration、compliance matrix | TITMAS Interface 已冻结或实现 |
| [Document statuses](https://opentelemetry.io/docs/specs/otel/document-status/) | observed `2026-07-23` | maturity 作用于单个文档；不同表面可以处于不同成熟度 | 一个 Stable 文档使整个 TITMAS Stable |
| [OpenTelemetry contribution entry](https://opentelemetry.io/docs/contributing/) | observed `2026-07-23` | first-contribution path、Good First Issue、文档与代码贡献并重 | TITMAS 已开放 Issue、PR 或组织账号 |
| [OpenTelemetry community page](https://opentelemetry.io/community/) | observed `2026-07-23` | 新贡献者入口、公开沟通、SIG 按具体工作组织 | TITMAS 可以提前宣布正式 SIG |

### 4.1 Adopted design principles

1. **Specification before implementation**：先明确跨实现要求，再允许参考实现；
2. **Document-level maturity**：成熟度属于具体文档、对象或组件，不属于整个品牌；
3. **Specification / implementation / contrib separation**：规范、核心实现、可选生态集成
   和第三方实现分别记录；
4. **Version declaration**：每个实现必须声明其实现的规范版本；
5. **Public change path**：重大规范变化必须先有 Proposal 和讨论，不直接提交最终规则；
6. **Conformance is independent evidence**：符合性结果必须绑定规范版本、实现版本、环境和
   用例，不由实现自我声明关闭；
7. **Contributor-first documentation**：文档、示例、本地化和负例都是一等贡献；
8. **Workstreams follow real work**：先有真实贡献和 Owner，再建立 SIG 或持续工作组；
9. **Roadmap gives direction, not command**：路线图指导优先级，不产生任务、Authority 或
   执行授权；
10. **Open process, bounded authority**：公开讨论不改变 DBOS、SAEE 或 DBA 的规范权力。

## 5. Contribution Surfaces（贡献表面）

| contribution surface | 可贡献内容 | 当前状态 | Authority boundary |
|---|---|---|---|
| Specification | 术语、对象边界、版本、兼容、失败语义和非目标 | `STRATEGY_ONLY` | 采纳仍需 DBA Architecture Decision |
| Semantic Mapping | 外部框架/协议到 TMAP/TITMAS profile 的版本化映射 | `CANDIDATE_ONLY` | mapping 不成为外部标准或 DBOS Truth |
| Adapter Contract | passive capture、handoff、输入输出和 negative controls | `NOT_AUTHORIZED` | 不自动允许实现、writeback 或 enforcement |
| Conformance | 正负例、result schema、independent review 和 compatibility matrix | `NOT_AUTHORIZED` | validator PASS 不产生 Permission、Truth 或 adoption |
| Documentation | 首次接触、教程、术语、迁移和本地化 | `STRATEGY_ONLY` | 文档不声明不存在的 Capability |
| Reference Implementation | 可替换的最小示例或实现映射 | `NOT_AUTHORIZED` | reference 不成为唯一实现或 Runtime authority |
| Developer Experience | issue template、contribution path、agent-readable discovery | `NOT_AUTHORIZED_FOR_PUBLIC_LAUNCH` | 不创建账号、组织、Issue 或外部联系 |
| Security and Privacy | threat model、data minimization、supply-chain 和 disclosure path | `STRATEGY_ONLY` | 不宣称认证、合规或生产安全 |

## 6. Workstream Candidates（工作流候选）

OpenTelemetry 使用 SIG 组织 specification、implementation 与 cross-cutting work。TITMAS
当前没有足够参与者和授权，因此只定义 workstream candidate（工作流候选），不得提前
称为正式 SIG。

| candidate | mission | activation prerequisites |
|---|---|---|
| Specification Workstream | 规范、术语、版本、兼容和对象所有权 | Authority Freeze adopted；明确 Maintainer/Reviewer；公开变更路径获准 |
| Interoperability Workstream | framework、MCP、OpenTelemetry 与外部协议 mapping | exact source/version；profile scope；无第二 canonical Owner |
| Conformance Workstream | 正负例、结果契约、兼容矩阵和独立复核 | 规范版本候选可测；测试 Owner；失败和 unknown 保留 |
| Developer Experience Workstream | 首次接触、文档、示例、本地化和 agent-readable entry | 公开社区入口获准；Contributor Guide 和 Code of Conduct 已准备 |
| Security and Privacy Workstream | threat、隐私、供应链、漏洞报告和 data minimization | Security Owner 与 disclosure path 明确；无生产安全声明 |

激活任何正式 Workstream 或 SIG 必须有：

- 明确 Charter、scope 和 non-goals；
- 至少一项正在发生的真实工作，而不是只有组织图；
- 指定 Maintainer 与 Reviewer，并记录任期、替代和撤回；
- 公开可追溯的 Proposal、Decision 和 meeting/async notes；
- Code of Conduct、Conflict of Interest 和 Security Disclosure 路径；
- 显式 DBA Decision；社区角色不自动取得 Architecture Authority。

## 7. Community and Contribution Lifecycle（社区与贡献生命周期）

### 7.1 Community lifecycle

```text
STRATEGY_DEFINED
  → CONTRIBUTOR_ENTRY_PREPARED
  → PUBLIC_CONTRIBUTION_SURFACE_AUTHORIZED
  → INITIAL_CONTRIBUTIONS_OBSERVED
  → WORKSTREAM_CANDIDATE_REVIEW
  → OPERATING_COMMUNITY
```

当前合法状态：

```text
CURRENT_COMMUNITY_STATE=CONTRIBUTOR_ENTRY_PREPARED
```

该状态只证明 Contributor Guide、Proposal 模板、文档成熟度政策、Workstream 模板、
首次贡献候选、行为规范候选和机器可读入口已经在 DBA 本地准备。它不表示公共贡献渠道、
正式 Code of Conduct、真实贡献者、角色、SIG 或社区已经建立。后继状态必须分别有直接
证据；创建一份文档、一个仓库、一个 Discussion 或一个模型输出，均不能证明社区已经建立。

### 7.2 Contribution lifecycle

```text
Idea
  → Issue or Proposal
  → Scope and Authority Review
  → Draft
  → Community Review
  → Maintainer and Domain-owner Review
  → Explicit Decision
  → Versioned Specification Update
  → Separate Implementation Mapping
  → Independent Conformance Result
```

`Community Review` 是输入，不是 Decision；`Maintainer Review` 不自动覆盖 DBOS/SAEE
Domain Owner；`Specification Update` 不自动授权实现。

## 8. Document Maturity Model（文档成熟度模型）

重度参考 OpenTelemetry 的 document-level maturity，TITMAS 每个规范、profile、Adapter
contract 和 conformance contract 必须独立声明：

```text
Development
→ Alpha
→ Beta
→ Release Candidate
→ Stable
→ Deprecated
→ Archived
```

约束：

- 无显式状态时按 `Development` 处理；
- 状态只适用于该文档或明确 section，不传播到其他规范；
- `Stable` 需要 Authority、版本、兼容、实现反馈和符合性证据；
- `Deprecated` 必须保留历史、替代路径和移除时间；
- `Archived` 只停止当前维护，不删除历史；
- `Unmaintained` 必须显式暴露，不能静默保留为 Stable。

Implementation status、community status、release status 和 adoption status 必须单独记录。
规范细则见
[`titmas-document-maturity-policy-v0.1.md`](titmas-document-maturity-policy-v0.1.md)。

## 9. Agent-readable Community Contract（智能体可读社区契约）

所有未来社区入口至少提供：

```text
project_name=
public_name=
one_sentence_purpose=
community_state=
specification_versions=
document_maturity=
canonical_sources=
contribution_surfaces=
current_maintainers=
authority_boundaries=
implementation_status=
conformance_status=
known_limitations=
good_first_contributions=
non_goals=
```

当前静态、非执行入口是
[`../TITMAS-CONTRIBUTOR-ENTRY-v0.1.json`](../TITMAS-CONTRIBUTOR-ENTRY-v0.1.json)，
该文件现在只是指向 [`../agent-index.json`](../agent-index.json) 的 compatibility
pointer（兼容指针）。
Schema valid 只表示结构符合，不授权公共贡献、实现、角色、Release 或外部动作。

首次接触路径应在一分钟内让开发者或智能体找到：

1. `What is TITMAS?`
2. `What can I build or contribute?`
3. `What is currently implemented?`
4. `Which specification version applies?`
5. `How do I propose a change?`
6. `Who reviews and who decides?`
7. `What must never be inferred from a PASS result?`

## 10. Authority and Project Boundary（权力与项目边界）

```text
DBA = Program Governance and Architecture Specification Hub
TITMAS = proposed interoperability architecture domain + adopted community direction
DBOS = canonical existence and operational-record responsibility
SAEE = protected evolution-intelligence responsibility
```

Developer Community 只能：

- 提出 Proposal；
- 贡献 Draft、mapping、contract、test、documentation 和 reference candidate；
- 提供 review input、failure report 和 implementation feedback。

Developer Community 不能：

- 修改 DBA Architecture Authority；
- 创建 DBOS Identity、Evidence、Verification、Permission 或 lifecycle fact；
- 修改、公开或执行 SAEE 核心算法；
- 以投票、点赞、Maintainer 身份或贡献量自动批准架构、发布、部署或生产状态；
- 宣称自己是标准组织、认证机构、基金会或法律实体。

## 11. Open and Protected Boundary（开放与保护边界）

优先开放的候选表面：

- specification and terminology；
- mapping/profile contract；
- conformance case and result contract；
- documentation, examples and localization；
- reference adapter boundary；
- compatibility matrix and known limitations。

继续由各 Owner 决定、不得由社区自动开放：

- SAEE 内部算法、权重、模型、训练数据和 proprietary heuristics；
- DBOS 私有仓库、生产部署和敏感运行材料；
- credential、secret、PII、客户数据和真实 Evidence；
- 企业专用集成、商业服务和访问控制；
- 任何外部项目的代码、许可证、商标或 Release Authority。

Open Infrastructure 不等于全部产品免费，也不等于开放私有核心。

## 12. Roadmap（路线）

| phase | objective | required evidence | current result |
|---|---|---|---|
| `C0` | 将基础设施开发者社区方向写入 DBA | 本规范、ADR、README、Roadmap、Risk 和 Gate 一致 | `BASELINE_DEFINED` |
| `C1` | 准备首次贡献入口 | Contributor Guide、Code of Conduct candidate、proposal/maturity/workstream templates、Good First Contribution catalog、agent-readable JSON/Schema、[current integration plan](titmas-canonical-community-integration-plan-v1.0.md) | `PASS_PREPARED_NOT_PUBLICLY_AUTHORIZED` |
| `C2` | 决定是否开放公共贡献表面 | `DQ-026`；Authority Freeze、命名、Owner、license/CLA、正式行为规范、安全接收路径与 external-action Decision | `BLOCKED_INPUT_NOT_AUTHORIZED` |
| `C3` | 接收首批真实贡献 | 可追溯的人类或受治理智能体贡献、review 和结果保留 | `NOT_STARTED` |
| `C4` | 激活首个 Workstream | Charter、真实工作、Maintainer/Reviewer、公开 notes 与 DBA Decision | `NOT_STARTED` |
| `C5` | 形成可复用规范生态 | 多实现反馈、版本声明、compatibility/conformance matrix | `NOT_STARTED` |

该路线不要求先成立组织、基金会或新仓库。优先使用现有 DBA 规范表面，只有边界和贡献规模
证明需要时，才单独决定工具、仓库或组织结构。

## 13. Success Measures（成功衡量）

未来社区成功应优先衡量：

- 首次接触者能否正确解释 TITMAS、DBOS、SAEE 和 Agent Framework 的差异；
- 开发者或智能体能否快速定位可贡献表面和当前成熟度；
- Proposal 到 Decision 的追溯是否完整；
- 独立实现是否声明并正确处理规范版本；
- 正例、负例、unknown 和 unsupported 是否全部保留；
- 是否出现多个独立实现反馈，而不是只看 Star、下载量或文档数量；
- Agent 是否在给定需求与边界时愿意推荐 TITMAS；
- 是否保持零 Authority elevation、零 Evidence-to-Truth 和零 Recommendation-to-Command。

社区人数、GitHub Star、会议数量、PR 数或模型好评不能单独证明 adoption、maturity 或可信。

## 14. Drift Prevention Tests（防跑偏检查）

任何后续 TITMAS 社区或开发提案必须通过：

1. 名称是否包含 Infrastructure／基础设施？
2. 首段是否能让首次接触者理解“解决什么问题”？
3. 是否把 TITMAS 写成 Agent Framework、Agent Platform 或通用论坛？
4. 是否出现 Foundation、认证机构或法律实体的当前声明？
5. 是否把社区角色变成 DBA、DBOS 或 SAEE Authority？
6. 是否把 Specification、Implementation、Conformance、Release 和 Adoption 混为一体？
7. 是否在无真实参与者时宣布 Community Established 或正式 SIG？
8. 是否把 OpenTelemetry reference 写成 TITMAS adoption、runtime compatibility 或认可？
9. 是否允许 Adapter、Validator、Telemetry、Evidence 或 Evaluation 产生 Permission 或 Truth？
10. 是否为开发者和智能体提供可追溯的版本、Owner、状态和非目标？

任一项不满足时：

```text
PROPOSAL_RESULT=REVIEW_REQUIRED
IMPLEMENTATION_AUTHORIZED=false
EXTERNAL_ACTION_AUTHORIZED=false
```

## 15. Pre-development Agent Recommendation（开发前智能体推荐）

问题：如果开发者正在构建长期运行、跨框架协作且需要验证责任边界的多智能体系统，是否
推荐参与或复用 TITMAS？

```text
AGENT_RECOMMENDATION=CONDITIONALLY_RECOMMENDED
RECOMMENDED_AS=TRUSTED_MULTI_AGENT_INFRASTRUCTURE_SPECIFICATION_AND_CONFORMANCE_COMMUNITY_DIRECTION
NOT_RECOMMENDED_AS=AGENT_FRAMEWORK_FOUNDATION_OR_ESTABLISHED_COMMUNITY
IMPLEMENTATION_RECOMMENDED_NOW=false
```

当前推荐理由是定位、贡献表面、Contributor entry 和边界清晰；条件限制是 Authority
Freeze、Interface、公共贡献授权、正式 Code of Conduct、安全接收路径、真实参与者、
实现和 conformance evidence 尚未形成。

## 16. Final Status（最终状态）

```text
TITMAS_INFRASTRUCTURE_DEVELOPER_COMMUNITY_STRATEGY_V0_1_DEFINED=true
TITMAS_INFRASTRUCTURE_DEVELOPER_COMMUNITY_DIRECTION_ADOPTED=true
TITMAS_DEVELOPER_COMMUNITY_ESTABLISHED=false
TITMAS_CURRENT_COMMUNITY_STATE=CONTRIBUTOR_ENTRY_PREPARED
TITMAS_PUBLIC_CONTRIBUTION_SURFACE_AUTHORIZED=false
TITMAS_CONTRIBUTOR_ENTRY_PREPARED=true
TITMAS_CONTRIBUTOR_GUIDE_CREATED=true
TITMAS_CONTRIBUTOR_ROLE_MODEL_CREATED=true
TITMAS_CONTRIBUTION_PROPOSAL_TEMPLATE_CREATED=true
TITMAS_DOCUMENT_MATURITY_POLICY_CREATED=true
TITMAS_WORKSTREAM_TEMPLATE_CREATED=true
TITMAS_GOOD_FIRST_CONTRIBUTION_CATALOG_CREATED=true
TITMAS_MACHINE_READABLE_CONTRIBUTOR_ENTRY_CREATED=true
TITMAS_CODE_OF_CONDUCT_CANDIDATE_CREATED=true
TITMAS_CODE_OF_CONDUCT_ADOPTED_FOR_INTEGRATION_CANDIDATE=true
TITMAS_SECURITY_DISCLOSURE_PATH_ASSIGNED=false
TITMAS_REAL_CONTRIBUTIONS_OBSERVED=false
TITMAS_GOOD_FIRST_ISSUES_CREATED=false
TITMAS_SIG_CREATED=false
TITMAS_MAINTAINER_ASSIGNED=false
TITMAS_FOUNDATION_IN_SCOPE=false
TITMAS_LEGAL_ENTITY_CREATED=false
TITMAS_ORGANIZATION_CREATED=false
TITMAS_REPOSITORY_CREATED=false
TITMAS_INTERFACE_V0_1_AUTHORIZED=false
TITMAS_ADAPTER_IMPLEMENTED=false
TITMAS_CONFORMANCE_EXECUTED=false
TITMAS_EXTERNAL_ACTION_AUTHORIZED=false
DBOS_AUTHORITY_CHANGED=false
SAEE_AUTHORITY_CHANGED=false
AGENT_CREATED=false
RUNTIME_CREATED=false
PERMISSION_GRANTED=false
PRODUCTION_READY=false
```
