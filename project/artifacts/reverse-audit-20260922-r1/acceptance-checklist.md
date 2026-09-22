# 鹳雀楼返工验收草案

**这是拟定的返工合同，尚未接入 CLI，不是已经实现的自动门禁，也不构成任何新 PASS。**

机读主文件：[`acceptance-checklist.json`](acceptance-checklist.json)。所有带 SHA-256 的原图、原报告、视频和源码引用均固定到 `frozen/` 或 `checklist-evidence/`。JSON 的 `path` 指审计字节，`original_path` / `target_path` 指施工入口；后续工作区更新不改变本轮历史证据，下一版必须重新绑定。

当前视频继续标为 `PREVIEW_ONLY`；建议当前工作状态为 `NEEDS_REVISION`。历史技术 PASS 与艺术预览 PASS 保留原适用范围；用户已指出外观和 GitHub 演示偏差，不能汇总为“只剩 TITMAS”。

## 关闭规则

- 任一 P1 未关闭，或必要项目仍是 `UNKNOWN`，不得签发建筑保真/演示匹配视觉 PASS。
- 用户否定、资料纠错、Skill/演示、模型、材质、灯光、镜头、视频或合同变更，必须传播为受影响检查失效；保留旧报告，另写取代关系与原因。
- 建筑保真、演示匹配、技术验证、TITMAS 证据分开审查。技术或回执通过不能覆盖视觉失败。
- 未经相机标定，不填写测量容差、像素相似度或尺寸误差；JSON 中全部 `measurement_tolerance=null`。相近机位只能作定性和相对关系检查。
- 原图、私有治理资料仅作本地研究。这里没有新增上传、模型调用、服务恢复或发布操作。

## 建筑保真

### AF-001 · 用户否定与当前资料纠错进入所有下游工位 · P1 / OPEN

预期：新资料包必须包含当前用户纠错及R3状态，标明旧provenance被何版本取代；旧艺术预览PASS保持历史范围，不能压过当前VISUAL_REVIEW_REQUIRED或用户否定；同建筑出现新增纠错时，模型方案、视觉检查、视频交付均明确失效或待复核。

所需视图/证据：冻结资料全文对照；完整依赖清单与当前状态readback。

来源键：`user_rejection`, `source_corrections`, `project_visual_state`, `stale_provenance`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`pipeline/lib.mjs`（evaluateJob）；`pipeline/schemas/contract.schema.json`（$defs）；`pipeline/snapshot-app.mjs`（源码快照输入清单）；`pipeline/render-video.mjs`（固定帧与实际bundle检查）；`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）。

### AF-002 · 照片、文字事实与艺术选择可追溯 · P1 / OPEN

预期：将每个关键形制和尺寸标为observed、source_reported、artistic_choice或unknown；用户转述的73.9m、台基/楼身与开间资料需保留来源级别；缺原始附件不能升格为实测；两张相近正面斜视不代表背面、内部或所有方位已有依据。

所需视图/证据：照片01全景；照片02近景；来源事实表与模型参数映射。

来源键：`photo01`, `photo02`, `reported_dimensions`, `r3`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）；`app/src/heritage/guanque.ts`（TOWER; buildArchitecture; hall; lowerCorridor）。

### AF-003 · 整体轮廓、三层四檐与竖向层次 · P1 / OPEN

预期：先固定完成态轮廓再做材质与镜头；按原图逐项核查三组主要明层、四道主要檐线、上下平座及低暗构架带关系；不能把三层重复大厅或“像鹳雀楼”作为合格依据。

所需视图/证据：正面完成态；两张照片对应的斜正面完成态；可读各层边界的无装饰遮挡图。

来源键：`photo01`, `photo02`, `r3`, `reported_dimensions`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/guanque.ts`（TOWER; buildArchitecture; hall; lowerCorridor）；`app/src/heritage/roof.ts`（hipRoof; ringRoof）；`app/src/heritage/guanque.ts`（TOWER.halls; lowerCorridor; buildArchitecture）；`app/src/PagodaThreeScene.tsx`（相机预设与export相机）；`app/src/export-contract.ts`（ArchitectureExport; ExportFrame）；`pipeline/video/guanque-pilot-wide.json`（shots）。

