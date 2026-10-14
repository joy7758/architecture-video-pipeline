# 初始化模板

`node pipeline/cli.mjs init --id <slug> --building <name>` 是模板的唯一生成入口，直接生成四个完整初始 JSON 文件；不复制可能过期的示例任务，也不创建用户未下单的建筑。

字段说明见 `../CLI.md`，机器合同见 `../schemas/contract.schema.json`。模板默认没有来源、没有检查结果、没有视频，TITMAS 为 `NOT_CONNECTED`。所有真实证据必须由执行工位后填入。
