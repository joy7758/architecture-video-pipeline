# DBA Main Constitution Coherence Amendment v0.1

中文：DBA 主宪法一致性修正案 v0.1

- Status: `ACCEPTED_EFFECTIVE_ON_CANONICAL_MERGE`
- Contract ID: `DBA-MAIN-CONSTITUTION-COHERENCE-v0.1`
- Parent: [`PROGRAM-CHARTER.md`](../PROGRAM-CHARTER.md)
- Machine contract: [`main-constitution-principles.json`](main-constitution-principles.json)
- Human adoption decision: `APPROVED`
- Effective trigger: `CANONICAL_MAIN_MERGE_OF_PR_142`
- Canonical ref: `refs/heads/main`
- Candidate branch authority effect: `NONE`
- Implementation authorization: `false`

## 1. Purpose and effect

本修正案把已经分散在 Program Charter、ADR-032、ADR-033、ADR-039 和现行商业私有
基础设施战略宪法中的原则，整理为一组可追踪、可机读的父级规则；同时补充兼容优先、
组合责任、共享协议不等于共享控制器，以及真实环境反馈约束。

Human Owner 已正式批准本修正案。它在候选分支上不产生规范 Authority；当包含该决定的
PR #142 合并并可从 canonical `refs/heads/main` 到达时生效。该触发机制不改变现行
`TITMAS Commercial Agent Infrastructure` 身份，也不授权任何实现或运行效果。

## 2. Reused constitutional principles

### ADR-032 — Compositional Scale

复用 ADR-032：不追求单一无限强中心。系统覆盖能力来自大量职责简单、边界有限、可组合
主体及有限治理。必要的协调中心必须可替换、可撤销、可审计，不得因成为关键路径而获得
新的 Truth、Permission 或 Authority。

### ADR-033 — Dynamic Attention

复用 ADR-033：参与者可以按任务、上下文和证据动态选择，关系可以形成、过期和重组。
Attention（注意力）是资源分配和候选参与机制，不是中央控制、授权或事实来源。

### ADR-039 — Evidence-Based Change

复用 ADR-039：上下文、依赖、策略、权限、模型或组合发生实质变化时，早先结论不能静默
继承。重新核验只决定结论是否仍有支撑，不自动撤销权限，也不自动执行修复。

## 3. Proposed constitutional extensions

### DBA-P-COMPATIBILITY-BEFORE-INNOVATION

新增机制前必须完成 source-inspected reuse / overlap / ownership audit（来源核验的复用、
重叠与所有权审计）。可以复用兼容语义、协议或适配器时，不重复建设控制器、Evidence
Truth、Verification、Runtime 或 Provider。兼容性审计不等于采纳外部项目。

### DBA-P-HUMAN-CONSTITUTIONAL-SOVEREIGNTY

Agent、Reviewer、Evaluator、Runtime 和 Domain Owner 都可以提供材料或执行有界动作，
但不能自行修改宪法权威。宪法修正、不可逆效果、正式标准、认证、Release、Deployment
和商业承诺继续要求显式 Human Decision。

### DBA-P-COMPOSITION-ACCOUNTABILITY

组合不是匿名总体。每个参与主体的 identity、task、permission、version、dependency、
evidence 和 responsibility lineage 必须保留。单体 PASS 不自动组成组合 PASS；组合变化
后必须按受影响范围重新评价。

### DBA-P-SHARED-PROTOCOL-NOT-CONTROLLER

DBA 鼓励共享 Schema、reason code、evidence envelope 和 adapter contract，但共享协议不
意味着共享执行器或全局强制控制器。执行和执法留在各 canonical owner（规范所有者）
边界内，并接受共同契约验证。

### DBA-P-REAL-ENVIRONMENT-FEEDBACK

合成测试、本地测试、规范文件、CI PASS 或 Agent review 只能证明精确范围。没有对应的
真实环境证据时，不得声称跨平台执行、规模能力、生产就绪、外部采用或商业价值已证实。

## 4. Parent-child constitutional rule

子项目宪法必须：

1. 声明父级 contract ID 与版本；
2. 可以增加更严格的范围限制；
3. 不得覆盖父级 Authority、Evidence、Truth、Decision、Ownership 或 Human sovereignty；
4. 冲突时失败关闭为 `PARENT_CONSTITUTION_REVIEW_REQUIRED`；
5. 在父级或依赖变化后重新验证继承关系。

## 5. Machine constraints

