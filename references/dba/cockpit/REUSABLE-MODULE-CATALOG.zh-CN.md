# DBA 可复用模块目录 v0.1

## 1. 目录定位

本目录帮助其他项目查找已有能力、规范、验证夹具和 Owner，避免重复建设。机器来源为
[`reusable-module-catalog.json`](reusable-module-catalog.json)，Schema 为
[`reusable-module-catalog.schema.json`](reusable-module-catalog.schema.json)。

它不是 Runtime、模块商店、权限系统或自动安装器，也不会把历史文档、测试夹具或脚本
自动提升为 DCell、在线服务、生产能力或已采用依赖。

复用等级：

| 等级 | 含义 |
|---|---|
| `DIRECT_REUSE` | 可在已核验的精确非权威范围直接复用 |
| `ADAPTATION_REQUIRED` | 能力存在，但新项目需要 Owner 明确的适配器或合同映射 |
| `SPECIFICATION_ONLY` | 只有规范或规划合同，不声称有可调用实现 |
| `VERIFICATION_REQUIRED` | 已知 canonical Owner 和历史版本，使用前必须重新读取 Owner 当前来源 |

## 2. 模块列表

| 模块 ID | 职责与适用场景 | Owner / canonical 来源 | 实际入口 | 权限与副作用 | 版本与证据 | 复用等级 |
|---|---|---|---|---|---|---|
| `DBA-MOD-TITMAC-SCOUT-STATUS-BRIDGE-001` | 只读观察 `titmac-scout` 状态、CI 和 PR；可借鉴来源固定与失败关闭语义 | `joy7758/titmac-scout` 拥有实现与状态；DBA 拥有只读投影 | `cockpit/read_only_status_adapter.py`、`cockpit/source-registry.json`；本机 `tiamas-scout@0b2b4e5` 无 remote，仅为历史副本 | 只读 Owner 来源，只写本地投影；不修复、不合并、不部署 | `e4adbb...`；2026-08-08 投影已过期；历史副本不证明 canonical 当前状态 | `ADAPTATION_REQUIRED` |
| `DBA-MOD-EXTERNAL-CAPABILITY-DISCOVERY-PROFILE-002` | 外部能力来源绑定、指纹、去重、吸收分级和结果报告 | DBA Architecture Governance | `architecture/external-capability-discovery-absorption-profile-v0.2.json` | 只创建架构规划元数据；不创建 Evidence、Evaluation、Permission 或发布权 | v0.2；修订提案未激活 | `SPECIFICATION_ONLY` |
| `DBA-MOD-DISCOVERY-ABSORPTION-FIXTURE-001` | 验证来源身份、重名冲突、能力重叠和“引用吸收不等于代码采用” | DBA Architecture Governance | `architecture/discovery-validation/dcell-external-capabilities-test-001/` | 本地只读夹具；不安装、不执行外部代码 | `DCDAT-001`；`PASS_WITH_PARTIAL_SOURCE_COVERAGE` | `DIRECT_REUSE` |
| `DBA-MOD-GOVERNANCE-INTELLIGENCE-INTAKE-001` | 外部研究、协议、安全与生态信号的来源核验、版本钉住和声明纠偏 | DBA | `intelligence/agent-index.json` | reference-only；不下载模型、不扫描资产、不自动采用 | v0.1.0；当前包停留在 2026-08-16 | `ADAPTATION_REQUIRED` |
| `DBA-MOD-TITMAS-CONFORMANCE-HARNESS-001` | 验证 TITMAS Schema、Registry 和权力边界 | DBA TITMAS conformance surface | `python3 TITMAS/conformance/harness.py` | 本地读取并可生成报告；不认证、不授权、不部署 | root index v3.1.0；本目录任务未执行全量 Harness | `ADAPTATION_REQUIRED` |
| `DBA-MOD-AGENT-EVIDENCE-SEMANTIC-OWNER-001` | Execution Evidence 对象、Recorder 和 Adapter 的 canonical 语义 | `joy7758/agent-evidence` | Owner 仓库；DBA 仅保留复用审计引用 | 本目录不产生接入或 Evidence admission 权力 | 历史审计提交 `09385f...`，当前来源待复核 | `VERIFICATION_REQUIRED` |
| `DBA-MOD-SAEE-MODULE-DISCOVERY-MAPPING-001` | Evaluation、Reliability、Risk 和 Evolution Recommendation；module registry 只做发现映射 | `joy7758/SAEE` | Owner 仓库；当前具体 registry 路径 `UNKNOWN` | 映射与建议不激活模块 | 历史审计提交 `620230...`，当前来源待复核 | `VERIFICATION_REQUIRED` |