### AF-004 · 主顶、抱厦、腰檐坡度及接缝 · P1 / OPEN

预期：核查可见瓦坡而非隐藏坡段，主顶高于抱厦的关系由原图支持；主顶与抱厦交接、谷线、屋面厚度和飞檐曲线需在近景可解释；照片R3像素图谱仅供相对关系，不当作测绘标高。

所需视图/证据：屋顶正面与斜侧特写；檐下视图；主頂抱厦交接局部。

来源键：`photo01`, `photo02`, `r3`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/roof.ts`（hipRoof; ringRoof）；`app/src/heritage/guanque.ts`（TOWER.halls; lowerCorridor; buildArchitecture）；`app/src/heritage/guanque.ts`（TOWER; buildArchitecture; hall; lowerCorridor）。

### AF-005 · 平座、承托带、开间与层间比例 · P1 / OPEN

预期：核查两层平座近等宽、顶平座与顶檐相对宽度及支承带连续性；逐项核对下/中层7×5与顶层5×3开间的资料属性和模型映射；避免层间“细脖子”与平座无承托；不把回归常量断言当作照片保真证明。

所需视图/证据：各层平座同机位截图；顶层正面及侧面开间；承托带与檐下近景。

来源键：`photo01`, `photo02`, `r3`, `reported_dimensions`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/guanque.ts`（TOWER; buildArchitecture; hall; lowerCorridor）；`app/src/heritage/facade.ts`（门窗构件与立面工厂）；`app/src/heritage/guanque.ts`（hall; lowerCorridor; PLAQUES; addPlaques）；`app/src/heritage/roof.ts`（hipRoof; ringRoof）；`app/src/heritage/guanque.ts`（TOWER.halls; lowerCorridor; buildArchitecture）。

### AF-006 · 台基、月台、登台阶和栏杆比例/搭接 · P1 / OPEN

预期：按照片区别长短不同登台阶、前伸平台及低楼身台基；检查台阶后缘、栏杆、侧梯与台基的可见连接及遮挡；几何不穿插只证明连接正确；仍须单独比较照片中的宽高与轮廓关系。

所需视图/证据：完整台基斜正面；阶梯接平台局部；两侧梯及栏杆近景。

来源键：`photo01`, `photo02`, `r3`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/guanque.ts`（TOWER; buildArchitecture; hall; lowerCorridor）；`app/src/PagodaThreeScene.tsx`（相机预设与export相机）；`app/src/export-contract.ts`（ArchitectureExport; ExportFrame）；`pipeline/video/guanque-pilot-wide.json`（shots）。

### AF-007 · 门窗、回廊、牌匾位置与可辨识性 · P1 / OPEN

预期：对照朱褐隔扇、后退暗部、向上起拱门头及完整底层回廊；入口横匾与顶层竖匾仅用已定位证据，检查层位、方向与可见尺度；不能用同款白色栅栏替代不同楼层立面。

所需视图/证据：首层正面近景；中层和顶层立面近景；牌匾可读近景。

来源键：`photo01`, `photo02`, `r3`, `source_corrections`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/facade.ts`（门窗构件与立面工厂）；`app/src/heritage/guanque.ts`（hall; lowerCorridor; PLAQUES; addPlaques）；`app/src/heritage/guanque.ts`（TOWER; buildArchitecture; hall; lowerCorridor）；`app/src/heritage/materials.ts`（createHeritageMaterials）；`app/src/PagodaThreeScene.tsx`（scene renderer; lighting; camera）。

### AF-008 · 柱联方位、未见立面及装饰资料不足 · P1 / UNKNOWN

预期：R3记载柱联文本有报道，但挂置立面与西门归属待核；必须补定位证据或从验收范围中显式处理；未见背面、其他方向题字与隐蔽部位保持UNKNOWN，不能镜像复制当作事实；关键可见部位的证据缺口未解决不得把整个外观标为PASS。

所需视图/证据：入口柱联与对应来源方位对照；有新增证据时的侧后面视图。

来源键：`r3`, `reported_dimensions`, `photo01`, `photo02`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/facade.ts`（门窗构件与立面工厂）；`app/src/heritage/guanque.ts`（hall; lowerCorridor; PLAQUES; addPlaques）；`app/src/heritage/guanque.ts`（TOWER; buildArchitecture; hall; lowerCorridor）；`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）。

