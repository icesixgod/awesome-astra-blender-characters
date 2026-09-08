# Contributing / 参与贡献

欢迎用中文或英文提交 Issue 和 Pull Request。Please use Chinese or English.

## 有帮助的贡献 / Useful contributions

- 可复现的建模、参考一致性、UV、遮挡或工程可靠性问题。
- 能改变制作判断的流程改进；将具体角色参数保留在案例中。
- 安装说明修正、翻译和具备明确授权的验证案例。

Useful contributions include reproducible workflow problems, focused guidance improvements, documentation fixes, translations, and examples with clear redistribution rights.

## 修改约定 / Scope

- 技能入口在 `skills/blender-character-workflow/SKILL.md`，专项内容放在对应 `references/` 文档。
- 增删需要分发的技能文件时，同步更新 `scripts/install.py` 的 `PACKAGE_FILES` 清单；不要将本地配置或素材加入清单。
- 改动安装方式、依赖或能力范围时，同步更新两份 README。
- 区分实际观察的结果与待验证的方法。没有同一版本的可复核证据，不新增还原精度、速度或兼容性承诺。
- 不提交私人对话、凭证、本机用户路径、未经授权的参考图或生成目录。公开案例另行说明来源、授权、工具版本、补全区域和检查范围。
- 默认不把大型 `.blend` 或贴图加入 Git。需要公开素材时先在 Issue 中说明用途、大小与授权，再商定存储方式。

Keep the entry point focused and use the existing references for details. Update both READMEs for changes to installation, dependencies, or scope. Distinguish observed results from proposed methods, and include no private data or assets without redistribution rights.

When adding or removing distributed skill files, update `PACKAGE_FILES` in `scripts/install.py`. Keep local configuration and private assets out of that manifest.

## 验证 / Validation

在虚拟环境中安装 `requirements-dev.txt`，然后运行：

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests
git diff --check
```

Validation checks metadata, local documentation links, package self-containment, license consistency, and installation behavior. It does not evaluate character likeness. A workflow change should describe the actual scenario checked, the evidence, and any checks not performed. Documentation-only changes do not require running Blender.

PR 请说明问题、修改后的行为、验证结果与剩余限制。提交贡献时，你应有权按本仓库的 MIT 许可证提供所提交内容；第三方素材必须单独注明许可。

In a PR, explain the problem, resulting behavior, validation, and remaining limits. Contribute only material you are entitled to provide under this repository's MIT license, and identify third-party material separately.
