# Smoke Test — JSON Config Loader

Test run:

```text
1779316724_2026-05-20T183844-0400
```

Working directory:

```text
/data/data/com.termux/files/home/my_repos_dwb/no-code-jupyter-nb/src/no_code_jupyter_nb
```

## 1. Verify `NotebookConfig.from_dict(...)`

Command:

```bash
python -c \
"from no_code_jupyter_nb import NotebookConfig; \
print([member for member in dir(NotebookConfig) if not member.startswith('_')])"
```

Output:

```text
['current_category_key', 'current_maintainer_email', 'current_maintainer_name', 'current_subcategory_key', 'current_uri', 'from_dict', 'get_category_map', 'get_current_category', 'get_current_uri', 'original_no_code_email', 'original_no_code_maintainer', 'root_directory', 'selected_file']
```

Individual member checks:

```bash
to_check="from_dict" && [[ $(python -c "from no_code_jupyter_nb import NotebookConfig; print([member for member in dir(NotebookConfig) if not member.startswith('_')])") =~ ${to_check} ]] && echo -e "\n'${to_check}' checks\n" || echo -e "\n'${to_check}' does not check\n"

to_check="get_category_map" && [[ $(python -c "from no_code_jupyter_nb import NotebookConfig; print([member for member in dir(NotebookConfig) if not member.startswith('_')])") =~ ${to_check} ]] && echo -e "\n'${to_check}' checks\n" || echo -e "\n'${to_check}' does not check\n"

to_check="get_current_category" && [[ $(python -c "from no_code_jupyter_nb import NotebookConfig; print([member for member in dir(NotebookConfig) if not member.startswith('_')])") =~ ${to_check} ]] && echo -e "\n'${to_check}' checks\n" || echo -e "\n'${to_check}' does not check\n"

to_check="get_current_uri" && [[ $(python -c "from no_code_jupyter_nb import NotebookConfig; print([member for member in dir(NotebookConfig) if not member.startswith('_')])") =~ ${to_check} ]] && echo -e "\n'${to_check}' checks\n" || echo -e "\n'${to_check}' does not check\n"
```

Outputs:

```text
'from_dict' checks

'get_category_map' checks

'get_current_category' checks

'get_current_uri' checks
```

## 2. Verify `load_config_from_json(...)` imports

Command:

```bash
python -c "from no_code_jupyter_nb import load_config_from_json; print(load_config_from_json)"
```

Output:

```text
<function load_config_from_json at 0x7980ee1620>
```

The exact memory address may differ between runs.

## 3. Minimal config file

File:

```text
examples/minimal_config.json
```

Contents:

```json
{
  "current_category_key": "cat_1",
  "category_specs": [
    {
      "key": "cat_1",
      "label": "Category 1",
      "uri": "https://example.com",
      "preferred_filename": "cat_1.csv"
    }
  ]
}
```

## 4. End-to-end JSON hydration smoke test

Command:

```bash
python -c \
"from no_code_jupyter_nb import load_config_from_json; \
cfg = load_config_from_json('../../examples/minimal_config.json'); \
print(cfg); \
print(cfg.get_current_uri())"
```

Output:

```text
NotebookConfig(observables=GlobalObservables(runtime=RuntimeEnvironment(os_name='Android', machine_endianness='little', locale_name='C', machine_description='aarch64 / unknown-cpu', python_bitness=64, python_version=(3, 13, 13), is_windows=False, is_linux=False, is_macos=False, home_dir=PosixPath('/data/data/com.termux/files/home'), downloads_dir=PosixPath('/data/data/com.termux/files/home/Downloads')), default_case_sensitive_extensions=True, runtime_is_on_vs_code=False, runtime_is_on_jupyter_std_server=False, runtime_is_on_jupyter_lab=False, runtime_is_on_amazon_sagemaker=False, runtime_is_on_google_colab=False, runtime_is_on_binder=False, have_js_clipboard_access=False, have_pandas_clipboard_access=False), original_no_code_maintainer='', original_no_code_email='', current_maintainer_name='Dave Black', current_maintainer_email='user@domain.com', category_specs=[CategorySpec(key='cat_1', label='Category 1', uri='https://example.com', preferred_filename='cat_1.csv', subcategories=[], metadata={})], current_category_key='cat_1', current_subcategory_key=None, selected_file=None, current_uri=None, root_directory=None, runtime_options={})
https://example.com
```

## Result

This smoke test confirms:

- `NotebookConfig.from_dict(...)` is present.
- `NotebookConfig` helper methods are present.
- `load_config_from_json(...)` is exported from the package root.
- `examples/minimal_config.json` loads successfully.
- JSON data hydrates into a live `NotebookConfig`.
- Category data hydrates into `CategorySpec`.
- `cfg.get_current_uri()` returns the expected URI.

This establishes the first working vertical slice:

```text
JSON → dict → CategorySpec → NotebookConfig → usable config method
```

Commit message: 

> Add JSON config loader and smoke-test hydration pipeline

