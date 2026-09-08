# awesome-astra-blender-characters

**从人物参考图到可编辑 Blender 角色的 AI Agent 工作流。**

中文 · [English](README.en.md)

本仓库提供可安装的 `blender-character-workflow` 技能，组织九视图参考、脸部与头发制作、局部修模、多视图验收和工程交付，重点是二次元人物与静态插画风格。技能不固定模型版本。

发布内容是技能指令和制作参考文档。仓库暂未提供人物模型、示例渲染、训练权重或一键三维重建程序；安装与检查脚本只服务于技能分发。

## 能力与流程

| 阶段 | 内容 |
| --- | --- |
| 输入检查 | 查看原图和已有工程，确认范围、用途与必须保留的特征 |
| 九视图参考 | 新角色默认生成水平八方向与正上方共九张独立参考，检查方向、尺度与特征 |
| 配准与脸部 | 统一相机与关键点，先做低细节脸型，再完善眼睑眉睫、鼻口、下巴和耳部 |
| 头发与材质 | 主发束、发根覆盖、局部 UV、透明边缘、柔光、腮红与插画质感 |
| 局部修复 | 保留用户修改，定位缺口、穿插、纹理越界与头顶拉伸 |
| 验收交付 | 固定相机对照，分别报告外形、工程和用途检查，打包并重开最终 `.blend` |

局部修模直接进入相关阶段；仅整理文档不生成图片或修改工程。每轮修改比较实际渲染，未改善时重新定位原因。

全身、服装、绑定、动画和打印有按需扩展指导，当前公开包尚未提供这些用途的端到端验证案例。

## 环境与依赖

| 组件 | 何时需要 |
| --- | --- |
| 支持技能、图片查看及本地工具调用的 Agent 环境 | 执行工作流；提供 Codex 界面元数据 |
| 本地 Blender 与内置 Python／CLI | 建模、渲染和工程检查；先检测实际版本，仓库没有已验证的跨版本兼容矩阵 |
| 图像生成工具及 `imagegen` 技能 | 生成九视图或补纹理时；由宿主提供，本仓库不包含 |
| UI 自动化或 Blender MCP | 可选；CLI 可用时不要求 MCP |
| 外部 Python 3.10+ | 使用安装与维护脚本时；手动复制技能不需要 |
| PyYAML | 仅维护检查需要，见 `requirements-dev.txt` |

没有图像生成能力时，可提供已经检查合格的九视图，或明确调整本次视图范围。安装技能不会自动安装 Blender、图像模型或第三方创作软件。

## 安装

下载或克隆本仓库后，在仓库根目录运行：

```bash
python3 scripts/install.py
```

默认复制到用户的 `~/.agents/skills/blender-character-workflow/`。同名目录已存在时，安装器停止并保留原内容；更新前自行备份和移走旧目录。安装器不会启动 Blender、联网或修改 Agent 配置。

安装器只复制 `scripts/install.py` 中 `PACKAGE_FILES` 明确列出的技能文件，排除缓存、本地配置和额外素材，并拒绝包含符号链接的源目录。全部文件先复制到临时目录，成功后再移至目标位置；失败会清理临时产物，允许修复后重试。

也可指定技能父目录，例如目标项目内的 `.agents/skills`，或宿主实际使用的其他技能目录：

```bash
python3 scripts/install.py --destination /path/to/your-project/.agents/skills
```

手动安装时，将整个 `skills/blender-character-workflow/` 文件夹复制到技能目录，保留其中的 `LICENSE` 和原文件夹名称。

Codex 的用户与项目技能路径及发现方式见 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)。安装后若未显示，重新启动 Codex，并检查其他目录是否已有同名技能。

## 使用示例

在支持 `$` 技能引用的 Codex 界面中输入以下内容，并附上原图或实际工程路径：

```text
使用 $blender-character-workflow，按照这张参考图制作头部和头发，
不要脖子和身体，用于静态多角度展示。先完成九视图参考，再继续建模。
```

```text
使用 $blender-character-workflow，修复现有工程的刘海缺口和头顶 UV 拉伸。
保留当前脸型、眼睛和后发，在新版本中修改，并提供修改前后的固定视角对比。
```

```text
使用 $blender-character-workflow，检查这个 blend 的贴图依赖和多视图表现。
只做只读检查，分别说明外形、工程和用途方面实际检查了什么。
```

准备输入时说明主参考、制作范围、用途、必须保留的特征和输出格式。目标交付包括 `.blend`、来自同一版本的真实渲染、必要资源和简短检查说明。

## 使用边界

- 生成的侧后方和顶部属于设计补全；原图是主基准，生成图不是严格一致的三维投影。
- 灰模、工程重开和少量关键点误差分别提供有限证据，不能代表整体相似度获得认可。
- 原画局部 UV 可保留绘画光影；换光、动画和实时导出需独立检查。
- 静态展示通过不等于动画或打印可用，只承诺实际验证过的用途。

## 仓库结构

```text
skills/blender-character-workflow/
  SKILL.md                         技能入口
  LICENSE                          随技能分发的许可证
  agents/openai.yaml               Codex 界面元数据
  references/production-workflow.md
  references/blender-reliability.md
  references/static-illustration-finish.md
scripts/                           安装与仓库检查
tests/                             分发行为检查
docs/releasing.md                  GitHub 发布准备
```

详细流程从 [SKILL.md](skills/blender-character-workflow/SKILL.md) 进入。技能正文目前以中文维护，英文 README 提供安装、范围与使用说明。

## 参与维护

欢迎提交可复现的问题、流程改进和有明确授权的案例，见 [贡献指南](CONTRIBUTING.md)。维护检查：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests
```

上面的激活命令适用于 POSIX Shell；Windows 可使用 `.venv\Scripts\Activate.ps1`。GitHub Actions 运行相同检查，并用 `scripts/check_whitespace.py` 检查 PR 或 push 的实际提交范围；首次推送和手动运行检查整个提交树。检查范围是分发结构和安装行为，不执行人物建模。

## 许可证与素材

指令、文档和辅助脚本采用 [MIT License](LICENSE)，许可证随技能一并分发。人物参考图、角色设计、贴图和外部模板的权利需单独确认；仓库许可证不替第三方素材授予使用权。

这是社区项目，与 OpenAI 或 Blender Foundation 无官方隶属关系。
