# 逐项审查协议 v1

本应用将建筑保真、原演示匹配、技术检查分别记录，由本地协调门禁汇总。审查者可以是一个具备视觉能力的智能体，也可以是共享同版资料的多个有界工位；这些工位不是已注册、激活的 DCell。`review.mjs` 只校验记录和依赖，不运行视觉模型，不判断照片相似度。

## 机器入口

- `jobs/<id>/review-contract.json`：验收范围、来源清单、当前输入、逐项期望。
- `jobs/<id>/review-results.json`：同版合同下的真实观察、证据、限制和问题。
- `pipeline/schemas/review.schema.json`：合同、结果与访问记录的机器 schema；运行时仍逐项校验。
- `node pipeline/cli.mjs review <id>`：输出四组状态、18 项本地必审的覆盖率（鹳雀楼合同）、缺失/未知/失败项。
- `node pipeline/cli.mjs status <id>`：汇总应用阶段；`verify` 的最终发布前闸门仍因真实 TITMAS 未接入而不可通过。

`status` 和 `review` 成功输出 JSON 的退出码为 0；调用者必须读取 `ready` / `ready_for_user_review`，不得将退出码当成验收。

## 合同与当前工件

合同必须列出明确的 `expected`，按 `architectural_fidelity`、`reference_demo_match`、`technical`、`titmas_evidence` 分组。每项有唯一 ID、必需性、严重度、允许引用的 `input_ids` 与所需证据角色。前三组至少各有必需项；两个视觉组各需媒体对照，不能全部改成读文字。TITMAS 项标为 `external:true`，单独保留真实服务门禁。

鹳雀楼合同从倒查 20 项清单派生：9 项建筑、5 项演示、4 项技术、2 项外部 TITMAS。原倒查草案保持冻结，新合同绑定当前资料和历史原输出。该合同的存在不代表任何一项已完成。

每次评价重新计算 `source_checklist` 和全部 `input_bindings` 的 SHA-256。输入包括原图、原演示、用户纠错、原任务、模型计划、当前源码、冻结快照源码、镜头、实际视频与渲染记录。应用另强制合同绑定本 job 当前 request、sources、model-plan、视频清单及实际视频，不能保留旧文件后把旧审查用于另一交付。要求媒体对照的建筑/演示项还必须实际引用当前视频；PNG 可辅助定位。文件头只识别容器，实际解码和语义检查仍需工具及审查者。

新审查专用解析器允许当前 `jobs/<id>/`、`artifacts/`、`docs/`、`app/src/`、指定 app 配置、`vendor/` 与 `pipeline/video/`。拒绝跨 job、绝对路径、路径穿越和越界符号链接；旧协议路径权限保持原样。清单没有登记的新增资料不会自动被发现，收到新纠错后必须先更新规范资料和合同，再执行检查。不要只更改旧结果的哈希来“消除”过期。

## 实际审查步骤

1. 读取合同、原始纠错和上轮问题；确认待审源码/相机/视频版本。以原图约束建筑，以演示约束表现，先明确可观察范围；隐藏立面和没有依据的尺寸保持 UNKNOWN。
2. 使用真实查看工具打开所需原图、实际 MP4 和关键细部。视频的静帧只能证明该帧观察，时序判据还需要相应片段；不得仅凭路径、字幕或他人总结填写已看过。
3. 为每个实际访问保存 `review-access.v1` JSON：`input_id`、`input_sha256`、`method`、`observer_id`、`observed_at`、`trace_reference`。method 为 IMAGE_VIEW / VIDEO_REVIEW / FRAME_EXTRACTION / DOCUMENT_READ，与输入类型匹配；trace_reference 指向实际工具/观察记录。不能预填未来访问或编造回执。
4. 逐项写结果：`criterion_id`、`status`、`reviewer_id`、`reviewed_at`、具体 `observation`、`limitations`、`shared_dependencies`、证据 `input_id + locator + access_record{path,sha256}`、问题 `id/severity/status`。locator 写帧/时间区间/部位/页行等可复查位置。施工者不能自签 PASS；共享模型、资料和工具不代表独立错误源，应写入 shared_dependencies。
5. 问题关闭时提供同版修复依据 `resolution_evidence{path,sha256}`。保留上次 FAIL 与观察；本轮另记修订。协调者复核矛盾和遗漏，不能投票抹去 P1 或 UNKNOWN。
6. 执行 `review` 和 `status`。必需项缺失、UNKNOWN、NOT_RUN、NOT_APPLICABLE、FAIL、未关闭 P1、失效输入、缺访问记录均不能通过。已有视频时会进入 NEEDS_REVISION。

访问记录只是本地自述的观察记录，文件哈希不会证明真实身份、工具真的执行过或模型看懂了图片。它不是 TITMAS 回执，也不是防恶意伪造的认证。服务认证和独立核验仍由后续真实适配器按实际合同承担。

## 状态解释

`review.ready/content_ready=true` 仅表示本地必需逐项记录满足当前合同；不是质量真相或发布授权。TITMAS 组即使写入 PASS，本模块也不能认证。总 `gates.visual` 还要求原视觉检查有效且本地逐项门禁通过；旧 FAIL 不会自动消失。`gates.video` 表示原视频文件/清单完整性，不表示内容获准。技术旧 PASS 只覆盖原视频技术记录。

本轮实际新语义审查仍为 NOT_RUN，18 项本地必审均未填写；2 项 TITMAS 未执行。已知历史建筑与演示问题保持 FAIL。自动测试使用合成文件和观察记录验证控制逻辑，不作为图片、视频质量测评。

## 后续比较与回滚

[A0/C 比较计划](../artifacts/review-gate-20260923-r1/comparison-plan.md) 对比同资料同预算的单一多模态审查与有界分工。计划不是测量结果；当前没有证明多智能体更准、更快或更省钱。

本工作区无 Git 仓库。修改前文件保存在 `artifacts/review-gate-20260923-r1/before/`，清单为 `before-manifest.json`。回滚前先检查当前文件是否被后续任务修改，再仅恢复本批所改文件；不要批量覆盖后续工作。原模型、视频和倒查档案保留。
