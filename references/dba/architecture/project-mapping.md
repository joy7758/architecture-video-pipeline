---
spec_id: DBA-PROJECT-MAPPING-0.1
title: Initial Project Role Mapping v0.1
status: declared-architecture-role-registry
source_basis: user-provided-initial-mapping-and-read-only-local-discovery
program_governance_hub_defined: true
changes_project_facts: false
changes_repository_ownership: false
creates_project_relationships: false
---

# Initial Project Role Mapping v0.1（初始项目角色映射 v0.1）

## 1. 记录边界

本文件只登记 architecture role（架构角色），不改变项目事实、仓库归属、依赖关系、实现状态、能力状态、证据状态或权限。`mapped` 只表示“在 v0.1 中按此角色理解”，不表示“已集成”“已验证”“已采用”或“属于某仓库”。

现有 Digital Biosphere Architecture public meaning layer（公共语义层）与本规范的 canonical authority（规范权威）关系尚未完成人工对齐；因此本表不得被用来覆盖既有项目的 canonical terminology（规范术语）或 repository map（仓库映射）。

## 2. 初始映射

| project_id | 项目 | v0.1 架构角色 | 最近责任域 | 事实边界 | 待澄清的重复建设风险 |
|---|---|---|---|---|---|
| `PROJECT-DIGITAL-BIOSPHERE-ARCHITECTURE` | Digital Biosphere Architecture | Program Governance Hub（项目群治理中心）+ Architecture Specification Hub（架构规范中心）+ Architecture Authority Layer（架构权力层） | Program Governance / Architecture Governance / Rules | 驾驶舱管理组合、路线图、状态引用、依赖、决策、gate 与风险；`ADR-020` 指派 `zhangbin` 为 Human Program Owner，但 DBA 仍不是 Runtime、Entity、最终授权主体或执行权来源 | 与既有 public meaning layer 的 canonical reconciliation、其余角色任命、Git topology 和版本发布机制仍待定义 |
| `PROJECT-DBOS` | DBOS | Trusted Digital Entity Existence Infrastructure（可信数字实体存在基础设施）；Digital Biosphere Operating System；Operational Authority（运行权力）；Infrastructure Entity（基础设施实体）的架构角色示例 | Existence Governance / DBOS | DBOS repository 不是 Entity；DBOS 不是 Agent Application 或 Foundation Model；Operational Authority 不等于最终授权权，也不证明 Identity、Execution、Federation 或实体实例已存在 | 与 POP、Token Governor、证据组件的实现边界及未来实体资格需逐项契约化 |
| `PROJECT-SAEE` | SAEE | Evolution Intelligence Layer（演化智能层）；Evolution Engine；Evolution Authority（演化权力）；Evolution Entity（演化实体）的架构角色示例 | Evolution Governance / SAEE | SAEE repository 不是 Entity；Evolution Authority 只覆盖评价，不授予 DBOS 写权、执行权或架构修改权 | Governance Evolution 与 DBOS/Token Governor 的策略生效及未来实体资格需澄清 |
| `ARCH-LAYER-GOVERNANCE-DECISION` | Governance Decision Layer | Decision Authority（决策权力）的 record and state boundary（记录与状态边界） | SAEE 与 DBOS 之间的独立治理边界 | 不是项目实现、DBOS 模块、SAEE 模块、Runtime、Entity 或自动授权主体；`Decision Authority` 标签不定义最终授权者 | 最终 reviewer、decision authority、adoption authority 与职责分离规则尚需定义 |
| `ARCH-LAYER-TITMAS-DISCOVERY-EVOLUTION` | TITMAS Agent-Native Discovery Evolution Layer | 有界问题发现、修复候选、适应度选择、回滚与谱系的逻辑层 | DBA normative policy；补丁路由至既有 canonical owner | 不是新仓库、Runtime、生产执行器、Authority、Truth、Receipt 或 Certification owner；ER-1 只到 Draft PR | 跨仓补丁仍需目标 Owner 审查；ER-2 至 ER-4 无自动激活权 |
| `PROJECT-POP` | POP | Identity-related component（身份相关组件）；既有公共语义中也用于 portable persona interface（可移植人格接口） | DBOS Identity 相邻域 | 本表不声明 POP 是 DBOS 子模块、身份权威或已接入 DBOS | POP persona projection（人格投射）与 DBOS canonical identity（规范身份）的责任分界 |
| `PROJECT-ARO` | ARO / ARO-Audit | Evidence/Audit component（证据/审计组件） | DBOS Evidence/Verification 相邻域 | 本表不声明其采集、验证、审计或回放能力已实现或属于 DBOS | 与 Agent Evidence、DBOS Evidence Collection 的数据所有权和阶段边界 |
| `PROJECT-AGENT-EVIDENCE` | Agent Evidence | Evidence component（证据组件） | Execution-to-evidence handoff（执行到证据交接）相邻域 | Evidence package（证据包）不自动等于 DBOS 验证或 SAEE 评价 | 与 ARO 的审计职责、与 DBOS 的证据采集职责可能重叠 |
| `PROJECT-MEDIA-EVIDENCE` | TITMAS Media Evidence v0.1.0 | 已接纳的 AIGC media-review Application Profile / Reference Implementation candidate（人工智能生成内容媒体审核应用场景配置／参考实现候选） | Application / Media Governance Profile；DBOS Evidence 相邻域 | `MediaEvidenceObject` 已决定为 domain-local evidence-bearing record，不是 DBOS canonical Evidence Object；组合准入、112 项本地测试和公开合成 Demo 不表示 Truth、Identity、Legal Evidence、Production、Conformance 或 Adoption | `ADJACENT_CANDIDATE` 已接纳；private canonical source 和 status contract 已建立；未来 DBOS Evidence Admission mapping 仍须独立授权和实现 |
| `PROJECT-TOKEN-GOVERNOR` | Token Governor | Resource governance component（资源治理组件） | DBOS operational governance（运行治理）相邻域；为 SAEE 提供资源评价输入 | 本表不声明其是 DBOS 内置模块或拥有最终治理权 | 与 DBOS 执行约束、SAEE 资源适应度评价的边界 |
| `PROJECT-RESEARCH-AGENT` | Research Agent | Future Operational Digital Entity（未来运行型数字实体）；第一个 Pilot reference（试验参考） | Digital Entity / Operational | 只是参考规范与 Pilot 设计；没有创建 Agent、Identity、Runtime、Capability、Permission、任务或研究结果 | 接入前需满足 Digital Entity、Capability、授权、Evidence、评价与 Human Oversight 契约 |
| `ARCH-ROLE-DIGITAL-ORGANISM` | Digital Organism | SAEE Evaluation Target（SAEE 评价目标）；高级 Digital Entity qualification state | Evolution Evaluation + DBOS qualification record | 不是项目、Entity 实例、Agent、Runtime、Capability 或权限；SAEE 评价不自动产生资格 | 长期阈值、Lineage、生态范围、暂停与撤销状态机尚需定义 |

