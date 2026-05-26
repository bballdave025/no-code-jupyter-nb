from __future__ import annotations

from dataclasses import dataclass, field
import pathlib

from .categories import CategorySpec
from .environment import DEFAULT_OBSERVABLES, GlobalObservables


@dataclass
class NotebookConfig:
  '''
  Notebook/session/project choices.

  Does not recompute environment information.
  '''

  observables: GlobalObservables = field(
    default_factory=lambda: DEFAULT_OBSERVABLES
  )

  original_no_code_maintainer: str = "Dave Black"
  original_no_code_email: str = "user@domain.com"

  current_maintainer_name: str = "Dave Black"
  current_maintainer_email: str = "user@domain.com"

  category_specs: list[CategorySpec] = field(default_factory=list)

  current_category_key: str | None = None
  current_subcategory_key: str | None = None

  selected_file: pathlib.Path | None = None
  current_uri: str | None = None

  root_directory: pathlib.Path | None = None

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

  def get_current_uri(self) -> str | None:
    current_category = self.get_current_category()

    if current_category is None:
      return self.current_uri
    ##endof: if current_category is None

    return current_category.uri or self.current_uri
  ##endof: get_current_uri(self)

  @classmethod
  def from_dict(
        cls,
        raw: dict[str, object],
        category_specs: list[CategorySpec],
      ) -> "NotebookConfig":
    root_directory = raw.get("root_directory")

    return cls(
      original_no_code_maintainer=str(
        raw.get("original_no_code_maintainer", "")
      ),
      original_no_code_email=str(
        raw.get("original_no_code_email", "")
      ),
      current_maintainer_name=str(
        raw.get("current_maintainer_name", "Dave Black")
      ),
      current_maintainer_email=str(
        raw.get("current_maintainer_email", "user@domain.com")
      ),
      category_specs=category_specs,
      current_category_key=raw.get("current_category_key"),
      current_subcategory_key=raw.get("current_subcategory_key"),
      current_uri=raw.get("current_uri"),
      root_directory=(
        pathlib.Path(str(root_directory))
        if root_directory is not None
        else None
      ),
      runtime_options=dict(raw.get("runtime_options", {})),
    )
  ##endof: from_dict(...)

##endof: class NotebookConfig
