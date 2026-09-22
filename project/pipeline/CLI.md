# 本地任务 CLI 合同

本 CLI 管理任务文件、工位交接和证据门禁。操作员在对话中使用真实检索、施工、浏览器及检查工具；CLI 不自行抓网页、调用模型或冒充 TITMAS。需要 Node.js 22 或更新版本，无额外 npm 依赖。

## 命令

从仓库根目录运行。下列命令是模板，不会自动替用户下单某栋建筑。

```sh
node pipeline/cli.mjs init --id <slug> --building <建筑名称> --location <所在地> --era <建筑时代或版本>
node pipeline/cli.mjs status <slug>
node pipeline/cli.mjs review <slug>
node pipeline/cli.mjs handoff <slug>
node pipeline/cli.mjs verify <slug>
node --test pipeline/test/*.test.mjs
```

`init` 创建 `jobs/<slug>/request.json`、`sources.json`、`model-plan.json`、`checks.json`，已有目录一律拒绝覆盖。`status` 输出 JSON，新增 `review` 字段；`review` 命令仅输出该字段，成功输出仍不等于通过。`handoff` 只将有序 Markdown 工位提示输出到 stdout；调用者可以保存该内容或用于派发。`verify` 重新读取所有当前文件并计算哈希；只有 `READY_FOR_USER_REVIEW` 返回退出码 `0`，门禁未通过返回 `1`，参数或根任务读取错误返回 `2`。目前可信 TITMAS 适配器未实现，`verify` 必然不能返回通过。`status` 成功读取任务返回 `0`，不表示门禁通过。

任务 ID 是 1–64 位小写 ASCII 字母、数字及内部连字符，禁止路径字符。名称、位置与时代各最多 500 字符；未知位置或时代明确记 `UNKNOWN`。用户名称是数据，不能据此执行命令。

## 文件引用与哈希

每个证据引用均为 `{"path":"jobs/<id>/evidence/filename.png","sha256":"64位小写十六进制"}`。路径从**仓库根目录**起算，仅允许当前 `jobs/<id>/` 或项目 `artifacts/` 内的文件；拒绝绝对路径、反斜杠、`.`、`..`、空路径段和越界符号链接。文件必须实际存在，哈希对不上即为过期或被改动。任务身份、资料、方案或视频清单改动后，必须重新检查并重新绑定哈希，不能直接把旧检查结果改成新哈希。

来源包（存在 entries 时）、READY 方案、视频清单及 PASS 检查必须分别使用 `bindings.request_sha256` 绑定当前 `request.json` 的完整字节。更改建筑名称、地点、时代等任务字段，会使旧证据链全部失效并进入 `NEEDS_REVISION`，不能把另一栋建筑的旧视频改名后继续验收。

SHA-256 绑定是完整性检查，并不证明来源真实性、检查者身份或建筑准确性。图片校验支持 PNG/JPEG/WebP 文件头；视频校验支持 MP4/WebM 容器头。真正的解码、画面及播放检查仍由工具和独立检查者执行并保留证据。

## request.json

```json
{
  "schema_version": "1.0",
  "id": "building-demo",
  "building": {"name": "由用户指定", "location": "UNKNOWN", "era": "UNKNOWN"},
  "created_at": "2026-09-22T12:00:00Z",
  "intent": "LOCAL_ARTISTIC_ARCHITECTURAL_BREAKDOWN_VIDEO",
  "publication": "USER_ONLY",
  "measured_accuracy_claim": false
}
```

## sources.json

```json
{
  "schema_version": "1.0",
  "job_id": "building-demo",
  "bindings": {"request_sha256": "当前request.json实际SHA256"},
  "entries": [
    {"id": "source-1", "source_type": "WEB", "title": "实际资料标题", "url": "https://example.org/building", "accessed_at": "2026-09-22T12:00:00Z", "license": {"usage": "RESEARCH_ONLY", "publish_permission": "UNKNOWN"}}
  ],
  "views": [
    {"id": "front", "source_id": "source-1", "angle": "front", "image": {"path": "jobs/building-demo/reference/front.jpg", "sha256": "填写实际SHA256"}},
    {"id": "side", "source_id": "source-1", "angle": "side", "image": {"path": "jobs/building-demo/reference/side.jpg", "sha256": "填写实际SHA256"}}
  ],
  "notes": ["上述示例 URL 和哈希均为占位，不能形成通过证据。"]
}
```

至少需要两个不同视角、不同 SHA-256 的真实本地图片；角度标签不能为 `UNKNOWN`。每幅图需要能追溯到来源条目。所有来源记录标题、ISO 访问时间和许可。`source_type: "WEB"`（省略时默认值）必须记录真实 HTTP(S) URL；`source_type: "USER_PROVIDED"` 使用 `provenance: {"task_id":"原任务ID", "note":"原附件和接收背景说明"}`，不要求虚构网络 URL。用户提供图片仍须有真实本地引用及哈希，且不意味着用户拥有图片发布权。

照片默认 `RESEARCH_ONLY`（仅研究），`publish_permission` 为 `UNKNOWN`、`ALLOWED` 或 `DENIED`；研究门禁不授予图片再发布许可。模型可使用程序化材质，参考照片不要进入公开视频或网页素材，除非另行核清许可。`request.building.location` 或 `era` 为 `UNKNOWN` 时，发现层也未完成，不能进入 `READY_TO_BUILD`。

## model-plan.json

