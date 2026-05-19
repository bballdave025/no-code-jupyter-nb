from __future__ import annotations

from dataclasses import dataclass

class NoCodeJupyterNb:
  '''
  Factory-style helpers for no-code-ish Jupyter notebook UX.
  '''
##endof: class NoCodeJupyterNb


@dataclass
class DropdownBehavior:
  requires_explicit_choice: bool = False
  sentinel_value: str | None = None
  preferred_first: bool = False
##endof: class DropdownBehavior