### AF-009 · 屋瓦、斗栱彩画、屋脊鸱吻与材料观感 · P1 / OPEN

预期：依据实景对照灰青瓦与绿剪边、木色立面、石台和栏杆的颜色/粗糙度/尺度感；记录斗栱彩画、屋脊鸱吻及格心的实际差异；不得仅以“艺术简化”关闭用户指出的偏差；先修可见几何、屋面厚度和支承，再加装饰密度；不能以雾、亮度或滤镜遮盖。

所需视图/证据：相同光照设置下的全景；屋瓦与檐下特写；斗栱彩画及屋脊特写。

来源键：`photo01`, `photo02`, `r3`, `skill`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/materials.ts`（createHeritageMaterials）；`app/src/PagodaThreeScene.tsx`（scene renderer; lighting; camera）；`app/src/heritage/roof.ts`（hipRoof; ringRoof）；`app/src/heritage/guanque.ts`（TOWER.halls; lowerCorridor; buildArchitecture）；`app/src/heritage/facade.ts`（门窗构件与立面工厂）；`app/src/heritage/guanque.ts`（hall; lowerCorridor; PLAQUES; addPlaques）；`app/src/heritage/guanque.ts`（TOWER; buildArchitecture; hall; lowerCorridor）。

## GitHub演示匹配

### RD-001 · 冻结GitHub演示与明确可迁移的表现规则 · P1 / OPEN

预期：固定指定skill版本、演示原文件hash及已观察关键帧；从演示分别记录构件出现方式、运动距离、节奏、镜头、光照与画面组织；把楼型差异与表现差异分开，不能要求鹳雀楼复制钟楼建筑，也不能以用了skill名称替代效果核对。

所需视图/证据：上游演示全片；上游各结构阶段关键帧；同阶段候选视频对照。

来源键：`upstream_demo`, `skill`, `user_rejection`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）；`pipeline/lib.mjs`（evaluateJob）；`pipeline/schemas/contract.schema.json`（$defs）；`pipeline/snapshot-app.mjs`（源码快照输入清单）；`pipeline/render-video.mjs`（固定帧与实际bundle检查）。

### RD-002 · 施工与拆解动作语义匹配 · P1 / OPEN

预期：按演示观察确认逐构件/逐砌层出现、行程、停留和装配顺序，并映射到新镜头脚本；当前完成态→倒放→重建脚本是已知选择，必须单独检验是否满足用户要求的上游效果；如果需要真正分层爆炸拆解，另订构件组位移与层间关系；倒放不能直接签成已实现。

所需视图/证据：每个结构阶段的连续短片；拆解段与重建段逐帧对照；关键支承形成前后截图。

来源键：`upstream_demo`, `skill`, `film_plan`, `prior_model_plan`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/builder.ts`（HeritageBuilder.add; finish; aBuild; uBuildProgress）；`app/src/heritage/guanque.ts`（构件start/duration/lift与支承关系）；`app/src/timeline.ts`（共享进度时序）；`app/src/PagodaThreeScene.tsx`（相机预设与export相机）；`app/src/export-contract.ts`（ArchitectureExport; ExportFrame）；`pipeline/video/guanque-pilot-wide.json`（shots）；`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）。

### RD-003 · 构件粒度、支承依赖与运动连续性 · P1 / OPEN

预期：基座、框架、砌筑、楼面、上层、檐瓦、装饰需有清楚依赖；区别真实承托楼面与晚安装屋面，检查上层是否在支承形成前悬空；逐块运动的可见粒度与演示对照；整层突现/整体缩放/渐隐不自动等价。

所需视图/证据：地基至主体的连续镜头；各层启动点前后帧；檐下与梁柱接点局部。

来源键：`upstream_demo`, `skill`, `prior_visual`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/builder.ts`（HeritageBuilder.add; finish; aBuild; uBuildProgress）；`app/src/heritage/guanque.ts`（构件start/duration/lift与支承关系）；`app/src/timeline.ts`（共享进度时序）；`app/src/heritage/guanque.ts`（TOWER; buildArchitecture; hall; lowerCorridor）；`app/src/heritage/roof.ts`（hipRoof; ringRoof）；`app/src/heritage/guanque.ts`（TOWER.halls; lowerCorridor; buildArchitecture）。

