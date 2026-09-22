---
document_id: DBA-TITMAS-AGENT-EVALUATION-ENTRY-CONTRACT-0.1
title: TITMAS Agent Evaluation Entry Contract v0.1
title_zh: TITMAS 智能体评估入口契约 v0.1
version: 0.1.0
status: development-contract-source-prepared-not-deployed
maturity: Development
maturity_scope: entire-document
owner_ref: zhangbin
decision_reference: TITMAS-COMMERCIAL-EVALUATION-CE-G2
supersedes: NONE
superseded_by: NONE
compatibility_statement: "Additive machine entry for Commercial Evaluation Pack v0.2; no change to DBOS object semantics, SAEE evaluation semantics, Runtime state, Permission, Certification, SLA, or production compatibility."
implementation_feedback_refs: []
conformance_refs: []
known_limitations: [SEE_DOCUMENT_BODY]
document_type: non-executable-agent-evaluation-entry-contract
architecture_domain: TITMAS
primary_repository: digital-biosphere-architecture
observed_at: 2026-07-27
authority_effect: none
---

# TITMAS Agent Evaluation Entry Contract v0.1

## 1. Purpose（目的）

本契约定义一个陌生 AI Agent 如何以失败关闭方式发现和评估 TITMAS Developer Preview：

```text
Discovery
  -> Artifact Binding
  -> Dependency-aware Installation
  -> Synthetic Validation
  -> Failure Classification
  -> Bounded Recommendation
```

它解决的是机器入口一致性，不是产品功能。规范机器实例：

- [TITMAS-AGENT-EVALUATION-ENTRY-v0.1.json](../TITMAS-AGENT-EVALUATION-ENTRY-v0.1.json)
- [JSON Schema](schemas/titmas-agent-evaluation-entry.schema.v0.1.json)

## 2. Normative Keywords（规范关键词）

`MUST`、`MUST NOT`、`SHOULD` 和 `MAY` 只在本 Development 契约范围内表达要求。
它们不创建法律义务、Permission、Authority、Certification、SLA 或生产保证。

## 3. Discovery Contract（发现契约）

评估 Agent MUST 从以下已存在入口开始：

1. `https://redcrag.cn/llms.txt`
2. `https://redcrag.cn/agent-index.json`
3. `https://redcrag.cn/TITMAS-COMMERCIAL-EVALUATION-PACK-v0.2.json`

Agent MUST NOT：

- 推断未列出的域名或 API；
- 把搜索摘要当作 canonical source；
- 把未来 `titmas.cn` 当作当前已上线入口；
- 把 GitHub README、网站文案或模型回答单独当作 Capability Truth。

新契约网站路径处于 source-prepared、not-deployed 状态。在独立发布决定和部署回执出现前，
Agent MUST 从 GitHub canonical source 读取本契约，不得假设
`https://redcrag.cn/TITMAS-AGENT-EVALUATION-ENTRY-v0.1.json` 已可用。

## 4. Artifact and Install Contract（产物与安装契约）

机器实例 MUST 绑定：

- distribution；
- version；
- exact filename；
- exact URL；
- SHA-256；
- Python requirement；
- dependency policy。

评估 Agent MUST：

1. 保留 exact filename，不重命名 wheel；
2. 下载后计算 SHA-256 并与契约比较；
3. 在隔离 Python `>=3.11` 环境中安装；
4. 让 `pip` 解析并安装 wheel 声明的依赖；
5. 保留下载、hash、安装和失败结果。

`--no-deps` MUST NOT 被当作合规安装路径。因测试 harness 主动省略依赖产生的
`ModuleNotFoundError` MUST 分类为 harness/configuration failure，不能自动升级为 artifact defect。

## 5. Validation Contract（验证契约）

唯一 v0.1 合成首跑：

```text
fixture:
  https://redcrag.cn/examples/titmas-first-run/entity-object.synthetic.v0.1.json

command:
  dbos-validate OBJECT_FILE

expected_exit_code:
  0

expected_result:
  PASS
```

`PASS` 只表示：

> 该合成对象在该 validator 版本下通过本地结构和治理约束检查。

`PASS` 不表示：

- Truth；
- real Agent execution；
- Capability、Permission 或 Authority；
- Registration 或 Activation；
- Security、Compliance 或 Certification；
- Customer Adoption、SLA 或 Production Readiness。

## 6. Availability Observation Contract（可用性观察契约）

Public URL 的 HTTP 结果属于 observation（观察），不是 SLA。

每条未来 observation MUST 至少记录：

- observed_at；
- observer_reference；
- target_url；
- HTTP status 或 transport error；
- latency；
- artifact digest（适用时）；
- result；
- raw receipt reference。

规则：

- 成功和失败均 MUST 保留；
- 传输失败 MUST 与 hash、install、validation failure 分开；
- Agent MUST NOT 静默重试并只保留成功结果；
- 单次或短窗口可用不产生 availability guarantee；
- 当前契约没有定义 uptime target、support commitment 或 SLA。

