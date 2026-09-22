# 3D 建筑拆解视频流水线 · 跨环境交接

这是现有本地项目的私有交接快照。当前鹳雀楼样片状态为 **NEEDS_REVISION / visual=FAIL**；技术通过不等于视觉验收。

先读 [START-HERE.md](START-HERE.md)，运行 `python3 verify_handoff.py` 校验 1080 个文件，再进入 `project/` 工作。主项目、必要驾驶舱资料及旧 Scout 历史副本均已包含；不需要访问原 macOS 磁盘。

- `project/`：源码、锁文件、Skill、参考照片、原演示视频、任务、当前交付视频和审计证据。
- `references/dba/`：驾驶舱选定目录与 8 项可复用模块目录；不是完整仓库。
- `references/scout-historical/`：历史静态参考，许可 UNKNOWN，不能推断可直接采用。
- `manifest.json`：交接文件 SHA-256；它固定初始快照，后续修改应生成新版本，不能伪造旧快照校验成功。

依赖目录、Git 内部数据、dist、缓存和批量渲染帧已排除。完整交接 ZIP 另见仓库 Release；其中同样不含这些排除项。

接手目标：修正通用发现、施工、审核及失效传播流水线；先核对已有 review gate，避免重复实现。详情见 START-HERE.md。无密钥随包提供，外部服务须另行验证和配置。
