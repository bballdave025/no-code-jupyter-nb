from __future__ import annotations

from dataclasses import dataclass

from typing import Literal

InstructionLevel = Literal[
  "normal",
  "just_shift_enter",
  "look_above",
  "stop_and_choose",
]

VisibilityLevel = Literal[
  "normal",
  "advanced",
  "dangerous",
]

@dataclass
class NotebookBlock:
  name: str
  cell_type: Literal["code", "markdown"]
  content: str

  title: str = ""

  instruction_level: InstructionLevel = "normal"

  visibility: VisibilityLevel = "normal"

  auto_run_hint: bool = False

  depends_on: list[str] = field(default_factory=list)
##endof: class NotebookBlock