### RD-004 · 镜头节奏、主体占比与细节可读性 · P1 / OPEN

预期：分镜对照上游展示节奏、观看角度、主体尺寸与近景机会；竖屏规格可保留，但必须证明关键构件在最终画幅中可看清；避免只扩大取景而让建筑主体过小；不能只检查没裁切就签镜头效果PASS。

所需视图/证据：上下游完整画幅并排；开场/施工/完成阶段对应帧；最终MP4细节可读抽样。

来源键：`upstream_demo`, `film_plan`, `delivered_video`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/PagodaThreeScene.tsx`（相机预设与export相机）；`app/src/export-contract.ts`（ArchitectureExport; ExportFrame）；`pipeline/video/guanque-pilot-wide.json`（shots）；`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）。

### RD-005 · 演示中的材质、灯光与成品微缩建筑质感 · P1 / OPEN

预期：提炼上游不同材质的色彩、粗糙度、微表面和地面接触关系，再用鹳雀楼资料约束外观；檐下细节可读且有接触阴影，亮度不能吞没细部；具体颜色/曝光/镜头参数属于待比对的艺术参数，当前不填虚构相似度。

所需视图/证据：完成态对应角度；檐下近景；石/木/瓦材质同光照比较。

来源键：`upstream_demo`, `skill`, `delivered_video`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/materials.ts`（createHeritageMaterials）；`app/src/PagodaThreeScene.tsx`（scene renderer; lighting; camera）；`app/src/PagodaThreeScene.tsx`（相机预设与export相机）；`app/src/export-contract.ts`（ArchitectureExport; ExportFrame）；`pipeline/video/guanque-pilot-wide.json`（shots）。

## 技术完整性

### TE-001 · 完整输入依赖与纠错失效传播 · P1 / OPEN

预期：来源、用户纠错、skill、演示、验收合同、模型计划、源码快照、镜头、视频及报告形成可追溯hash图；验证嵌套的provenance.evidence/source_snapshot/render_evidence及其下游有效性；原始资料更新、用户否定或模型/镜头变更后相关视觉/视频审批失效，并保留旧证据。

所需视图/证据：依赖图readback；变更/否定传播的真实门禁负例结果。

来源键：`evaluator`, `source_corrections`, `project_visual_state`, `prior_checks`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`pipeline/lib.mjs`（evaluateJob）；`pipeline/schemas/contract.schema.json`（$defs）；`pipeline/snapshot-app.mjs`（源码快照输入清单）；`pipeline/render-video.mjs`（固定帧与实际bundle检查）；`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）。

### TE-002 · 确定性、装配阴影与实际构建绑定 · P1 / OPEN

预期：新源码先检查数值与时序，再验证实际服务bundle来自指定快照；进度回退、暂停、重播及同帧重访确定；颜色与深度shader同进度；历史技术PASS仅属于旧视频hash；修订后重新检查受影响项，不改写旧记录。

所需视图/证据：0/中间阶段/1进度截图；同帧重访对照；浏览器运行记录与实际bundle hash。

来源键：`skill`, `prior_checks`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`app/src/heritage/builder.ts`（HeritageBuilder.add; finish; aBuild; uBuildProgress）；`app/src/heritage/guanque.ts`（构件start/duration/lift与支承关系）；`app/src/timeline.ts`（共享进度时序）；`app/src/PagodaThreeScene.tsx`（相机预设与export相机）；`app/src/export-contract.ts`（ArchitectureExport; ExportFrame）；`pipeline/video/guanque-pilot-wide.json`（shots）；`pipeline/lib.mjs`（evaluateJob）；`pipeline/schemas/contract.schema.json`（$defs）；`pipeline/snapshot-app.mjs`（源码快照输入清单）；`pipeline/render-video.mjs`（固定帧与实际bundle检查）。

### TE-003 · 实际MP4与交付包一致 · P1 / OPEN

预期：检查新视频完整解码、宽高、帧率、时长、缺帧/异常帧和静音状态；打开实际MP4检查全片及关键帧，不能仅审浏览器或PNG；封面、文案、视频与QA清单绑定同一run；未过门禁交付保持PREVIEW_ONLY。

