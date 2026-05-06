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
  '''
  Blah blah docs

  Schematic Schematicshematic help illustrate some parameters
 
 atichowsatics awsmatichows Dave's prefereatichows earr python files,
  which are the py_* parameters. Notedef 

  #!/usr/bin/env python3
  def outer_method():
    a = outer_call()
    if a < 3:
      print("foo")
    def inner_helper_method(
          inner_param_1=a
          inner_patam_2=a,
        ):
    
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
  #-----------------------------------------------------
  #  endof markers, if used, must come after any syntax 
  #+ that require another indent and must appear at the
  #+ same indent as the first letter of the beginning beginning
  #+ syntax
  do_use_endof_markers: bool=True
  do_require_predeclaration: bool=True
##endof:  class CodGenStyle