## 3. 发现能力与项目补证的区别

`Capability Discovery` 回答的是：外部或内部是否已有可复用技术能力、它是谁、哪个版本、
与现有模块重叠多少、应该 build、adapt、adopt、reference、defer 还是 reject。

`Project Evidence Gap Completion` 回答的是：一个具体项目还缺哪些事实才能继续，例如照片、
尺寸、建筑身份、位置、测量来源以及互相冲突的资料。它需要领域证据采集和冲突保留，不能
用“找到一个 GitHub 仓库”替代。

两者可以共享来源绑定、版本、摘要、冲突和 `UNKNOWN` 语义，但不能共享虚假的成熟度或
执行权。

## 4. 3D 建筑拆解流水线引用

消费方：`3d-building-disassembly-pipeline`。

请求来源：`codex-thread:01a0c8de-3616-71e3-90ce-93d66f246f80`。

可复用部分：

- 使用 Intelligence Intake 的来源固定、版本和冲突纠偏语义；
- 使用 External Capability Discovery Profile 的候选身份、去重和 adopt-before-build 比较；
- 使用 Discovery/Absorption Fixture 检查重名、错误合并和引用提升风险。

尚缺部分：

- 建筑照片与视角来源采集；
- 尺寸和测量 provenance；
- 建筑身份、地点和版本消歧；
- 冲突资料的并列保留与人工可读摘要；
- 一个由 3D 项目 Owner 负责的领域 Evidence Intake Adapter。

结论：现有发现层可以复用其来源身份、去重、边界和报告合同，但不能直接完成建筑资料补证。
本目录不实现建筑适配器，也不把 `titmac-scout` 复制成新的通用爬虫。

## 5. 使用规则

1. 先按模块 ID 读取机器目录，再读取 `actual_entries` 指向的 Owner 来源。
2. `STALE`、`UNKNOWN`、`VERIFICATION_REQUIRED` 必须保留，不能改写成 `PASS`。
3. `tiamas-scout` 只作为对话别名，机器身份始终是 `titmac-scout`。
4. 发现、评价、Evidence、Permission、Activation 和 Deployment 相互独立。
5. 复用目录只帮助路由和比较，不授予安装、凭据、网络、付款、合并或部署权限。

## 补充许可边界

- 历史本地副本 `/Users/zhangbin/GitHub/tiamas-scout` 的 `LICENSE=UNKNOWN`。
- 该副本只能作为设计参考或待许可核验候选，不能据此宣称代码可自由复制。
- Canonical Owner 与现行许可证仍需从规范来源重新核验。

## Scout 发现实现与状态桥的身份区分

### `DBA-MOD-TITMAC-SCOUT-GITHUB-OPPORTUNITY-DISCOVERY-001`

- **职责**：历史 `titmac-scout` 的 GitHub Issue 候选发现实现，不是 DBA 的 Scout 状态桥。
- **实际入口**：`/Users/zhangbin/GitHub/tiamas-scout/src/discovery/cli.rb`
- **观测版本**：本地历史副本 `0b2b4e5fab7ba4e3832786ce3d43704c782a778b`；无 remote；canonical checkout 未定位。
- **许可**：`LICENSE=UNKNOWN`，不可据此宣称代码可自由复制。
- **复用等级**：`VERIFICATION_REQUIRED`。
- **可候选复用**：固定查询预算、重试、归一化、摘要、覆盖缺失与失败报告结构。
- **不可直接复用**：同 URL 去重没有来源冲突或版本语义；同日报告可能覆盖；状态索引没有版本失效语义。
- **领域边界**：它不能替代建筑照片、尺寸、建筑身份和冲突来源解析等项目证据缺口采集。