`Digital Entity` 在本表中只是角色分类，不是新对象类型。Digital Organism 的资格关系以 [`digital-organism-crosswalk.md`](digital-organism-crosswalk.md) 为准；与 LAU（Life-like Autonomous Unit，类生命自治单元）或其他主体术语的关系仍未完成 canonical terminology reconciliation（规范术语对齐）。

## 3. Commercial Private Infrastructure Strategic Mapping

```text
DBOS_ROLE=TRUSTED_DIGITAL_ENTITY_EXISTENCE_INFRASTRUCTURE
SAEE_ROLE=EVOLUTION_INTELLIGENCE_LAYER
DBA_ROLE=PROGRAM_GOVERNANCE_AND_ARCHITECTURE_SPECIFICATION_HUB
TITMAS_ROLE=COMMERCIAL_PRIVATE_AGENT_INFRASTRUCTURE
PRIVATE_CORE_IS_CANONICAL=true
PUBLIC_INTEROPERABILITY_SURFACES_RETAINED=true
PUBLIC_SURFACE_NE_OPEN_SOURCE_CORE=true
DBA_IS_PROGRAM_COCKPIT=true
DISCOVERY_EVOLUTION_ROLE=LOGICAL_LAYER
DISCOVERY_EVOLUTION_NORMATIVE_OWNER=DBA
DISCOVERY_EVOLUTION_NE_RUNTIME=true
DBOS_GOVERNS_EXISTENCE=true
SAEE_GOVERNS_EVOLUTION=true
DBOS_NE_AGENT_APPLICATION=true
DBOS_NE_FOUNDATION_MODEL=true
DBOS_NE_SAEE=true
```

Research Agent、Medical Agent、Enterprise Agent、Robot Agent 和其他 Industry Agent 默认属于 Application / Digital Entity 生态。只有跨应用复用、契约化且不引入领域 Authority 的能力，才可以申请进入 DBOS core roadmap。

Enterprise Deployment、Industry Solution、Audit、Compliance、Certification 和 Advanced Governance 默认属于商业或 Governance Service Ecosystem。它们可以使用 DBOS，但不能通过客户、收入、listing 或付费关系改写 DBOS/SAEE 边界。

该战略映射以 [`commercial-private-infrastructure-strategy-constitution.md`](commercial-private-infrastructure-strategy-constitution.md) 为当前最高方向约束，不改变任何项目的 capability truth、evidence truth、implementation status、release status、commercial availability、Authority 或 Permission。原开放基础设施宪法仅保留历史效力。

