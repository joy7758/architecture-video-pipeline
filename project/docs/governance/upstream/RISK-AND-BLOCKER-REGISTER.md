---
document_id: DBA-RISK-BLOCKER-REGISTER-0.1
title: Digital Biosphere Program Risk and Blocker Register v0.1
title_zh: 数字生物圈项目群风险与阻塞台账 v0.1
status: active-risk-register
as_of_date: 2026-08-02
risk_acceptance_authority_assigned: true
---

# Digital Biosphere Program Risk and Blocker Register v0.1（数字生物圈项目群风险与阻塞台账 v0.1）

## 1. Risk Scale（风险等级）

- `CRITICAL`：可能导致越权、历史破坏、错误发布或不可恢复状态；
- `HIGH`：阻塞核心项目群推进或使驾驶舱失真；
- `MEDIUM`：增加重复建设、漂移或维护成本；
- `LOW`：局部可恢复问题。

风险等级不自动产生停止、授权或风险接受决定。

## 2. Active Risks（当前风险）

| risk_id | level | 风险 | 当前证据 | 缓解措施 | Owner 状态 |
|---|---|---|---|---|---|
| `R-002` | `HIGH` | DBA 本地 Git root 是 `/Users/zhangbin/Documents/New project`，不是 DBA 目录；远端树保留额外目录层 | 2026-07-21 `git rev-parse --show-toplevel` 与已发布远端结构 | 处理 `DQ-002`；在决定前禁止历史重写、删除或 force push | `DECISION_REQUIRED` |
| `R-003` | `HIGH` | 核心项目没有经 DBA 确认的统一 canonical status source | DBOS、SAEE 有多个 README、status、manifest 和证据表面；Pilot 有独立 readiness 状态 | 处理 `DQ-003`，为每项目记录一个规范入口及冲突规则 | `DOMAIN_CONFIRMATION_REQUIRED` |
| `R-004` | `MEDIUM` | 核心项目工作树存在大量当前变化，静态快照容易过期或误读 | 2026-07-21 只读 Git observation | 驾驶舱只记录 commit、branch、时间和状态来源；dirty count 不作为成熟度 | `MITIGATED_BY_POLICY` |
| `R-005` | `HIGH` | DBOS ↔ SAEE 接口曾只有 Specification，容易被误写成已集成 | 2026-07-21 已完成同一 synthetic envelope 的 scoped local conformance；没有生产 Runtime、写回或真实 Evidence | 保留 `SCOPED_LOCAL` 限定；clean clone 与 source release 后再评审更高状态 | `LOCAL_MITIGATION_VALIDATED_NOT_RELEASED` |
| `R-006` | `MEDIUM` | Research Agent Pilot 没有发现 `origin`，且当前 `NOT_READY` | Pilot README、Git observation | 先完成 Human Review 和 source approval；远端决策独立处理 | `PILOT_OWNER_INPUT_REQUIRED` |
| `R-007` | `MEDIUM` | POP、ARO、Agent Evidence、Token Governor 与 DBOS/SAEE 存在潜在重复责任 | DBA project mapping 与本地候选发现 | 逐项目执行 Portfolio Admission 和 duplicate capability review | `REVIEW_REQUIRED` |
| `R-008` | `MEDIUM` | 静态驾驶舱可能把旧观察继续展示为当前事实 | 当前没有 refresh cadence 或只读 adapter | 每个快照必须带 `observed_at`；过期标记 `STALE`；处理 `DQ-007` | `POLICY_DEFINED_IMPLEMENTATION_PENDING` |
| `R-009` | `HIGH` | Program Governance 被误读为 DBOS/SAEE 执行或代码控制权 | 用户原始管理意图与现有 authority model 的语义张力 | 在 Charter、Program Governance Spec 和 AGENTS 中固定权力分离 | `MITIGATED_BY_SPECIFICATION` |
| `R-010` | `HIGH` | 当前 Program Governance Cockpit 与既有 DBA public meaning layer 可能形成双重 DBA 入口和规范漂移 | README canonicality、project mapping 与既有独立公开仓库 | 处理 `DQ-008`；决定单一前门、交叉引用、迁移或长期分工，决定前不得声称已完成 canonical reconciliation | `DECISION_REQUIRED` |
| `R-011` | `HIGH` | DBOS 当前文档演化与 `DBOS-EXP-0001` 冻结 identity evidence 的校验语义冲突 | Version-aware historical binding 已实现；旧 digest 未改写；34/34 validators 通过并对当前漂移发 warning | source 隔离与 clean-clone 回归后再决定是否正式关闭 | `LOCAL_MITIGATION_VALIDATED_NOT_RELEASED` |
| `R-012` | `MEDIUM` | DBOS 默认顶层测试曾发现 0 tests，开发者可能误读结果 | `tools/run_tests.py` 现在逐目录运行且零测试失败；`main@cd3f867` 为 334/334 tests；wheel 不再安装误导性的仓库测试命令 | 发布时区分源码测试入口与已安装 wheel 的 validation smoke，并保留分发负例 | `MITIGATED_REMOTE_MAIN_VALIDATED_NOT_RELEASED` |
| `R-014` | `HIGH` | 3–5 人小样本、个别正面反馈或试用 PASS 可能被过度解释为客户验证、市场采用或发布授权 | External Developer Trial Plan 明确样本仅验证 onboarding、理解、使用和问题相关性信号 | 预冻结成功阈值；保留失败；Trial Result、Customer Validation、Release、Adoption 分开；发布仍需 `DQ-009` | `MITIGATED_BY_PLAN_NOT_YET_TESTED` |
| `R-015` | `MEDIUM` | 站点完整构建树在 2026-07-30 新通告下报告 9 项 high，均来自 ESLint/minimatch/brace-expansion 开发工具链 | `npm audit --omit=dev` 为 0；45/45 tests、静态构建和机器事实失败关闭检查通过；服务器只部署静态文件，不部署 Node.js 或构建依赖 | 保持静态部署边界；等待兼容的 ESLint/Next 工具链修复；禁止 `npm audit fix --force` 触发破坏性主版本变化或降级 | `MITIGATED_RUNTIME_ZERO_DEV_TOOLCHAIN_RESIDUAL_DISCLOSED` |
| `R-016` | `HIGH` | Agent API 模型的推荐或 `PASS` 被误写成真实客户采用、market fit（市场匹配）或发布授权 | `TMAI-ACV-20260721-001` 是 12 个受控、给定材料的模型会话，不含真实生产调用 | 固定 `Agent Recommendation ≠ Customer Adoption ≠ Release`；保留 Human `released_by_ref` | `MITIGATED_BY_PROTOCOL` |
| `R-017` | `MEDIUM` | 给定 URL 后的机器理解或元数据 description 命中被误写成 open-web discovery（开放网络自然发现） | `TMAI-OWD-20260722-001` 首轮 6 查询无命中；修复后 GitHub 完整新 description 已命中，但规范英文名、中文名和 4 个公开搜索仍无精确命中 | 保留 `OPEN_WEB_DISCOVERY=PARTIAL_METADATA_ONLY`；`ADR-022` 仅为 v0.1 接受该限制，后续继续复查 | `ACCEPTED_LIMITATION_FOR_V0_1_RECHECK_OPEN` |
| `R-018` | `HIGH` | DBOS 保持 private，使 AI agent 能理解 TMAI 但不能自主获取、运行或复用核心存在基础设施 | exact public-safe wheel 已作为 GitHub Release asset 公开并通过匿名 hash 和隔离安装复验 | 整仓继续 private；只使用有界包并保持 Runtime/Permission 非声明 | `MITIGATED_BY_PUBLIC_SAFE_WHEEL_RELEASE_DBOS_PRIVATE` |
| `R-019` | `HIGH` | 直接公开 DBOS 整仓会披露本机路径和未纳入发布的项目资产清单 | `main@cd3f867` 有 48 个跟踪文件包含 `/Users/...`；0 Gitleaks findings 不能消除该 metadata exposure（元数据暴露） | 禁止整仓公开；使用不含 registry/evidence/reports/paths 的 39-file public-safe wheel | `WHOLE_REPOSITORY_PUBLIC_FAIL_CLOSED` |
| `R-024` | `HIGH` | “Agent absolute priority” 被误读为 Agent 可自我授权或替代人类法律责任 | `ADR-035` 将 Agent 设为首要客户和验证主体 | 固定 `AGENT_PRIORITY_NE_AGENT_AUTHORITY`；合同、付款、法律责任、不可逆授权和安全停止继续由人类承担 | `MITIGATED_BY_CONSTITUTIONAL_BOUNDARY` |
| `R-025` | `HIGH` | Stage 5.7 通过品牌提示、事后调分、失败删除或供应商混用人为提高 TITMAS 胜率 | 24 会话已执行；独立 Auditor 对随机化、品牌提示、隐藏答案、hash、失败保留和结果改写全部 PASS | 保留冻结配置、24 份脱敏会话、私有 raw evidence、Manifest 和 Auditor 输出；不得把合成基准升级为采用或生产证据 | `MITIGATED_BY_STAGE5_7_AUDIT_PASS_RESIDUAL_OVERCLAIM_RISK` |
| `R-026` | `CRITICAL` | 多租户 API 发生跨租户读取、写入、配额消耗或 Receipt 访问 | Gateway `c319001…` 已有 application + forced-RLS 测试；2026-08-12 bounded incident/rollback 后使用 app role 完成只读 cross-Tenant negative recheck | 每次对象查询显式 tenant binding；防御纵深；完整负向矩阵；任何新 release/restore 后复验；任一发现立即 `BLOCKED_SECURITY` | `MITIGATED_BOUNDED_RUNTIME_RECHECK_PASS_NOT_CERTIFIED` |
| `R-027` | `HIGH` | 将 Stage 5.8 的 `NOT_ASSESSED`、替换率失败或 12 个未知改写成组合成功 | Gateway `dee6c286...` 保留完整聚合与报告 | DBA 只做 source-pinned 投影；禁止为改善结果重复执行；商业架构记录限制 | `MITIGATED_BY_RETAINED_SOURCE` |
| `R-028` | `CRITICAL` | Receipt 被伪造、链被篡改或被宣传成 Truth/Authorization/Certification | CR-01 保留 1,661 条历史 Receipt，其中 1,659 签名有效、2 条无法验证、0 链失败；D04 三次 Canary 均失败并已永久关闭 | 旧账本永久归类为内部实验账本；不得删除、重签、allowlist、升级或迁移；未来生产账本只允许 Paid Beta 后独立 clean genesis | `MITIGATED_BY_FAILED_RETAINED_CLOSURE_PRODUCTION_LEDGER_NOT_CREATED` |
| `R-029` | `HIGH` | 幂等重试导致重复使用量或账单计数 | Usage/Billing Ledger 和事务/idempotency tests 已实现；2026-08-12 rollback 后完成只读 duplicate、Quota 和 Billing-binding 检查，CR-01 全量 reconciliation 仍未执行 | tenant-operation-idempotency 唯一约束和原子事务；保留补偿记录；每次恢复后重新对账 | `MITIGATED_BOUNDED_RECHECK_PASS_CR01_FULL_RECONCILIATION_NOT_EXECUTED` |
| `R-030` | `HIGH` | 原始客户对象、Token、Provider Key 或签名私钥进入数据库、日志或模型 | 商业 PostgreSQL 候选已部署；实现、备份 allowlist 和 disclosure scans 未发现持久化 raw payload 或 secret | 继续默认不持久化 payload；结构化 allowlist 日志；secret scan；停止条件 | `MITIGATED_IMPLEMENTATION_CONTINUOUS_RECHECK_REQUIRED` |
| `R-031` | `HIGH` | 技术候选被误写成价格、付款、生产或成熟商业采用 | 所有 readiness 状态均为 false，付款与采用计数为 0 | 独立 machine state；Human gates；真实时间和外部采用不可伪造 | `MITIGATED_BY_STATE_MACHINE` |
| `R-032` | `HIGH` | 模型或工件名称未变化时，Harness、提示、安全策略、网络、沙箱、凭据、工具、协议、Runtime、执行风格、监控或停止机制变化，旧信任／安全／可靠性／就绪结论仍被静默继承 | 2026-08-01 Execution-Context Trust Invalidation Profile；2026-08-15 Anthropic Session、AWS dual revision 与 OpenTelemetry evidence-origin 一手来源交叉映射；2026-08-16 IBM Runtime migration、AWS approved revision 与 MCP tool-list claim-scoped 参考夹具 | `ADR-039` 要求 gate 绑定 execution-context manifest；Agent declared version 与 effective Session state 分开；Registry latest／approved／bound revision 分开；observation origin 与 signer／accountability 分开；只有 Claim 实际依赖的维度变化才路由重评；缺失或变化时 fail closed，不得自动保留 `PASS`；Agent Baseline Check 仍因 D16 冻结为未实现候选 | `MITIGATED_BY_GOVERNANCE_PROFILE_AND_REFERENCE_CASES_CANDIDATE_IMPLEMENTATION_DEFERRED_BY_D16` |
| `R-033` | `CRITICAL` | 217 个开放 PR、持续自动清理／性能建议和邻接标准／Demo 扩展掩盖 P0-10 仍未通过，导致“更多代码、仓库或 PR”被误写为 Agent-first readiness | D16 owner-wide PR 快照；唯一主线 PR `titmas-integrations#5` 的 CI 为 SUCCESS，但保留 `P0_10_RESULT=FAIL_CLOSED_AFTER_RUNTIME_ALIGNMENT` | 冻结所有非阻塞开发；只允许 D15 最后诊断、最多一个独立授权的单层修复 PR 和一次最终复测；所有其他 PR 延期 | `MITIGATED_BY_D16_FREEZE_ACTIVE` |
| `R-034` | `HIGH` | `tiamas-scout` 对话标签、`titmac-scout` 机器身份与 D19 DBA Draft 实现混用，可能形成错误远端、重复发现层或双重状态事实源 | D21 已把唯一状态源合并到 private canonical `titmac-scout/main`；旧拼写本地目录仍有并发未提交工作且未触碰 | 冻结 machine ID；旧目录只读保留；DBA exact-main read-only projection；PR #105/#106 在等价证明前保持 Draft | `MITIGATED_CANONICAL_STATUS_ACTIVE_OWNERSHIP_MIGRATION_PENDING` |
| `R-035` | `HIGH` | 驾驶舱把静态声明当作当前 GitHub CI、PR 或 remote Head，或继续展示过期观察，造成虚假绿色进度 | D21 将状态声明与 GitHub API 观察分离；source、remote、CI 与 PR freshness 独立记录，GitHub 观察不可用时 partial fail closed | `SOURCE_STALE`、`SOURCE_DRIFT`、`SOURCE_INVALID`、`SOURCE_UNAVAILABLE` 停止源投影；动态观察缺失/过期返回 `SOURCE_STALE_OR_PARTIALLY_STALE`；不得手工成功覆盖 | `MITIGATED_BY_D21_CANONICAL_DYNAMIC_OBSERVATION_ADAPTER` |
| `R-036` | `CRITICAL` | 自修复或进化能力可能滑向自授 Authority、秘密积累、无限重试、证据删除、语义弱化或生产自我保护 | D19 只定义 DBA 架构与规范合同；执行实现归属 `titmac-scout` 的独立 Draft PR | ER-0 至 ER-4 分级；owner fail-closed；最多三变体、一 PR、有限重试；保留失败/回滚；宪法、人类停止和不可逆授权不可自改 | `MITIGATED_BY_D19_ARCHITECTURE_SCOUT_IMPLEMENTATION_REVIEW_REQUIRED` |
| `R-CM-001` | `CRITICAL` | 历史合成 Receipt 缺少可验证公钥，使结构恢复被误写成完整恢复或通过账本完整性闸门 | 1,661 条已检查、1,659 签名有效、2 条无保留公钥、0 链失败；D04 第三次 Canary 仍失败 | D04 关闭失败并保留；禁止第四次重试及历史修改；旧账本仅供内部开发/研究，生产 clean genesis 延后到 Paid Beta 决策 | `D04_CLOSED_FAILED_RETAINED` |
| `R-CM-002` | `HIGH` | 公开 `/api/v1/readiness` 的粗粒度 `backup_restore_ready=true` 与规范状态 `backup_restore_drill=false` 冲突，可能误导智能体把备份完整性或结构恢复误读为完整恢复 | 2026-07-31 live endpoint 与 DBA `commercial-readiness.json`、CR-01 报告交叉核验 | 若 P0 最终形态实施被另行授权，必须把 backup integrity、structural restore、Receipt integrity、full restore 与 RTO 分开并由证据状态驱动；在授权前不做 status-only 线上修改 | `ACTIVE_FINAL_FORM_CORRECTION_REQUIRED_IMPLEMENTATION_NOT_AUTHORIZED` |
| `R-CM-003` | `HIGH` | 未来生产 signer、算法、不可导出边界和运营责任尚未决定 | D04 不再建设内部 signer/clean ledger；当前 `PRODUCTION_SIGNER_CREATED=false`、`KMS_PURCHASE_AUTHORIZED=false` | 延后到 Paid Beta 前的独立 signer 决策；禁止从旧账本或 PR #36 继承 Key、异常或实现 | `DEFERRED_TO_PAID_BETA_HUMAN_DECISION` |
| `R-CM-004` | `CRITICAL` | 已完成的主要基础设施被误写成 Agent-first acceptance、最终技术候选或生产就绪 | D03-D13 已形成机器事实、API v1、Runtime alignment、SDK 和 MCP；D12 仍为 `FAIL_CLOSED_AFTER_RUNTIME_ALIGNMENT` | D16 冻结唯一 P0-10 接入闭环；保留 readiness 分层，只有 D15 限额、单层修复决策和一次复测可继续 | `MITIGATED_BY_D16_FREEZE_AGENT_ACCEPTANCE_OPEN` |
| `R-CM-005` | `HIGH` | 上游版本、许可证或安全状态随时间变化，使采用矩阵过期 | 15 个项目只按 2026-08-01 官方页面/Release 做点时审计 | 每次引入或升级前刷新 Release、LICENSE、SECURITY/advisory、NOTICE、transitive dependency 和服务条款；法律责任由 Human Owner 承担 | `MITIGATED_BY_REFRESH_GATE` |
| `R-CM-006` | `HIGH` | 过早引入 OpenMeter、OpenFGA、OPA、NATS、Temporal、APISIX 或 OpenBao，导致单机系统运维膨胀和重复建设 | 当前 1 台服务器、并发 10、约 19 RPS、0 付费客户；各项目的运行依赖与触发器已记录 | P2 全部 fail-closed 到量化/结构触发器和单独 Human Decision；禁止把通用组件包装成 TITMAS 核心 | `MITIGATED_BY_TRIGGERED_DEFER_POLICY` |