```text
DISTRIBUTED_COMPLEXITY_GENERATION=true
CENTERS_MAY_EMERGE=true
BOOTSTRAP_CENTER_ALLOWED=true
PERMANENT_ABSOLUTE_CENTER=false
CENTER_MUST_BE_REPLACEABLE=true
CENTER_MUST_BE_AUDITABLE=true
CENTER_IS_NOT_IMMUNE_FROM_EVOLUTION=true
EXISTING_STANDARD_REVIEW_REQUIRED=true
DUPLICATE_CORE_FORBIDDEN=true
PROFILE_BEFORE_CORE_EXPANSION=true
ADAPTER_BEFORE_NEW_RUNTIME=true
GAP_EVIDENCE_REQUIRED_FOR_NEW_DEFINITION=true
HUMAN_OR_ORGANIZATION_IS_FINAL_AUTHORITY=true
AGENT_RECOMMENDATION_NE_AUTHORITY=true
AGENT_CANNOT_SELF_AUTHORIZE=true
CELL_CANNOT_SELF_AUTHORIZE=true
AGENT_CANNOT_AMEND_PARENT_CONSTITUTION=true
CELL_CANNOT_AMEND_PARENT_CONSTITUTION=true
COMPONENT_CONFORMANCE_NE_COMPOSITION_CONFORMANCE=true
COMPOSITION_REQUIRES_REEVALUATION=true
COMPOSITION_GRAPH_REQUIRED_FOR_CONSEQUENTIAL_ACTION=true
COMPOSITE_AUTHORITY_ESCALATION_FORBIDDEN=true
CHANGE_EVENT_REQUIRED=true
SILENT_AUTHORITY_INHERITANCE=false
HIGH_RISK_PERMISSION_REVALIDATION_REQUIRED=true
EVIDENCE_REQUIRED_FOR_TRUST_RESTORATION=true
APPLICABLE_CONSTRAINT_INTERSECTION_REQUIRED=true
HUMAN_APPROVAL_ALWAYS_REQUIRED=false
NOT_APPLICABLE_CONSTRAINT_NE_MISSING_CONSTRAINT=true
UNKNOWN_APPLICABILITY_FAILS_CLOSED=true
SHARED_PROTOCOL_NE_SHARED_CONTROLLER=true
IDENTITY_PLURALISM=true
MULTIPLE_DISCOVERY_PATHS=true
DIRECT_INVOCATION_ALLOWED_WHERE_POLICY_PERMITS=true
REGISTRY_PORTABILITY_REQUIRED=true
VERIFIER_REPLACEABILITY_REQUIRED=true
DOCUMENTED_CAPABILITY_NE_OPERATIONAL_CAPABILITY=true
SYNTHETIC_TEST_NE_EXTERNAL_ADOPTION=true
REAL_GOAL_AND_DEADLINE_EVIDENCE_REQUIRED=true
CAPABILITY_CLAIM_REQUIRES_EXECUTION_EVIDENCE=true
```

## 6. Preserved current facts

本修正案明确保留：

- `DBOS_GOVERNS_EXISTENCE=true`；
- `SAEE_GOVERNS_EVOLUTION=true`；
- C-01 公开产品仍只有 Gate、Receipt、Audit、Health；
- Observer 仍是入口，不是第五个产品；
- D04 继续 `CLOSED_FAILED_RETAINED`；
- P0-10 继续 `FAIL_CLOSED_AFTER_RUNTIME_ALIGNMENT`；
- 历史失败 Receipt 与失败证据不删除、不覆盖、不重写为 PASS。

## 7. Non-effects

```text
HUMAN_ADOPTION_DECISION=APPROVED
EFFECTIVE_TRIGGER=CANONICAL_MAIN_MERGE_OF_PR_142
CANONICAL_REF=refs/heads/main
CONSTITUTION_EFFECTIVE_WHEN_REACHABLE_FROM_CANONICAL_MAIN=true
CURRENT_STRATEGIC_CONSTITUTION_REPLACED=false
IMPLEMENTATION_AUTHORIZED=false
MERGE_AUTHORIZED=true
RELEASE_AUTHORIZED=false
DEPLOYMENT_AUTHORIZED=false
NEW_RUNTIME_CREATED=false
NEW_CONTROL_PLANE_CREATED=false
NEW_TRUTH_SOURCE_CREATED=false
NEW_PRODUCT_CREATED=false
D04_REOPENED=false
P0_10_RESULT_REWRITTEN=false
```
