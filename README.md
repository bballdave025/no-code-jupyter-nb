# no-code-jupyter-nb

A lightweight toolkit for building no-code and low-code interfaces inside Jupyter notebooks.

Designed for:

- VS Code + Python/Jupyter extensions
- Classic Jupyter Notebook
- JupyterLab
- Local notebook workflows
- Rapid internal tools
- Non-programmer-friendly notebook UX

## Features

- Dropdown factories
- File selectors
- Native file dialog support (`tkinter`)
- Clipboard copy/paste helpers
- URI launch buttons
- Markdown display helpers
- Structured config objects
- Extensible file-extension workflows

## Installation

```bash
pip install no-code-jupyter-nb
```

(Or local editable install:)

```bash
pip install -e .
```

## Quick Example

```python
from no_code_jupyter_nb import NoCodeJupyterNb, NotebookConfig

cfg = NotebookConfig()

selector = NoCodeJupyterNb.return_csv_file_selector(
    config=cfg,
    file_extension="csv"
)

display(selector)
```

## File Type Flexibility

Any extension may be used:

```python
file_extension="xlsx"
file_extension="pdf"
file_extension="txt"
```

## Environment Notes

Works best in:

- VS Code notebooks
- Local Jupyter
- JupyterLab

Some clipboard features depend on platform/browser permissions.

## Philosophy

Reduce notebook friction.

Enable useful workflows for people who should not need to code.

## License

MIT
