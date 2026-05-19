Bootstrap/package-structure pass is now validated on Android Termux (Pixel 10, Python 3.13).

Highlights:

- editable install succeeds via:
  `python -m pip install -e .`
- SSH-authenticated GitHub clone validated
- package root exports validated
- "GlobalObservables.detect()" exercised successfully on Android/Termux runtime
- import smoke tests pass for:
  - `GlobalObservables`
  - `NotebookConfig`
  - `CategorySpec`
  - `RenderStyle`
  - `CodeGenStyle`

During smoke testing, a real packaging/import issue was discovered and fixed:

    from dataclasses import dataclass, field

was required in `notebook_blocks.py`.

Heavyweight notebook/release dependencies are intentionally deferred from the lightweight bootstrap validation path for now.

This PR is intentionally:

- structure-first
- import-first
- environment/bootstrap-first

rather than a full notebook-runtime stabilization pass.

Lean-to (minimum-viable) first. Cathedral (full-featured) later.