## 3. Active Blockers（当前阻塞）

| blocker_id | 阻塞事项 | 阻塞范围 | 解除条件 | 不阻塞 |
|---|---|---|---|---|
| `B-002` | DBA Git topology（Git 拓扑）未决定 | 独立仓库根、干净发布结构和后续自动化 | `DQ-002` 选择并执行单独授权的迁移方案 | 当前工作树内的非破坏性文档更新 |
| `B-003` | canonical status source 未确认 | 自动或周期性可信状态汇总 | DBOS、SAEE、Pilot 各自提供 source + freshness + conflict policy | 当前时间点只读 snapshot |
| `B-004` | Research Agent Human Review 与 approved source 不完整 | Prototype Authorization Review 和实验 | Pilot 自己的 readiness gate 达到可审查状态并获得人工决定 | Pilot 规范改进和 DBA 项目群规划 |
| `B-005` | 两个 DBA 语义表面未完成 canonical reconciliation | 对外唯一入口、规范优先级和自动检索路由 | `DQ-008` 形成决定并完成引用/迁移验证 | 当前仓库作为 Program Governance Cockpit 的工作树基线 |
| `B-CM-004` | 生产账本与生产 signer 仅有 clean-genesis 原则，没有 Paid Beta 授权 | 生产 Receipt 权威、真实客户数据、付款、生产恢复和商业长运行 | `PAID_BETA_LAUNCH_AUTHORIZED` 后独立完成 signer、数据保留、合同责任、Genesis、备份恢复和回滚决策 | 已完成的非账本 P0 基础设施事实；不包括 Agent-first acceptance 或新扩展 |
| `B-013` | P0-10 Unknown-Agent 完整接入在 Runtime 对齐后仍 fail closed | Agent-first technical acceptance、新功能恢复和本轮最终形态候选结论 | D15 达到单层高置信根因门槛后完成一次独立授权修复及一次最终复测，或按 D16 记录 `NOT_ASSESSED_DIAGNOSTIC_LIMIT_REACHED`／`FAIL_CLOSED` 终态 | 保留既有机器事实、API v1、SDK、MCP 和历史工件；不授权其扩展 |

