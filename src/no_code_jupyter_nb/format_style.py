from __future__ import annotations

from dataclasses import dataclass

from .environment import DEFAULT_OBSERVABLES, GlobalObservables


@dataclass
class RenderStyle:
  '''
  Formatting preferences for generated Python and notebook code.

  This object records indentation and line-length choices separately for
  `.py` files and generated notebook cells.
  '''
  
  py_indent: int=2
  py_indent_for_params_beyond_def: int=6
  py_indent_for_closing_paren_beyond_def: int=4
  ipynb_indent: int=4
  ipynb_indent_for_params_beyond_def: int=12
  ipynb_indent_for_closing_paren_beyond_def: int=4
  max_line_length: int=79
  preferred_line_length: int=72
##endof:  class RenderStyle


@dataclass
class CodeGenStyle:
  '''
  Structural code-generation preferences.

  These settings control optional conventions such as predeclared scope
  variables,  explicit ##endof markers after indented blocks,
  and whether single or double quotes are used in triplicate
  for docstrings.
  '''

  do_use_endof_markers: bool=True
  do_require_predeclaration: bool=True
  docstring_choice: str="three_singles"
##endof:  class CodeGenStyle
