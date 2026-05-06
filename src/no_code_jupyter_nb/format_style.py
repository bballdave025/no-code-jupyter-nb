from __future__ import annotations

from dataclasses import dataclass, field

from .environment import DEFAULT_OBSERVABLES, GlobalObservables

@dataclass
class RenderStyle:
  py_indent: int = 2
  ipynb_indent: int = 4
  max_line_length: int = 79
  preferred_line_length: int = 72
##endof:  class RenderStyle

@dataclass
class CodGenStyle:
  do_use_endof_markers: True
=True
  do_require_predeclaration: bool=True
##endof:  class CodGenStyle
