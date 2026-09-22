# Happycapy 实体文件交接

这是本地文件快照，不是已上传或已部署的项目。解压后先运行 `python3 verify_handoff.py`，全部哈希匹配后再核对项目。

## 路径映射
- `/Volumes/ORICO_DATA/Projects/3d盖楼` → `project/`
- `/Users/zhangbin/Documents/New project/digital-biosphere-architecture` → `references/dba/`（选定子目录快照，非完整仓库）
- `/Users/zhangbin/GitHub/tiamas-scout` → `references/scout-historical/`（历史副本，无 remote，许可 UNKNOWN）

原证据中的绝对路径和哈希原样保留，不要全局替换历史文件；读取时用以上映射。Git 元数据、依赖目录、构建 dist、缓存与大批渲染 frames 已排除；倒查关键帧、原照片、原演示和交付 MP4 保留。不要声称可以重查未传输的逐帧原文件。excluded-files.json 记录逐文件排除项，目录排除规则见 manifest.json。

## 当前事实与接手顺序
目标是修正通用流水线：客户资料 → 缺口发现补证 → 建筑规划 → Hailey Skill 施工 → 独立视觉检查及真实 TITMAS → 视频 → 用户发布。用户已认可 DCell 模块合同、版本绑定、失效传播方案；不要仅修鹳雀楼。

1. 读 project/AGENTS.md、README.md、agent-index.json、docs/governance/project-intake.json。
2. 读 jobs/guanque-pilot/delivery/current-status.json：NEEDS_REVISION、visual FAIL；旧技术 PASS 仅对应原视频，旧视觉 PASS 已被取代。
3. 读 artifacts/reverse-audit-20260922-r1/report.md 及 index.html；Skill 版本无误，问题主要为建筑细节简化、演示镜头/动画偏差、过低验收门槛与纠错未传入验收。
4. 读 docs/pipeline-dcell-repair-proposal.md、pipeline/REVIEW.md、pipeline/review.mjs、jobs/guanque-pilot/review-contract.json。已有本地记录门禁，不能当作已完成视觉评审。
5. 读 docs/discovery-reuse-assessment.md 和 references/dba/cockpit/REUSABLE-MODULE-CATALOG.zh-CN.md。8 项目录是复用评估，不是8个已激活服务；建筑补证适配器尚未实现。
6. 实现缺口合同、来源/冲突/停止条件、版本依赖与选择性失效；保留 UNKNOWN、失败和历史记录；用鹳雀楼失败用例及第二种建筑验证流水线，再返工模型与出片。

发现层区分找技术模块与补建筑资料；旧 Scout 只搜 GitHub Issue，不能直接补照片/尺寸，许可未核实前仅作设计参考。驾驶舱快照可能有未提交内容，不能宣称等同远端某 commit。TITMAS 未连接本任务；历史“不可用”报告不是当前服务实况，新入口曾被其他任务报告为 https://titmas-api.dcell.net/sandbox/v0.1 ，需要重新核查能力/授权，不含凭据，不能当作视觉认证。

## Linux 起步
在 project/app 运行 npm ci，然后按项目 README 检查和构建。需要 Node >=22.13、浏览器 WebGL2；视频流程另需浏览器和 ffmpeg。原记录中的本地服务地址不会随压缩包迁移。本次只验证包完整性，没有在 Happycapy/Linux 执行项目。
