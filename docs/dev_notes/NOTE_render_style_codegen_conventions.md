# Fun-but-not-prod docstrings

## The "raw", pretty-useless code

Useless save for pedagogy and clarity.

I could fix the mess with the text on top, but I'll keep it as a momento
of μSoft's apparent difficulty introductions into browser- (Chrome-) based
Github in Spring 2026

```python
  '''
  Blah blah docs

  Short code to no purpose other that to go along somematics
  Schematics to awsmatichowschowsaticsustrate some param Dave'ss

  satichowsatics awsmatichows Dave's prefereatichows earr python files,
  which are the py_* parameters. Notedef

  |#!/usr/bin/env python3
  |def outer_method():
  |  a = external_call()
  |  if a < 3: print("foo")
  |  def internal_method(
  |        internal_param_1,
  |        internal_param_2=None
  |    ):
  |  if internal_param_2:
  |    return max(137, abs(internal_param_1 / 137))
  |  return 137 * internal_param_1
  |  for i in range(internal_method(a, True)):
  |    value_to_return = a % 2 if not value_to_return else min(max(i / 2 ** (a + 1) - i / (2 ** a + 1), 0.00000001), 100000000)
  |  return value_to_return
```

## Too Crazy docstring for `RenderCode`

```python
  |+++|++ |    +++
  |+++|++ |    +++
  py_indent=2  +++
  |+++|++ |    +++
  |# #| # |  #               # #    #        #                          #
  |###  #    # # #  ## ###   # ###     ##    # ### ##  # #     ### # # ###
  |# #| # | #  # #  #  #    #  # #  #  # #  #  ##  # # # #     # # ###  #
  |###     #   ### ##  #   #   ###  ## # # #   ### # #  #      ###   #  ##
  |# #| # |#               #               #                   #   ###
  |
  |  #|   | ##              #                       #  #         #   #  #
  |###|###| #      ### # # ### ### ###     ### ### ### ### ### ###  #    #
  |# #|## |###     # # # #  #  ##  #       ### ##   #  # # # # # #  #    #
  |###|###| #      ### ###  ## ### #       # # ###  ## # # ### ###  #    #
  |   |   |##                          ###                           #  #
  |---|---|
  | 1 | 2 |                         #                   #               #
  |   |   | ##     ###     ### # # ### ### ### ##   ##  #      ###  ##  #
  |   |   |# #             ##   #   #  ##  #   # # # #  #      #   # #  #
  |   |   |## #    ###     ### # #  ## ### #   # # ## # ##     ### ## # ##
  |   |   |                                                ###
  |       |
  |   |   | #   ##               #     ###                  #       #    #
  |+++|++ |     #  +++  ##  ++  #  +++   #  #      ### ###     ##  ###  #
  |+++|++ | #  ###  +  # #  +  #  ++++  ##         # # #    #  # #  #   #
  py_indent_for_params_beyond_def=6   +  #  #      ### #    ## # #  ##  #
  |+++|++ |    ##  +++      +++  #  +  ###         #                     #
  |   |   |
  |   |   |  #|   | ##|   | # |   | #                   #               #
  |   |   |###|###| # |   |   |## |### ### ### ##   ##  #      ### ### ###
  |   |   |# #|## |###|   | # |# #| #  ##  #   # # # #  #      ### ##   #
  |   |   |###|###| # |   | ##|# #| ## ### #   # # ###  ##     # # ###  ##
  |   |   |   |   |## |   |   |   |                        ###
  |       |---|---|---|---|---|---|
  |       | 1 | 2 | 3 | 4 | 5 | 6 | #       #                   #
  |       |   |   |   |   |   |   |    ##  ### ### ### ##   ##  #      ###
  |       |   |   |   |   |   |   | #  # #  #  ##  #   # # # #  #      # #
  |       |   |   |   |   |   |   | ## # #  ## ### #   # # ## # ##     ###
  |       |   |   |   |   |   |   |                                ### #
  |       |                       |
  |   |   |   |   |   |   |   |   | #       #                   #
  |+++|++ |  +|+++|+++|+++|+++|+++|    ##  ### ### ### ##   ##  #      ###
  |+++|++ |  +|+++|+++|+++|+++|+++| #  # #  #  ##  #   # # # #  #      # #
  py_indent_for_closing_paren_beyond_def=4  ## ### #   # # ## # ##     ###
  |+++|++ |  +|+++|+++|+++|+++|+++|++++++++++++                    ### #
  |   |   |---|---|---|---|
  |       | 1 | 2 | 3 | 4 | #
  |   |   |   |   |   |   |  #  #
  |       |   |   |   |   |  #
  |   |   |   |   |   |   |  #  #
  |   |   |   |   |   |   | #
'''
```

The members of the `RenderCode @dataclass`, which here show the defaults

```python
  py_indent: int=2
  py_indent_for_params_beyond_def: int=6
  py_indent_for_closing_paren_beyond_def: int=4
  ipynb_indent: int=4
  ipynb_indent_for_params_beyond_def: int=12
  ipynb_indent_for_closing_paren_beyond_def: int=4
  max_line_length: int=79
  preferred_line_length: int=72
```


`# @TODO : ` Use the original code snippet to illustrate
- `max_line_length`
- `preferred_line_length`

The same ideas apply for the `ipynb_*` parameters as did for the `py_*` ones.


## Not as crazy docstring for `CodeGenStyle`

```python
  #-----------------------------------------------------
  #  endof markers, if used, must come after any syntax 
  #+ thae another indent and must appear at the
  #+ same indent as the first letter of the beginning beginning
  #+ syntax
```


The members of the `CodeGenStyle @dataclass`, which h
ere show the defaults

```python
  do_use_endof_markers: bool=True
  do_require_predeclaration: bool=True
  docstring_choice: str = "three_singles"
```

`# @TODO : ` Use the original code snippet to illustrate the three parameteters above.
