# Codex Project Instructions

## Project identity

- Workspace Ledger ID: `CX-0028`
- Name: awesome-astra-blender-characters
- Lifecycle: `long_term`
- Purpose: Maintain and share a reusable Blender character creation and repair skill, with reference preparation, visual checks, and editable project delivery.

## Working agreement

- Read this file and the existing project documentation before changing files.
- Inspect the repository structure and reuse its established commands and conventions.
- Keep changes scoped to the current request and preserve unrelated user work.
- Run the smallest relevant tests, linters, and builds after making changes.
- Update README or project documentation when behavior, setup, or public interfaces change.
- Never commit credentials, API keys, tokens, or private local files.
- Ask before destructive operations, publishing, deployment, or changes to external systems.

## Repository conventions

- The distributable skill lives in `skills/blender-character-workflow/`. Keep its invocation name stable even though the repository has a different name.
- Keep public workflow guidance independent of private project paths, logs, character assets, and historical benchmark numbers.
- Keep the Chinese and English README aligned when installation, dependencies, or scope changes.
- Run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests` for packaging changes; install development dependencies from `requirements-dev.txt` first.
- Documentation or packaging work must not launch Blender, generate reference images, or overwrite an installed skill.

## Workspace Ledger metadata

- `.workspace-ledger/project.toml` is managed by Workspace Ledger. Keep its ID and number stable.
- Use Workspace Ledger to change lifecycle and archive state.
