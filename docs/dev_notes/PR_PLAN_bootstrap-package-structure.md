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
- [x] Ensure package imports working:

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
  - [x] `python -c "from no_code_jupyter_nb import GlobalObservables"` returns `0`
  - [x] `python -c "from no_code_jupyter_nb import NotebookConfig"` returns `0`
  - [x] `python -c "from no_code_jupyter_nb import CategorySpec"` returns `0`
  - [x] `python -c "from no_code_jupyter_nb import RenderStyle"` returns `0`
  - [x] `python -c "from no_code_jupyter_nb import CodeGenStyle"` returns `0`

Terminal input/output for tests and some package structure visualization:

```python
~/my_repos_dwb/no-code-jupyter-nb $ cd
~ $ date +'%s_%Y-%m-%dT%H%M%S%z'
1779146125_2026-05-18T191525-0400
~ $ pwd
/data/data/com.termux/files/home
~ $ python -c "from no_code_jupyter_nb import CodeGenStyle"
~ $ echo $?
0
~ $ python -c "from no_code_jupyter_nb import RenderStyle"
~ $ echo $?
0
~ $ python -c "from no_code_jupyter_nb import CategorySpec"
~ $ echo $?
0
~ $ python -c "from no_code_jupyter_nb import NotebookConfig"
~ $ echo $?
0
~ $ python -c "from no_code_jupyter_nb import GlobalObservables"
~ $ echo $?
0
~ $ date +'%s_%Y-%m-%dT%H%M%S%z'
1779146329_2026-05-18T191849-0400
~ $ cd -
/data/data/com.termux/files/home/my_repos_dwb/no-code-jupyter-nb
~/my_repos_dwb/no-code-jupyter-nb $ ls -lAH
total 39
drwx------. 7 u0_a389 u0_a389  3452 May 18 18:56 .git
-rw-------. 1 u0_a389 u0_a389  4688 May 13 19:19 .gitignore
-rw-------. 1 u0_a389 u0_a389 11357 May 13 19:19 LICENSE
-rw-------. 1 u0_a389 u0_a389  1302 May 13 19:19 README.md
drwx------. 4 u0_a389 u0_a389  3452 May 13 19:25 docs
-rw-------. 1 u0_a389 u0_a389  1810 May 14 21:17 pyproject.toml
drwx------. 4 u0_a389 u0_a389  3452 May 13 19:27 src

~/my_repos_dwb/no-code-jupyter-nb $ tree -a -I __pycache__ --charset=ascii src/no_code_jupyter_nb
src/no_code_jupyter_nb
|-- __init__.py
|-- categories.py
|-- environment.py
|-- file_tools.py
|-- format_style.py
|-- json_tools.py
|-- nb_config.py
|-- ncjn_widgets.py
|-- notebook_blocks.py
`-- notebook_renderer.py

1 directory, 10 files
~/my_repos_dwb/no-code-jupyter-nb $
~/my_repos_dwb/no-code-jupyter-nb $ git branch
* feature/bootstrap-package-structure
  main
  ~/my_repos_dwb/no-code-jupyter-nb $ date +'%s_%Y-%m-%dT%H%M%S%z'
  1779146420_2026-05-18T192020-0400
  ~/my_repos_dwb/no-code-jupyter-nb $
```

And, for one good, useful implementation check, where I have formatted the output:

```bash
~/my_repos_dwb/no-code-jupyter-nb $ cd
~ $ python -c \
> "from no_code_jupyter_nb import GlobalObservables; "\
> "DEFAULT_OBSERVABLES = GlobalObservables.detect(); "\
> "print(DEFAULT_OBSERVABLES);"
GlobalObservables(
  runtime=RuntimeEnvironment(
    os_name='Android', 
    machine_endianness='little', 
    locale_name='C', 
    machine_description='aarch64 / unknown-cpu', 
    python_bitness=64, 
    python_version=(3, 13, 13), 
    is_windows=False, 
    is_linux=False, 
    is_macos=False, 
    home_dir=PosixPath('/data/data/com.termux/files/home'), 
    downloads_dir=PosixPath('/data/data/com.termux/files/home/Downloads')
  ), 
  default_case_sensitive_extensions=True, 
  runtime_is_on_vs_code=False, 
  runtime_is_on_jupyter_std_server=False, 
  runtime_is_on_jupyter_lab=False, 
  runtime_is_on_amazon_sagemaker=False, 
  runtime_is_on_google_colab=False, 
  runtime_is_on_binder=False, 
  have_js_clipboard_access=False, 
  have_pandas_clipboard_access=False
)
~ $ date +'%s_%Y-%m-%dT%H%M%S%z'                        1779146652_2026-05-18T192412-0400                       ~ $
```

