# TITMAS Project Constitution: Unified Entry and DCell Amendment v0.1

中文：TITMAS 项目宪法：统一入口与 DCell 修正案 v0.1

- Status: `ACCEPTED_EFFECTIVE_ON_CANONICAL_MERGE`
- Contract ID: `TITMAS-PROJECT-CONSTITUTION-COHERENCE-v0.1`
- Parent contract: `DBA-MAIN-CONSTITUTION-COHERENCE-v0.1`
- Machine contracts:
  - [`titmas-project-constitution.json`](titmas-project-constitution.json)
  - [`dcell-module-governance-profile.json`](dcell-module-governance-profile.json)
- Human adoption decision: `APPROVED`
- Effective trigger: `CANONICAL_MAIN_MERGE_OF_PR_142`
- Canonical ref: `refs/heads/main`
- Candidate branch authority effect: `NONE`
- Implementation authorization: `false`

## 1. Constitutional inheritance

TITMAS 继承 DBA 主宪法。TITMAS 可以针对 action control（行动控制）、execution evidence
（执行证据）、Receipt、Audit、Health 和跨平台互操作增加更严格约束，但不能覆盖 DBA、
DBOS、SAEE、Human Owner 或 Agent Evidence 的规范所有权。

```text
TITMAS_INHERITS_DBA=true
TITMAS_MAY_OVERRIDE_DBA=false
DBOS_GOVERNS_EXISTENCE=true
SAEE_GOVERNS_EVOLUTION=true
AGENT_EVIDENCE_OWNS_EXECUTION_EVIDENCE_SEMANTICS=true
```

## 2. TITMAS role

TITMAS 的候选宪法角色是：

- 对跨 Runtime 的机器契约进行一致性约束；
- 定义有界执行前检查和失败关闭语义；
- 对上下文、组合、策略和证据变化要求重新核验；
- 连接兼容 Evidence、Receipt、Verification 与 Evaluation 接口。

TITMAS 不是 Agent Runtime、基础模型、Truth Source、最终 Authority、通用编排器或认证
机构。它不拥有 DBOS 的存在事实，也不拥有 SAEE 的演化评价算法。

```text
TITMAS_ROLE=CROSS_PLATFORM_CONSTITUTIONAL_ENFORCEMENT_REVALIDATION_AND_EVIDENCE_INTEROPERABILITY
TITMAS_IS_AGENT_RUNTIME=false
TITMAS_IS_MODEL_PROVIDER=false
TITMAS_IS_FINAL_TRUTH_SOURCE=false
TITMAS_IS_FINAL_CONSTITUTION_AUTHORITY=false
```

## 3. Unified entry without centralized control

Unified entry（统一入口）是逻辑契约目标：Human 和 Agent 应能通过一致的 discovery、
catalog、schema、preflight、reason code 和 receipt verification 路径理解系统。

它不表示：

- 所有 Runtime 必须通过一个全局网关；
- 建立物理单点控制中心；
- TITMAS 可以替各 Domain Owner 执行策略；
- 统一入口已经实现或通过真实跨平台验证。

执行前检查和证据核验可以由 Gateway、sidecar、CI adapter、MCP adapter 或其他未来接入点
分布式实施，但每个接入点必须保留同一机器契约、Owner、版本、权限和 Evidence lineage。

```text
DEFAULT_UNIFIED_ENTRY_GOAL=true
GLOBAL_MANDATORY_ENTRY_CLAIM=false
LOGICAL_UNIFIED_ENTRY=true
PHYSICAL_SINGLE_GATEWAY_REQUIRED=false
DISTRIBUTED_ENFORCEMENT_REQUIRED=true
SOVEREIGN_CENTRAL_RUNTIME=false
```

## 4. DCell module governance

DCell 是可组合数字主体模块的候选治理概念。它可以采用 skill-like selection（技能式
选择），但必须达到 cell-grade governance（细胞级治理）：

```text
Skill
  -> Capability Module
    -> DCell Candidate
      -> Ecological DCell
```

分类不授予 Permission。升级到更高分类需要另行定义的 Evidence、评价和 Human Decision；
本修正案不创建实例、Catalog、Resolver、Runtime 或 Marketplace。

```text
DCELL_MODULE_SELECTION_ALLOWED=true
SKILL_LIKE_SELECTION_EXPERIENCE=true
CELL_GRADE_GOVERNANCE_REQUIRED=true
CELL_SELECTION_NE_AUTHORIZATION=true
CELL_INSTALLATION_NE_ACTIVATION=true
CELL_ACTIVATION_NE_EXTERNAL_EFFECT_PERMISSION=true
```

### Minimum contract

每个候选模块至少声明：

- `cell_id`、`logical_identity`、`version`、`provider_or_operator`；
- `capability_contract`、`input_contract`、`output_contract`；
- `allowed_actions`、`forbidden_actions`；
- `required_data`、`data_retention`、`external_side_effects`；
- `evidence_obligations`、`lifecycle_state`；
- `upgrade_path`、`rollback_path`、`replacement_semantics`、`revocation_path`；
- `known_limitations`。

