# PR1: Bootstrap package structure + observables + config skeleton

Relevant branch: `bballdave025/no-code-jupyter-nb:feature/bootstrap-package-structure`

## Implementation note (2026-05-12):

Where implementation details changed during bootstrap work:
- original plans are shown with strike-through
- implemented replacements/consolidations are shown in italics

## Summary

Initial bootstrap of `no_code_jupyter_nb` as an importable package.

This PR establishes the core structure needed to support:
- JSON → Config → Widgets → NotebookBlocks → IPYNB pipeline
- cross-platform runtime detection via `GlobalObservables`
- future no-code notebook generation

No full functionality yet — this is a foundation pass.

---

## Checklist

### Packaging
- [x] Created `src/no_code_jupyter_nb/`
- [x] Added `__init__.py` with `__version__`
- [x] Added/updated `pyproject.toml`
- [x] Configured `bump-my-version`


### _Implementation note:_
- _`NotebookConfig` is exported from `nb_config.py`_
- _`RenderStyle` and `CodeGenStyle` are exported from `format_style.py`_
- _Public imports should still work from package root: `no_code_jupyter_nb`_

### Core structure
- [x] `environment.py` with `GlobalObservables` + `.detect()`
- [x] ~~`config.py`~~  `nb_config.py` with `NotebookConfig` *changed module filename to `nb_config.py`*
- [x] `categories.py` with `CategorySpec`
- [x] ~~`render_style.py` (`RenderStyle`)~~ *`RenderStyle` combined with `CodeGenStyle` into `format_style.py`*
- [x] ~~`codegen_style.py` (`CodeGenStyle`)~~ *`CodeGenStyle` combined with `RenderStyle` into `format_style.py`*
- [x] `json_tools.py` (load/write/add/remove placeholders)

### Behavior (initial)
- [x] Define `DEFAULT_OBSERVABLES = GlobalObservables.detect()`
- [x] Wire `NotebookConfig(observables=...)`
- [ ] Ensure package imports working:

```python
from no_code_jupyter_nb import (
  GlobalObservables,
  NotebookConfig,
  CategorySpec,
  RenderStyle,
  CodeGenStyle,
)
```

- The import checks, one at a time:
  - [ ] `python -c "from no_code_jupyter_nb import GlobalObservables"` returns `0`
  - [ ] `python -c "from no_code_jupyter_nb import NotebookConfig"` returns `0`
  - [ ] `python -c "from no_code_jupyter_nb import CategorySpec"` returns `0`
  - [ ] `python -c "from no_code_jupyter_nb import RenderStyle"` returns `0`
  - [ ] `python -c "from no_code_jupyter_nb import CodeGenStyle"` returns `0`
