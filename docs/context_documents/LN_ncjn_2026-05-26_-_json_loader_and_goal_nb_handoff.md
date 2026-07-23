# CONTEXT DOCUMENT — Continuation

## Project

**Name:**
no-code-jupyter-nb

**Description:**
`no-code-jupyter-nb` is a Python package for generating guided,
executable Jupyter notebooks from structured configuration objects,
reusable widget abstractions, and explicit notebook block definitions.
It supports no-code / low-code notebook workflows for non-programmer
users while preserving strong state validation, runtime awareness, and
recoverable UX behavior.

---

## Continuation Metadata

**Prepared at:**
1779835200_2026-05-26T00:00:00-0400

Generated via:

```text
date +'%s_%Y-%m-%dT%H:%M:%S%z'
```

(Boston, MA time)

**Continued from chat:**
No-code Jupyter Notebook

**Also involving:**
- Android / Termux bootstrap workflow
- GitHub SSH and small-PR workflow
- JSON config loading and dataclass hydration
- OCR transcription of the prototype goal notebook
- guided notebook UX and human-in-the-loop tooling patterns
- Vim / Bash / editable install validation

---

## Author / Source

**User (GitHub):**
@bballdave025

**User (ChatGPT):**
{{optional}}

---

## Intent for This Context

Resume implementation of `no-code-jupyter-nb` immediately after the
JSON config loader PR was completed and merged. This document preserves
project state, architecture, design constraints, coding conventions,
completed work, and the next sprint path as of 2026-05-26.

---

## Usage Instructions

- Treat this document as **authoritative project state**.
- Continue with **minimal re-derivation**.
- Reinterpret only when explicitly requested.
- Prioritize implementation throughput over tutorialization.
- Preserve lean-to / KISINSS execution philosophy.
- Do not prematurely expand dependencies or architecture.
- Prefer small focused PRs, but not so small that handoff acceleration
  is compromised.

*ENDOF: Context Document Header*

------------------------------------------------------------------------

# Project Mental Model

`no-code-jupyter-nb` is not merely a widget package and not merely a
notebook writer. The project is a structured system for turning explicit
configuration into guided notebook workflows.

The core pipeline is:

```text
JSON → Config objects → Widget factories → Notebook blocks → IPYNB file
```

The notebook is treated as a **guided human state machine**. It is meant
to help non-programmer users move through a workflow safely, with clear
instructions, recoverable failure modes, visible state, and loud
validation.

The guiding principle is:

> Separate environment facts, user configuration, UI, and execution flow.

This means:

- environment facts belong in `GlobalObservables`,
- user/session/project state belongs in `NotebookConfig`,
- category metadata belongs in `CategorySpec`,
- notebook-generation units belong in `NotebookBlock`,
- notebook rendering belongs in `NotebookRenderer`,
- JSON loading belongs at the serialization/deserialization boundary,
- widgets should update structured config/state rather than loose globals.

The prototype notebook showed that the real challenge is not only running
Python code. The harder problem is making the workflow traversable for
humans who are busy, interrupted, uncertain, under-trained, or afraid of
breaking something.

Therefore, UX clarity and operational recoverability are architectural
requirements, not decoration.

------------------------------------------------------------------------

# Current High-Level Architecture

Relevant package layout at this checkpoint:

```text
src/no_code_jupyter_nb/
  __init__.py
  categories.py
  environment.py
  file_tools.py
  format_style.py
  json_tools.py
  nb_config.py
  ncjn_widgets.py
  notebook_blocks.py
  notebook_renderer.py
```

Current responsibilities:

```text
environment.py
  Runtime/platform/global observables.

categories.py
  CategorySpec and category/subcategory metadata.

nb_config.py
  NotebookConfig and session/project state.

json_tools.py
  JSON file loading and dataclass hydration orchestration.

format_style.py
  RenderStyle and CodeGenStyle conventions.

notebook_blocks.py
  NotebookBlock semantic cell/block records.

notebook_renderer.py
  Notebook rendering skeleton.

ncjn_widgets.py
  Widget behavior/factory skeletons.

file_tools.py
  Filesystem/path helpers, currently still skeletal.
```

The architecture has deliberately avoided a single `NoCodeJupyterNb`
God-class. The old prototype class is useful as migration/reference
material, but the package should continue separating concerns by module
and dataclass responsibility.

