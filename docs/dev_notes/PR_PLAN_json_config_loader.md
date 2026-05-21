# PR: JSON config loader + dataclass hydration path

Relevant branch:
`feat/json-config-loader`

---

## Summary

Implements the first real JSON → abstraction execution path for
`no_code_jupyter_nb`.

This PR introduces lightweight JSON loading and hydration into:
- `CategorySpec`
- `NotebookConfig`

The goal is to establish a clean, executable vertical slice of the
future pipeline:

```text
JSON → Config objects → Notebook workflow
```

This is intentionally:
- lightweight,
- dataclass-first,
- validation-light,
- and dependency-minimal.

No schema engine or notebook orchestration yet.

---

## Scope

This PR includes:

- lightweight JSON loading helpers
- `CategorySpec` hydration
- `NotebookConfig` hydration
- minimal validation/checking
- executable smoke-test examples
- optional future-ready validation hooks

This PR does NOT include:
- notebook rendering
- widget orchestration
- notebook block dependency systems
- plugin systems
- full schema enforcement
- traitlets/pydantic migration
- automatic notebook generation

---

## Explicit non-goals

Non-goals for this PR:

- full JSON schema system
- runtime mutation engine
- CLI tooling
- notebook execution flow
- automatic widget inference
- generalized serialization framework
- advanced validation semantics

Lean-to only.

---

## Architectural intent

This PR establishes the first stable execution path from serialized
configuration into structured runtime abstractions.

Key design goals:

- JSON remains source-of-truth
- dataclasses remain core abstraction layer
- runtime remains lightweight
- optional dependencies remain optional
- validation should degrade gracefully
- object hydration should remain explicit and readable

The loader should be understandable by future maintainers without
framework archaeology.

---

## Checklist

Items in _italics_ are those not included in the original checklist, often the implementation of one part of the config or category loading.

### Packaging / structure

- [ ] Create/update `load_config_from_json(...)`
  - [x] _minimal JSON_
- [ ] Ensure imports remain lightweight
- [ ] Avoid introducing hard runtime dependencies
- [ ] Export loader helpers if appropriate

### Core implementation

- [ ] Load JSON from file
  - [x] _minimal JSON_
- [ ] Parse category records
  - [x] _minimal JSON_
- [ ] Hydrate `CategorySpec`
  - [x] _minimal JSON_
- [ ] Hydrate `NotebookConfig`
- [ ] Support default category selection
- [ ] Support optional/missing fields safely
- [ ] Preserve explicit metadata semantics

### Validation / smoke tests

- [x] Minimal valid JSON config loads successfully
- [x] `CategorySpec` list hydrates correctly
- [ ] `NotebookConfig.current_category_key` works
- [x] `config.get_current_category()` works
- [x] `config.get_current_uri()` works
- [ ] Import checks still succeed
  - [x] _minimal JSON_

### UX / notebook behavior

- [ ] Preserve loud/failure-first philosophy
- [ ] Avoid silent malformed-category behavior
- [ ] Prefer explicit exceptions over hidden defaults

---

## Implementation notes

### Current implementation direction

The current implementation intentionally prefers:

- explicit dataclass hydration
over
- automatic framework magic

and:

- lightweight helper validation
over
- heavyweight runtime dependency systems

### Validation direction

Potential future optional dependency:

```toml
[project.optional-dependencies]
validation = [
  "jsonschema>=4,<5",
  ]
```

  However:

  - schema validation is NOT required for this PR
  - runtime should still function without optional validators installed

  ### Traitlets note

  `traitlets` was discussed but intentionally deferred.

  Reason:
  - too much framework gravity too early
  - current architecture still stabilizing
  - dataclass-first approach remains clearer for now

  ---

  ## Terminal validation

  Planned validation examples:

  ```bash
  python -c \
  "from no_code_jupyter_nb import load_config_from_json; \
  cfg = load_config_from_json('config.json'); \
  print(cfg)"
  ```

  and:

  ```bash
  python -c \
  "from no_code_jupyter_nb import load_config_from_json; \
  cfg = load_config_from_json('config.json'); \
  print(cfg.get_current_uri())"
  ```

  ---

  ## Future follow-up notes

  Likely future PRs after this:

  - generalized file selector abstraction
  - notebook block rendering integration
  - highlighted messaging helpers
  - category/subcategory gating cleanup
  - optional schema validation
  - notebook renderer expansion

  ---

  ## Deferred intentionally

  Deferred for now:

  - notebook orchestration engine
  - automatic widget generation
  - block dependency graph systems
  - advanced runtime state machine logic
  - plugin architecture
  - CLI mutation tooling
  - full notebook compiler concepts

  The notebook itself remains an important architecture-discovery surface.
