# 📘 Automated_BookGen

## Overview

**Automated_BookGen** is a modular, automation-first book generation system that transforms a book title and editorial notes into a structured outline, chapter content, and ultimately a compiled manuscript. The system is designed around **human-in-the-loop editorial control**, **stateful workflows**, and **LLM-driven generation**, closely mirroring a real-world publishing pipeline.

Unlike one-shot AI writing tools, Automated_BookGen enforces **gated progression**, **context preservation**, and **editorial feedback loops** at every stage of content creation.

---

## Current Implementation Status (Updated)

As of now, the project has implemented the **core foundation of the system**, including:

* Structured outline generation using an LLM
* Strict system and user prompts for outline and content generation
* Persistent storage using SQLite (designed to be Supabase-compatible)
* Chapter-level data modeling
* Regeneration-aware notes handling (`before_notes` / `after_notes`)
* Streamlit-based frontend for outline input and review
* Per-heading editorial notes capture
* DOCX export pipeline
* Email notification integration (Gmail SMTP)

The project is actively evolving toward full end-to-end automation.

---

## 1. What the System Currently Does

### Input & Outline Generation

* Users enter:

  * Book title
  * Mandatory editorial notes (`before_notes`)
* An **Outline Generation Agent** produces a structured outline in strict JSON format
* The outline is rendered in the frontend, chapter by chapter
* Editors can add **optional notes per chapter** for refinement

### Editorial Control

* Notes are split into:

  * `before_notes` → initial guidance
  * `after_notes` → regeneration feedback
* Status flags are used to control workflow progression
* No step auto-advances without satisfying required conditions

### Data Persistence

* All books and headings are stored in a relational schema
* Each heading/chapter is stored independently
* Designed to support:

  * Regeneration
  * Auditing
  * Pause/resume workflows

### Content Generation (Foundation Ready)

* A **Content Generation Agent** prompt structure is implemented
* Each chapter is generated independently
* Previous chapter summaries are passed as context
* Output includes both:

  * Full content
  * A concise summary for chaining

### Export

* All stored chapter content can be compiled into a `.docx` file
* Ordering is preserved using `heading_number`
* Output is editor-ready

### Notifications

* Email notifications are integrated via Gmail SMTP
* Used for:

  * Outline ready
  * Review required
  * Workflow completion
  * Error or pause states

---

## 2. System Architecture & Code Explanation

### High-Level Flow

1. User submits book title and initial notes
2. Outline is generated and stored
3. Editor reviews outline and adds notes per chapter
4. Chapters are generated sequentially with context
5. Each chapter can be approved or regenerated
6. Approved chapters are compiled into a final document
7. Notifications are sent at key checkpoints

---

## 3. Code Structure Overview

### `db_utils.py`

Responsible for **all database operations**.

Key responsibilities:

* Initialize database schema
* Create and manage:

  * `books` table
  * `headings` table
* Support CRUD operations:

  * Add/update/delete books
  * Add/update/delete headings
* Handle timestamps and status updates

Key design choices:

* `before_notes` and `after_notes` explicitly separated
* Status-driven workflow control
* SQLite used for MVP, schema compatible with Supabase/Postgres

---

### Prompt Definitions

The system uses **strict prompt contracts** to ensure predictable outputs.

#### Outline Generation Prompts

* Enforce mandatory editorial notes
* Output strictly structured JSON
* Designed for regeneration and review

#### Content Generation Prompts

* Generate one chapter at a time
* Consume:

  * Book title
  * Current heading
  * Sub-headings
  * Previous chapter summaries (dict)
  * Optional editorial notes
* Output content + summary for chaining

---

### Streamlit Frontend (`app.py`)

Provides a **lightweight editorial UI**.

Current features:

* Book title and note input
* Outline generation trigger
* Outline rendering with expandable chapters
* Optional per-chapter notes input
* Session-based state management

Designed to later support:

* Multi-page navigation
* Chapter approval buttons
* Regeneration triggers
* Authentication

---

### Export Pipeline

* Reads all headings from DB
* Orders them by `heading_number`
* Writes structured content into a `.docx` file
* Ready for PDF extension

---

### Email Notifications

* Implemented using Gmail SMTP with App Passwords
* Triggered programmatically
* Easily extendable to MS Teams or Slack

---

## 4. Why the Design Matters

This system intentionally avoids:

* Stateless generation
* One-shot prompts
* Hardcoded flows

Instead, it prioritizes:

* Editorial realism
* Deterministic workflows
* Auditability
* Regeneration safety
* Long-form consistency

This makes it suitable for:

* Publishing pipelines
* Enterprise documentation
* Knowledge products
* Research reports
* AI-assisted editorial teams

---

## 5. Updated MVP Phases

### Phase 1 — Foundation (Completed)

* Prompt architecture
* Outline generation
* DB schema
* Frontend input
* DOCX export
* Email notifications

### Phase 2 — Chapter Generation (In Progress)

* Sequential chapter generation
* Context chaining via summaries
* Per-chapter regeneration
* Status-based locking

### Phase 3 — Full Compilation & Review

* Final review gates
* End-to-end automation
* Versioned exports

### Phase 4 — Post-MVP Enhancements

* Web editor UI
* Source-backed research
* Vector DB for long context
* Multi-language support
* Cost and usage tracking

---

## Summary

**Automated_BookGen** is not just an AI writing tool—it is an **editorial automation system**.

Its strengths lie in:

* Structured workflows
* Human oversight
* Context-aware generation
* Production-grade extensibility

The current implementation establishes a solid, extensible foundation and demonstrates a clear path toward a full-scale automated publishing platform.

---
