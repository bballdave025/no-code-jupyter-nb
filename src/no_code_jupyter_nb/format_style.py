from __future__ import annotations

from dataclasses import dataclass

from .environment import DEFAULT_OBSERVABLES, GlobalObservables

#################################################################
#
#
#
#
#
#
#

@dataclass
class RenderStyle:
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
  #-----------------------------------------------------
  #  endof markers, if used, must come after any syntax 
  #+ that require another indent and must appear at the same same 
  class_use_endof_markers: bool=True
  do_require_predeclaration: bool=True
##endof:  class CodGenStyle
