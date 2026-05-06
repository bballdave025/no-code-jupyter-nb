from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .categories import CategorySpec
from .environment import DEFAULT_OBSERVABLES, GlobalObservables


@dataclass
class NotebookConfig:
  """
  Notebook/session/project choices.

  Does not recompute environment information.
  """

  observables: GlobalObservables = field(
    default_factory=lambda: DEFAULT_OBSERVABLES
  )
  maintainer_name: str = "Dave Black"
  maintainer_email: str = "user@domain.com"
  category_specs: list[CategorySpec] = field(default_factory=list)
  current_category_key: str | None = None
  current_subcategory_key: str | None = None
  selected_file: Path | None = None
  current_uri: str | None = None
  root_directory: Path | None = None
  runtime_options: dict[str, object] = field(default_factory=dict)

  def get_category_map(self) -> dict[str, CategorySpec]:
    return {spec.key: spec for spec in self.category_specs}
  ##endof: get_category_map(self)

  def get_current_category(self) -> CategorySpec | None:
    category_map = self.get_category_map()

    if self.current_category_key is None:
      return None
    ##endof: if self.current_category_key is None

    return category_map.get(self.current_category_key)
  ##endof: get_current_category(self)
##endof: class NotebookConfig
