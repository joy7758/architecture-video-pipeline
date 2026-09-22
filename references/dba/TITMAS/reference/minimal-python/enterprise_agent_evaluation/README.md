# TITMAS Enterprise Agent Review

TITMAS 企业智能体实战评测帮助企业先用合成场景测试一套 AI 智能体方案是否值得进入下一步：它不只看回复是否流畅，还保留何时应交给人工、是否触及业务红线、实际成本、响应时间与证据引用。

它是本地、受控的专业评测工具，不是 Agent Runtime（智能体运行时）、自动执行器、认证服务或公共 SaaS（软件即服务）后台。

## 三分钟快速开始

在本目录的上一级 `TITMAS/reference/minimal-python/` 中运行：

```bash
export DASHSCOPE_API_KEY='仅在本机环境变量中设置'
export DASHSCOPE_BASE_URL='https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
export TITMAS_LIVE_TESTS=1

python -m enterprise_agent_evaluation preflight
python -m enterprise_agent_evaluation review --provider bailian-direct --output-dir ./titmas-review-output
python -m enterprise_agent_evaluation report --result ./titmas-review-output/titmas-enterprise-agent-review.json --output-dir ./titmas-review-output
```

随后直接在浏览器打开 `titmas-review-output/titmas-enterprise-agent-review.html`。

默认使用滚动模型别名 `qwen3.7-max`。如当前账号可用，可通过 `TITMAS_BAILIAN_MODEL=qwen3.7-max-2026-05-20` 选择固定快照；报告会如实记录 `SNAPSHOT_PINNED`、`ROLLING_ALIAS` 或不可观察限制。

## 本版本包含

- 阿里云百炼直接模型调用：无需创建百炼 Workflow、知识库或 Dify；
- 青岚家居 6 个完全合成的企业客服案例，每个运行两次；
- 严格四行输出合同、无自动重试与 24 次调用 / 20 元人民币上限；
- 红线、政策依据、人工升级、成本、延迟和现有 Evidence Reference 的统一结果；
- 从同一个 canonical result（规范结果对象）生成 JSON 与独立 HTML 报告。

## 安全与边界

- API Key 只从本机环境变量读取，不写入仓库、报告或样例。
- 默认场景只允许合成数据；不得提交客户、个人、机密或生产数据。
- Evidence Reference（证据引用）不等于 Truth（真相）；评测不产生执行权限。
- 自动暂定评估不等于人工最终裁决；高分不等于可部署。
- Dify 适配器保留为 `OFFLINE_CONTRACT_VERIFIED`，并非本版真实调用的前置条件。

完整发布状态与当前不能声称的内容见 [商业测试版边界](COMMERCIAL-BETA-BOUNDARY.md)。

## 本周研究的实验性兼容评测

本目录还包含三个只使用合成数据、可重复运行的实验性评测单元：

- `constraint_survival.py`：分别检查约束内容、强制力、授权主体、不可验证时的回退以及最终效果约束是否存活；
- `execution_outcome_projection.py`：把“命令被接受、执行完成、系统报告、现实效果、稳定结果”分层记录；它是引用既有 EEOAP statement（执行证据声明）的 sidecar（旁路投影），不修改 EEOAP v0.1 核心；
- `evaluation_integrity.py`：把证据不足、语义无依据、不可比较、不可识别和主动放弃表示为 typed stop（类型化停止），并把答案正确性与轨迹有效性分开。

运行全部本地测试：

```bash
python3 -m unittest discover -s enterprise_agent_evaluation/tests -p 'test_*.py' -v
```

这些单元只生成评测结果和兼容投影，不生成数字排名，不创建执行权限、Agent Runtime、Evidence Truth（证据真相源）或发布授权。高分、`PASS` 或“效果已观察”都不能单独升级为部署、合规、生产稳定性或认证结论。
