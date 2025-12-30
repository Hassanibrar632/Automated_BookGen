# 📘 Automated_BookGen

## Overview

**Automated_BookGen** is a modular, scalable automated book generation system designed to transform a simple book title into a fully compiled manuscript. The system leverages Large Language Models (LLMs), structured workflow automation, and human-in-the-loop review mechanisms to ensure quality, control, and editorial oversight at every stage of content creation.

The architecture is built around gated workflows, conditional branching, and persistent state management, making it suitable for long-form content generation such as books, reports, and structured publications.

---

## 1. Description

Automated_BookGen accepts a book title and editorial notes as input, generates a structured outline, incrementally writes chapters with contextual awareness, and compiles a final draft in standard document formats (.docx, .pdf, or .txt).

Key characteristics of the system include:

* Feedback-driven generation with editor approval gates
* Chapter-by-chapter context chaining using summaries
* Persistent storage of outlines, chapters, notes, and summaries
* Modular design allowing easy extension and replacement of components
* Automation-first workflow using orchestration tools (e.g., n8n or Python)
* Support for notifications and pause/resume states

The system is intentionally designed to resemble a real editorial workflow rather than a one-shot AI text generator.

---

## 2. Explanation of System Architecture & Workflow

### High-Level Flow

1. **Input ingestion** (Title + editorial notes)
2. **Outline generation** with mandatory pre-notes
3. **Editorial review and iteration of outline**
4. **Sequential chapter generation**
5. **Context preservation using chapter summaries**
6. **Per-chapter editorial gating**
7. **Final compilation and export**
8. **Notifications at each critical checkpoint**

---

### Core Components

#### 1. Automation Engine

* Orchestrates workflow stages
* Handles conditional logic, pauses, retries, and branching
* Tools: n8n / Python scripts

#### 2. Database (Supabase)

Stores:

* Titles and metadata
* Outline drafts and revisions
* Chapter content
* Chapter summaries (for context chaining)
* Editorial notes and approval statuses
* Final output metadata

#### 3. LLM Layer

* Generates outlines and chapters
* Consumes structured prompts with editorial notes and context
* Can be extended to support multiple providers (OpenAI, Gemini, Anthropic)

#### 4. Human-in-the-Loop Controls

* Editors can:

  * Add notes before outline generation
  * Revise outlines post-generation
  * Add per-chapter improvement notes
  * Approve or pause progression at every stage

#### 5. Notification System

* Triggers email or MS Teams alerts when:

  * Outline is ready for review
  * Chapter feedback is required
  * Workflow is paused due to missing input
  * Final draft is compiled

---

### Context Handling (Critical Design Choice)

Each chapter generation step includes:

* Summaries of all previous chapters
* The full outline
* Chapter-specific editorial notes

This ensures:

* Narrative continuity
* Logical progression
* Reduced hallucination
* Consistent tone and scope

---

## 3. MVP Phases

### Phase 1 — Foundation & Data Model (MVP Core)

**Goal:** Establish structure, persistence, and basic generation.

* Define Supabase schema:

  * Titles
  * Outline drafts
  * Status flags
* Input ingestion (Google Sheet / Excel / local file)
* LLM-based outline generation
* Mandatory `notes_on_outline_before` gate
* Outline stored for editor review
* Manual status updates to proceed or pause

**Deliverables:**

* Working outline generation
* DB schema screenshots
* Stored outline drafts with status flags

---

### Phase 2 — Chapter Generation with Context Chaining

**Goal:** Enable controlled, sequential chapter writing.

* Generate chapters one at a time from outline
* Store each chapter independently
* Generate and store chapter summaries
* Use cumulative summaries as context for next chapter
* Editorial gating per chapter:

  * Wait for notes
  * Regenerate if needed
  * Pause if input missing

**Deliverables:**

* Multi-chapter generation
* Verified context chaining
* Chapter-level approval workflow

---

### Phase 3 — Final Compilation & Export

**Goal:** Produce a complete, review-ready manuscript.

* Validate all chapters are approved
* Handle final review notes
* Compile chapters into:

  * `.docx`
  * `.txt` (PDF optional)
* Store final output metadata
* Trigger completion notification

**Deliverables:**

* Final compiled book file
* Export pipeline
* Completion alerts

---

### Phase 4 — (Post-MVP Enhancements)

**Optional but extensible**

* Web-based editor UI
* Source-backed research integration
* Vector DB for long-context retrieval
* Version history and diff tracking
* Multi-language book generation
* Cost and token usage tracking

---

## Summary

Automated_BookGen is designed as an **editorial automation system**, not just an AI writer. Its strength lies in:

* Structured workflows
* Human oversight
* Context-aware generation
* Production-grade extensibility

This makes it suitable for real-world publishing pipelines, enterprise documentation, and scalable content automation platforms.

---
