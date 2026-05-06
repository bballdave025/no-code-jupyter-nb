from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CategorySpec:
  """
  Replaces parallel matching lists and makes JSON-driven setup easier.
  """

  key: str
  label: str
  uri: str = ""
  preferred_filename: str | None = None
  subcategories: list[str] = field(default_factory=list)
  metadata: dict[str, Any] = field(default_factory=dict)
##endof: class CategorySpec
