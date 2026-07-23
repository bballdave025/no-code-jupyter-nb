# Context Documents

This directory contains **continuation-ready context documents** (Lab
Notebook / LN files) for the **{{PROJECT_NAME}}** project.

> **Repository customization**
>
> Replace `{{PROJECT_NAME}}`, `{{SHORT_PROJECT_MARKER}}`, and any other
> `{{...}}` placeholders in this README with values appropriate for this
> repository.

These are **not** polished documentation. They are:

-   structured snapshots of project state,
-   continuation-ready checkpoints,
-   architecture and design records,
-   "lab notebook" entries for engineering progress.

------------------------------------------------------------------------

# Purpose

Each document is designed to answer:

> **If I had to resume this work in a fresh environment, what would I
> need to know?**

They preserve:

-   current architecture
-   terminology
-   naming decisions
-   design constraints
-   implementation status
-   next-step execution plans
-   important non-obvious insights
-   active questions

Think of these as **checkpoint files for thinking**, not summaries.

------------------------------------------------------------------------

# Documentation Hierarchy

``` text
README.md
    ↓
Project Charter
    ↓
Lab Notebook / Context Documents
    ↓
Experiment Notes
```

Each layer answers a different question.

------------------------------------------------------------------------

# Context Document Header Template

Use **double-brace placeholders** (`{{...}}`) rather than angle
brackets.

``` text
*BEGIN: Context Document Header*

# CONTEXT DOCUMENT — Continuation

## Project

**Name:**
{{Short project name}}

**Description:**
{{1–3 sentences: what this project is and what it produces}}

---

## Continuation Metadata

**Prepared at:**
{{ssssssssss_YYYY-mm-ddTHH:MM:SS±ZZZZ}}

Generated via:

date +'%s_%Y-%m-%dT%H:%M:%S%z'

(Boston, MA time)

**Continued from chat:**
{{Exact chat title}}

**Also involving:**
- {{Related topic}}
- {{Related topic}}
- *(or: no other subjects specified)*

---

## Author / Source

**User (GitHub):**
@bballdave025

**User (ChatGPT):**
{{optional}}

---

## Intent for This Context

{{1–2 sentences describing what this continuation should enable}}

---

## Usage Instructions

- Treat this document as **authoritative project state**.
- Continue with **minimal re-derivation**.
- Reinterpret only when explicitly requested.

*ENDOF: Context Document Header*
```

------------------------------------------------------------------------

# Pre-Context-Document Prompt (PCDP)

Before pasting a context document into a fresh chat, you may send a
short PCDP to establish context and immediate goals.

``` text
## Current Work

Project:
{{Very short project description}}

Starting with:
- {{Step}}
- {{Step}}
- {{Step}}

---

## Upcoming Context Document

The next message will be a CONTEXT DOCUMENT for:

{{Full project name}}

This continues discussion begun in:

"{{Previous chat title}}"

---

## Timing

Preparation:
{{YYYY-MM-DDTHH:MM:SS±ZZ:ZZ}}

(Optional) New chat:
{{YYYY-MM-DDTHH:MM:SS±ZZ:ZZ}}

---

## Instructions for Next Message

Instructions
- Do not summarize.
- Do not reformat.
- Do not analyze.
- Do not critique.
- Do not extract bullet points.
- Do not optimize language.
- Treat the context document as authoritative state.
- Your response should only:
  1. Confirm receipt.
  2. Confirm readiness to continue.

---

## Immediate Focus

Help me:

{{Concrete, task-oriented, ADHD-friendly next task}}

*End of PCDP*
```

## Practical Note

In normal use, the **Instructions for Next Message** section is often
**omitted**.

Experience has shown that including it sometimes causes models to
interpret the transferred context as operational instructions rather
than project state. In most cases, the PCDP simply establishes the
project, immediate focus, and previous chat, after which the Context
Document supplies the authoritative state.

Typical workflow:

``` text
PCDP (optional)
      ↓
Context Document (authoritative)
      ↓
Continue work
      ↓
Update / create new LN document before stopping
```

------------------------------------------------------------------------

# Naming Convention

``` text
LN_{{SHORT_PROJECT_MARKER}}_YYYY-MM-DD_{{optional-tag}}_-_{{short-slug}}.md
```

Examples:

``` text
LN_ncjn_2026-05-01_ctx01_-_config-class-architecture.md
LN_ncjn_2026-06-30_parked_-_widget-refactor.md
```

`LN` = Lab Notebook.

The project marker should remain short.

The optional tag is usually omitted unless it adds useful context.

------------------------------------------------------------------------

# Retrieval Tip

1.  Sort by filename.
2.  Open the newest `LN_*`.
3.  Resume from **Immediate Next Steps** (or equivalent).

------------------------------------------------------------------------

*End of README*
