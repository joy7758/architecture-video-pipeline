# 发现层复用评估 · 建筑视频流水线

日期：2026-09-23。范围：既有发现资产检索、复用判断、消费方接入要求。未运行建筑资料检索任务，未安装或激活新服务。

## 结论

优先复用现有发现流程、候选去重、来源记录和状态核验能力；建筑资料补证需要领域适配。当前没有证据证明已存在能直接接收建筑资料缺口并自动完成补证的通用服务。

两种发现任务必须分别标识：

- **能力发现**：寻找可复用代码、工具、Skill、服务及其能力，比较是否值得接入。
- **资料补证**：寻找当前建筑的照片、尺寸、形制和版本依据，解决输入资料缺口或冲突。

名称中含 discovery 或 scout 不足以证明同时支持这两种任务。

## 已核对资产

| 资产 | 已观察能力 | 建筑流程复用判断 |
|---|---|---|
| titmac-scout；tiamas-scout 为历史别名/本地旧目录名 | DBA 有 canonical 状态投影；找到的本地历史代码具备 GitHub Issue 候选发现、筛选和去重流程 | 可参考或适配候选管理；不能直接当作建筑图片、尺寸搜索器；本地旧副本不证明当前 canonical 实现 |
| 外部能力发现与吸收 v0.2 | 来源身份、版本、新鲜度、候选去重、变更失效等合同规则 | 可作为接口设计参考；文件明确 REVISED_PROPOSAL_NOT_ACTIVE、implementation_owner=UNASSIGNED，不能标为已运行模块 |
| DCDAT-001 发现试验 | 七个外部能力候选的来源核对、身份去重及 REFERENCE_ONLY 登记 | 复用记录格式和执行方法；试验明确没有自动运行时、安装或代码采用 |
| cockpit/read_only_status_adapter.py | 按 Owner、精确 revision 和摘要检查源状态，生成驾驶舱只读投影 | 适合模块状态核验，不能替代建筑资料检索或图像判断 |
| 本项目 CODEX_RESEARCH_ADAPTER | 已声明资料研究工位和 sources.json 输出要求 | 作为现阶段执行角色；不宣称已经完成缺口触发器、预算管理或可复用服务接口 |

### Scout 版本与代码边界

本地历史副本位于 `/Users/zhangbin/GitHub/tiamas-scout`，HEAD 为 `0b2b4e5fab7ba4e3832786ce3d43704c782a778b`，无 remote；限定范围内未找到已核验的 canonical Owner 工作区。驾驶舱旧投影指向 `e4adbbbbb149871f108fcf384369182d8c5765f4`，其 `fresh_until=2026-08-11T16:38:30Z` 已过期；文件内历史 FRESH/PASS 不代表现在仍然有效。

本轮独立只读审查者为 `/root/discovery_reuse`，没有运行 Scout 或其测试。复用评价为 `CONDITIONALLY_RECOMMENDED`，仅限候选部件和设计方法。

该历史副本未找到明确许可证文件或带许可证的包清单，记录为 `LICENSE=UNKNOWN`。设计参考不等于代码许可；抽取代码前需核实 canonical Owner 的许可证或相应授权。

| 旧实现入口 | 可借鉴内容 | 适配/阻断条件 |
|---|---|---|
| `src/discovery/source_collector.rb` | 查询覆盖、错误、数量上限、超时与有界重试 | 连接器仅允许 `api.github.com` HTTPS GET；新增资料来源应独立适配，不能直接放开任意域名 |
| `src/discovery/support.rb` | 确定性排序、归一化、时间和 SHA-256 工具 | 核验 canonical 版本、许可和目标环境后再决定代码复用 |
| `src/discovery/deduplicator.rb:6` | Issue/URL 身份归并 | 当前保留第一条内容，仅合并 query_ids；缺少内容版本和冲突语义，不能原样用作资料去重 |
| `src/discovery/daily_report.rb:16` | 配置摘要、查询覆盖、失败、未知和候选引用 | 可借鉴报告合同，需关联建筑 gap_id |
| `src/discovery/daily_report.rb:79` | 日报写出 | 同日固定文件名可能覆盖历史；必须改为独立 run/attempt 目录及不可变证据 |
| `src/discovery/status_index.rb:97` | 历史记录聚合 | 按目录/最高状态推断 READY_FOR_REVIEW；不具备版本失效规则，不能作为流水线验收状态机 |

