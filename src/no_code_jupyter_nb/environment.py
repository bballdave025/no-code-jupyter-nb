from __future__ import annotations

from dataclasses import dataclass
import pathlib
import locale as locale_module
import os
import platform
import struct
import sys


@dataclass(frozen=True)
class RuntimeEnvironment:
  os_name: str
  machine_endianness: str
  locale_name: str
  #machine_word_size: int
  machine_description: str
  python_bitness: int
  python_version: tuple[int, int, int]
  is_windows: bool
  is_linux: bool
  is_macos: bool
  home_dir: pathlib.Path
  downloads_dir: Path

  @classmethod
  def detect(cls) -> "RuntimeEnvironment":
    os_name = platform.system()
    home_dir = pathlib.Path.home()

    return cls(
      os_name=os_name,
      machine_endianness=sys.byteorder,
      locale_name=locale_module.getlocale()[0] or "",
      #machine_word_size=struct.calcsize("P") * 8,
      machine_description=(
        f"{platform.machine()} / "
        f"{platform.processor() or 'unknown-cpu'}"
      ),
      python_bitness=struct.calcsize("P") * 8,
      python_version=sys.version_info[:3],
      is_windows=(os_name == "Windows"),
      is_linux=(os_name == "Linux"),
      is_macos=(os_name == "Darwin"),
      home_dir=home_dir,
      downloads_dir=home_dir / "Downloads",
    )
  ##endof: detect(cls)
##endof: class RuntimeEnvironment


@dataclass(frozen=True)
class GlobalObservables:
  runtime: RuntimeEnvironment
  default_case_sensitive_extensions: bool
  runtime_is_on_vs_code: bool
  runtime_is_on_jupyter_std_server: bool
  runtime_is_on_jupyter_lab: bool
  runtime_is_on_amazon_sagemaker: bool
  runtime_is_on_google_colab: bool
  runtime_is_on_binder: bool
  have_js_clipboard_access: bool
  have_pandas_clipboard_access: bool

  @classmethod
  def detect(cls) -> "GlobalObservables":
    runtime = RuntimeEnvironment.detect()
    env_vars = os.environ

    runtime_is_on_vs_code = "VSCODE_PID" in env_vars
    runtime_is_on_google_colab = "COLAB_RELEASE_TAG" in env_vars
    runtime_is_on_binder = "BINDER_SERVICE_HOST" in env_vars
    runtime_is_on_amazon_sagemaker = (
      "SAGEMAKER_INTERNAL_IMAGE_URI" in env_vars
      or "SM_CURRENT_HOST" in env_vars
    )

    # @TODO: Refine Jupyter/Lab detection from active kernel metadata.
    runtime_is_on_jupyter_std_server = False
    runtime_is_on_jupyter_lab = False

    # @TODO: JS clipboard often requires browser/user-event confirmation.
    have_js_clipboard_access = False

    try:
      import pandas  # noqa: F401
      have_pandas_clipboard_access = True
    except ImportError:
      have_pandas_clipboard_access = False
    ##endof: try/except

    return cls(
      runtime=runtime,
      default_case_sensitive_extensions=not runtime.is_windows,
      runtime_is_on_vs_code=runtime_is_on_vs_code,
      runtime_is_on_jupyter_std_server=runtime_is_on_jupyter_std_server,
      runtime_is_on_jupyter_lab=runtime_is_on_jupyter_lab,
      runtime_is_on_amazon_sagemaker=runtime_is_on_amazon_sagemaker,
      runtime_is_on_google_colab=runtime_is_on_google_colab,
      runtime_is_on_binder=runtime_is_on_binder,
      have_js_clipboard_access=have_js_clipboard_access,
      have_pandas_clipboard_access=have_pandas_clipboard_access,
    )
  ##endof: detect(cls)

  @property
  def os_name(self) -> str:
    return self.runtime.os_name
  ##endof: os_name(self)

  @property
  def home_dir(self) -> pathlib.Path:
    return self.runtime.home_dir
  ##endof: home_dir(self)

  @property
  def downloads_dir(self) -> pathlib.Path:
    return self.runtime.downloads_dir
  ##endof: downloads_dir(self)
##endof: class GlobalObservables


DEFAULT_OBSERVABLES = GlobalObservables.detect()
