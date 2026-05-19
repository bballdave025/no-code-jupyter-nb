For this class
- shift from parallel lists toward structured category records,

- and incorporate the later preference for tkinter-based local file selection over browser upload widgets. The OCR pages consistently evolve toward helper functions plus a factory-style widget API, and they explicitly note that browser upload widgets cannot reliably control the picker’s starting directory, while tkinter can via initialdir. They also evolve Method 3 toward a do_use_pandas=True clipboard default because that works locally and in VS Code Jupyter, whereas the JavaScript clipboard path is more environment-sensitive.  


I’d structure it around two dataclasses:

- `CategorySpec`: one record per category, replacing your matching tables.

- `NotebookConfig`: the notebook-wide state/config container.


That also gives `preferred_csv_filename` a clean home: it belongs on the category record, not in another parallel list. The OCR’d later design also clearly converges on helper functions like ensure_dir, copy_file_to_dir, open_csv_picker, validate_csv_path, format_status, and a create_fileupload_to_copy(...) factory with multiple selection methods under a radio selector.  

Here is a coherent first-pass implementation.

```python
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional, Literal
import json
import os
import shutil
import webbrowser

import ipywidgets as widgets
from IPython.display import display, Markdown, Javascript


AllowedOutputType = Literal["info_", "action_", "exception"]


@dataclass
class CategorySpec:
    """
    Replaces your old parallel lists such as:
      - CATEGORY_OPTIONS
      - CATEGORY_URLS
      - PREFERRED_CSV_FNAMES

    One object = one category.
    """
    key: str
    label: str
    uri: str = ""
    preferred_csv_filename: Optional[str] = None

    # Optional local HTML fallback metadata
    fallback_html_filename: Optional[str] = None
    fallback_html_title: Optional[str] = None
    fallback_html_text: Optional[str] = None


@dataclass
class NotebookConfig:
    """
    Notebook-wide state/config that used to live in globals.
    """
    maintainer_name: str = "Dave Black"
    maintainer_email: str = "user@domain.com"

    category_specs: list[CategorySpec] = field(default_factory=list)
    current_category_key: Optional[str] = None

    current_uri: Optional[str] = None
    csv_file: Optional[Path] = None
    used_csv_file: Optional[Path] = None
    table_data_root: Optional[Path] = None
    full_tdr_path: Optional[Path] = None

    default_file_location: Optional[Path] = None
    start_dir: Optional[Path] = None

    clipboard_use_pandas: bool = True

    def get_category_keys(self) -> list[str]:
        return [spec.key for spec in self.category_specs]

    def get_category_labels(self) -> list[str]:
        return [spec.label for spec in self.category_specs]

    def get_category_map(self) -> dict[str, CategorySpec]:
        return {spec.key: spec for spec in self.category_specs}

    def get_current_category(self) -> Optional[CategorySpec]:
        if self.current_category_key is None:
            return None
        return self.get_category_map().get(self.current_category_key)

    def get_current_uri(self) -> Optional[str]:
        spec = self.get_current_category()
        if spec is None:
            return self.current_uri
        return spec.uri or self.current_uri

    def get_preferred_csv_filename(self) -> Optional[str]:
        spec = self.get_current_category()
        if spec is None:
            return None
        return spec.preferred_csv_filename

    def ensure_default_paths(self) -> None:
        if self.default_file_location is None:
            self.default_file_location = NoCodeJupyterNb.default_project_dir()
        self.default_file_location.mkdir(parents=True, exist_ok=True)

        if self.start_dir is None:
            self.start_dir = NoCodeJupyterNb.default_start_dir()

    @classmethod
    def from_category_specs(
        cls,
        category_specs: list[CategorySpec],
        maintainer_name: str = "Dave Black",
        maintainer_email: str = "user@domain.com",
        default_category_key: Optional[str] = None,
    ) -> "NotebookConfig":
        cfg = cls(
            maintainer_name=maintainer_name,
            maintainer_email=maintainer_email,
            category_specs=category_specs,
            current_category_key=default_category_key,
        )
        cfg.ensure_default_paths()
        if cfg.get_current_category() is not None:
            cfg.current_uri = cfg.get_current_uri()
        return cfg


class NoCodeJupyterNb:
    """
    Factory-style helpers for no-code-ish Jupyter notebook UX.
    """

    # ----------------------------
    # Path / filesystem helpers
    # ----------------------------

    @staticmethod
    def default_project_dir(project_name: str = "MyProject") -> Path:
        home = Path.home()
        return home / "Documents" / project_name

    @staticmethod
    def default_start_dir() -> Path:
        return Path.home() / "Downloads"

    @staticmethod
    def ensure_dir(path: Path | str) -> Path:
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @staticmethod
    def move_to_front(item, lst: list) -> list:
        if item in lst:
            new_list = list(lst)
            new_list.remove(item)
            return [item] + new_list
        return list(lst)

    @staticmethod
    def validate_csv_path(raw: str | Path) -> Path:
        p = Path(str(raw).strip().strip('"').strip("'").strip("{}"))
        if not p.exists():
            raise ValueError(f"Path does not exist: {p}")
        if p.suffix.lower() != ".csv":
            raise ValueError(f"File is not a CSV: {p.name}")
        return p

    @staticmethod
    def copy_file_to_dir(src: Path | str, dest_dir: Path | str) -> Path:
        src_path = Path(src)
        dest_dir_path = NoCodeJupyterNb.ensure_dir(dest_dir)
        dest_path = dest_dir_path / src_path.name
        shutil.copy2(src_path, dest_path)
        return dest_path

    @staticmethod
    def format_status(
        dest_path: Optional[Path] = None,
        error: Optional[str] = None,
    ) -> str:
        if error:
            return f"Error: {error}"
        if dest_path:
            return f"Copied to:\n{dest_path}"
        return "No file selected."

    # ----------------------------
    # Presentation helpers
    # ----------------------------

    @staticmethod
    def create_highlighted_str(
        config: NotebookConfig,
        bare_string: str = "text to highlight not yet defined",
        type_of_output: AllowedOutputType = "info_",
    ) -> str:
        always_left = "# LOOK! #"

        exception_high_low = "# " + "!~" * 34 + "!"
        exception_type_left = "!~!"
        exception_first_text = (
            " EXCEPTION TEXT! THERE SHOULD BE INSTRUCTIONS.\n"
            " IF SO, FOLLOW THEM!"
        )
        exception_last_text = (
            " IF YOU'RE LOST, THAT'S Dave's or\n"
            f" {config.maintainer_name}'s FAULT. PLEASE\n"
            f" CONTACT THE LATTER AT {config.maintainer_email},\n"
            " OR CONTACT THE DATA PEOPLE."
        )

        info_high_low = "# " + "--" * 34 + "-"
        info_type_left = "---"
        info_first_text = (
            " INFORMATION TEXT. YOU SHOULD CHECK THAT\n"
            " THE INFORMATION IS CONSISTENT WITH YOUR\n"
            " TASK AND CATEGORY."
        )
        info_last_text = " THAT'S ALL FOR NOW."

        action_high_low = "# " + "=?==" * 17 + "="
        action_type_left = "=?="
        action_first_text = (
            " ACTION TEXT! WILL YOU GO DO THIS ACTION?\n"
            " IF NOT, YOU'LL BE STUCK SOMETIME LATER."
        )
        action_last_text = (
            " IF THINGS ARE UNCLEAR, FEEL FREE TO BLAME\n"
            f" Dave, BUT YOU'LL NEED TO CONTACT {config.maintainer_name}\n"
            f" AT {config.maintainer_email}, OR FEEL FREE\n"
            " TO CONTACT THE DATA PEOPLE."
        )

        if type_of_output == "exception_":
            this_type_high_low = exception_high_low
            this_type_left = exception_type_left
            this_type_first_text = exception_first_text
            this_type_last_text = exception_last_text
        elif type_of_output == "action_":
            this_type_high_low = action_high_low
            this_type_left = action_type_left
            this_type_first_text = action_first_text
            this_type_last_text = action_last_text
        elif type_of_output == "info_":
            this_type_high_low = info_high_low
            this_type_left = info_type_left
            this_type_first_text = info_first_text
            this_type_last_text = info_last_text
        else:
            raise ValueError(f"Unsupported type_of_output: {type_of_output}")

        highlighted_str = "\n" + this_type_high_low + "\n" + this_type_high_low + "\n"

        for line in this_type_first_text.splitlines():
            highlighted_str += f"{always_left}{this_type_left} {line}\n"

        highlighted_str += f"{always_left}{this_type_left}\n"

        for line in bare_string.splitlines():
            highlighted_str += f"{always_left}{this_type_left} {line}\n"

        highlighted_str += f"{always_left}{this_type_left}\n"

        for line in this_type_last_text.splitlines():
            highlighted_str += f"{always_left}{this_type_left} {line}\n"

        highlighted_str += this_type_high_low
        return highlighted_str

    @staticmethod
    def print_markdown(md_str: str) -> None:
        display(Markdown(md_str))

    # ----------------------------
    # HTML / URI helpers
    # ----------------------------

    @staticmethod
    def create_html_pg(
        bare_filename: str = "no-filename-given",
        title: str = "No Title Given",
        text_content: str = "No Content Given",
        do_go: bool = False,
        output_dir: Optional[Path | str] = None,
    ) -> str:
        if not bare_filename:
            bare_filename = "no-category-chosen"

        safe_name = Path(bare_filename).name
        if not safe_name.endswith(".html"):
            safe_name = f"{safe_name}.html"

        out_dir = Path(output_dir) if output_dir is not None else Path.cwd()
        out_dir.mkdir(parents=True, exist_ok=True)

        html = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
</head>
<body>
  <h1>READ THIS MESSAGE</h1>
  <p>{text_content}</p>
  <h2>Go back to the Jupyter notebook!</h2>
</body>
</html>
"""
        out_path = out_dir / safe_name
        out_path.write_text(html, encoding="utf-8")

        complete_url = out_path.resolve().as_uri()
        if do_go:
            webbrowser.open(complete_url)
        return complete_url

    @staticmethod
    def create_uri_button(
        uri_or_getter: str | Callable[[], Optional[str]],
        button_description: str = "Open URL",
        button_icon: str = "external-link",
        status_label: Optional[widgets.Label] = None,
    ) -> widgets.VBox:
        button = widgets.Button(description=button_description, icon=button_icon)
        output = widgets.Output()

        def _resolve_uri() -> Optional[str]:
            if callable(uri_or_getter):
                return uri_or_getter()
            return uri_or_getter

        def _on_click(_btn: widgets.Button) -> None:
            output.clear_output()
            uri = _resolve_uri()
            with output:
                if uri:
                    webbrowser.open(uri)
                    if status_label is not None:
                        status_label.value = f"Opened: {uri}"
                else:
                    print("No URI is currently available.")

        button.on_click(_on_click)
        return widgets.VBox([button, output])

    @staticmethod
    def create_copy_button(
        text_to_copy: str | Callable[[], str],
        button_description: str = "Copy URL",
        button_icon: str = "copy",
        use_js_not_pandas: bool = False,
    ) -> widgets.VBox:
        button = widgets.Button(description=button_description, icon=button_icon)
        output = widgets.Output()

        def _resolve_text() -> str:
            return text_to_copy() if callable(text_to_copy) else text_to_copy

        def _copy_with_pandas(value: str) -> None:
            import pandas as pd
            pd.DataFrame([[value]]).to_clipboard(index=False, header=False)

        def _on_click(_btn: widgets.Button) -> None:
            output.clear_output()
            value = _resolve_text()

            if use_js_not_pandas:
                copy_js = Javascript(
                    "navigator.clipboard.writeText("
                    f"{json.dumps(value)})"
                )
                with output:
                    display(copy_js)
            else:
                try:
                    _copy_with_pandas(value)
                except Exception as exc:
                    with output:
                        print(f"Clipboard copy failed: {exc}")

        button.on_click(_on_click)
        return widgets.VBox([button, output])

    # ----------------------------
    # Category-driven widgets
    # ----------------------------

    @staticmethod
    def create_category_dropdown(
        config: NotebookConfig,
        label: str = "Choose:",
    ) -> widgets.Dropdown:
        options = [(spec.label, spec.key) for spec in config.category_specs]

        dropdown = widgets.Dropdown(
            options=options,
            description=label,
            style={"description_width": "initial"},
        )

        if config.current_category_key is not None:
            dropdown.value = config.current_category_key

        def _on_change(change) -> None:
            if change["type"] == "change" and change["name"] == "value":
                config.current_category_key = change["new"]
                config.current_uri = config.get_current_uri()

        dropdown.observe(_on_change, names="value")
        return dropdown

    @staticmethod
    def create_category_uri_button(
        config: NotebookConfig,
        button_description: str = "Open category URI",
    ) -> widgets.VBox:
        return NoCodeJupyterNb.create_uri_button(
            uri_or_getter=config.get_current_uri,
            button_description=button_description,
            button_icon="external-link",
        )

    # ----------------------------
    # CSV selection helpers
    # ----------------------------

    @staticmethod
    def open_csv_picker(start_dir: Path | str) -> Optional[Path]:
        import tkinter as tk
        from tkinter import filedialog

        start_dir_path = Path(start_dir)

        root = tk.Tk()
        root.withdraw()
        root.call("wm", "attributes", ".", "-topmost", True)

        chosen = filedialog.askopenfilename(
            title="Choose a CSV file",
            initialdir=str(start_dir_path),
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        root.destroy()

        return Path(chosen) if chosen else None

    @staticmethod
    def open_drag_drop_window(
        dest_dir: Path | str,
        on_success: Callable[[Path], None],
        on_error: Callable[[str], None],
        start_dir: Optional[Path | str] = None,
    ) -> None:
        import tkinter as tk
        from tkinter import filedialog

        try:
            from tkinterdnd2 import TkinterDnD, DND_FILES
        except ImportError:
            on_error("tkinterdnd2 is not installed. Run: pip install tkinterdnd2")
            return

        dest_dir_path = NoCodeJupyterNb.ensure_dir(dest_dir)
        initial_dir = Path(start_dir) if start_dir is not None else dest_dir_path

        root = TkinterDnD.Tk()
        root.title("Drag & Drop a CSV — or click Browse")
        root.geometry("420x180")
        root.call("wm", "attributes", ".", "-topmost", True)

        instruction = tk.Label(
            root,
            text="Drag a CSV file here\nor click Browse",
            font=("Segoe UI", 13),
            pady=20,
            relief="groove",
            width=40,
        )
        instruction.pack(padx=20, pady=(20, 8), fill="x")

        def _handle_path(raw: str) -> None:
            cleaned = raw.strip().strip("{").strip("}")
            try:
                src = NoCodeJupyterNb.validate_csv_path(cleaned)
                dest_path = NoCodeJupyterNb.copy_file_to_dir(src, dest_dir_path)
                on_success(dest_path)
            except Exception as exc:
                on_error(str(exc))
            finally:
                root.destroy()

        def _on_drop(event) -> None:
            _handle_path(event.data)

        def _on_browse() -> None:
            chosen = filedialog.askopenfilename(
                title="Choose a CSV file",
                initialdir=str(initial_dir),
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            )
            if chosen:
                _handle_path(chosen)
            else:
                root.destroy()

        instruction.drop_target_register(DND_FILES)
        instruction.dnd_bind("<<Drop>>", _on_drop)

        browse_btn = tk.Button(
            root,
            text="Browse...",
            command=_on_browse,
            font=("Segoe UI", 10),
        )
        browse_btn.pack()

        root.mainloop()

    @staticmethod
    def create_paste_button(
        on_paste: Callable[[str], None],
        button_description: str = "Paste from Clipboard",
        button_icon: str = "paste",
        do_use_pandas: bool = True,
    ) -> widgets.VBox:
        button = widgets.Button(description=button_description, icon=button_icon)
        display_box = widgets.Textarea(
            value="",
            placeholder="Pasted path will appear here...",
            disabled=True,
            layout=widgets.Layout(width="420px", height="48px"),
        )
        js_output = widgets.Output()

        def _read_clipboard_pandas() -> str:
            import pandas as pd
            df = pd.read_clipboard(header=None)
            value = str(df.iloc[0, 0])
            return value.strip().strip('"').strip("'")

        paste_js = Javascript("""
        navigator.clipboard.readText().then(function(text) {
            console.log(text);
        });
        """)

        def _on_click(_btn) -> None:
            js_output.clear_output()
            try:
                if do_use_pandas:
                    text = _read_clipboard_pandas()
                    display_box.value = text
                    if text:
                        on_paste(text)
                else:
                    with js_output:
                        display(paste_js)
                        print("JS clipboard read triggered. Paste manually if needed.")
            except Exception as exc:
                display_box.value = f"Clipboard read failed: {exc}"

        button.on_click(_on_click)
        return widgets.VBox([button, display_box, js_output])

    @staticmethod
    def create_csv_file_selector(
        config: NotebookConfig,
        dest_dir: Path | str,
        start_dir: Optional[Path | str] = None,
        include_drag_drop: bool = True,
        include_paste: bool = True,
    ) -> widgets.VBox:
        """
        Four-method selector:
        1. Look in default
        2. Text entry + Go
        3. Paste from clipboard
        4. Drag & Drop / Browse
        """
        dest_dir_path = NoCodeJupyterNb.ensure_dir(dest_dir)
        start_dir_path = Path(start_dir) if start_dir is not None else (
            config.start_dir or NoCodeJupyterNb.default_start_dir()
        )

        status_label = widgets.Label(value="No file chosen yet.")

        def reset_status() -> None:
            status_label.value = "No file chosen yet."

        def set_success(dest_path: Path) -> None:
            config.csv_file = dest_path
            config.used_csv_file = dest_path
            status_label.value = NoCodeJupyterNb.format_status(dest_path)

        def set_error(message: str) -> None:
            status_label.value = NoCodeJupyterNb.format_status(None, error=message)

        def attempt_copy(raw_path: str) -> None:
            try:
                src = NoCodeJupyterNb.validate_csv_path(raw_path)
                dest_path = NoCodeJupyterNb.copy_file_to_dir(src, dest_dir_path)
                set_success(dest_path)
            except Exception as exc:
                set_error(str(exc))

        # Method 1
        default_btn = widgets.Button(
            description="Look in Default",
            button_style="primary",
            icon="folder-open",
            layout=widgets.Layout(width="180px"),
        )

        def _on_default_click(_btn) -> None:
            reset_status()
            src = NoCodeJupyterNb.open_csv_picker(start_dir_path)
            if src is None:
                status_label.value = "No file selected."
                return
            try:
                set_success(NoCodeJupyterNb.copy_file_to_dir(src, dest_dir_path))
            except Exception as exc:
                set_error(str(exc))

        default_btn.on_click(_on_default_click)
        panel_default = widgets.VBox([default_btn])

        # Method 2
        path_input = widgets.Text(
            placeholder=r"e.g. C:\Users\Dave\Downloads\data.csv",
            layout=widgets.Layout(width="420px"),
        )
        go_btn = widgets.Button(
            description="Go",
            button_style="success",
            icon="check",
            layout=widgets.Layout(width="80px"),
        )

        def _on_go_click(_btn) -> None:
            reset_status()
            attempt_copy(path_input.value)

        go_btn.on_click(_on_go_click)
        panel_text = widgets.VBox([widgets.HBox([path_input, go_btn])])

        panels: list[widgets.Widget] = [panel_default, panel_text]
        method_labels = ["Look in default", "Text entry and press Go"]

        # Method 3
        if include_paste:
            def _on_paste(text: str) -> None:
                reset_status()
                attempt_copy(text)

            panel_paste = NoCodeJupyterNb.create_paste_button(
                on_paste=_on_paste,
                do_use_pandas=config.clipboard_use_pandas,
            )
            panels.append(panel_paste)
            method_labels.append("Paste file path from clipboard")

        # Method 4
        if include_drag_drop:
            dnd_btn = widgets.Button(
                description="Open Drag & Drop Window",
                button_style="warning",
                icon="arrows",
                layout=widgets.Layout(width="240px"),
            )

            def _on_dnd_click(_btn) -> None:
                reset_status()
                NoCodeJupyterNb.open_drag_drop_window(
                    dest_dir=dest_dir_path,
                    on_success=set_success,
                    on_error=set_error,
                    start_dir=start_dir_path,
                )

            dnd_btn.on_click(_on_dnd_click)
            panel_dnd = widgets.VBox([dnd_btn])
            panels.append(panel_dnd)
            method_labels.append("Drag & Drop / Browse")

        radio = widgets.RadioButtons(
            options=method_labels,
            value=method_labels[0],
            layout=widgets.Layout(width="320px"),
        )

        for i, panel in enumerate(panels):
            panel.layout.display = "flex" if i == 0 else "none"

        def _on_radio_change(change) -> None:
            if change["type"] == "change" and change["name"] == "value":
                reset_status()
                selected = change["new"]
                for label, panel in zip(method_labels, panels):
                    panel.layout.display = "flex" if label == selected else "none"

        radio.observe(_on_radio_change, names="value")

        return widgets.VBox(
            [
                widgets.HTML("<h3>Which method would you like to use to choose your CSV file?</h3>"),
                radio,
                widgets.VBox(panels),
                status_label,
            ],
            layout=widgets.Layout(gap="10px"),
        )

```

