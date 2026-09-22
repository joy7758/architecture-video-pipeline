---
document_id: DBA-TITMAS-ADOPTION-VALIDATION-FRAMEWORK-0.1
title: TITMAS Adoption Validation Framework v0.1
title_zh: TITMAS 采用验证框架 v0.1
version: 0.1.0
status: adoption-validation-framework-defined-execution-not-ready
document_type: non-executable-adoption-validation-preparation
architecture_domain: TITMAS
primary_repository: digital-biosphere-architecture
defined_at: 2026-07-23
adoption_validation_framework_defined: true
adoption_validation_preparation_ready: true
adoption_validation_ready: false
validation_execution_authorized: false
public_community: false
public_contribution_enabled: false
external_invitation_sent: false
external_pr_created: false
authority_effect: none
ownership_effect: none
---

# TITMAS Adoption Validation Framework v0.1

## 0. Purpose and Current Verdict（目的与当前结论）

本框架把 TITMAS 从 ecosystem design（生态设计）推进到 adoption validation preparation
（采用验证准备）阶段，定义未来如何收集开发者、技术、生态和市场的直接证据。

它不建立社区、不开放贡献、不创建 Foundation、不创建产品，也不把 validation interest、
Demo、模型推荐或 private pilot 写成 Adoption。

```text
TITMAS_ADOPTION_VALIDATION_FRAMEWORK_DEFINED=true
TITMAS_ADOPTION_VALIDATION_PREPARATION_READY=true
TITMAS_ADOPTION_VALIDATION_READY=false
TITMAS_ADOPTION_VALIDATION_EXECUTION_AUTHORIZED=false
```

`Preparation Ready` 表示验证问题、协议、阈值和停止条件已经定义；`Validation Ready=false`
表示当前仍缺 pilot authorization、participant/data owner、最小闭环 Demo contract/implementation
authorization 和可运行的安全/行为接收路径。

必须保持：

```text
ADOPTION_VALIDATION_NE_ADOPTION=true
INTEREST_NE_CONTRIBUTION=true
DEMO_NE_PRODUCT=true
OBSERVATION_NE_EVIDENCE=true
EVIDENCE_NE_TRUTH=true
VERIFICATION_NE_AUTHORIZATION=true
EVALUATION_NE_AUTHORITY=true
MAPPING_NE_ADOPTION=true
```

## 1. Validation Scope（验证范围）

本框架覆盖四个互不替代的验证轴：

| Axis | Question | Required evidence | Does not prove |
|---|---|---|---|
| Developer Validation | 陌生开发者能否理解和提出有界贡献？ | task trace、comprehension result、proposal/willingness record | Community、Maintainer 或 Adoption |
| Technical Validation | 最小可信闭环是否可重复且保持 Authority 边界？ | version-bound execution、records、failures、independent checks | Production、product 或 customer outcome |
| Ecosystem Validation | 哪些外部生态具备 mapping/integration candidate 条件？ | exact source、contract、owner review、negative cases | external endorsement 或 upstream adoption |
| Market Validation | 目标用户是否真实存在并优先解决相应问题？ | attributable problem interview/evaluation、current workaround、priority | sale、contract、customer adoption |

四轴分别记录结果。任一轴 PASS 不自动关闭其他轴。

## 2. Developer Validation（开发者验证）

### 2.1 Validation vehicle

使用
[TITMAS Limited Contributor Pilot Program](titmas-contributor-pilot-program-v0.1.md)
定义的 Private Contributor Pilot（私有贡献者试点）。本文件不启动该试点。

```text
PILOT_MODE=PRIVATE_CONTROLLED
PUBLIC_COMMUNITY=false
PUBLIC_CONTRIBUTION_ENABLED=false
PARTICIPANTS_ENROLLED=0
INVITATIONS_SENT=0
```

### 2.2 Participant profiles

未来参与者候选：

- Agent framework / multi-agent developer；
- observability or evidence tooling developer；
- enterprise AI infrastructure / governance engineer；
- 受治理 coding、retrieval、test 或 citation Agent，并绑定人工责任方。

