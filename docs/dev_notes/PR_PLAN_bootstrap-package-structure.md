# TlBootstrap package structure + observables + config skeleton

Relevant branch: `bballdave025/no-code-jupyter-nb:feature/bootstrap-package-structure`

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

### Core structure
- [ ] `environment.py` with `GlobalObservables` + `.detect()`
- [ ] `config.py` with `NotebookConfig`
- [ ] `categories.py` with `CategorySpec`
- [ ] `render_style.py` (`RenderStyle`)
- [ ] `codegen_style.py` (`CodeGenStyle`)
- [ ] `json_tools.py` (load/write/add/remove placeholders)

### Behavior (initial)
- [ ] `DEFAULT_OBSERVABLES = GlobalObservables.detect()`
- [ ] `NotebookConfig(observables=...)` wired
- [ ] Package imports working:

```python
from no_code_jupyter_nb import (...)
```




