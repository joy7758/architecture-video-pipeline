# TITMAS 商业测试版验收

| 项目 | 结果 |
|---|---|
| 能做什么 | 用六个合成企业客服案例评测百炼直接模型的回复边界、人工升级、红线、成本、延迟和 Evidence Reference。 |
| 真实调用 | 12 次；无自动重试。 |
| 真实供应商 | 阿里云百炼。 |
| 案例 | 青岚家居 6 个合成企业客服案例。 |
| 重大红线检测 | PASS（逻辑独立执行）。 |
| 证据记录 | PASS（仅现有 Evidence Reference 绑定）。 |
| HTML 报告 | PASS。 |
| JSON 报告 | PASS；与 HTML 同源于 canonical result。 |
| 秘密扫描 | PASS。 |
| 目标测试 | 91 PASSED / 0 FAILED（R1、R2A、商业测试版与 C-01）。 |
| 完整符合性 | 147 PASSED / 0 FAILED；不得以通过替代生产或客户验证。 |
| 可以公开演示 | YES，仅限脱敏合成样例。 |
| 可以给早期客户受控试用 | YES，仅限本地、合成数据与人工服务边界。 |
| 生产就绪 | NO。 |

```text
COMMERCIAL_BETA_READY=true
PRODUCTION_READY=false
CUSTOMER_VALIDATED=false
CERTIFIED=false
```

```text
TITMAS_DRIFT_CHECK
CORE_INTEROPERABILITY_OBJECTIVE_PRESERVED=true
NEW_CONTROL_AUTHORITY_CREATED=false
NEW_TRUTH_SOURCE_CREATED=false
DUPLICATE_EVIDENCE_OR_VERIFICATION_CREATED=false
RUNTIME_OR_EXECUTOR_CREATED=false
CURRENT_CAPABILITY_OVERCLAIMED=false
PUBLIC_LAUNCH_AUTHORIZED=false
COMMUNITY_ESTABLISHED=false
TITMAS_DRIFT_CHECK_RESULT=PASS_WITH_RECORDED_LIMITATIONS
```