## 4. 接入分类说明

### 4.1 Authority role interpretation

- Digital Biosphere Architecture → Program Governance Hub + Architecture Authority Layer：维护项目组合、路线图、状态引用、依赖、决策队列、gate、风险、规则、ADR 和变更流程；不运行 DBOS，不控制 SAEE 算法，也不覆盖子项目事实；
- DBOS → Operational Authority：管理有界运行与记录，但不能单方面修改架构；
- SAEE → Evolution Authority：形成演化评价与 Recommendation，但不能单方面修改架构；
- Governance Decision → Decision Authority boundary：记录显式 Decision，不自带最终授权者，不执行变化。

这些 Authority 标签是 architecture responsibility（架构责任），不是权限授予、组织任命、账号能力或 Entity 分类。三种权力的详细分离见 [`architecture-authority-model.md`](architecture-authority-model.md)。

### 4.2 POP

POP 可以提供 portable persona object（可移植人格对象）或身份投射语义；DBOS 的架构责任是维护存在治理中的主体身份引用与状态。v0.1 不决定 POP 是否实现、承载或仅适配 DBOS Identity。该关系需要后续 ADR 与接口契约。

### 4.3 ARO 与 Agent Evidence

v0.1 将二者都登记在证据相邻域，但不把二者合并：

- Agent Evidence 更接近 execution-to-evidence handoff（执行到证据交接）；
- ARO / ARO-Audit 更接近 post-execution audit and review（执行后审计与复核）；
- DBOS 保留 Evidence Collection 与 Verification 的架构责任；
- SAEE 只消费并评价相应材料。

具体仓库能力、数据格式与集成状态必须以各自当前证据为准，本映射不能替代仓库审计。

### 4.4 Token Governor

Token Governor 的资源、预算、策略或运行约束记录可以成为 DBOS 运行治理的相邻输入，也可以成为 SAEE 适应度与风险评价的数据来源。它不因此拥有 SAEE 演化算法，也不自动成为 DBOS 状态权威。

### 4.4A Media Evidence

TITMAS Media Evidence v0.1.0 已由人工项目组合决定作为 `ADJACENT_CANDIDATE` 接纳，
分类为 Application Profile 和 Reference Implementation candidate。它可以展示媒体生成、
来源记录、异议、审核决定和离线复核如何组合，但不成为通用 Evidence authority、智能审核
平台或 DBOS 模块。

`MediaEvidenceObject` 已由人工边界决定确认为 domain-local evidence-bearing record。
未来仍须另有明确的 DBOS Evidence Admission 契约、授权和版本映射；任何单方均不能宣布
mapping 成立。项目组合接纳、网站展示和本地测试都不能越过该边界。详见
[`TITMAS-PROP-20260801-MEDIA-EVIDENCE-001`](../TITMAS/specifications/proposals/titmas-media-evidence-profile-admission-v0.1.md)
和
[`TITMAS-MEDIA-EVIDENCE-ADMISSION-BOUNDARY-D01`](../TITMAS/specifications/decisions/titmas-media-evidence-admission-boundary-decision-v0.1.md)。
项目组合决定见
[`TITMAS-DEC-20260801-MEDIA-EVIDENCE-PORTFOLIO-001`](../TITMAS/specifications/decisions/titmas-media-evidence-portfolio-admission-decision-v0.1.md)。

### 4.5 Research Agent

Research Agent 是 Future Operational Digital Entity 和 Operational Entity Example。基础 Purpose、Identity、reference Capability Profile、Evidence Model、SAEE Evaluation 和 Lifecycle 见 [`research-agent-specification.md`](research-agent-specification.md)；第一个 Pilot 的设计边界、研究问题和评价入口分别见 [`research-agent-pilot-specification.md`](research-agent-pilot-specification.md)、[`research-agent-research-plan.md`](research-agent-research-plan.md) 与 [`research-agent-evaluation-framework.md`](research-agent-evaluation-framework.md)。这些模型没有实例化主体，也没有注册身份、创建 Capability、授予 Permission、创建 Runtime、执行研究或产生论文状态。

### 4.6 Digital Organism

Digital Organism 是 SAEE Evaluation Target，而不是 SAEE 创建的 Entity。DBOS 提供 Identity、History、Execution、Evidence 和 Lineage records；SAEE 评价 Adaptation、Fitness 与 Evolution；Governance Decision 决定是否采纳资格变化；DBOS 记录状态。资格不授予 Permission。

### 4.7 Governance Decision Layer

Governance Decision Layer 的角色是 Decision Authority boundary（决策权力边界）：