## 4. Resolved Risk and Cleared Blockers（已解决风险与已解除阻塞）

| item_id | 原问题 | 解除证据 | 保留边界 |
|---|---|---|---|
| `R-001` | Program Authority 未指派 | `ADR-020` 指派 `zhangbin` 并记录复核、替代和权力边界 | 不产生运行、演化、账号或发布权；重大 release 时复核 |
| `R-013` | 三仓库没有冻结、可引用、可复验的最终远端 source commits | DBA `91928e3`、DBOS `0caa2c4`、SAEE `2173c25`；完整 Clean Clone、331 tests、34 validators、8 Adapter tests 和 19/19 blobs 通过 | 只关闭 source/clean-clone 风险；不产生外部验证或发布授权 |
| `B-001` | 没有已记录的 Program Owner / decision source | `DQ-001` / `ADR-020`，`decided_by_ref=zhangbin` | 每个执行、外部联系和发布动作仍遵循各自 gate |
| `B-007` | 三仓库 source commits 未冻结且跨仓库 Clean Clone 未通过 | `CLEAN-CLONE-VALIDATION-REPORT.md` 后继结果 `PASS` | DBOS 是 authenticated private clone；外部试用仍受 `B-008` 阻塞 |
| `B-008` | 缺少 3–5 名人类开发者或招募渠道 | `ADR-021` 采用 AI agent 为首要客户并完成 12/12 受控模型基线 | 人类试用没有执行、没有被改写成通过；未来仍可作为次级可用性研究 |
| `B-009` | Agent Customer Validation 基线的 exact invocation、composition、positive fit 和 simple-task negative control 未达阈值 | `TMAI-ACV-20260722-002` 用相同阈值复测：12/12 sessions、全部阈值通过；原 `001=CONDITIONAL` 保留 | 只解除 agent-readable packaging blocker；不产生 DBOS 公开、客户采用或发布授权 |
| `B-010` | DBOS 没有已发布的公开 package、API 或面向 AI agent 的受控可调用路径 | `ADR-022`、exact GitHub Release asset、匿名 SHA-256 和隔离安装复验 | 只解除有界 package 获取阻塞；没有公共 Runtime、托管 API、Permission 或整仓公开 |
| `B-011` | 规范名称与公开网络仍未命中 TMAI | `ADR-022` 为 Developer Preview v0.1 显式接受并继续披露 `PARTIAL_METADATA_ONLY` | 只解除 v0.1 发布阻塞；发现事实没有升级，索引刷新后仍需复查 |
| `B-CM-001` | D04 旧账本异常与重试路线长期开放 | `ADR-038`：三次失败全部保留；D04/PR #36 永久关闭；禁止第四次 Canary；旧账本冻结为内部实验账本 | 不是 CR-01 通过；生产账本仍不存在，Paid Beta clean genesis 另行决定 |
| `B-CM-002` | transition-manifest signer 阻塞 D04 内部 clean-ledger 实施 | `ADR-038` 取消 D04 实施路线，不再为内部账本创建或购买 signer | 不表示生产 signer 已解决；该问题转入 Paid Beta 的 `B-CM-004` |
| `B-CM-003` | 最终形态采用矩阵尚未获得实施授权 | D03-D13 已按独立 Human Decisions 完成有界 P0 机器事实、API、Runtime、SDK 和 MCP 工作；D16 将广义实施问题标记为 superseded | 只解除旧的广义实施决策阻塞；P0-10 Agent-first acceptance 转入 `B-013`，P1/P2、账本、Paid Beta 和生产仍未授权 |

