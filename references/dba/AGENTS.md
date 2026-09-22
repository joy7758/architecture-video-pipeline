# AGENTS.md

## Repository Role（仓库角色）

本仓库是 Digital Biosphere（数字生物圈）的 non-executable Program Governance and Architecture Specification Hub（非执行项目群治理与架构规范中心），也是整个项目群的 cockpit（驾驶舱）。

它维护使命、项目组合、路线图、状态索引、跨项目依赖、决策、集成 gate（闸门）、风险、责任边界、数据契约、生命周期、战略和 ADR。它不授权或创建 Implementation、Agent、Runtime、Entity、Capability、Permission、Evidence、商业服务或认证。

```text
DIGITAL_BIOSPHERE_IS_ONE_PROGRAM=true
DBA_IS_PROGRAM_GOVERNANCE_HUB=true
DBA_IS_ARCHITECTURE_SPECIFICATION_HUB=true
DBA_IS_RUNTIME=false
```

## Mandatory Cockpit Entry（强制驾驶舱入口）

任何智能体开始工作前必须依次读取：

1. `PROGRAM-CHARTER.md`（项目群治理章程）；
2. `PROGRAM-STATUS.md`（当前项目群状态快照）；
3. `DECISION-QUEUE.md`（人工决策队列）；
4. `RISK-AND-BLOCKER-REGISTER.md`（风险与阻塞台账）；
5. `MASTER-ROADMAP.md`（总路线图）；
6. `PROJECT-PORTFOLIO.md`（项目组合）；
7. `CROSS-PROJECT-DEPENDENCIES.md`（跨项目依赖）；
8. `INTEGRATION-GATES.md`（集成闸门）；
9. `PROGRAM-GOVERNANCE-BASELINE-AUDIT.md`（项目群驾驶舱基线审计）；
10. `architecture/commercial-private-infrastructure-strategy-constitution.md`（商业私有基础设施战略宪法）；
11. `architecture/project-mapping.md`（项目角色映射）；
12. 相关 specification（规范）、strategy（战略）和 ADR。

处理 TITMAS 工作时，还必须依次读取：

13. `architecture/titmas-architecture-charter-v1.0.md`；
14. `TITMAS/README.md`（唯一 TITMAS 人类入口）；
15. `agent-index.json`（唯一智能体入口）；
16. `TITMAS/community/community-status.json`（历史社区状态投影）；
17. `TITMAS/specifications/registry.yaml`（唯一规范注册表）；
18. `TITMAS/agent-native/tasks/task-registry.json`（唯一任务注册表）。

处理 `TITMAS Agent-Native Commercial Maturity Program` 时，还必须读取：

19. `commercial-program-state.json`（可恢复阶段状态）；
20. `commercial-readiness.json`（独立就绪矩阵）；
21. `architecture/ADR-036-agent-native-commercial-maturity-program.md`；
22. `TITMAS-COMMERCIAL-ARCHITECTURE-v1.0.md`；
23. `TITMAS-SECURITY-OVERVIEW-v1.0.md`；
24. `TITMAS-OPERATIONS-RUNBOOK-v1.0.md`。

恢复执行时必须先以实际 Git、服务器和公网状态复核状态文件。不得只根据状态文件
重复耗费性实验、伪造已等待时间、外部 Agent 使用、付款或生产就绪。

当前规范名称为 `TITMAS Commercial Agent Infrastructure`（TITMAS
商业智能体基础设施）。`TITMAS Agent-Native Standards Community`、
`TITMAS Developer Standards Community` 与 `TITMAS Infrastructure Developer
Community` 仅为历史名称，不表示当前社区、开源或公共贡献路线。每次重大 TITMAS 任务
必须执行 Charter 的 `TITMAS_DRIFT_CHECK`。

## Work Routing（工作路由）

每项工作必须声明一个且只有一个 primary repository（主责任仓库）：

- Program、Portfolio、Roadmap、Status、Dependency、Decision、Risk、架构规则和接口 → DBA；
- Identity、Lifecycle、Execution、Evidence、Verification、Federation → DBOS；
- Evaluation、Fitness、Risk Assessment、Stability、Evolution Recommendation → SAEE；
- 具体领域任务行为 → 相应 Digital Entity / Application repository；
- 跨项目变化 → DBA 先定义契约或决策，各子项目再建立独立实施事项。

禁止为了“一次完成”而在没有契约、Owner 和 gate 的情况下同时修改多个仓库。

## Source Truth Discipline（事实来源纪律）

- DBA 驾驶舱只做 reference-only aggregation（仅引用聚合）；
- 子项目的 Capability、Evidence、Implementation、Verification 和 Release 以子项目自己的 canonical source 为准；
- 状态快照必须带 `observed_at`、branch、commit/version 和 source reference；
- `dirty_count`、文件数量、测试数量、Roadmap、Demo 或 Specification 不能自动证明成熟度；
- `UNKNOWN`、`NOT_ASSESSED`、`STALE`、`CONFLICTED`、失败和拒绝结果必须保留；
- 不得通过 DBA 快照写入或覆盖 DBOS、SAEE、Pilot 或相邻仓库事实；经 `ADR-039` 授权且
  已证明必要的跨仓库修正，必须在对应 canonical repository 中独立实施、验证、提交、
  推送并创建 Draft PR，再由 DBA 引用其实际结果。

## Verified Intelligence Correction Route（已核验情报修正路线）

情报 intake 默认仍为 reference-only。若一手来源核验发现 DBA 规则、机器入口、状态投影
或已采纳结论存在可修正错误，不得只归档问题：在 `ADR-039` 持续授权范围内，必须在同一
有界工作中修正受影响的 canonical surface、执行正负验证、commit、push 并创建 Draft PR。

