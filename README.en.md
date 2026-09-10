# awesome-astra-blender-characters

**An AI agent workflow for turning character references into editable Blender projects.**

[中文](README.md) · English

This repository distributes the `blender-character-workflow` skill: reference preparation, face and hair modeling, focused repairs, multi-view inspection, and project delivery. Its focus is stylized anime characters and static illustration finishes. The skill does not prescribe a model version.

The package contains instructions and production references. It currently includes no character assets, sample renders, model weights, or one-click reconstruction program. Repository scripts install and validate the skill; they do not build characters. The skill instructions are maintained in Chinese.

## Workflow and capabilities

1. Inspect the original image, existing project, scope, and intended use; state any scope assumptions.
2. For a new character, generate or reuse nine checked references: eight horizontal directions, 45° apart, plus a top view.
3. Align references, cameras, scale, and landmarks.
4. Build the face at low detail; inspect front, side, and oblique neutral renders, especially chin closure and depth, before refining features or building the full hairstyle.
5. Build hair volumes, native strands, root coverage, crown-to-long-hair transitions, materials, local UVs, and illustration details.
6. Extend to body, clothing, accessories, or rigging when requested.
7. Inspect appearance, project integrity, and intended use separately; state UV and intersection-check coverage, then package and reopen the final `.blend`.

Focused repairs enter the relevant stage without regenerating every reference. Documentation work does not launch Blender or generate images. An unanswered scope question does not authorize omitting visible parts of the reference. Compare actual renders of the problem view and adjacent views after each change, revisit the cause if it persists, and produce the delivery views from one explicitly saved version once the local result is stable.

[Illustration-finish diagnostics](skills/blender-character-workflow/references/static-illustration-finish.md) cover image-texture UV validation, skin-tone adjustments that preserve blush, separate eye-surface/iris/lens checks, and isolation of hair support surfaces, inner layers, and native strands. [Execution reliability](skills/blender-character-workflow/references/blender-reliability.md) covers native-curve and shader-mode inputs, state preservation during local edits, and recovery from real-time viewport failures. Existing guidance also covers transparency, gaps, intersections, pole distortion, version identity, and camera framing.

Body, animation, printing, and export guidance is included, but the public package does not yet include end-to-end validation examples for those uses.

## Requirements

- An agent environment that can load skills, inspect images, and use local tools. Codex UI metadata is included.
- A local Blender installation with its bundled Python and CLI. Detect the actual version; no cross-version compatibility matrix is claimed. Character-specific scripts are created during the task.
- An image-generation tool and the `imagegen` skill when generating references or textures. These are supplied by the host, not this repository.
- UI automation or Blender MCP is optional when a working CLI is available.
- External Python 3.10+ is needed only for repository helper scripts. PyYAML is a development dependency for validation.

Without image generation, supply an already checked reference set or explicitly change the requested view scope. Installing the skill does not install Blender, image models, or other creative applications.

## Install

After downloading or cloning the repository, run from its root:

```bash
python3 scripts/install.py
```

This copies the skill to `~/.agents/skills/blender-character-workflow/`. It refuses to overwrite an existing destination. Before updating, back up and move the previous installation yourself. The installer does not access the network, launch Blender, or edit agent configuration.

Only files explicitly listed in `PACKAGE_FILES` in `scripts/install.py` are copied. Local configuration, caches, and extra assets are excluded, and source directories containing symbolic links are rejected. Files are staged in a temporary directory before moving into place; failed copies are cleaned up so installation can be retried.

To choose a skill parent directory, such as a target project's `.agents/skills` or another location used by your host:

```bash
python3 scripts/install.py --destination /path/to/your-project/.agents/skills
```

For manual installation, copy the entire `skills/blender-character-workflow/` directory, including its `LICENSE`. Keep the skill folder name unchanged.

See the [official OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) for local discovery paths. If the skill does not appear, restart Codex and check for installations with the same name in other locations.

## Use

In a Codex interface supporting `$` skill mentions, attach a reference image or provide an actual project path:

```text
Use $blender-character-workflow to make the head and hair from this reference.
Exclude the neck and body. The result is for static multi-angle viewing.
Prepare and check the nine reference views, then continue modeling.
```

```text
Use $blender-character-workflow to fix the fringe gaps and top-of-head UV stretching.
Preserve the current face, eyes, and back hair. Work in a new version and show
before-and-after renders from the same cameras.
```

```text
Use $blender-character-workflow to inspect this blend's texture dependencies
and multi-view appearance. Perform read-only checks and report appearance,
project integrity, and intended-use checks separately.
```

Specify the primary reference, scope, intended use, features to preserve, and output format. Expected deliverables include an editable `.blend`, renders from that version, required resources, and a concise inspection report.

## Limits

Generated hidden views are design completions, not calibrated projections; the original image remains the primary reference. Neutral renders, file reopening, and landmark error each provide limited evidence, and none alone proves overall likeness. Image-projected lighting requires separate evaluation for relighting or animation. Static validation does not establish animation or printing suitability.

Using UVs for every image texture does not give every hair strand an independently paintable atlas. Valid UV ranges, nondegenerate UV faces, and limited intersection sampling do not establish distortion-free mapping, brush usability, or an intersection-free assembly. Reports must identify the checked objects, methods, and untested areas.

## Contents and development

Start with [SKILL.md](skills/blender-character-workflow/SKILL.md), which links to production, execution reliability, and illustration-finish references. The skill folder also contains its license and `agents/openai.yaml`. Helpers live in `scripts/`, with distribution tests in `tests/`.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes. [The release checklist](docs/releasing.md) describes GitHub preparation. Run local checks with:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests
```

The activation command is for POSIX shells; on Windows use `.venv\Scripts\Activate.ps1`. GitHub Actions runs these packaging and installation checks and uses `scripts/check_whitespace.py` to check committed PR or push changes. First pushes and manual runs check the whole committed tree. These checks do not execute character production.

## License and assets

Instructions, documentation, and helper scripts are under the [MIT License](LICENSE), also included in the skill directory. References, character designs, textures, and external templates require their own rights review; this license grants no rights to third-party assets.

This is a community project with no official affiliation with OpenAI or the Blender Foundation.