Example usage

```python
category_specs = [
    CategorySpec(
        key="No_Category_Chosen",
        label="No_Category_Chosen",
        uri=NoCodeJupyterNb.create_html_pg(
            bare_filename="no-category-chosen",
            title="Please Use Dropdown",
            text_content="Please choose a category before continuing.",
            do_go=False,
        ),
        preferred_csv_filename=None,
    ),
    CategorySpec(
        key="Category_1",
        label="Category_1",
        uri="https://whatever.that-domain.com/file-store/r?cat=1&blah=FirstCategory",
        preferred_csv_filename="Cat_1.csv",
    ),
    CategorySpec(
        key="Category_2",
        label="Category_2",
        uri="https://whatever.that-domain.com/file-store/r?cat=2&blah=SecondCategory",
        preferred_csv_filename="Cat_2.csv",
    ),
]

config = NotebookConfig.from_category_specs(
    category_specs=category_specs,
    default_category_key="No_Category_Chosen",
    maintainer_name="Dave Black",
    maintainer_email="user@domain.com",
)

category_dropdown = NoCodeJupyterNb.create_category_dropdown(config, label="Choose:")
display(category_dropdown)

display(NoCodeJupyterNb.create_category_uri_button(config))
display(
    NoCodeJupyterNb.create_copy_button(
        text_to_copy=lambda: config.get_current_uri() or "",
        use_js_not_pandas=False,
    )
)

display(
    NoCodeJupyterNb.create_csv_file_selector(
        config=config,
        dest_dir=config.default_file_location,
        start_dir=config.start_dir,
        include_drag_drop=True,
        include_paste=True,
    )
)
```


My thoughts for the next refinement are:
1. freeze this shape,
2. rename `create_csv_file_selector` to whatever you like best,
3.   - pass in an `extension: str` parameter
4. then do a second pass to make the class more clean in naming, comments, and notebook ergonomics.

A few important decisions were: using category records instead of matching tables, preferring tkinter for local file selection because it supports a real starting directory, and defaulting clipboard paste toward the pandas path because it works across local browser Jupyter and VS Code Jupyter while the JS path is more situational. 
