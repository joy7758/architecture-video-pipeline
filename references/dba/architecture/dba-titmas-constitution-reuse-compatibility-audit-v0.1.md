# DBA / TITMAS Constitution Reuse and Compatibility Audit v0.1

中文：DBA / TITMAS 宪法复用与兼容性审计 v0.1

- Status: `SOURCE_INSPECTED_READ_ONLY_AUDIT`
- Audited at: `2026-08-13`
- Canonical DBA base: `main@352cdc2dfc548be62cfb3ffcb84e33b541b419f8`
- Adoption effect: `NONE`
- Dependency effect: `NONE`
- Implementation authorization: `false`

## 1. Audit question

在新增父子宪法与 DCell 模块治理契约前，现有内部项目或外部上游是否已经拥有相同规范
责任？本审计只用于避免重复建设和定义兼容边界，不构成采用、集成、依赖、认可或产品声明。

## 2. Internal ownership and overlap

本轮从远程 canonical `main` 创建只读干净检出；未修改任何子仓库。

| Repository | Inspected revision | Existing ownership | Constitutional consequence |
|---|---:|---|---|
| `joy7758/digital-biosphere-os` | `04dfce65a2e58cbd9fbf7d1fcb12e30e0425697b` | Identity、lifecycle、capability record、execution record、evidence/verification reference；`DBOS governs existence` | DCell 契约只引用存在治理，不创建第二套 registry、permission 或 evidence system |
| `joy7758/SAEE` | `620230bd75b066b47885b092c35439ae0e5da4e9` | Evaluation、reliability、stability、risk 和 evolution recommendation；module registry 是发现映射 | DCell 变化可以触发评价输入，但 DBA/TITMAS 不复制 SAEE 算法，SAEE 不激活模块 |
| `joy7758/agent-evidence` | `09385f47a33273d8c72bbca9d3ae57aff0d5c0d9` | Execution evidence object/profile、recorder 和 adapter 语义 | DCell 只声明 evidence requirements；不复制 canonical execution-evidence semantics |
| `joy7758/titmas-integrations` | `6d1f076f886b99241a0f1a75e76166ff66f7279b` | 生成 SDK、MCP Adapter、integration surfaces 与 P0-10 retained failure evidence | 统一入口是合同目标，不反向改 SDK/MCP，不重写 P0-10 FAIL |
| `joy7758/titmas-sandbox-gateway` | `1a065f1702e355d5f5ed566bdfd3e895cdca2540` | Gate、Receipt、Audit、Health 的商业参考执行与 Gateway 边界 | 本轮不创建或修改 Gateway，不把逻辑统一入口写成全局物理控制点 |

### Internal conclusion

| Required concern | Existing source or observed gap | Disposition |
|---|---|---|
| Identity | DBOS identity and entity records | Reuse DBOS ownership; identity pluralism remains an interoperability rule |
| Boundary | DBOS capability boundary plus DBA authority rules | Reuse; DCell can only narrow the effective intersection |
| Evidence | Agent Evidence semantics plus DBOS evidence references/admission boundary | Reuse; no second evidence core |
| Authorization | Governance Decision and DBOS permission lifecycle contracts | Reuse; selection and evaluation remain non-authoritative |
| Receipt | TITMAS Gateway / Receipt product boundary | Reuse; DCell upgrade receipt is a requirement, not a new engine |
| Audit | TITMAS Audit product and retained evidence history | Reuse; no second audit chain |
| Health | TITMAS Health product boundary | Reuse; a Health Cell would be a module projection, not a fifth product |
| AHRP Memory | No canonical AHRP runtime or manifest identified in the audited DBA base | Name retained only as a user-selectable example; implementation not claimed |
| Scout drift detection | Cockpit read-only `titmac-scout` projection and source registry exist | Reuse source projection; no new scanner or authority |
| DCell manifest | No canonical DCell manifest contract identified in the audited DBA base | Define only the minimum governance gap; no registry or resolver |
| Lifecycle | DBOS entity lifecycle and architecture lifecycle specifications | Reuse; module lifecycle cannot self-activate |
| Conformance | Existing TITMAS harness, schemas and fail-closed fixtures | Extend the existing harness; do not create a second conformance system |

```text
NEW_INTERNAL_RUNTIME_REQUIRED=false
NEW_EVIDENCE_SYSTEM_REQUIRED=false
NEW_EVALUATION_ENGINE_REQUIRED=false
NEW_GATEWAY_REQUIRED=false
DBA_OWNS_CONSTITUTIONAL_CONTRACT=true
CHILD_REPOSITORIES_REMAIN_CANONICAL_OWNERS=true
```

## 3. Official upstream compatibility audit

来源仅使用官方文档或官方仓库。License 是本次观察到的仓库级事实；未来真实采用仍需重新
检查版本、子目录和商业条款。