### Activation classes

- `MANDATORY`：仅可由已采纳宪法或策略明确要求；
- `POLICY_REQUIRED`：仅在匹配策略与有效授权时要求；
- `USER_SELECTABLE`：Human 可在有效权限交集内选择；
- `EXPERIMENTAL`：默认不进入生产链路，且不得继承稳定结论。

自然语言请求只能形成 selection proposal（选择建议），不能直接激活模块。

Mandatory Constitutional Cells 至少表达 Constitution Gate、Identity and Version Binding、
Minimum Receipt 与 Authorization Reference 四项逻辑能力。普通用户不能关闭这些能力，
但不要求每项能力成为独立进程或仓库。Experimental Cells 默认仅允许 `SANDBOX`、
`SHADOW`、`MONITOR` 或 `CANARY`，不自动获得高风险生产权限。

Policy-Required Cells 可以包括 Evidence Verification、Context Assurance、Human Approval
与 Audit；是否启用由父级宪法、组织规则、任务风险和司法辖区决定。User-Selectable Cells
可以包括 AHRP Memory、Health、Drift Watch、Research 与 Cost Optimization，但这些名称
只是分类示例，不声明当前已有实现或实例。

### Permission intersection

```text
effective permission
= intersection of all applicable constraints
  (parent constitution
   ∩ organization policy
   ∩ role policy
   ∩ task authorization
   ∩ agent boundary
   ∩ DCell boundary
   ∩ current context
   ∩ Human approval when applicable)
```

这里的“适用”必须显式判断：不适用约束不等于缺失约束；无法判断约束是否适用时，必须
`NOT_ASSESSED` 并失败关闭。Human approval（人工审批）不是每次行动都无条件要求；只有
组织策略、风险等级、行动类别或显式升级规则要求时才成为适用约束。有效 standing
authorization（常设授权）只有在策略明确允许且当前 scope、期限和绑定均有效时，才可满足
对应审批义务。

决策结果必须区分：

- `ALLOW_OR_READY`：全部适用约束满足，且没有待满足的审批义务；它不是执行结果；
- `NEEDS_APPROVAL`：审批已成为适用约束，但缺少有效、匹配且未过期的审批；
- `BLOCK`：存在适用的不可覆盖拒绝，或某项适用约束明确不满足；
- `NOT_ASSESSED_AND_FAIL_CLOSED`：适用性或必需输入未知，不得继续。

一次性审批必须绑定 principal、Agent及版本、task、action及resource、constitution version、
适用时的 composition digest，以及 scope 与 expiry。它不能扩大父级宪法，也不能覆盖
non-overridable deny（不可覆盖拒绝）。组合不聚合 Authority，新增、移除、更新或重组
模块后必须重新评价受影响组合。

```text
APPLICABLE_CONSTRAINT_INTERSECTION_REQUIRED=true
HUMAN_APPROVAL_ALWAYS_REQUIRED=false
HUMAN_APPROVAL_REQUIRED_WHEN_POLICY_REQUIRES=true
HUMAN_APPROVAL_REQUIRED_WHEN_RISK_CLASS_REQUIRES=true
HUMAN_APPROVAL_REQUIRED_WHEN_ACTION_CLASS_REQUIRES=true
HUMAN_APPROVAL_REQUIRED_ON_EXPLICIT_ESCALATION=true
NOT_APPLICABLE_CONSTRAINT_NE_MISSING_CONSTRAINT=true
UNKNOWN_APPLICABILITY_FAILS_CLOSED=true
ONE_TIME_APPROVAL_CAN_EXPAND_PARENT_CONSTITUTION=false
ONE_TIME_APPROVAL_CAN_OVERRIDE_NON_OVERRIDABLE_DENY=false
```

高影响任务必须能够导出或复用 `COMPOSITION_GRAPH`、`AUTHORITY_GRAPH`、
`DATA_FLOW_GRAPH` 与 `EVIDENCE_GRAPH`。安全单体的组合不自动等于安全组合；必须检查数据
流、副作用、循环调用、智能体互相批准和组合式权限升级。

## 5. Change revalidation

DCell 版本、Provider、Operator、模型、Skill、工具、输入输出契约、数据范围、存储位置、
司法辖区、外部副作用或 Adapter 变化时，必须形成：

```text
CHANGE_DETECTED
  -> HIGH_RISK_PERMISSION_SUSPENDED
  -> CONTRACT_DIFF
  -> CONSTITUTIONAL_PREFLIGHT
  -> SYNTHETIC_SHADOW_OR_CANARY_TEST
  -> RESTORE_LIMIT_QUARANTINE_OR_ROLLBACK
DCELL_CHANGE_REQUIRES_REVALIDATION=true
NEW_DCELL_VERSION_AUTOMATIC_HIGH_RISK_INHERITANCE=false
CONTRACT_BREAK_REQUIRES_NEW_VERSION_OR_LINEAGE=true
UPGRADE_RECEIPT_REQUIRED=true
```