| blocker_id | 原阻塞 | 解除证据 | 保留边界 |
|---|---|---|---|
| `B-006` | 冻结 `README.md` digest 与当前文档漂移导致 validator 失败 | Version-aware historical binding；34/34 validators `PASS`；旧 digest 未改写 | 仅当前本地工作树解除；未发布、未做 clean clone |

## 5. Risk Handling Rules（风险处理规则）

1. 风险只能由显式人工决定接受、缓解、转移或关闭；
2. `MITIGATED_BY_SPECIFICATION` 不表示运行风险已消失；
3. 失败、冲突和未知必须保留历史；
4. 子项目风险事实由子项目维护，DBA 只引用与项目群相关的摘要；
5. `CRITICAL` 或 `HIGH` 风险涉及 destructive action（破坏性操作）、权限、发布或外部影响时必须停止并请求新授权；
6. blocker 解除必须引用直接证据，不能只因计划存在而关闭。

```text
TRACKED_RISKS=33
ACTIVE_RISKS=31
RESOLVED_RISKS=2
ACTIVE_BLOCKERS=7
BLOCKERS_CLEARED=10
LOCAL_BLOCKERS_CLEARED_NOT_RELEASED=1
RISKS_ACCEPTED=1
RISK_REGISTER_GRANTS_AUTHORITY=false
```