所需视图/证据：实际新MP4全片；编码元数据；首中末及问题发生时间点截图。

来源键：`delivered_video`, `prior_checks`, `film_plan`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`pipeline/lib.mjs`（evaluateJob）；`pipeline/schemas/contract.schema.json`（$defs）；`pipeline/snapshot-app.mjs`（源码快照输入清单）；`pipeline/render-video.mjs`（固定帧与实际bundle检查）；`app/src/PagodaThreeScene.tsx`（相机预设与export相机）；`app/src/export-contract.ts`（ArchitectureExport; ExportFrame）；`pipeline/video/guanque-pilot-wide.json`（shots）；`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）。

### TE-004 · 独立审查、明确问题与状态汇总 · P1 / OPEN

预期：建筑保真、演示匹配、技术、TITMAS分别记录；审查者不能是对应施工作者；逐项issue_id/严重度/证据/处置；任一P1未关闭或必需项UNKNOWN时不得视觉PASS；总状态必须反映当前用户否定与资料纠错，不能将唯一next_station错误指向TITMAS。

所需视图/证据：新检查逐项记录；聚合状态readback；历史与当前状态并列审计。

来源键：`prior_visual`, `prior_status`, `project_visual_state`, `evaluator`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`pipeline/lib.mjs`（evaluateJob）；`pipeline/schemas/contract.schema.json`（$defs）；`pipeline/snapshot-app.mjs`（源码快照输入清单）；`pipeline/render-video.mjs`（固定帧与实际bundle检查）；`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）。

## TITMAS证据

### TM-001 · 真实服务身份、能力与项目兼容合同 · P1 / UNKNOWN

预期：当前保持NOT_CONNECTED/NOT_RUN，前次网络记录不冒称本次存活检查；接入前取得当前canonical入口、服务版本与真实能力合同，分清公共v1与sandbox/v0.1；仅使用已获项目授权的实际服务能力，不把本地验证器更名成TITMAS。

所需视图/证据：真实服务能力/身份回读；当前尚未取得。

来源键：`titmas_discovery`, `titmas_scope`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）；`pipeline/lib.mjs`（evaluateJob）；`pipeline/schemas/contract.schema.json`（$defs）；`pipeline/snapshot-app.mjs`（源码快照输入清单）；`pipeline/render-video.mjs`（固定帧与实际bundle检查）。

### TM-002 · 真实回执、独立核验与有限结论 · P1 / UNKNOWN

预期：仅在真实服务执行后登记原始回执与独立验证证据，绑定本次来源/模型/镜头/视频/检查摘要；回执完整性或schema通过不代表建筑真实、照片相似或演示效果匹配；身份、签名、版本、过期或摘要不匹配必须拒绝；具体机制以实际合同为准，当前不虚构回执。

所需视图/证据：实际原始回执；独立验证结果及失效负例；当前均无。

来源键：`titmas_scope`, `prior_checks`；冻结路径、原始路径和 hash 见 JSON 的 `source_evidence_registry`。

模型入口：`jobs/guanque-pilot/sources.json`（entries; views; bindings）；`jobs/guanque-pilot/model-plan.json`（recognizable_features; components; assembly; camera; bindings）；`jobs/guanque-pilot/checks.json`（technical; visual; titmas; video）；`pipeline/lib.mjs`（evaluateJob）；`pipeline/schemas/contract.schema.json`（$defs）；`pipeline/snapshot-app.mjs`（源码快照输入清单）；`pipeline/render-video.mjs`（固定帧与实际bundle检查）。

## 下一轮交接

先冻结照片、当前纠错和上游演示的分镜规则，再修完成态几何；建筑静帧逐项审查后再修装配、材质与镜头，最后检查实际新 MP4。每项结论须绑定同版来源、源码、模型计划、相机和视频，记录审查者、差异、未知项及问题关闭原因。

TITMAS 保持 `NOT_CONNECTED/NOT_RUN`，直到真实服务身份、项目兼容合同、实际执行和独立回执验证均有证据。它不能替代照片与视频效果审查。

本清单没有关闭任何项目。共 20 项，均为 `OPEN` 或 `UNKNOWN`。
