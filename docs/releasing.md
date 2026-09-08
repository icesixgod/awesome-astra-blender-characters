# GitHub 发布准备

本文件记录维护者发布步骤。执行检查不等于授权创建远程仓库、推送或发布 Release；这些外部操作须由仓库所有者明确要求。

## 仓库信息草案

| 字段 | 准备值 |
| --- | --- |
| Repository name | `awesome-astra-blender-characters` |
| Description | `An agent skill for Blender character creation and repair, with nine-view references, face and hair workflows, and visual validation.` |
| Topics | `blender`, `codex`, `agent-skills`, `character-modeling`, `anime`, `3d-modeling` |
| License | MIT |
| 首次版本建议 | `v0.1.0`，实际发布时再创建标签 |
| GitHub 所属账户或组织 | `icesixgod` |

README 使用仓库相对链接，不依赖尚未创建的远程地址。

## 本地检查

- [ ] 确认根目录与技能目录的 `LICENSE` 一致，版权署名符合维护者意愿。
- [ ] 在虚拟环境中安装 `requirements-dev.txt`，运行下列命令。
- [ ] 阅读 `git diff`、新增文件及待提交清单，确认没有私人路径、凭证、原始对话或无授权素材。
- [ ] 检查将被推送的提交历史。`.gitignore` 不会清除已跟踪文件或历史内容。
- [ ] `.workspace-ledger/` 仅保留在本地并由 Git 忽略，不应加入提交；保留本地 `project.toml` 的受管 ID 和编号。历史提交仍可能含有工作区元数据，`AGENTS.md` 也会公开，发布前核对范围。
- [ ] 确认公开描述保留静态角色与动画用途的验证边界。

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests
git diff --check
git status --short
git ls-files
git log --all --oneline
```

检查脚本不联网检查外部链接，也不是凭证扫描器或 Blender 质量评估器。需要结合实际变更审阅。

CI 使用 `scripts/check_whitespace.py` 检查已提交内容：PR 比较共同祖先到当前提交，push 比较推送前后提交；首次推送、手动运行或旧提交不可用时检查整个提交树。本地也可用 `python3 scripts/check_whitespace.py --base BASE --head HEAD` 检查指定范围。

## 获得发布指令后

1. 确认 GitHub 账户或组织，以及公开仓库名称。
2. 审阅并提交准备好的文件，再创建或连接远程仓库并推送。避免用模板生成的 README 覆盖当前文档。
3. 设置上方 Description 和 Topics，确认许可证和两种语言的 README 显示正常。
4. 在 GitHub 上确认 Actions 实际运行通过，本地检查通过不代表远程 CI 已运行。
5. 设置适合维护者的分支保护和私密漏洞报告渠道后，再对外承诺对应流程。
6. 若需要首次 Release，确认提交、标签和说明对应同一版本，不把尚未公开的建模案例写入成绩。

## 首次 Release 说明草案

### Included

- Installable `blender-character-workflow` skill with nine-view reference preparation.
- Face, hair, static illustration, UV, occlusion, and Blender reliability guidance.
- Chinese and English READMEs, MIT license, contribution guidance, and issue templates.
- Local installation and repository validation scripts, with packaging tests and a CI workflow.

### Validation scope

The release packages instructions and references. Packaging checks do not prove character likeness or Blender version compatibility. No sample character assets, model weights, or end-to-end animation validation are included.

实际发布时补入对应提交的检查结果。当前文档是发布草案，不表示已经创建远程仓库或发布版本。
