# TITMAS Enterprise Agent Review 商业测试版边界

本文件只定义 `TITMAS Enterprise Agent Review v0.1.0-beta.1` 的产品级边界，不改变 TITMAS 其他私有基础设施、DBOS 或 SAEE 的状态。

## 商业测试版的含义

当发布清单与脱敏合成报告均记录真实百炼直接模型调用时，本工具可以用于公开产品介绍、合成数据演示、设计伙伴的受控试用，以及受控的评测、选型和诊断服务。

它不是生产运行保证、认证、法律合规证明或客户长期验证。

```text
COMMERCIAL_BETA_READY=true
PRODUCTION_READY=false
CUSTOMER_VALIDATED=false
LONG_TERM_VALIDATED=false
SECURITY_CERTIFIED=false
COMPLIANCE_CERTIFIED=false
SLA_AVAILABLE=false

BAILIAN_DIRECT_ADAPTER=LIVE_VERIFIED
DIFY_ADAPTER=OFFLINE_CONTRACT_VERIFIED
DIFY_LIVE_VERIFIED=false
```

本状态仅依据 `0.1.0-beta.1` 的 12 次合成案例直接模型调用，完整结果摘要为
`dceef259a0a9a40ab4ef53229216ac6d35b7d18858412cb6b5b86b29f0351c14`。
它不改变整个 TITMAS 商业基础设施的全局成熟度状态。

## 证据与权限边界

```text
EVIDENCE_NE_TRUTH=true
VERIFICATION_NE_AUTHORIZATION=true
EVALUATION_NE_EXECUTION_AUTHORITY=true
HUMAN_JUDGMENT_REQUIRED_FOR_FINAL_BUSINESS_CONCLUSION=true
HIGH_SCORE_NE_SAFE_TO_DEPLOY=true
```

首版报告把模型输出、规则命中、政策依据、成本、耗时和 Evidence Reference（证据引用）保存为运行材料；它不创建规范 Evidence Object（证据对象）、第二事实源、第二授权链、客户档案、支付系统、在线控制台或运行服务。

## 真实验证门槛

发布前必须同时满足：

1. 6 个合成案例各运行两次，最多 24 次调用；
2. 至少 10/12 次调用产生可解析的规范输出；
3. 累计模型估算成本不超过 20 元人民币；
4. 红线逻辑、Evidence Reference 捕获、HTML 与 JSON 同源和秘密扫描均通过；
5. 脱敏公开样例不含 API Key、认证头、账号/工作空间标识或本机绝对路径。

模型失败保留为评测结果，不会被自动重试或改写。
