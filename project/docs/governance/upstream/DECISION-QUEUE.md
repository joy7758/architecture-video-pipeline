---
document_id: DBA-DECISION-QUEUE-0.1
title: Digital Biosphere Program Decision Queue v0.1
title_zh: 数字生物圈项目群决策队列 v0.1
status: active-decision-register-owner-decisions-recorded
decision_records_created: true
authority_assignments_created: true
last_reviewed: 2026-08-02
---

# Digital Biosphere Program Decision Queue v0.1（数字生物圈项目群决策队列 v0.1）

## 1. Queue Rule（队列规则）

本队列暴露需要人工决定的项目群事项。进入队列不等于批准；Priority（优先级）不等于 Authorization（授权）；关闭事项必须保留结果、理由、范围和 `decided_by_ref`。

合法状态：`OPEN`、`READY_FOR_REVIEW`、`BLOCKED_INPUT`、`DECIDED`、`DEFERRED`、`REJECTED`、`SUPERSEDED`。项目组合准入可使用有界终态 `CLOSED_ACCEPTED_AS_ADJACENT_CANDIDATE`，但该终态只关闭 G0，不关闭 G3-G8。

## 2. Open Decisions（开放决策）

| decision_id | Priority | 决策问题 | 当前状态 | 所需输入 | 决策影响 | 禁止自动推断 |
|---|---|---|---|---|---|---|
| `DQ-002` | `P0` | DBA 是否应成为独立 Git root（Git 根目录），而不是父目录仓库中的子目录？ | `READY_FOR_REVIEW` | 当前本地/远端拓扑、历史保留方案、迁移风险 | 仓库边界、GitHub 根展示、后续自动化和发布 | 允许重写历史、删除父仓库或强制推送 |
| `DQ-003` | `P0` | DBOS、SAEE、Research Agent Pilot 各自哪个文件/manifest 是 canonical status source？ | `OPEN` | 各 Domain Owner 的来源确认、刷新频率、冲突规则 | 驾驶舱状态可信度和后续只读同步 | README、测试数量或 Git dirty 自动等于项目状态 |
| `DQ-004` | `P1` | 第一个跨项目里程碑是否选择 DBOS ↔ SAEE data contract conformance？ | `OPEN` | 字段映射、版本、现有实现审计、正负用例范围 | `M3` 的正式启动与 Owner 分派 | 已存在接口实现或允许直接调用 SAEE |
| `DQ-005` | `P1` | Research Agent Pilot 何时可以进入 Prototype Authorization Review（原型授权审查）？ | `BLOCKED_INPUT` | Human Review、approved sources、independent reviewer decision、protocol freeze | `M5` 是否进入人工授权 | `NOT_READY` 自动升级，或由 DBA 创建 Agent/Runtime |
| `DQ-006` | `P2` | POP、ARO、Agent Evidence、Token Governor、ACP 哪些进入正式 Portfolio？ | `OPEN` | 每个项目的目的、Owner、canonical source、重复能力和接口边界 | 项目组合与依赖范围 | 本地发现、历史关联或相邻角色等于正式准入 |
| `DQ-007` | `P2` | 驾驶舱状态采用人工周期刷新，还是未来建立只读 adapter（适配器）？ | `OPEN` | source contracts、安全边界、维护成本、staleness 需求 | 状态同步机制 | 允许 DBA 写入子仓库或自动改变项目状态 |
| `DQ-008` | `P0` | 当前 Program Governance Cockpit 与既有 Digital Biosphere public meaning layer 的 canonical relationship（规范关系）是什么？ | `READY_FOR_REVIEW` | 两个仓库的使命、受众、当前 URL、历史、重叠文件和迁移/引用方案 | 单一前门、规范优先级和避免双重 DBA 权威 | 当前驾驶舱自动覆盖、删除或合并既有 public meaning layer |
| `TITMAS-AGENT-ACTION-GATE-ADMISSION-D01` | `P1` | 是否将 TITMAS Agent Action Gate 作为有界 `ADJACENT_CANDIDATE` 纳入项目组合？ | `READY_FOR_REVIEW` | public `main@6f1c83b`、PR `#2` merged、两项 contract check PASS、44 tests、Action Gate／6 MCP tool／agent-evidence adapter、真实 sandbox Draft PR `#3`、一次官方 AgentTeams v1.2.0 operator-supervised 本地 smoke 和完整 DBA 项目管理 policy grant；评审时仍须处置 per-Worker MCP ACL、Skill materialization、自治链、DBOS Permission、Runtime enforcement、Gateway 和 audit-record Owner 的重复／映射风险 | 只决定 G0 项目组合准入和后续 G2/G3 审查路线 | implementation merge、CI PASS、validator PASS、advisory agent review、sandbox 外部写入、临时 smoke 或管理授权自动等于准入、持久 AgentTeams、生产就绪、release、比赛提交或采用 |
| `TITMAS-P0-10-POST-D15-DISPOSITION` | `P0` | D15 完成后，是否满足提出一次单层有界修复的条件，或应以诊断额度耗尽结束本轮开发？ | `BLOCKED_INPUT` | D15 脱敏结构诊断；`ROOT_CAUSE_CONFIDENCE`；竞争层排除证据；执行上下文和限制 | 只决定是否提出一个后续有界 remediation decision，或记录 `NOT_ASSESSED_DIAGNOSTIC_LIMIT_REACHED` | D15 自动实施修复、扩大诊断、增加 observability、创建第二个修复 PR 或追加复测 |