------------------------------------------------------------------------

# Completed Through This Checkpoint

## Bootstrap/package structure

The package was bootstrapped successfully with:

- `src/no_code_jupyter_nb/`
- root exports through `__init__.py`
- `pyproject.toml`
- editable install workflow
- GitHub SSH workflow
- Android / Termux validation
- package version aligned to `0.2.0`

Smoke-tested imports have included:

```python
from no_code_jupyter_nb import (
  GlobalObservables,
  NotebookConfig,
  CategorySpec,
  RenderStyle,
  CodeGenStyle,
)
```

A prior bootstrap issue was discovered and fixed:

```python
from dataclasses import dataclass, field
```

was required in `notebook_blocks.py`.

## JSON loader PR

The JSON config loader PR was completed and merged by this checkpoint.

Branch:

```text
feat/json-config-loader
```

Commit message used:

```text
Add JSON config loader and dataclass hydration path
```

PR implemented the first real vertical slice:

```text
JSON → dict → CategorySpec → NotebookConfig → usable config methods
```

The PR was intentionally:

- lightweight,
- dataclass-first,
- validation-light,
- dependency-minimal.

It avoided:

- schema engines,
- `traitlets`,
- `pydantic`,
- notebook orchestration,
- automatic widget inference,
- generalized serialization frameworks,
- and heavy validation/runtime frameworks.

Validated commands included:

```bash
python -m pip install -e .
```

and:

```bash
python -c "from no_code_jupyter_nb import CategorySpec, NotebookConfig, load_config_from_json, load_json_file; print('imports check')"
```

Output:

```text
imports check
```

End-to-end smoke test:

```bash
python -c "from no_code_jupyter_nb import load_config_from_json; cfg = load_config_from_json('examples/minimal_config.json'); print(cfg.current_category_key); print(cfg.get_current_category()); print(cfg.get_current_uri())"
```

Output:

```text
cat_1
CategorySpec(key='cat_1', label='Category 1', uri='https://example.com', preferred_filename='cat_1.csv', subcategories=[], metadata={})
https://example.com
```

The branch was merged, then cleaned up locally and remotely.

------------------------------------------------------------------------

# Current Vertical Slice

The current working vertical slice is:

```text
examples/minimal_config.json
      ↓
load_config_from_json(...)
      ↓
load_json_file(...)
      ↓
CategorySpec.from_dict(...)
      ↓
NotebookConfig.from_dict(...)
      ↓
cfg.get_current_category()
cfg.get_current_uri()
```

This is the first executable proof that JSON can be the source of truth
for structured notebook state.

Minimal example JSON:

```json
{
  "current_category_key": "cat_1",
  "category_specs": [
    {
      "key": "cat_1",
      "label": "Category 1",
      "uri": "https://example.com",
      "preferred_filename": "cat_1.csv"
    }
  ]
}
```

The loader currently supports minimal valid JSON and explicit dataclass
hydration. More complex validation is intentionally deferred.

------------------------------------------------------------------------

# Key Components

## GlobalObservables

`GlobalObservables` is foundational infrastructure. It detects runtime
and system environment once and should not be recomputed casually.

It includes concepts such as:

- OS/runtime identity,
- Python version/bitness,
- home/download directories,
- Jupyter/VS Code/Colab/Binder/SageMaker style runtime flags,
- clipboard capability flags,
- case-sensitivity defaults.

Important future refinement:

Android/Termux should not be collapsed into a simplistic Linux boolean.
Better future modeling:

```text
is_windows
is_linux_kernel
is_linux_desktop
is_android
is_termux
is_wsl
is_cygwin
is_macos
is_posixish
```

The useful question is not merely “what OS am I on?” but “what
assumptions are safe?”

## NotebookConfig

`NotebookConfig` holds notebook/session/project choices. It does **not**
recompute environment information.

Known fields include:

```text
observables
original_no_code_maintainer
original_no_code_email
current_maintainer_name
current_maintainer_email
category_specs
current_category_key
current_subcategory_key
selected_file
current_uri
root_directory
runtime_options
```

Known methods include:

```text
get_category_map()
get_current_category()
get_current_uri()
from_dict(...)
```

`NotebookConfig.from_dict(...)` exists and is part of the JSON hydration
path.

## CategorySpec