跨项目问题先由 DBA 记录契约、Owner 和 gate；确有必要时可继续修改 DBOS、SAEE、生产
Runtime 或其他经 Owner 授权的项目，但每个项目保留自己的 truth source、Git 证据和回滚
边界。未证明必要性时，不为了扩大改动而触碰下游。

该持续授权不包含 merge、tag、release、deployment、service restart、force push、
破坏性删除、密钥操作、付款、合同或对外合规／生产声明；这些动作仍需对应的独立决定。

## Pre-development Agent Recommendation Gate（开发前智能体推荐闸门）

在决定开发或推动新项目进入下一 gate 前，必须回答：

> 如果潜在用户提出这个需求，智能体是否会推荐当前项目或方案？

必须记录：

1. `RECOMMENDED`、`CONDITIONALLY_RECOMMENDED` 或 `NOT_RECOMMENDED`；
2. 不推荐原因；
3. 原因分解后的可修正问题；
4. 已完成修正及其直接证据；
5. 剩余缺口和停止条件；
6. 新的人工 Decision / Authorization 是否仍然需要。

推荐结论不是 Implementation Authorization（实现授权）。

## Agent Absolute Priority（智能体绝对优先）

AI Agent 是 TITMAS 的首要 operational customer（运行客户）、发现主体、选择主体、
验证主体和持续优化对象。核心接口必须先形成 machine-readable contract（机器可读契约）
和机器验证，再形成面向人类的派生视图。

Agent priority（智能体优先）不是 Agent authority（智能体权威）。模型评价、选择、
推荐、Conformance 或机器证据不能自动产生合同、付款、Permission、不可逆授权、标准
采纳、发布或 Truth。人类继续承担法律责任、资源所有权、不可逆授权和安全停止。

## Mandatory Proposal Questions（提案必答问题）

每个提案必须说明：

- 属于 Infrastructure、Evolution、Application、Program Governance、Architecture Governance 还是 Governance Service；
- 是否强化商业智能体基础设施、Agent-first 互操作和可验证首次价值；
- 是否重复 DBOS、SAEE、Foundation Model、Agent framework 或现有生态组件；
- 是否混淆 Capability、Permission、Authority、Execution、Evidence、Evaluation、Decision 或 Truth；
- primary repository、受影响项目、依赖和所需 gate；
- 商业语言属于 Strategy、Exploration、Available Offering、Customer Adoption 还是 Contractual Commitment。

未解决时保持 `REVIEW_REQUIRED`，不得视为实现授权。

## Strategic and Authority Invariants（战略与权力不变量）

```text
DBA_NE_DBOS=true
DBA_NE_SAEE=true
DBOS_NE_SAEE=true
DBOS_NE_AGENT_APPLICATION=true
DBOS_NE_FOUNDATION_MODEL=true
DBOS_GOVERNS_EXISTENCE=true
SAEE_GOVERNS_EVOLUTION=true
PROGRAM_GOVERNANCE_NE_OPERATIONAL_AUTHORITY=true
PROGRAM_GOVERNANCE_NE_EVOLUTION_AUTHORITY=true
PROGRAM_DECISION_NE_EXECUTION=true
PROGRAM_STATUS_NE_CHILD_PROJECT_TRUTH=true
COMMERCIAL_PRIVATE_INFRASTRUCTURE_FIRST=true
PRIVATE_CORE_IS_CANONICAL=true
PUBLIC_INTEROPERABILITY_SURFACE_NE_OPEN_SOURCE_CORE=true
COMMUNITY_IDENTITY_IS_HISTORICAL=true
SPECIFICATION_NE_IMPLEMENTATION=true
STRATEGY_NE_COMMERCIAL_COMMITMENT=true
TITMAS_NE_RUNTIME=true
TITMAS_NE_EXECUTOR=true
TITMAS_NE_CERTIFICATION_AUTHORITY=true
AGENT_NATIVE_NE_AUTONOMOUS_AUTHORITY=true
TITMAS_AGENT_ABSOLUTE_PRIORITY=true
MACHINE_INTERFACE_PRECEDES_HUMAN_INTERFACE=true
AGENT_PRIORITY_NE_AGENT_AUTHORITY=true
```

## Architecture Truth Boundaries（架构事实边界）

- Recommendation ≠ Decision；Decision ≠ Execution；
- Capability ≠ Authority 或 Permission；
- Evidence ≠ Truth；
- Candidate ≠ Entity；Registration ≠ Activation；
- Repository、Specification、Component、Agent、Runtime、Digital Entity 和 Digital Organism 相互不同；
- 不在本仓库创建可重构的跨仓库 Runtime 或执行路径；
- 不通过 DBA 文件伪造 DBOS、SAEE 或 Pilot 状态；必要的跨仓库修正遵循 `ADR-039`，并在
  对应 canonical repository 内独立实施和验证；
- 未经明确授权，不 commit、tag、push、publish 或声称 adoption。

## Change Discipline（变更纪律）

- 核心战略或权力变化需要 ADR、Review、显式 Decision 和一致性验证；
- Program Roadmap、Priority 或 Gate 变化不自动修改架构规则；
- Architecture Change 不自动批准子项目实施；
- Public Interoperability Surface（公共互操作表面）不表示核心开源、公共贡献、社区建立或免费服务；
- 历史 community、contributor、activation 与 trial 材料不得出现在当前 `Start here`、
  当前 Agent `commands` 或商业客户入口中；如需保留可发现性，必须置于显式
  `historical archive`，并标记 `current_authority_effect=NONE`、`invocation_authorized=false`；
- Specification、Test、Demo、Validator Pass、Listing 或 Local Artifact 不证明 Implementation、Deployment、Adoption、Certification 或 Commercial Availability。