旧 CLI 输入固定 YAML 查询配置，输出 GitHub 机会日报，没有建筑 gap list 接口。固定 AI 基础设施关键词提取不等于建筑事实或视觉识别。现有运行命令仅作为历史入口定位，本轮不建议直接调用补证。

## 最小适配范围

保留既有候选/来源管理方式，为建筑领域增加以下合同和适配行为：

1. 输入建筑身份、年代/版本、已有参考包，以及带 `gap_id` 的具体缺口。
2. 每个缺口记录重要性、需要的证据类型、受阻工位、搜索范围和预算。
3. 支持资料页面、图片/视频视角和尺寸文献的定向发现；每个结论引用实际打开或查看的内容。
4. 输出来源记录、事实/冲突/未知项、素材使用限制和缺口处置结果；保留反证，不静默覆盖客户资料。
5. 明确结果为已找到证据、部分补齐、来源冲突、未找到或预算耗尽。关键未解决缺口阻止依赖它的验收。
6. 新参考进入新版参考包，通过依赖机制使受影响的规划、施工和审查结果失效；历史资料和旧回执保留。

这些是消费方接入要求，尚未实现为发现运行时或自动补证器。

## 目录责任和调用原则

模块目录由 DBA 维护，建筑项目只保存目录引用和选用记录。模块身份、输入输出、调用方式与验证状态从目录读取；能力、执行和当前可用性仍以 Owner 的实际来源为准。

每次复用先确认任务类型，再核对模块版本、输入输出兼容性、所需权限、验证时间与限制。历史实现、仅规范和待核实项目不得被目录使用者自动当作可直接调用服务。选择模块不等于已经运行，也不扩大项目权限。

驾驶舱现有任务 `DBA - Digital Survival Theory Foundation`（`019f93ea-3361-7850-b3e1-877fcd273a0e`）已完成首版 8 项目录，并接入 DBA `agent-index.json`：

- [中文模块列表](</Users/zhangbin/Documents/New project/digital-biosphere-architecture/cockpit/REUSABLE-MODULE-CATALOG.zh-CN.md>)
- [机器目录](</Users/zhangbin/Documents/New project/digital-biosphere-architecture/cockpit/reusable-module-catalog.json>)
- [目录 Schema](</Users/zhangbin/Documents/New project/digital-biosphere-architecture/cockpit/reusable-module-catalog.schema.json>)

| 模块 | 目录 ID | 本次复用等级 |
|---|---|---|
| Scout 状态桥 | `DBA-MOD-TITMAC-SCOUT-STATUS-BRIDGE-001` | 需适配 |
| Scout 历史 GitHub 机会发现实现 | `DBA-MOD-TITMAC-SCOUT-GITHUB-OPPORTUNITY-DISCOVERY-001` | 待核验当前来源及许可 |
| 外部能力发现与吸收规范 | `DBA-MOD-EXTERNAL-CAPABILITY-DISCOVERY-PROFILE-002` | 仅规范 |
| 发现/吸收验证夹具 | `DBA-MOD-DISCOVERY-ABSORPTION-FIXTURE-001` | 可直接复用静态案例；不表示实时发现服务 |
| 情报 Intake | `DBA-MOD-GOVERNANCE-INTELLIGENCE-INTAKE-001` | 需领域适配 |
| TITMAS 合同校验工具 | `DBA-MOD-TITMAS-CONFORMANCE-HARNESS-001` | 需合同映射与适配 |
| Agent Evidence 语义 Owner | `DBA-MOD-AGENT-EVIDENCE-SEMANTIC-OWNER-001` | 待核验当前来源 |
| SAEE 模块发现映射 | `DBA-MOD-SAEE-MODULE-DISCOVERY-MAPPING-001` | 待核验当前来源 |

首版目录为本地工作区工件，未 commit/push。目录完成不表示条目都已经执行或通过目标项目验收。本项目 `agent-index.json`、`pipeline/integrations.json` 和流水线手册已挂接目录引用。驾驶舱报告已通过 Schema、ID 唯一性、入口引用、中文覆盖、消费关系及 Scout 身份/许可边界检查；消费方再次核对结果见 `docs/governance/discovery-catalog-readback-20260923.json`。