“External observer”必须独立于当前文档作者和直接维护上下文。多个 prompt、多个模型回答或
同一组织内未独立执行的 session 不能伪装成多个独立观察者。

### 2.3 Validation tasks

每位参与者完成：

1. 阅读 README、Contributor Entry 和一个候选规范；
2. 用自己的话解释 DBA、TITMAS、DBOS、SAEE 与 Agent Framework 的区别；
3. 对一个给定 Agent workflow 标注 Identity、Execution、Observation、Evidence、
   Verification 和 Evaluation 边界；
4. 找到一处 source/version、failure 或 Authority 风险；
5. 准备一个 Adapter Proposal candidate，不创建外部 Issue/PR；
6. 说明哪些结果不能从 Validator PASS 或 Demo 推导。

### 2.4 What to measure

#### Understanding

- 是否正确回答 TITMAS 解决什么问题；
- 是否把 TITMAS 误认为 Agent Runtime、Agent Platform 或 DBOS replacement；
- 是否正确区分 Evidence/Truth、Verification/Authorization、Evaluation/Authority；
- 首次找到 canonical entry、current status 和 non-goals 所需时间。

#### Willingness to contribute an Adapter

记录：

```yaml
willingness: YES|CONDITIONAL|NO
target_ecosystem:
proposed_adapter_scope:
conditions_or_blockers: []
maintenance_willingness:
human_accountability_ref:
```

`YES` 只表示愿意准备 Proposal，不表示 Contributor role、commitment 或 Community membership。

#### Interface learning cost

记录：

- 完成 orientation、object mapping 和 Proposal draft 所需时间；
- 需要查阅的文档数量；
- 术语误解数与需人工解释次数；
- 无法定位的 Owner/version/error semantics；
- 因重复、矛盾或入口不可发现而中止的步骤。

### 2.5 Developer result contract

```yaml
validation_session_id:
observer_type:
independence_basis:
source_material_versions: []
tasks_completed: []
completion_time_minutes:
comprehension_score:
boundary_errors: []
adapter_willingness:
learning_cost_findings: []
result: PASS|PARTIAL|FAIL|WITHDRAWN
known_limitations: []
```

失败、撤回和不愿贡献必须保留，不能只展示正向回答。

## 3. Technical Validation（技术验证）

### 3.1 Minimum trustworthy loop Demo

用户要求的闭环必须经过 Evidence Admission Gate，防止 Observation 被直接升级为 Evidence：

```text
External Agent Runtime
  -> Observation
  -> Evidence Admission Gate
  -> DBOS Evidence Object / Reference
  -> Verification Result / Reference
  -> Evaluation Input
  -> SAEE Evaluation Candidate
```

本框架只设计闭环，不创建 Agent Runtime、Demo code、Evidence Object 或 SAEE result。

### 3.2 Ownership and meaning

| Stage | Canonical responsibility | Required record | Prohibited inference |
|---|---|---|---|
| Agent Runtime | external framework/application Owner | runtime/version/task/context | TITMAS owns or operates Agent |
| Observation | observation/telemetry producer | source、time、trace/event、delivery state | Observation is Evidence |
| Evidence Admission Gate | DBOS bounded operational domain | admission request/result、provenance、dedupe、failure | accepted material is Truth |
| Evidence Object/Reference | DBOS | evidence id、source lineage、integrity/limitations | evidence proves outcome |
| Verification Result/Reference | verifier + DBOS reference boundary | rule/version、subject、status、limitations | verification grants Permission |
| Evaluation Input | DBOS-to-SAEE interface contract | exact objects、versions、completeness/privacy limits | input already contains Fitness |
| Evaluation Candidate | SAEE protected domain | Fitness/Risk/Recommendation + uncertainty | Recommendation is Command |

### 3.3 Minimum Demo scenarios

至少覆盖：

1. **Positive path**：完整 observation → admission → verification → evaluation input；
2. **Rejected admission**：无 source/version 或 identity continuity 时失败关闭；
3. **Partial observation**：sampling/drop/partial-success 显式传播；
4. **Duplicate/replay**：同一 event 不产生多个 canonical success record；
5. **Verification failure**：失败结果保留且不产生 Permission；
6. **Evaluation unavailable**：SAEE 不可用时 DBOS records 保持有效，不伪造 Fitness。