## 6. Usability as a constitutional safety property

Agent-first 不等于只提供底层 Schema。面向首次价值的入口必须：

- 提供稳定机器契约，以及使用显式声明的 principal locale 或 market locale 的可理解 Human 说明；
- 不要求用户先掌握隐藏 CLI、猜测 Schema 或手工复制秘密；
- 明确失败原因、修正路径、限制和是否需要 Human Decision；
- 保留 `NOT_ASSESSED`，不得为了简单而伪造 PASS。

基础宪法不硬编码任何全球 Human locale。机器 contract 与本地化解释必须并存，关键状态
不能只显示机器代码。中国市场继续通过现有 C-01 Human entry surface 的 `CHINA` 市场
Profile 默认 `zh-CN` 和简体中文；英文 reason code 可以保留，但必须同时提供中文解释。
这是一项入口设计约束，不授权网站、Console、SDK、MCP、国际化系统或 Runtime 修改。

自然语言规则必须依次经过结构化候选、声明 locale 的等价回显、主体和范围、冲突／空白／例外检查、
合成测试、Human confirmation、签名与版本发布。自然语言不得直接生效。

```text
USABILITY_IS_CONSTITUTIONAL_REQUIREMENT=true
USABILITY_IS_SAFETY_PROPERTY=true
HUMAN_READBACK_MUST_BE_COMPREHENSIBLE=true
HUMAN_READBACK_MUST_USE_DECLARED_PRINCIPAL_OR_MARKET_LOCALE=true
LOCALE_MUST_BE_EXPLICITLY_DECLARED=true
CRITICAL_STATUS_MUST_NOT_BE_MACHINE_CODE_ONLY=true
MACHINE_CONTRACT_AND_LOCALIZED_EXPLANATION_MUST_COEXIST=true
GLOBAL_HARDCODED_HUMAN_LOCALE=false
MARKET_PROFILE=CHINA
CHINA_MARKET_UI_DEFAULT=SIMPLIFIED_CHINESE
DEFAULT_HUMAN_LOCALE=zh-CN
CRITICAL_STATUS_REQUIRES_CHINESE_EXPLANATION=true
ENGLISH_REASON_CODE_MAY_BE_RETAINED=true
ENGLISH_REASON_CODE_REQUIRES_CHINESE_EXPLANATION=true
CLI_REQUIRED_FOR_FIRST_VALUE=false
MANUAL_SCHEMA_EDIT_REQUIRED=false
LONG_LIVED_SECRET_PASTE_REQUIRED=false
PROGRESSIVE_DISCLOSURE=true
REVERSIBLE_ACTIONS_VISIBLE=true
NATURAL_LANGUAGE_RULE_DIRECT_ACTIVATION=false
HUMAN_READBACK_REQUIRED=true
CONFLICT_DETECTION_REQUIRED=true
SYNTHETIC_TEST_REQUIRED=true
SIGNED_HUMAN_APPROVAL_REQUIRED=true
```

## 7. Product boundary

产品数量保持为四：

1. TITMAS Gate；
2. TITMAS Receipt；
3. TITMAS Audit；
4. TITMAS Health。

Observer 是入口层，DCell 是模块治理层，二者均不是第五个产品。

```text
C01_STABLE_ID_PRESERVED=true
C01_MEANING_PRESERVED=true
FIRST_VALUE_BEFORE_ENFORCEMENT=true
MONITOR_BEFORE_ENFORCE=true
PUBLIC_PRODUCT_COUNT=4
DCELL_LAYER_IS_FIFTH_PRODUCT=false
OBSERVER_IS_FIFTH_PRODUCT=false
```

## 8. Non-claims and retained failures

```text
TITMAS_INHERITS_DBA=true
TITMAS_MAY_OVERRIDE_DBA=false
TITMAS_IS_FINAL_CONSTITUTION_AUTHORITY=false
HUMAN_ADOPTION_DECISION=APPROVED
EFFECTIVE_TRIGGER=CANONICAL_MAIN_MERGE_OF_PR_142
CANONICAL_REF=refs/heads/main
CONSTITUTION_EFFECTIVE_WHEN_REACHABLE_FROM_CANONICAL_MAIN=true
IMPLEMENTATION_AUTHORIZED=false
UNIFIED_AGENT_ENTRY_IMPLEMENTED=false
SELECTABLE_DCELL_LIBRARY_IMPLEMENTED=false
CROSS_PLATFORM_ENFORCEMENT_PROVEN=false
EIGHTY_AGENT_SCALE_PROVEN=false
PRODUCTION_READY=false
COMMERCIAL_OFFERING_AVAILABLE=false
REAL_CUSTOMER_ADOPTION_PROVEN=false
D04_CLOSED_FAILED_RETAINED=true
P0_10_FAIL_CLOSED_RETAINED=true
HISTORICAL_RECEIPT_FAILURES_RETAINED=true
```