```json
{
  "schema_version": "1.0",
  "job_id": "building-demo",
  "status": "READY",
  "builder_id": "实际施工者身份",
  "skill": "lhlGitHub/threejs-architecture-effects",
  "bindings": {"request_sha256": "当前request.json实际SHA256", "sources_sha256": "当前sources.json实际SHA256"},
  "recognizable_features": ["参考图能支持的标志特征"],
  "components": ["构件及程序参数/源码入口"],
  "assembly": ["可重复的施工先后顺序和时间"],
  "camera": ["镜头时间、位置和目标"],
  "limitations": ["艺术重现，不是测绘复原或结构仿真"]
}
```

初始状态是 `DRAFT`。只有完整记录上述五个非空字符串数组、实际施工者、指定 Skill 和当前来源哈希，才可成为有效 `READY` 方案。

## checks.json

`technical` 与 `visual` 使用相同字段。`PASS` 必须来自实际检查，不能从预期结果推断；`NOT_RUN`、`UNKNOWN`、`FAIL` 均不通过。视觉检查者不能与 `builder_id` 相同，其第一份证据必须是真实图片截图，并且来源包必须已有至少两个视角。以下示例保留初始值：

```json
{
  "schema_version": "1.0",
  "job_id": "building-demo",
  "technical": {"status": "NOT_RUN", "reviewer_id": "UNASSIGNED", "checked_at": null, "evidence": [], "bindings": {"request_sha256": null, "sources_sha256": null, "model_plan_sha256": null, "video_manifest_sha256": null}, "findings": []},
  "visual": {"status": "NOT_RUN", "reviewer_id": "UNASSIGNED", "checked_at": null, "evidence": [], "bindings": {"request_sha256": null, "sources_sha256": null, "model_plan_sha256": null, "video_manifest_sha256": null}, "findings": []},
  "titmas": {"status": "NOT_CONNECTED", "connector_id": null, "raw_receipt": null, "independent_verification": {"status": "NOT_RUN", "verifier_id": null, "evidence": null}},
  "video": {"status": "NOT_RUN", "manifest": null}
}
```

检查通过时记录实际 `reviewer_id`、ISO `checked_at`、`evidence` 引用数组和四个当前 SHA-256（任务、来源、方案、视频清单）。所有视觉/技术通过结果都绑定**最终视频清单**，因此可以先生成预览，再检查成片，最后记录结果。`findings` 使用字符串数组，记录适用边界、未确认点或改进建议；结论失败时写 `FAIL`。

生成视频后将 `video.status` 设为 `RENDERED`，并设置 `video.manifest` 文件引用。视频清单路径通常是 `jobs/<id>/video-manifest.json`。

TITMAS 当前必须保持 `NOT_CONNECTED`。手工填入 `PASS`、伪造 connector 名称或添加回执文件都不会通过。未来正式适配器必须验证已登记的服务身份、实际原始回执，以及独立验证者对回执和本任务内容的核验；单独修改任务 JSON 不能开启门禁。本地其它检查工具的结果不能冒充 TITMAS 服务。

## video-manifest.json

```json
{
  "schema_version": "1.0",
  "job_id": "building-demo",
  "status": "RENDERED",
  "video": {"path": "jobs/building-demo/output/preview.mp4", "sha256": "实际视频SHA256"},
  "poster": {"path": "jobs/building-demo/output/poster.png", "sha256": "实际图片SHA256"},
  "spec": {"duration_seconds": 24, "fps": 30, "width": 1920, "height": 1080},
  "bindings": {"request_sha256": "当前request.json实际SHA256", "sources_sha256": "当前sources.json实际SHA256", "model_plan_sha256": "当前model-plan.json实际SHA256"}
}
```

`poster` 可省略。视频必须是实际 MP4/WebM，规格为正数、宽高为正整数。清单绑定任务、来源与方案，再由 checks 引用清单当前哈希。清单允许增加渲染器版本、命令、源码快照或 ffprobe 结果等记录。

## 阶段语义

| 阶段 | 含义 |
| --- | --- |
| `DRAFT` | 初始化且尚无资料或执行记录 |
| `NEEDS_REFERENCE` | 已开始准备但参考图、来源或许可记录不足 |
| `READY_TO_BUILD` | 来源与施工方案完整；继续施工或检查 |
| `NEEDS_REVISION` | 文件不合法、哈希过期、检查失败、自签视觉或方案未就绪 |
| `PREVIEW_ONLY` | 存在有效预览视频；仍须看 `gates` / `blockers`，不等于验收通过 |
| `READY_FOR_USER_REVIEW` | 预留给全部检查通过及可信 TITMAS 已接入的未来版本；当前不可达 |

已有 `RENDERED` 视频或宣称视觉 PASS 时，必需逐项审查缺失/无效会进入 `NEEDS_REVISION`。尚未出片的初始 DRAFT/READY_TO_BUILD 保留原语义。

优先级：完整性/失败错误 → `NEEDS_REVISION`；否则有有效视频 → `PREVIEW_ONLY`；否则按资料和方案推导阶段。`PREVIEW_ONLY` 仍须查看具体门禁，逐项审查未通过的成片已由新门禁转为 `NEEDS_REVISION`；用户可以查看视频，这不将未知项改成通过。发布始终由用户执行。

机器可发现合同在 `pipeline/schemas/contract.schema.json`。运行时由零依赖 `lib.mjs` 执行必要字段及证据完整性检查，未嵌入通用 JSON Schema 验证器。


## 逐项审查扩展

见 [REVIEW.md](REVIEW.md) 与 `pipeline/schemas/review.schema.json`。运行时由 `review.mjs` 校验。旧 schema 与字段继续保留；新增合同和结果采用独立版本，不把 schema 文件存在当作运行时校验。已声明的 `provenance.evidence`、`source_snapshot`、`render_evidence` 引用也验证其实际文件哈希。逐项合同另外直接绑定当前工作源码和冻结快照文件，以检测只改快照内容、未改 manifest 的情况。
