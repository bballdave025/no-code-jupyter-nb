import pathlib

from typing import Literal

@dataclass
class FileSelectionResult:
  selected_path: pathlib.Path | None
  preferred_found: bool
  candidates: list[pathlib.Path]

  confidence: Literal[
    "preferred",
    "fallback",
    "none",
  ]
##endof: class FileSelectionResult

class FileSystemOps:

  @staticmethod
  def ensure_structure(
      root: pathlib.Path,
      subcats: list[str],
      verbose: bool = True,
  ) -> None:
    pass
  ##endof: ensure_structure(...)
##endof: class FileSystemOps
