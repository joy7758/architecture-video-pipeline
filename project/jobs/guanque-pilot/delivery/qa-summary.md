# 流水线首轮验收

已完成固定源码快照、1080×1920 / 30 fps / 24 秒静音 MP4、封面及文案。模型检查与生产构建通过；服务实际加载的 bundle 与所选快照匹配，源码稳定，同帧重访 3/3 一致。独立审查对实际视频全片解码及六个时间点画面抽样通过。

CLI 的 11 项门禁测试通过。两项独立审查发现已经修复：建筑身份全链绑定；实际服务 bundle 与源码快照匹配。旧 SOURCE_HASH_CHANGED 和错配 bundle 的失败记录保留。

最终状态：PREVIEW_ONLY。来源、模型方案、技术检查、独立艺术视觉检查和视频为 true；TITMAS 为 false。verify 按预期退出 1。

用户选择真实 TITMAS 服务。已从 DBA fetched main 81245d1 定位其 Owner joy7758/titmas-sandbox-gateway；当前登记无可用公共 API，网络核验也未得到有效 JSON 服务合同。没有获取或创建凭据，没有 API POST、TITMAS 回执、服务恢复或发布。恢复接入条件见 pipeline/titmas-handoff.json。

独立推荐：RECOMMENDED_FOR_LOCAL_ARTISTIC_PREVIEW_PIPELINE。它适合由智能体协调的本地艺术预览制作；包含真实 TITMAS 的完整验收链仍未跑通。