## 3. Closed Program Decision（已关闭项目群决策）

| decision_reference | 结果 | 来源 | 效力 |
|---|---|---|---|
| `ADR-016` | `ACCEPTED`：DBA 升级为 Program Governance + Architecture Specification cockpit | 2026-07-21 用户明确目标 | 允许更新 DBA 文档和治理入口；不授权修改 DBOS、SAEE、Pilot、Runtime 或外部状态 |
| `ADR-017` | `ACCEPTED`：进入 Trusted Multi-Agent Infrastructure Developer Preview v0.1 阶段 | 2026-07-21 用户明确目标 | 允许按 DBA / DBOS / Demo / SAEE 责任域推进受限实现；不授权发布、生产 Runtime、自动 Permission 或 Evidence 改写 |
| `ADR-018` | `SUPERSEDED_AS_PRIMARY_BY_ADR-021`：3–5 人 External Developer Trial 保留为可选次级研究 | 2026-07-21 原目标与后继客户模型决定 | 不授权招募、外部联系、试用执行、客户验证或发布 |
| `ADR-019` | `ACCEPTED_AND_EXECUTED`：清理过期云端应用资产并在 `redcrag.cn` 根入口部署双语 TMAI 网站候选 | 2026-07-21 用户明确清理与网站要求 | 只授权公开网站候选及其 GitHub prerelease；不授权 Developer Preview Release、DBOS 公开、SAEE 边界变更或外部试用 |
| `ADR-020 / DQ-001` | `ACCEPTED`：指派 `zhangbin` 为 Human Program Owner | `decided_by_ref=zhangbin`，2026-07-21T22:48:39+08:00 | 项目群决定来源生效，重大 release 时复核；不产生 DBOS 运行权、SAEE 演化权或自动发布权 |
| `ADR-020 / DQ-010` | `SUPERSEDED_FOR_PRIMARY_ROUTE`：原决定为 `AUTHORIZE_AFTER_CLEAN_CLONE_PASS` | Clean Clone 与原技术包仍保留 | 人类试用未执行；不再作为首要发布 gate，也不产生外部联系或协作者权限 |
| `ADR-020 / DQ-011` | `ACCEPTED`：`A_PUBLIC_SAFE_EXTRACTION_EXACT_19_FILES` | `decided_by_ref=zhangbin`、`saee_domain_owner_ref=zhangbin` | 只允许冻结 19 文件及精确 blob；不允许 private core、第二套 evaluator 或正式发布 |
| `ADR-020 / DQ-012` | `ACCEPTED`：DBA、DBOS、SAEE Owner-created public surfaces 采用 `Apache-2.0` | `decided_by_ref=zhangbin` | 允许发布根 `LICENSE`；不重许可第三方材料、数据或依赖 |
| `ADR-019 / DQ-013` | `SUPERSEDED`：不再采用独立子路径问题 | 2026-07-21 Human Owner 清理和网站决定 | `redcrag.cn` 根入口网站候选已执行；不等于 Developer Preview Release |
| `ADR-020 / DQ-014` | `ACCEPTED`：`PRIVATE_COLLABORATOR_TRIAL` | `decided_by_ref=zhangbin` | DBOS 保持 private；不授权 public visibility、具体协作者、Permission 或发布 |
| `ADR-021 / DQ-010` | `SUPERSEDED_FOR_PRIMARY_ROUTE`：人类参与者招募不再是首要客户验证路径 | 2026-07-21 Human Owner 明确核心客户是 AI agent | 不把未执行的人类试用改写成通过；可作为未来次级可用性研究保留 |
| `ADR-021 / DQ-015` | `ACCEPTED_AND_EXECUTED_PASS`：`ADOPT_AGENT_NATIVE_CUSTOMER_VALIDATION` | `decided_by_ref=zhangbin`；`001=CONDITIONAL`、`002=PASS` | 两轮各 12 次会话全部保留；不创建 Agent／Runtime，不授权发布、DBOS 公开或客户采用 |
| `ADR-022 / DQ-016` | `ACCEPTED_EXECUTION_AUTHORIZED`：只公开 exact public-safe wheel，DBOS 整仓保持 private | `decided_by_ref=zhangbin`；`DQ-016=PUBLISH_PUBLIC_SAFE_DBOS_WHEEL`；`WHOLE_DBOS_REPOSITORY_VISIBILITY=KEEP_PRIVATE` | 只授权精确 hash/bytes/source 的 GitHub Release asset；不授权整仓公开、PyPI、Runtime、Permission 或扩大 package 内容 |
| `ADR-022 / B-011` | `ACCEPTED_LIMITATION_FOR_V0_1`：接受 `PARTIAL_METADATA_ONLY` 作为 Developer Preview v0.1 的已披露发现限制 | `OPEN_WEB_LIMITATION=ACCEPT_PARTIAL_METADATA_ONLY_FOR_V0_1`；`decided_by_ref=zhangbin` | 不再阻塞 v0.1；不得写成规范名称或公开网络自然发现已经通过，后续仍可复查 |
| `ADR-022 / DQ-009` | `ACCEPTED_EXECUTION_AUTHORIZED`：批准 `Trusted Multi-Agent Infrastructure Developer Preview v0.1` 正式发布 | `released_by_ref=zhangbin`；2026-07-22T02:59:31+08:00 | 授权 GitHub Release、exact wheel 和百度云 formal deployment；只有执行和外部复验全部通过后才可记录为 `RELEASED` |
| `ADR-023` | `ACCEPTED_EXECUTION_AUTHORIZED`：批准 TITMAS 明亮版公开网站源文件推送和现有承载环境发布 | `decided_by_ref=zhangbin`；2026-07-23 用户明确授权 | 允许发布同一已验证网站版本并保留回滚点；不授权 `titmas.cn` 提前切换、GitHub 组织变更、公开贡献、Agent、Runtime 或 Permission |
| `TITMAS-PRIVATE-CORE-COMMERCIALIZATION-SUPERSESSION-D01` | `ACCEPTED_EXECUTION_AUTHORIZED`：所有核心仓库保持 private，并建立源分类、默认拒绝导出、商业草案和私有智能体客户评估候选 | `decided_by_ref=zhangbin`；2026-07-29 | 废止恢复公开可见性的旧建议并关闭当前公共贡献运行面；保留 PR #41/#42/#45、Welcome Issue #43 与此前公开阶段历史；不授权公开导出、公开镜像、客户访问、真实模型调用、Release 或 Deployment |
| `ADR-035 / TITMAS-AGENT-ABSOLUTE-PRIORITY-CONSTITUTIONAL-CORRECTION-D01` | `ACCEPTED_EXECUTION_AUTHORIZED`：AI Agent 成为 TITMAS 首要运行客户、选择和验证主体；E01 降级为历史可选兼容性观察；进入 Stage 5.7 匿名选择与 ROI 基准 | `decided_by_ref=zhangbin`；2026-07-30 | 允许治理修正、E01 重分类和有界 Stage 5.7 基准；不产生 Agent 自我授权、商业采用、正式标准、生产或人类责任移除 |
| `ADR-036 / TITMAS-AGENT-NATIVE-COMMERCIAL-MATURITY-PROGRAM-D01` | `ACCEPTED_EXECUTION_AUTHORIZED_WITH_HUMAN_GATES`：进入可恢复、Agent-first 商业技术成熟度计划 | `decided_by_ref=zhangbin`；2026-07-30 | 允许现有私有 Gateway 内的可逆多租户、Receipt、计量、账单预览、测试和现有百度云候选部署；不授权真实价格、付款、合同、法律发布、DNS、证书、正式 SLA、客户生产数据、认证或公共收费上线 |
| `ADR-037 / CR01-D02` | `ACCEPTED_DESIGN_ONLY_THEN_SUPERSEDED_BY_D04_CLOSURE`：保持历史 Receipt 不可变并设计异常清单与清洁账本 epoch | `decided_by_ref=zhangbin`；2026-07-31 | 当时只授权设计并要求下一决定为 `CR01-D03`；后续 D04 三次失败与 `ADR-038` 已关闭该实施路线，历史设计不得恢复为当前授权 |
| `ADR-038 / TITMAS-D04-FINAL-CLOSURE-AND-ADOPTION-AUDIT-D01` | `ACCEPTED_AND_EXECUTED_GOVERNANCE_ONLY`：D04 在三次失败后永久关闭；PR #36 关闭未合并；旧账本永久归类为内部实验账本；未来生产账本采用 Paid Beta 后的独立 clean genesis；完成优先采用成熟上游的最终形态审计 | `decided_by_ref=zhangbin`；2026-08-01 | 只授权 DBA 最终处置和只读上游审计；不授权第四次 Canary、PR #36 重开/合并/移植、Gateway 修改、Migration 0005、生产账本、部署、购买、客户数据、付款或生产声明 |
| `ADR-039 / DBA-VERIFIED-CORRECTION-AND-CONTEXT-CONTINUITY-D01` | `ACCEPTED_EXECUTION_AUTHORIZED`：采纳执行上下文结论连续性规则，并持续授权已核验问题的有界修正、测试、commit、push 与 Draft PR | `decided_by_ref=zhangbin`；2026-08-01 | 可在证明必要时修改 DBA、DBOS、SAEE、生产 Runtime 与其他 Owner 授权项目的 canonical repository；不授权 merge、tag、release、deployment、service restart、force push、破坏性删除、密钥／付款／合同动作或合规／生产声明 |
| `TITMAS-MEDIA-EVIDENCE-ADMISSION-D01` | `CLOSED_ACCEPTED_AS_ADJACENT_CANDIDATE`：TITMAS Media Evidence v0.1.0 作为应用场景配置与参考实现候选纳入项目组合 | `TITMAS-DEC-20260801-MEDIA-EVIDENCE-PORTFOLIO-001`；`decided_by_ref=ZHANGBIN`；2026-08-01 | 只关闭 G0 项目组合准入；G1 为事实源通过，G2 仅为边界通过；G3-G8 仍分别保持未评估、未授权、未执行或未发布未采用；不授权 DBOS mapping、实现、标准、核心、生产或采用 |
| `TITMAS-FINAL-FORM-IMPLEMENTATION-D01` | `SUPERSEDED_BY_D16_AFTER_BOUNDED_P0_IMPLEMENTATION`：原广义最终形态实施问题不再是当前开放开发入口 | D03-D13 的有界事实及 D16；2026-08-02 | 已完成的机器事实、API v1、Runtime 对齐、生成式 SDK 和 MCP Adapter 保留；未完成的 Agent-first acceptance 只走 D15 及 D16 限额；不恢复 P1/P2、生产账本、部署、付费或新功能授权 |
| `TITMAS-MAINLINE-CLOSURE-AND-DEVELOPMENT-FREEZE-D16` | `ACCEPTED_GOVERNANCE_FREEZE_ACTIVE`：唯一主线冻结为 Unknown-Agent 完整接入闭环，非阻塞开发暂停 | `decided_by_ref=zhangbin`；2026-08-02 | 允许只读 PR 分类、驾驶舱冻结记录和 D15 最后诊断；不授权代码、merge、PR closure、deployment、release、package publication 或新标准／生产声明 |
| `TITMAS-AGENT-NATIVE-DISCOVERY-SELF-HEALING-AND-EVOLUTION-D19-V2-1` | `ACCEPTED_BOUNDED_EXCEPTION_TO_D16`：允许建立证据驱动的有界自修复与自进化架构、参考实现和 ER-1 Draft PR 演示 | `decided_by_ref=zhangbin`；2026-08-02 | 只允许 self-observation、RCA、最多三变体、隔离实现、测试、适应度、选择、回滚、谱系与 Draft PR；不授权 merge、release、deployment、生产修改、自授权、数据库/API/Schema 语义变化或 P0-10 重开 |
| `ADR-040 / TITMAS-TITMAC-SCOUT-CANONICAL-IDENTITY-AND-COCKPIT-PROGRESS-BRIDGE-D20` | `ACCEPTED_EXECUTION_AUTHORIZED_DRAFT_REVIEW_REQUIRED`：冻结 `titmac-scout` 机器身份、唯一状态合同与 DBA 只读按需桥接 | `decided_by_ref=zhangbin`；2026-08-02 | 允许 private canonical remote、status/schema、source registry、fail-closed projection、测试与最多两个 Draft PR；不授权 PR #105/#106 merge/close、运行、发布、部署、数据库、跨仓写回、P0-10 或 D04 重开 |
| `ADR-040 / TITMAS-TITMAC-SCOUT-CANONICAL-STATUS-ACTIVATION-AND-COCKPIT-REBIND-D21` | `ACCEPTED_EXECUTED_SCOUT_MERGED_DBA_REBIND_READY_FOR_REVIEW`：分离 Scout 静态声明与 GitHub 动态观察，PR #1 已用 merge commit 进入 canonical `main`，DBA PR #107 仅重绑定该 exact source | `decided_by_ref=zhangbin`；2026-08-02 | 授权更新/合并 Scout PR #1 与更新/合并 DBA PR #107；不授权 PR #105/#106 变化、自愈/演化实现迁移、Runtime、数据库、部署、发布、P0-10 或 D04 重开 |
| `ADR-041 / TITMAS-COMMERCIAL-CONSTITUTION-C01-LOW-FRICTION-ENTRY-D29-INTEGRATION` | `ACCEPTED_ARCHITECTURE_FREEZE`：将低门槛进入与渐进式价值冻结为 C-01，并原位约束 D29、四产品组合、Observer 非产品入口及 Human/Agent 双入口 | `decided_by_ref=zhangbin`；2026-08-03 | 允许文档、机器契约、测试、Draft PR 及满足精确闸门后的 merge commit；不授权控制台、网站、Observer/Gate/Health Runtime、数据库、客户、联系、合同、收费、部署、公开内核、owner map/resolver、PR #113 或 D04/P0-10 重开 |
| `TITMAS-D29-SECURITY-FINDINGS-20260812-01` | `EXECUTED_BOUNDED_AND_CLOSED`：授权一次有界 incident/formal rollback；CR-01 以失败保留处置，旧 Ledger 禁止作为未来 D29 launch baseline；`human:zhangbin` 指派为 Support Owner 与 Security Contact | `decided_by_ref=zhangbin`；2026-08-12 | Gateway PR #57/#58 merged；2 个 High closed；0 open Blocker，1 retained disposition；D04 未重开；执行权限已撤销；Backup Owner、独立安全评价及商业 Gate 仍开放 |
| `ADR-042 / TITMAS-COMMERCIAL-PRIVATE-INFRASTRUCTURE-DIRECTION-D30` | `ACCEPTED_STRATEGIC_CORRECTION`：当前身份改为 TITMAS Commercial Agent Infrastructure；私有核心为 canonical；公共 Schema/SDK/MCP/验证资料仅为有界互操作表面；社区、Open Core 与 Developer Ecosystem First 降为历史路线 | `decided_by_ref=zhangbin`；2026-08-04 | 允许 DBA 宪法、当前人类入口、机器入口和历史状态投影同步；不授权核心源码公开、公共贡献、社区重启、License 变化、客户、商业报价、实现、Release 或 Deployment |