`CategorySpec` replaces fragile parallel lists.

Current shape:

```python
@dataclass
class CategorySpec:
  key: str
  label: str
  uri: str = ""
  preferred_filename: str | None = None
  subcategories: list[str] = field(default_factory=list)
  metadata: dict[str, Any] = field(default_factory=dict)
```

`CategorySpec.from_dict(...)` exists and is part of the JSON hydration
path.

`CategorySpec` supports future category/subcategory behavior, preferred
filenames, URLs, validation metadata, and category-specific workflow
information.

## NotebookBlock

`NotebookBlock` represents an explicit notebook-generation unit.

Current concepts include:

```text
name
cell_type
title
content
instruction_level
visibility
auto_run_hint
depends_on
```

Known instruction levels include:

```text
normal
just_shift_enter
look_above
stop_and_choose
```

Known visibility levels include:

```text
normal
advanced
dangerous
```

Important design decision:

> Instruction headers are explicit metadata, not inferred from content.

Do not infer “LOOK ABOVE” or “STOP” behavior heuristically from cell
text unless explicitly asked to redesign this.

## RenderStyle and CodeGenStyle

`RenderStyle` controls code/notebook rendering preferences.

Project-local formatting preferences are intentional and should be
followed when generating code for this repo:

```python
py_indent: int = 2
py_indent_for_params_beyond_def: int = 6
py_indent_for_closing_paren_beyond_def: int = 4
ipynb_indent: int = 4
ipynb_indent_for_params_beyond_def: int = 12
ipynb_indent_for_closing_paren_beyond_def: int = 4
max_line_length: int = 79
preferred_line_length: int = 72
```

Docstrings are preferred with triple single quotes:

```python
'''
Docstring text.
'''
```

`##endof:` markers are intentional and valued.

Example style:

```python
def load_config_from_json(
      config_path: pathlib.Path | str,
    ) -> NotebookConfig:
  raw = load_json_file(config_path)
  return NotebookConfig.from_dict(raw=raw, category_specs=[])
##endof: load_config_from_json(...)
```

This style is not meant to be the One True Python Style. It is a
configurable rendering philosophy. Other generated notebooks/code should
eventually be able to target different style cultures, including classic
Vim or standard 4-space Python styles.

------------------------------------------------------------------------

# Widget / UX Design Model

The prototype notebook demonstrates a repeated design pattern:

```text
instruction → user action → state update → validation → loud feedback
```

The notebook behaves as a guided state machine for human users.

Important UX concepts:

- state gating,
- loud validation,
- recoverable errors,
- step-by-step enforcement,
- fast-forward mode once stable,
- explicit “LOOK ABOVE” / “STOP” moments,
- defensive fallback pages,
- copy buttons and open-link buttons,
- dropdown-driven config mutation,
- file selectors with recovery paths.

## Gate dropdowns

Used when the user must explicitly choose.

Behavior:

- includes sentinel value, such as `No_Category_Chosen`,
- throws loud recoverable exception if not changed,
- no silent defaults.

Rule:

> No silent defaults allowed.

## File dropdowns / discovered-state dropdowns

Used when files already exist and the system is discovering state.

Behavior:

- scans directory,
- filters by extension,
- prefers expected filename,
- defaults to best guess,
- warns user to verify.

Rule:

> Default allowed, but must be loudly verified.

## Highlighted output system

The old prototype’s `create_highlighted_string(...)` is important
architecture, not merely visual noise.

It distinguishes:

```text
info_
action_
exception_
```

and provides conspicuous output so users do not silently miss important
state changes or required actions.

This should eventually become a lightweight console/notebook UX helper,
not a buried one-off function.

------------------------------------------------------------------------

# Prototype OCR / Goal Notebook State

Four PDF chunks of the redacted prototype/goal notebook exist and were
uploaded in prior chat context:

```text
sync01.pdf  — 15 pages
sync02.pdf  — 15 pages
sync03.pdf  — 24 pages
sync04.pdf  — 18 pages
```

Natural processing order:

```text
sync01.pdf → sync02.pdf → sync03.pdf → sync04.pdf
```

The OCR is imperfect but highly informative. It captures the old
notebook’s architecture and UX evolution:

- ipykernel/bootstrap setup,
- dependency checking,
- maintainer guidance,
- highlighted output helpers,
- fallback HTML pages,
- category dropdowns,
- URL/copy/open buttons,
- subcategory selection,
- file export instructions,
- source table directory checks,
- filesystem self-healing,
- validation flow.

## OCR transcription conventions

Use:

```text
⌨
```

for unresolved uncertainty.

Unicode codepoint:

```text
U+2328 KEYBOARD
```

Use:

```text
███
```

for inline redaction spans.

Reason:

`▮▮▮` had visible spacing/glyph side-bearing issues in many fonts, even
in monospaced contexts. `███` is denser and better for inline redaction.

Use:

```text
[redacted line(s)]
```

for full-line or multi-line redactions.

OCR philosophy:

- preserve meaning,
- preserve structure,
- preserve uncertainty,
- avoid hallucinated reconstruction,
- keep transcription reviewable,
- mark uncertainty rather than guessing.

Important division of labor:

- Assistant should aggressively flag unclear OCR with `⌨`, because the
  user has author-familiarity bias.
- User should adjudicate corrections and redactions.

------------------------------------------------------------------------

# Dependency Philosophy

Core package should remain lightweight.

Current posture:

```text
core dependencies: none or very few
notebook dependencies: optional
validation dependencies: optional and deferred
scientific stack: optional
release/dev tools: optional
```

Previously discussed optional dependency groups:

```toml
[project.optional-dependencies]
dev = [
  "build",
  "pytest",
  "bump-my-version",
]

release = [
  "bump-my-version",
]

notebook = [
  "ipykernel",
  "ipywidgets>=8",
  "pandas>=2,<3",
  "numpy>=2,<3",
]

test = [
  "pytest",
  "ipywidgets>=8",
  "pandas>=2,<3",
  "numpy>=2,<3",
]
```

Potential future validation extra:

```toml
[project.optional-dependencies]
validation = [
  "jsonschema>=4,<5",
]
```

`traitlets` was discussed and deferred.

Reason:

- too much framework gravity too early,
- project architecture still stabilizing,
- dataclass-first approach remains clearer,
- validation should degrade gracefully without optional dependencies.

`jsonschema` is a better future optional validation candidate because it
matches the current boundary: JSON config compliance before dataclass
hydration.

------------------------------------------------------------------------

# Git / PR Workflow State

The project is using small focused PRs with explicit PR plans and PR
comments.

Preferred branch flow:

```bash
git switch main
git pull --rebase
git switch -c feat/some-focused-feature
git push -u origin feat/some-focused-feature
```

Preferred cleanup after PR merge:

```bash
git switch main
git pull --rebase
git branch -d feat/some-focused-feature
```

Use `git pull --rebase` for feature-branch divergence unless there is a
specific reason not to.

The user learned and successfully used rebase during this work.

Useful graph inspection:

```bash
git log --oneline --decorate --graph -n 12
```

PR plan/comment pattern:

```text
docs/dev_notes/PR_PLAN_<slug>.md
docs/dev_notes/PR_COMMENT_<slug>.md
```

PR/checklist documents are not fluff. They are future-context
compression and help preserve intent, drift, rationale, validation, and
scope boundaries.

Good commit-message style for this repo:

```text
Add JSON config loader and dataclass hydration path
```

Commit messages can stay concise because PR docs hold the detailed
“why/how/scope/validation” material.

------------------------------------------------------------------------

# Current Known Design Decisions

Locked or strongly preferred decisions:

- Do not port the old `NoCodeJupyterNb` prototype as a God-class.
- Dataclasses are preferred over parallel lists.
- JSON is the source-of-truth/config boundary.
- Hydration is explicit and readable.
- `GlobalObservables` is computed once and passed/held, not recomputed.
- Gate dropdowns and discovered-state dropdowns are different concepts.
- Instruction metadata is explicit, not inferred.
- Builder/core layer remains lightweight.
- Heavy notebook/scientific dependencies remain optional.
- UX clarity is more important than clever code elegance.
- Loud recoverable errors are preferred over hidden failure.
- Notebook structure is a guided state machine for humans.
- Lean-to first; cathedral later.

------------------------------------------------------------------------

# Immediate Next Steps

The JSON loader PR is complete. The next work should start from `main`
after pulling latest.

Recommended next sprint choices:

## Option A — OCR canonical Markdown

Create canonical Markdown transcription/context for the prototype goal
notebook.

