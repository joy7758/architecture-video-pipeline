# 3D 盖楼 · 建筑视频流水线

本对话为总指挥：指定建筑 → 资料发现 → 建筑规划 → Hailey Skill 施工 → 独立检查 / TITMAS → 视频交付 → 用户发布。

**当前鹳雀楼交付需要返工（NEEDS_REVISION）**：照片保真与原演示表现复核未通过，旧艺术预览 PASS 已被取代。原视频与历史记录保留，技术 PASS 不代表外观合格。查看[倒查报告](artifacts/reverse-audit-20260922-r1/report.md)、[可视对照页](artifacts/reverse-audit-20260922-r1/index.html)和[当前交付状态](jobs/guanque-pilot/delivery/current-status.json)。

- 工作方式与工位：[流水线手册](pipeline/README.md)
- 机读任务操作：[CLI 合同](pipeline/CLI.md)，运行 `node pipeline/cli.mjs help`
- 首个任务：[鹳雀楼 pilot](jobs/guanque-pilot/request.json)，运行 `node pipeline/cli.mjs status guanque-pilot`
- 接入事实：[integrations.json](pipeline/integrations.json)。DBA 当前登记的 TITMAS 公共服务不可用；[服务核查](docs/governance/titmas-service-discovery.json)。接通前保持预览状态。

以下是首个样本“鹳雀楼 · 更上一层楼”的交互演示说明。

本地可交互的鹳雀楼营造动画。按现存建筑照片与官方外观描述创作的程序化艺术重现；非测绘复原、结构仿真或考古结论。

## 快速打开

```sh
cd app
npm ci
npm run dev -- --port 4186
```

打开 http://127.0.0.1:4186 。生产检查：根目录 `npm run check && npm run build`；`npm run preview` 在 http://127.0.0.1:4187 提供构建后的页面。
环境：Node.js >=22.13、npm、支持 WebGL2 的桌面浏览器。首次安装依赖需要联网，场景本身不调用模型、不请求外部模型素材。

## 照片对照与当前修订

第三轮逐图审查：[photo-comparison-r3.md](docs/photo-comparison-r3.md)。当前仍需外观审阅，未标记实景复原合格。
本地并排页 http://127.0.0.1:4196/ 提供用户原照片和可旋转模型；可用 `python3 -m http.server 4196 --bind 127.0.0.1 --directory artifacts/photo-audit-r3/view` 重启对照页，同时需运行4187预览服务。

## 操作

- 自动播放约24秒；重新营造从头开始。
- 播放/暂停；拖动施工进度会暂停并定位。
- 0.5× / 1× / 2× 播放速度。
- 拖动旋转、滚轮缩放；全景/正面/门脸与匾额/飞檐细赏切换到建成状态。
- 系统偏好减少动态效果时默认不自动播放。

## 智能体入口

先读 `agent-index.json`。建筑参数与工厂：`app/src/heritage/guanque.ts`；屋面相贯：`roof.ts`；门窗：`facade.ts`；GPU装配与材质批处理：`builder.ts`；纹理：`materials.ts`；镜头与资源生命周期：`PagodaThreeScene.tsx`；交互：`App.tsx`；时间线：`timeline.ts`。
`data-progress`、`data-playing`、`data-view` 和 `.three-scene[data-render-stats]` 提供可读取的观察状态。fps 为 rAF 回调频率；renderFps 是提交重绘次数，不等于 GPU 完成帧率。

## 来源与许可

复用 Hailey 的 MIT Skill 与基础渲染器，版本锁定 `693ca2ec1193e7355054f14d7deb1427439a24d0`。
https://github.com/lhlGitHub/threejs-architecture-effects
原许可保留于 `app/LICENSE` 与 `vendor/architecture-skill/LICENSE`。
建筑模型、场景与界面改造见本项目源码。所有建筑表面纹理由程序生成，参考照片未打包。
- 运城市政府建筑介绍：https://www.yuncheng.gov.cn/doc/2020/07/21/71073.shtml
- 实际查看的正面照片：https://dimg04.c-ctrip.com/images/0EQ5i12000b50n6rx6C4F_W_640_10000.jpg?proc=autoorient

## 验证与限制

`npm run check` 检查几何数值、时间线结束、批处理及重复构建确定性；浏览器观察另见 `docs/verification.md`。
造型采用高台、三层主体、四檐关系与抱厦特征；彩画、屋脊、开间比例均为简化艺术处理。不包含室内陈设、真实结构受力或低端手机性能保证。本地固定帧 MP4 导出见 `pipeline/video/README.md`，视频与 TITMAS 检查分开记录。
治理快照只作为本地参考，见 `docs/governance/project-intake.json`；驾驶舱报备不表示项目组合正式准入或部署。

最近一次用户纠错对照：见 [docs/photo-comparison.md](docs/photo-comparison.md)。上一版楼层檐口、顶层开间、首层回廊和匾额问题已修正；未知楹联不补写，局部装饰仍简化。