当前状态：

```text
TIME_WINDOW_AVAILABILITY_OBSERVATION_EXECUTED=false
AVAILABILITY_SLA_DEFINED=false
```

## 7. Failure Taxonomy（失败分类）

| Code | Stage | Retryable | Meaning |
|---|---|---:|---|
| `ENTRY_DISCOVERY_UNAVAILABLE` | discovery | yes | canonical 入口暂时不可访问 |
| `CONTRACT_VERSION_UNSUPPORTED` | discovery | no | Agent 不支持该契约版本 |
| `ASSET_FETCH_TRANSPORT_ERROR` | fetch | yes | 下载发生网络或 HTTP 传输错误 |
| `ARTIFACT_HASH_MISMATCH` | integrity | no | 下载字节与 exact SHA-256 不同 |
| `ARTIFACT_FILENAME_CHANGED` | integrity | no | wheel 被重命名或文件名不一致 |
| `UNSUPPORTED_ENVIRONMENT` | install | no | Python 或平台不满足声明条件 |
| `INSTALL_DEPENDENCY_RESOLUTION_FAILED` | install | conditional | 声明依赖无法解析或安装 |
| `VALIDATOR_NOT_EXECUTABLE` | validation | conditional | CLI 不存在、不可启动或依赖缺失 |
| `VALIDATION_RESULT_FAIL` | validation | no | validator 正常运行但返回 FAIL |
| `BOUNDARY_ASSERTION_FAILED` | recommendation | no | 输出产生 Truth/Authority/Permission 等越权声明 |

Retryable 只表示可以由后续有界协议决定重试；它不是自动重试授权。

## 8. Safe Recommendation Policy（安全推荐策略）

Agent 只有在以下步骤全部通过后，才 MAY 推荐 TITMAS 用于离线、只读评估：

```text
CANONICAL_DISCOVERY_PASS
AND CONTRACT_VERSION_SUPPORTED
AND ARTIFACT_FETCH_PASS
AND ARTIFACT_SHA256_PASS
AND DEPENDENCY_AWARE_INSTALL_PASS
AND SYNTHETIC_VALIDATION_PASS
AND BOUNDARY_ASSERTION_PASS
```

允许输出：

```text
RECOMMEND_FOR=OFFLINE_READ_ONLY_EVALUATION
```

必须同时输出：

```text
DO_NOT_RECOMMEND_FOR=PRODUCTION
AVAILABLE_COMMERCIAL_OFFERING=false
PRODUCTION_READY=false
CERTIFICATION_AVAILABLE=false
SLA_DEFINED=false
```

任何关键步骤失败或未知时，结果 MUST 是 `DO_NOT_RECOMMEND_UNTIL_RESOLVED`，并保留失败码。
Agent Recommendation 不产生 Governance Decision、Authorization、Permission 或 Execution。

## 9. Version and Compatibility（版本与兼容）

- Contract v0.1 对 Commercial Evaluation Pack v0.2 是 additive（增量）的；
- 不修改 Pack v0.2 的历史结果；
- patch 版本 MAY 添加非必填描述或 failure detail；
- 新 required field 或语义变化 MUST 提升 minor/major 版本并声明兼容性；
- 不支持的版本 MUST 失败关闭为 `CONTRACT_VERSION_UNSUPPORTED`；
- Deprecated 不等于 Deleted，历史契约必须保留。

## 10. Ownership and Authority（所有权与权力）

| Surface | Owner / role | Explicit limit |
|---|---|---|
| Contract and Schema | DBA Architecture Governance | 不执行 DBOS 或修改 SAEE |
| Entity / execution / evidence reference facts | DBOS | 不产生演化评价 |
| Fitness / risk / evolution evaluation | SAEE | 不授权、不执行 |
| Adoption or production decision | explicit Governance Decision | 不等于 Execution |
| Agent recommendation | advisory consumer output | 不产生 Authority |

## 11. Current Truth（当前事实）

```text
AGENT_EVALUATION_ENTRY_CONTRACT_DEFINED=true
AGENT_EVALUATION_ENTRY_SCHEMA_DEFINED=true
AGENT_EVALUATION_ENTRY_INSTANCE_DEFINED=true
CONTRACT_MATURITY=Development
WEBSITE_SOURCE_PREPARED=true
WEBSITE_DEPLOYED=false
TIME_WINDOW_AVAILABILITY_OBSERVATION_EXECUTED=false

IMPLEMENTATION_CREATED=false
RUNTIME_CREATED=false
API_CREATED=false
AGENT_CREATED=false
PERMISSION_CREATED=false
COMMERCIAL_OFFER_CREATED=false
CERTIFICATION_CREATED=false
SLA_DEFINED=false
PRODUCTION_READY=false
```