Suggested files:

```text
docs/ocr/OCR_CANONICAL_sync01.md
docs/ocr/OCR_CANONICAL_sync02.md
docs/ocr/OCR_CANONICAL_sync03.md
docs/ocr/OCR_CANONICAL_sync04.md
```

Start with `sync01.pdf`.

Pass 1 goals:

- preserve structure,
- repair obvious OCR corruption,
- insert `⌨` for uncertainty,
- use `███` for inline redactions,
- preserve code blocks,
- preserve headings,
- preserve intent.

Do not try to reconstruct perfect executable code on pass 1.

## Option B — generalized file selector widget

Implement the reusable file-selection abstraction derived from the
prototype pattern:

```text
scan directory → find files → prefer expected filename → populate dropdown → fallback if missing → fail loudly if none
```

This belongs mostly in widget/file tooling, not in config hydration.

## Option C — NotebookBlock renderer integration

Upgrade notebook renderer to accept `NotebookBlock` lists and emit basic
IPYNB JSON.

Keep this small:

- markdown cell,
- code cell,
- minimal metadata,
- explicit block ordering,
- no dependency graph yet.

## Recommended next PR

If continuing implementation rather than OCR, recommended next branch:

```bash
git switch main
git pull --rebase
git switch -c feat/notebook-block-renderer
```

or:

```bash
git switch main
git pull --rebase
git switch -c feat/file-selector-widget
```

Given the current desire to reduce context transfer cost, OCR canonical
Markdown is likely the highest-leverage next activity before more code.

------------------------------------------------------------------------

# Deferred Work

Do not build yet unless explicitly requested:

- full notebook generator,
- block dependency system,
- advanced CLI tooling,
- multi-notebook output,
- plugin architecture,
- full schema validation,
- traitlets/pydantic migration,
- tmux/dotfile optimization,
- scientific-stack stabilization,
- generalized workflow engine,
- automatic widget inference.

These are future work, not current sprint work.

------------------------------------------------------------------------

# Open Questions / Risks

## OCR fidelity

The prototype notebook PDFs contain enough structure to be useful, but
OCR quality varies. Treat OCR correction as canonicalization with
uncertainty markers, not as perfect reconstruction.

## Namespace and exports

Current compromise:

- Classes are exported at package root.
- JSON module namespace is also exported.
- Functional JSON helpers are exported at root for convenience.

Example:

```python
from no_code_jupyter_nb import NotebookConfig
from no_code_jupyter_nb import load_config_from_json
import no_code_jupyter_nb as ncjn
ncjn.json_tools.load_config_from_json(...)
```

Do not add full submodule namespace exports for every class unless there
is a clear need.

## Style enforcement

The project has strong local formatting conventions, but no formatter is
currently enforcing them. Assistant-generated code should respect local
style manually.

## Optional dependency boundary

Avoid accidentally making notebook/scientific packages hard core
dependencies.

## Work/IP boundary

The reusable patterns in this project are generic engineering/tooling
patterns: dataclass config, notebook UX, state gating, widget factories,
recoverable validation, and no-code notebook infrastructure. Do not copy
proprietary employer logic, data, schemas, or task-specific algorithms
into the public/general package.

------------------------------------------------------------------------

# Sprint Mode Reminder

Default collaboration mode for this project:

- implementation-first,
- concise,
- ADHD-friendly,
- fast but not reckless,
- preserve architecture boundaries,
- avoid unnecessary tutorialization,
- answer understanding questions when asked,
- then return to productivity mode.

Useful phrase:

> Mine the prototype. Do not reincarnate the God Class.

Another useful phrase:

> Lean-to first. Cathedral later.

------------------------------------------------------------------------

# Summary Handoff

As of this checkpoint, `no-code-jupyter-nb` has moved from package
skeleton into its first working executable config slice. JSON config can
now hydrate `CategorySpec` and `NotebookConfig`, and the package root can
load a minimal JSON config and return useful config methods.

The next major value unlock is reducing repeated chat/context overhead by
canonicalizing the OCR/prototype notebook into Markdown, starting with
`sync01.pdf`.

After that, the likely code path is either the generalized file selector
or the `NotebookBlock` renderer path.

The project should continue using focused PRs, explicit PR plans,
smoke-test evidence, and lightweight architecture preservation.

*End of context document.*