| Upstream / official source | License observation | Reusable capability | TITMAS should not rebuild | Adapter feasibility | Constitutional conflict | Adoption authorized |
|---|---|---|---|---|---|---|
| [Open Policy Agent](https://www.openpolicyagent.org/docs) | Apache-2.0 | 通用策略决策引擎 | 通用策略语言 | `POSSIBLE_FUTURE_MAPPING` | None if Owner and Human Authority remain external | `false` |
| [OPAL](https://github.com/permitio/opal) | Apache-2.0 | 向 OPA/Cedar 分发策略与数据 | 策略分发控制面 | `POSSIBLE_FUTURE_MAPPING` | A mandatory central distributor would conflict | `false` |
| [in-toto](https://github.com/in-toto/in-toto) | Apache-2.0 | 供应链 layout/link 完整性 | 供应链证明格式 | `POSSIBLE_PROFILE_MAPPING` | None when Evidence remains non-Truth | `false` |
| [Witness](https://github.com/in-toto/witness) | Apache-2.0 | attestation 生成与验证 | 通用 attestation runtime | `POSSIBLE_PROFILE_MAPPING` | None when Verification remains non-Authorization | `false` |
| [Rekor](https://github.com/sigstore/rekor) | Apache-2.0 | 透明日志 | 第二套透明日志 | `POSSIBLE_RECEIPT_REFERENCE` | A mandatory global log would conflict | `false` |
| [ContextForge](https://github.com/IBM/mcp-context-forge) | Apache-2.0 | MCP/A2A/REST/gRPC gateway、registry、proxy | 统一协议 Gateway | `POSSIBLE_ENTRY_ADAPTER` | A physical single gateway requirement would conflict | `false` |
| [agentgateway](https://github.com/agentgateway/agentgateway) | Apache-2.0 | MCP/A2A/LLM proxy 安全、治理、可观察性 | 第二套 Agent Gateway | `POSSIBLE_ENFORCEMENT_ADAPTER` | None for distributed, owned enforcement | `false` |
| [Faramesh](https://github.com/faramesh/faramesh-core) | Apache-2.0 | 执行前确定性治理与证据 | 相邻 pre-action control plane | `POSSIBLE_CONTRACT_MAPPING` | Authority ownership requires explicit review | `false` |
| [AgentTeams](https://github.com/agentscope-ai/AgentTeams) | Apache-2.0 | Matrix 多智能体协作 | 协作 Agent Runtime | `POSSIBLE_RUNTIME_TEST_TARGET` | TITMAS becoming its orchestrator would conflict | `false` |
| [LiteLLM](https://github.com/BerriAI/litellm) | 核心 MIT，企业目录另有条款 | 多模型 Gateway 与 provider 统一 | 模型 Gateway | `POSSIBLE_MODEL_ENTRY_ADAPTER` | License scope and centralization need review | `false` |
| [Langfuse](https://github.com/langfuse/langfuse) | 核心 MIT Expat，EE 目录另有条款 | LLM observation、trace 与 evaluation | 可观察性平台 | `POSSIBLE_OBSERVATION_ADAPTER` | Observation as Evidence would conflict | `false` |
| [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) | Apache-2.0 | 厂商中立遥测接收、处理与导出 | 遥测 Collector | `POSSIBLE_OBSERVATION_TRANSPORT` | Telemetry as Truth would conflict | `false` |

## 4. Build-versus-adopt disposition

| Concern | Current disposition | Reason |
|---|---|---|
| General policy engine | `ADOPT_OR_ADAPT_CANDIDATE` | OPA/Cedar 生态已覆盖，不应自建语言 |
| Policy distribution | `ADOPT_OR_ADAPT_CANDIDATE` | OPAL 已提供相邻能力 |
| Supply-chain attestation | `MAP_BEFORE_BUILD` | in-toto/Witness/Rekor 已有成熟对象 |
| Agent/MCP gateway | `INTEGRATE_NOT_REPLACE` | ContextForge、agentgateway、LiteLLM 已覆盖运行入口 |
| Telemetry collection | `REFERENCE_ONLY` | OpenTelemetry/Langfuse 提供 observation；Evidence admission 仍需边界 |
| TITMAS constitutional contract | `RETAIN_CANONICAL_OWNERSHIP` | 外部项目不拥有 DBA 父子宪法、产品组合和 Human Authority 边界 |
| DCell governance profile | `DEFINE_CONTRACT_ONLY` | 需要统一最小契约与权限交集，但不创建模块 Runtime |

## 5. Limitations

- 未执行外部代码、性能、互操作或安全测试；
- 未建立任何 dependency、vendor relationship 或 formal adoption；
- 上游功能和许可证可能变化，实施前必须在固定版本重新审计；
- “compatibility candidate” 只表示值得未来映射，不表示当前兼容或推荐生产使用。

```text
UPSTREAM_ADOPTION_EXECUTED=false
NEW_DEPENDENCY_ADDED=false
INTEROPERABILITY_PROVEN=false
LICENSE_APPROVAL_GRANTED=false
EXTERNAL_AUTHORITY_CREATED=false
```
