CONTEXT DOCUMENT for continuation of the "C++-struct-like, Python-built Jupyter Config Class — a system for generating guided, no-code Jupyter notebooks from structured JSON, with strong UX gating, cross-platform observables, and reusable widget factories" project

DOCUMENT PREPARED FOR CONTINUATION: 1762016096_2026-05-01T12:54:56-0400

CONTINUED FROM CHAT ENTITLED:
C++ Jupyter Config Class
ALSO INVOLVING
(no other subjects specified)

FROM USER @bballdave025 (GitHub)

---

## Project Overview

This project builds a **Python package** that behaves like a **C++-style struct/config system** for Jupyter notebooks, enabling:

- no-code / low-code notebook execution
- guided user workflows with enforced state transitions
- JSON-driven configuration → notebook generation
- reusable widget factories (dropdowns, buttons, file selectors)
- cross-platform runtime awareness via `GlobalObservables`

The system is designed to produce **fully executable notebooks** that guide non-programmer users through structured data workflows (especially CSV-based pipelines).

---

## Core Architectural Model

Pipeline:

```text
JSON → Config objects → Widget factories → Notebook blocks → IPYNB file
```

Key principle:

> Separate **environment facts**, **user configuration**, **UI**, and **execution flow**

---

## Key Components (Current State)

### 1. GlobalObservables (FOUNDATIONAL — TO IMPLEMENT FULLY)

Purpose:
- detect runtime + system environment once
- avoid recomputation
- unify cross-platform behavior

Includes:
- OS detection (Windows/Linux/macOS)
- paths (home, downloads)
- Python version + bitness
- runtime detection (VS Code, Jupyter, Colab, etc.)
- clipboard capabilities
- case-sensitivity rules

Usage:

```python
DEFAULT_OBSERVABLES = GlobalObservables.detect()
```

Injected into:

```python
NotebookConfig(observables=DEFAULT_OBSERVABLES)
```

---

### 2. NotebookConfig (SESSION STATE)

Holds:
- selected category
- selected subcategory
- selected file
- maintainer info
- root directory
- runtime options

Does NOT recompute environment info.

---

### 3. CategorySpec (CRITICAL REFACTOR)

Replaces fragile parallel lists.

```python
CategorySpec:
  key
  label
  uri
  preferred_filename
  subcategories
  metadata
```

Supports:
- category → URL mapping
- validation rules (row counts, etc.)
- filename expectations

---

### 4. Dropdown Behavior Model (IMPORTANT DISTINCTION)

#### Gate Dropdowns

Used when:
- user must explicitly choose

Behavior:
- includes sentinel value (`No_Category_Chosen`)
- throws loud, recoverable exception if not changed

Rule:
> No silent defaults allowed

---

#### File Dropdowns (DISCOVERED STATE)

Used when:
- files already exist (user downloaded/exported)

Behavior:
- scans directory
- filters by extension
- prefers expected filename
- defaults to best guess
- warns user to verify

Failure:
- if no files found → highlighted exception with instructions

Rule:
> Default allowed, but must be loudly verified

---

### 5. File Selection Pattern (ABSTRACTION TARGET)

```text
scan directory
→ find files
→ prefer expected filename
→ populate dropdown
→ fallback if missing
→ fail loudly if none
```

This is now considered a reusable abstraction.

---

### 6. Widget Factory Layer

Existing / planned:

- `create_dropdown`
- `create_copy_button`
- `create_uri_button`
- `return_file_selector`
- `return_text_input`

All widgets:
- update config state
- display loud contextual info
- support non-programmer UX

---

### 7. Highlighted Output System

`create_highlighted_string(...)`

Acts as:
- UI messaging system
- severity signaling (`info_`, `action_`, `exception_`)
- user guidance layer

This is effectively a **console UX framework**.

---

### 8. NotebookBlock (NEXT IMPLEMENTATION STEP)

Represents a unit of notebook generation:

```python
NotebookBlock:
  title
  content
  instruction_level   # normal / look_above / aggressive
  visibility          # normal / advanced
  auto_run_hint       # “spam Shift+Enter”
```

Important:

> Instruction headers (e.g., “LOOK ABOVE!!!”) are **explicit metadata**, not inferred.

---

### 9. UX Design Pattern (CRITICAL INSIGHT)

The notebook behaves as a:

> **guided state machine for human users**

Features:
- state gating
- loud validation
- recoverable errors
- step-by-step enforcement
- fast-forward mode once stable

---

### 10. Filesystem Self-Healing

Pattern:
- ensure directories exist
- create missing paths automatically
- print actions

Will become:

```python
FileSystemOps.ensure_structure(...)
```

---

### 11. JSON Configuration System (PLANNED)

Responsibilities:
- define categories
- define render style
- define file behavior
- drive notebook generation

Will support:
- adding/removing categories via helper functions
- optional schema validation

---

### 12. JSON Mutation Tools (PLANNED)

Functions:

```python
add_to_json_cli(...)
remove_from_json_cli(...)
backup_json_file(...)
```

Purpose:
- avoid manual editing
- preserve backups
- support iterative config building

CLI wiring deferred.

---

### 13. RenderStyle (DAVE-SPECIFIC)

Controls:

- indentation (2 vs 4 spaces)
- max line length (79)
- preferred line length (72)
- `##endof:` markers
- notebook vs `.py` formatting differences

---

### 14. Notebook Writer (PARTIAL)

Already exists in minimal form:

- writes `.ipynb` JSON
- includes seed/setup cell

Will expand to:
- accept `NotebookBlock` list
- inject headers
- apply render style

---

### 15. Packaging

- Apache 2.0 license selected
- `pyproject.toml` in use
- `bump-my-version` configured
- supports both:
  - wheel (`.whl`)
  - source (`sdist`) for restricted environments

---

## Design Decisions (Locked)

- **Do NOT infer instructional headers from content**
- **Separate gate dropdowns from convenience dropdowns**
- **Use dataclasses over parallel lists**
- **GlobalObservables computed once**
- **Notebook generation driven by explicit structure, not heuristics**
- **JSON is source of truth for configuration**
- **UX clarity > code elegance**

---

## Immediate Next Steps (Lean-To Execution)

1. Implement `GlobalObservables.detect()`
2. Implement `load_config_from_json(...)`
3. Implement generalized `return_file_selector(...)`
4. Define `NotebookBlock`
5. Upgrade notebook writer to accept blocks

Minimal success condition:

```python
cfg = load_config_from_json("config.json")
display(return_file_selector(cfg))
```

---

## Deferred (Do NOT build yet)

- full notebook generator
- block dependency system
- advanced CLI tooling
- multi-notebook output

---

## Conceptual Summary

This project is evolving into:

> A structured system for turning configuration into guided, executable notebooks for non-programmer users, with strong guarantees around correctness, visibility, and recoverability.

---

*End of context document.*
