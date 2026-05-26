from __future__ import annotations

import json
import pathlib
from typing import Any

from .categories import CategorySpec
from .nb_config import NotebookConfig


def load_json_file(
      config_path: pathlib.Path | str,
    ) -> dict[str, Any]:
  path = pathlib.Path(config_path)

  with path.open("r", encoding="utf-8") as ifh:
    raw = json.load(ifh)
  ##endof: with path.open(...)

  if not isinstance(raw, dict):
    raise TypeError("Config JSON root must be an object/dict.")
  ##endof: if not isinstance(raw, dict)

  return raw
##endof: load_json_file(...)


def load_config_from_json(
      config_path: pathlib.Path | str,
    ) -> NotebookConfig:
  raw = load_json_file(config_path)

  raw_categories = raw.get("category_specs", [])

  if not isinstance(raw_categories, list):
    raise TypeError("Config field 'category_specs' must be a list.")
  ##endof: if not isinstance(raw_categories, list)

  category_specs = [
    CategorySpec.from_dict(item)
    for item in raw_categories
  ]

  return NotebookConfig.from_dict(
    raw=raw,
    category_specs=category_specs,
  )
##endof: load_config_from_json(...)


def add_to_json_cli(
      thing_added: str,
      description: dict,
      config_json: pathlib.Path | str,
      do_backup: bool = True,
    ) -> None:
  pass
##endof: add_to_json_cli(...)


def remove_from_json_cli(
      thing_removed: str,
      key: str,
      config_json: pathlib.Path | str,
      do_backup: bool = True,
    ) -> None:
  pass
##endof: remove_from_json_cli(...)