## 6. TITMAS Integration Risks and Blockers（TITMAS 集成风险与阻塞）

| item_id | level | state | evidence | required treatment |
|---|---|---|---|---|
| `R-020` | `HIGH` | `MITIGATION_IN_PROGRESS` | community core previously existed across multiple unmerged branches and overlapping entries | selective attributable integration, duplicate removal, one-entry checks and Human merge review |
| `R-021` | `HIGH` | `ACTIVE_BLOCKER` | GitHub Private Vulnerability Reporting read-only check returned disabled on 2026-07-29 | activate a real private security transport only after `COMMUNITY-HD-02`; do not invent an email or active path |
| `R-022` | `HIGH` | `MITIGATED_BY_FAIL_CLOSED_POLICY` | prepared community files could be misread as an established or launched community | status schema fixes `community_established=false`, public launch/contribution false and external counts zero |
| `R-023` | `MEDIUM` | `MITIGATED_BY_ARCHIVE_BOUNDARY` | Ecology Box and calibration assets had displaced the open-standards mainline | retain only one immutable research index; freeze calibration v0.3 |
| `B-012` | `HIGH` | `ACTIVE` | no active private security receiving transport | blocks public launch and public contribution activation; does not block a Draft integration PR |

```text
PUBLIC_LAUNCH_BLOCKER_SECURITY_TRANSPORT=true
CALIBRATION_V0_3_AUTHORIZED=false
COMMUNITY_ESTABLISHED=false
RISK_ACCEPTANCE_NOT_INFERRED=true
```