- 规范 Decision Object 与治理状态转换；
- 记录显式授权主体作出的 Review、Decision 与 Adoption；
- 把已批准且已采纳的变化交回 DBOS lifecycle control；
- 不产生 SAEE Recommendation；
- 不执行 DBOS 状态变化；
- 不成为 DBOS 模块或 SAEE 模块；
- 遵循 Architecture Governance 维护的规则，但不等于完整的 Architecture Authority；
- 不创建 Runtime、Entity、Capability 或权限。

该层不是新的软件项目。表中的登记只为架构检索和责任分离，不声明实现、部署或组织权威已经存在。

### 4.8 Entity classification interpretation

- DBOS → Infrastructure Entity architecture role；
- SAEE → Evolution Entity architecture role；
- Future Research Agent → Operational Entity role。

这些映射只描述架构职责。Repository、Component 或名称不是 Entity 实例；实际对象必须满足 [`digital-entity-specification.md`](digital-entity-specification.md) 的最低要求，并由 DBOS 完成 Registered 与后续状态治理。分类不等于权限，也不改变现有 capability truth 或 evidence truth。

## 5. 映射状态常量

```text
PROJECT_ROLES_RECORDED=true
PROJECT_FACTS_CHANGED=false
PROJECTS_MERGED=false
INTEGRATIONS_IMPLEMENTED=false
RESEARCH_AGENT_CREATED=false
GOVERNANCE_DECISION_LAYER_RECORDED=true
GOVERNANCE_DECISION_RUNTIME_CREATED=false
GOVERNANCE_DECISION_ENTITY_CREATED=false
DBOS_ENTITY_ROLE_CLASS=INFRASTRUCTURE_ENTITY
SAEE_ENTITY_ROLE_CLASS=EVOLUTION_ENTITY
FUTURE_RESEARCH_AGENT_ROLE_CLASS=OPERATIONAL_ENTITY
RESEARCH_AGENT_ROLE=FUTURE_OPERATIONAL_DIGITAL_ENTITY
RESEARCH_AGENT_REFERENCE_CLASS=OPERATIONAL_ENTITY_EXAMPLE
RESEARCH_AGENT_SPECIFICATION_DEFINED=true
RESEARCH_AGENT_PILOT_SPECIFICATION_DEFINED=true
RESEARCH_AGENT_PILOT_IMPLEMENTED=false
RESEARCH_AGENT_PILOT_EXECUTED=false
DIGITAL_ORGANISM_ROLE=SAEE_EVALUATION_TARGET
DIGITAL_ORGANISM_INSTANCE_CREATED=false
DIGITAL_ENTITY_INSTANCE_CREATED=false
CANONICAL_RECONCILIATION_COMPLETE=false
ARCHITECTURE_AUTHORITY_LAYER_RECORDED=true
ARCHITECTURE_AUTHORITY_ASSIGNED=false
PROGRAM_GOVERNANCE_HUB_RECORDED=true
PROGRAM_GOVERNANCE_COCKPIT_DEFINED=true
PROGRAM_AUTHORITY_ASSIGNED=true
PROGRAM_OWNER_REF=zhangbin
PROGRAM_OWNER_ASSIGNMENT_REFERENCE=ADR-020
PROGRAM_STATUS_CHANGES_PROJECT_FACTS=false
DBOS_AUTHORITY_ROLE=OPERATIONAL_AUTHORITY
SAEE_AUTHORITY_ROLE=EVOLUTION_AUTHORITY
GOVERNANCE_DECISION_ROLE=DECISION_AUTHORITY_BOUNDARY
AUTHORITY_ROLE_GRANTS_PERMISSION=false
DBOS_STRATEGIC_ROLE=TRUSTED_DIGITAL_ENTITY_EXISTENCE_INFRASTRUCTURE
SAEE_STRATEGIC_ROLE=EVOLUTION_INTELLIGENCE_LAYER
DBOS_NE_AGENT_APPLICATION=true
DBOS_NE_FOUNDATION_MODEL=true
TITMAS_CURRENT_STRATEGY=COMMERCIAL_PRIVATE_AGENT_INFRASTRUCTURE
PRIVATE_CORE_IS_CANONICAL=true
PUBLIC_INTEROPERABILITY_SURFACES_RETAINED=true
PUBLIC_SURFACE_NE_OPEN_SOURCE_CORE=true
HISTORICAL_OPEN_INFRASTRUCTURE_STRATEGY_AUTHORITY_EFFECT=NONE
MEDIA_EVIDENCE_PORTFOLIO_ADMISSION_GRANTED=true
MEDIA_EVIDENCE_PORTFOLIO_CLASSIFICATION=ADJACENT_CANDIDATE
MEDIA_EVIDENCE_DBOS_MAPPING_AUTHORIZED=false
MEDIA_EVIDENCE_CORE_COMPONENT=false
MEDIA_EVIDENCE_STANDARD=false
MEDIA_EVIDENCE_PRODUCTION_READY=false
```
