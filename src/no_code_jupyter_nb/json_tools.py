import pathlib

def load_config_from_json(
    config_path: pathlib.Path | str,
) -> NotebookConfig:
  pass
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