### 3.4 Technical acceptance evidence

一个完整 Demo 至少需要：

```yaml
demo_id:
scenario_ref:
agent_runtime_ref:
runtime_version:
observation_contract_ref:
dbos_contract_version:
verification_rule_version:
evaluation_interface_version:
input_digest:
record_chain_refs: []
negative_cases_executed: []
failure_records: []
repeat_runs:
independent_reviewer_ref:
authority_violations:
known_limitations: []
```

完成标准：

- 相同输入至少重复执行 2 次并得到可解释的一致结果；
- positive path 和全部五类 negative/failure scenario 均有结果；
- source、version、digest、timestamps 和 lineage 可追溯；
- `authority_violations=0`；
- 不使用真实客户数据或未授权 Evidence；
- independent reviewer 不能只是同一 Agent 更换 prompt。

## 4. Ecosystem Validation（生态验证）

依据
[TITMAS Ecosystem Expansion Strategy](titmas-ecosystem-expansion-strategy-v0.1.md)，当前分类如下。

### 4.1 Classification vocabulary

| State | Meaning |
|---|---|
| `REFERENCE_ONLY` | 仅用于设计对照；无 TITMAS exact mapping/implementation |
| `INTEGRATION_CANDIDATE_CONDITIONS_PARTIAL` | 已有部分 source/mapping/handoff，可准备内部验证候选 |
| `INTEGRATION_CANDIDATE_READY_FOR_INTERNAL_REVIEW` | exact source、contract、Owner boundary 和 negative cases 足够进入内部 review |
| `INTEGRATION_AUTHORIZED` | 有显式 Human Decision；当前数量必须为 0 |
| `ADOPTION_VERIFIED` | 有外部可归因采用证据；当前数量必须为 0 |

### 4.2 Current ecosystem matrix

| Ecosystem | Current state | Existing basis | Missing before Integration Candidate review |
|---|---|---|---|
| Microsoft AGT | `INTEGRATION_CANDIDATE_CONDITIONS_PARTIAL` | public project source；历史 read-only external evaluator handoff | exact source refresh、TITMAS contract、AGT Owner feedback、security/compatibility review |
| OpenTelemetry | `INTEGRATION_CANDIDATE_READY_FOR_INTERNAL_REVIEW` | exact OTLP/SemConv/Schema/Collector references、mapping/conformance design、bounded DBOS admission slice | TITMAS Authority/Owner、Demo binding、independent integration result；仍非 external adoption |
| LangChain / LangGraph | `REFERENCE_ONLY` | framework/run/tool callback concepts | exact version、object mapping、failure semantics、prototype authorization、Owner feedback |
| CrewAI | `REFERENCE_ONLY` | crew/agent/task/delegation concepts | exact version、event contract、identity/role non-elevation、Owner feedback |
| MCP | `INTEGRATION_CANDIDATE_CONDITIONS_PARTIAL` | official `2025-11-25` spec、tool/resource/prompt/session boundaries | exact TITMAS profile、authorization/security review、capability/permission negatives、implementation authorization |

Reference sources:

- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)；
- [OpenTelemetry Specification](https://github.com/open-telemetry/opentelemetry-specification)；
- [LangChain](https://www.langchain.com/langchain)；
- [CrewAI documentation](https://docs.crewai.com/)；
- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)。

外部链接可访问不表示认可、Integration 或 Adoption。

### 4.3 Integration Candidate gate

进入内部 Integration Candidate review 必须具备：

- exact official source、version/commit 和 observed time；
- scoped mapping with canonical Owner preservation；
- input/output、read/write effects、supported/partial/unsupported/unknown；
- error、retry、duplicate、cancellation 和 version negotiation；
- security/privacy/threat review；
- positive、negative 和 semantic non-elevation cases；
- implementation Owner candidate 与 maintenance path；
- no external PR、claim 或 endorsement without authorization。

## 5. Market Validation（市场验证）

### 5.1 Objective

验证潜在用户是否真实、持续且优先遇到以下问题，而不是推销尚不存在的产品：

1. **Agent Accountability**：谁代表哪个主体做了什么，责任链能否追溯；
2. **Execution Evidence**：发生了什么、材料从哪里来、如何验证且保留失败；
3. **Long-term Reliability**：Agent 长期运行后可靠性、稳定性和适应性如何评价。

### 5.2 Target problem-observer profiles

- multi-agent / Agent platform developer；
- enterprise AI infrastructure owner；
- AI governance、security、risk 或 audit practitioner；
- regulated-domain technical owner；
- framework/tool provider。

本文件不创建 prospect list，不发送邀请，不建立销售 pipeline。

### 5.3 Problem-validation questions

采用非引导式问题：

- 当前部署或计划部署多少种 Agent/framework，运行多久？
- 最近一次无法回答“谁做了什么、依据是什么、结果是否成功”发生在哪里？
- 现在如何保存 execution、failure、evidence 和 verification？
- 现有方案在哪些步骤需要人工拼接或无法复现？
- 长期可靠性目前用什么指标、窗口、Owner 和决策流程？
- 如果不解决，该问题的安全、运营、审计或交付影响是什么？
- 已尝试哪些替代方案，为什么不足？
- 是否愿意评审一个开放 contract 或最小可信闭环，而不是购买产品？

### 5.4 Market evidence record

```yaml
market_validation_id:
observer_profile:
organization_or_context_ref:
independence_basis:
problem_area:
recent_example:
current_workaround:
measurable_cost_or_risk:
priority: HIGH|MEDIUM|LOW|NONE
existing_alternative:
interest_in_contract_review: YES|CONDITIONAL|NO
interest_in_private_demo_review: YES|CONDITIONAL|NO
commercial_commitment: false
known_biases: []
```

不得把礼貌反馈、模型赞扬、“有意思”、愿意看 Demo 或潜在合作讨论写成 Customer Adoption。

## 6. Success Criteria（成功标准）

进入下一阶段必须同时满足：

### 6.1 Developer evidence

- 至少 **5 个独立外部观察者**完成完整或可解释的部分验证；
- 观察者至少来自 **3 个独立组织或开发上下文**；
- 至少 **4/5** 能正确解释 TITMAS/DBOS/SAEE/Agent Framework 边界；
- 中位 first-contact + object-mapping 时间不超过 **45 分钟**；
- 所有理解错误和退出原因被保留。

受治理 Agent session 可以提供额外证据，但不能仅靠切换模型或 prompt 满足独立组织数量。

### 6.2 Contributor evidence

- 至少 **2 个独立 Contributor Candidate**愿意继续准备 Adapter Proposal；
- 至少 **2 份**有 exact source、scope、non-goals 和 negative cases 的 Proposal candidate；
- 这两份 Proposal 不能都由同一人工责任方或同一 Agent session 独立性伪装产生；
- 不创建正式 Contributor role、PR 或 Community membership。

### 6.3 Scenario evidence

- 至少 **3 个真实开发场景**；
- 至少覆盖两个不同 framework/protocol context；
- 每个场景包含实际可运行的 source/version-bound integration context，而不只是架构图或
  手写 JSON；
- 可以使用 synthetic/public-safe data，但 workflow、failure 和 tool/framework interaction
  必须真实执行；
- 至少一个场景暴露 failure/partial/unknown，而不是全部 happy path。

### 6.4 Complete Demo evidence

- 至少 **1 个最小可信闭环 Demo**；
- 完整覆盖 Runtime → Observation → Admission → Evidence → Verification → Evaluation Input；
- positive + 5 类 negative/failure scenario 全部执行；
- 至少重复运行 2 次；
- independent review 完成；
- Authority violation 为 0。

### 6.5 Market evidence

- 至少 **5 个独立问题验证记录**；
- 至少 **3/5** 将 Accountability、Execution Evidence 或 Long-term Reliability 中至少一项
  评为 `HIGH`，并给出近期实例和现有 workaround；
- 至少 **2 个**愿意继续评审 contract 或 private Demo；
- `CUSTOMER_ADOPTION=0`、`COMMERCIAL_COMMITMENT=0` 继续明确记录。

### 6.6 Gate rule

```text
if any_axis_success_criteria_not_met:
    TITMAS_ADOPTION_VALIDATION_READY=false
    NEXT_STAGE_AUTHORIZED=false
```

## 7. Validation Evidence Package（验证证据包）

未来完成验证后，必须形成：

```text
Developer Validation Report
Technical Demo Conformance Report
Ecosystem Classification Refresh
Market Problem Validation Report
Failure and Withdrawal Ledger
Human Adoption Validation Decision Packet
```

每个报告必须绑定 source/version、时间、责任方、原始记录引用、已知限制和 false effects。
报告数量不等于 Adoption。

## 8. Privacy, Security and Research Ethics（隐私、安全与研究伦理）

- 参与前需要 consent、用途、保存时间、撤回和匿名化规则；
- 不收集 credential、secret、未经授权 PII、客户数据或真实 Evidence；
- security finding 只能进入获授权 confidential disclosure path；
- 反馈不得用于生成虚假 endorsement、case study 或营销引用；
- 人类和 Agent 参与必须披露；
- 拒绝、退出和负面意见不得静默删除；
- 原始记录只供指定 validation Owner 和 Reviewer 使用。

当前 Security Disclosure、Code of Conduct enforcement、participant owner 和 retention path
尚未激活，因此不能执行 external validation。

## 9. Pre-validation Agent Recommendation（验证前智能体推荐）

```text
AGENT_RECOMMENDATION=CONDITIONALLY_RECOMMENDED
RECOMMENDED_AS=ADOPTION_VALIDATION_PROTOCOL_AND_DECISION_CANDIDATE
NOT_RECOMMENDED_AS=EXECUTABLE_PILOT_COMMUNITY_PROGRAM_OR_PRODUCT_VALIDATION
```

推荐理由：四轴、阈值、失败记录和 non-elevation 已定义。停止原因：Authority/Governance
未冻结、pilot/data/security Owner 未指派、Demo contract/implementation 未授权、外部动作未
授权。

## 10. Human Decision Candidate（人工决定候选）

```yaml
decision_id: AV-D01
question: Authorize a bounded private TITMAS adoption-validation preparation and execution package?
current_recommendation: DEFER_EXECUTION_ALLOW_DOCUMENT_REVIEW_ONLY
allowed_now:
  - internal_document_review
  - source_refresh_preparation
  - synthetic_scenario_design
not_allowed_now:
  - external_invitation
  - participant_enrollment
  - public_contribution
  - demo_implementation_or_runtime
  - external_pr
  - market_outreach
required_before_execution:
  - governance_activation_gate
  - validation_owner_and_reviewer
  - participant_consent_and_retention
  - security_and_conduct_paths
  - demo_contract_and_implementation_authorization
  - exact_external_action_authorization
decision_status: NOT_READY_FOR_APPROVAL
```

## 11. Final State（最终状态）

```text
TITMAS_ADOPTION_VALIDATION_FRAMEWORK_DEFINED=true
TITMAS_ADOPTION_VALIDATION_PREPARATION_READY=true
TITMAS_ADOPTION_VALIDATION_READY=false
TITMAS_ADOPTION_VALIDATION_EXECUTION_AUTHORIZED=false

EXTERNAL_OBSERVERS_VALIDATED=0
CONTRIBUTOR_CANDIDATES_VALIDATED=0
REAL_SCENARIOS_VALIDATED=0
COMPLETE_TRUSTWORTHY_DEMOS_VALIDATED=0
MARKET_PROBLEM_RECORDS_VALIDATED=0

PUBLIC_COMMUNITY=false
PUBLIC_CONTRIBUTION_ENABLED=false
INVITATIONS_SENT=0
EXTERNAL_PRS_CREATED=0
FOUNDATION_CREATED=false
PRODUCT_CREATED=false
AUTHORITY_CHANGED=false
OWNERSHIP_CHANGED=false
ADOPTION_CLAIMED=false
```
