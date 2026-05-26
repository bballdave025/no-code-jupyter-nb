ON config loader + dataclass hydration path

This PR establishes the first executable JSON → abstraction hydration
path for `no_code_jupyter_nb`.

The implementation intentionally remains:
- lightweight,
- dataclass-first,
- validation-light,
- and dependency-minimal.

The current vertical slice is now:

```text
JSON → dict → CategorySpec → NotebookConfig → usable config methods
```

Validated functionality includes:

- `CategorySpec.from_dict(...)`
- `NotebookConfig.from_dict(...)`
- `load_json_file(...)`
- `load_config_from_json(...)`
- package-root export wiring
- executable end-to-end hydration tests
- minimal example config loading

Smoke-test validation now succeeds for:

```bash
python -c \
"from no_code_jupyter_nb import CategorySpec, NotebookConfig, load_config_from_json, load_json_file; \
print('imports check')"
```

and:

```bash
python -c \
"from no_code_jupyter_nb import load_config_from_json; \
cfg = load_config_from_json('examples/minimal_config.json'); \
print(cfg.current_category_key); \
print(cfg.get_current_category()); \
print(cfg.get_current_uri())"
```

with successful output:

```text
cat_1
CategorySpec(
  key='cat_1',
  label='Category 1',
  uri='https://example.com',
  preferred_filename='cat_1.csv',
  subcategories=[],
  metadata={}
)
https://example.com
```

Current implementation intentionally avoids:
- schema engines,
- traitlets,
- pydantic,
- notebook orchestration,
- automatic widget inference,
- generalized serialization frameworks,
- and heavy validation/runtime frameworks.

Reason:
the architecture is still stabilizing, and explicit dataclass hydration
currently provides the clearest implementation path.

This PR is intended to establish:
- executable structure,
- readable hydration semantics,
- and maintainable lightweight configuration flow

before introducing additional framework gravity.

Future likely follow-up areas include:
- generalized file selectors
- notebook block integration
- highlighted messaging helpers
- optional schema validation
- notebook renderer expansion