## 4. Decision Closure Contract（决策关闭契约）

任何 `DECIDED` 项必须至少记录：

```text
decision_id=
decision_result=accepted|rejected|deferred|superseded
decided_by_ref=
decided_at=
accepted_scope=
rejected_scope=
affected_projects=
required_followups=
execution_authorized=true|false
release_authorized=true|false
```

如果 `decided_by_ref` 缺失，状态必须保持 `OPEN` 或 `BLOCKED_INPUT`。

```text
DECISION_QUEUE_ACTIVE=true
OPEN_DECISIONS=9
CONDITIONALLY_DECIDED_NOT_EFFECTIVE=0
QUEUE_CREATES_AUTHORITY=false
QUEUE_CREATES_PERMISSION=false
QUEUE_EXECUTES_DECISIONS=false
```

## 5. TITMAS Canonical Integration Decision（TITMAS 规范集成决定）

| decision_reference | status | accepted scope | explicitly not authorized |
|---|---|---|---|
| `TITMAS-OPEN-STANDARDS-COMMUNITY-INTEGRATION-D01` | `ACCEPTED_EXECUTION_AUTHORIZED` | branch from latest `origin/main`; selective path port; entry, registry, status and CI repair; candidate Code of Conduct adoption; temporary role records; one bounded internal agent-native contribution cycle; commit, push and Draft PR | merge to `main`; public contribution activation; public launch or announcement; external invitation; tag, release, deployment; Foundation, certification or commercial offer; calibration v0.3; formal Ecology Box execution |
| `TITMAS-COMMUNITY-CYCLE-001-D01` | `ACCEPTED_ONCE` | one deterministic, low-risk integration-branch contribution of no more than five files with exact Qwen and Kimi advisory reviews | authority, security contact or Stable-status changes; DBOS/SAEE changes; Ecology Box execution; merge to `main` |

```text
DECIDED_BY_REF=zhangbin
CG_HD_01=ACCEPT
CG_HD_02=ACCEPT
CG_HD_03=DEFER
CG_HD_04=DEFER
CALIBRATION_SUBTRACK_STATUS=FROZEN_AFTER_DETERMINISTIC_GROUNDING_REMEDIATION
```
