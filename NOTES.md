# Project Progress Notes

## Status: Step 1 Complete — Basic Web App

---

## What's Been Decided (Architecture)

### AI vs Pure Logic Split
- **Only 2 AI calls** in the entire app:
  1. **Topic Identification** (cheap model — Gemini Flash)
     - Input: raw question text + predefined topic ID list
     - Output: `{"topics": ["topic_id_1", "topic_id_2"]}` — JSON only, no free-form
  2. **Question Generation** (main call — Gemini Flash or better)
     - Output: `{"question": "...", "latex": "...", "figure_spec": {...} | null}`

- **Pure logic (no AI):**
  - Prerequisite/topic tree → hardcoded knowledge graph (`topic_graph.py`)
  - Geometry rendering → matplotlib from `figure_spec` JSON
  - Hint retrieval → graph traversal by depth
  - Math formatting → LaTeX string handling
  - Difficulty classification → derived from topic depth in graph

### AI Provider
- Google Gemini (not Anthropic/Claude)
- Package: `google-generativeai`
- API key from env var `GEMINI_API_KEY`

---

## What's Been Built

### Files Created
| File | Status | Description |
|------|--------|-------------|
| `CLAUDE.md` | ✅ Done | Project rules — auto-loaded into AI context |
| `NOTES.md` | ✅ Done | This file |
| `requirements.txt` | ✅ Done | flask, python-dotenv (Gemini to be added) |
| `app.py` | ✅ Done | Flask app, `/` route, `/api/generate` placeholder |
| `templates/index.html` | ✅ Done | Full UI with MathJax, sidebar, input/output panels |
| `static/css/style.css` | ✅ Done | Dark theme, card layout, topic tags, spinner |
| `static/js/app.js` | ✅ Done | Fetch, MathJax re-render, category selector, Ctrl+Enter |
| `output/figures/` | ✅ Done | Empty dir, ready for matplotlib PNGs |

### Files NOT Yet Created
| File | Description |
|------|-------------|
| `models.py` | Dataclasses: Question, TopicNode, FigureSpec |
| `topic_graph.py` | Hardcoded math knowledge graph + traversal logic |
| `geometry_renderer.py` | Matplotlib renderer — takes FigureSpec, outputs PNG |
| `math_formatter.py` | LaTeX formatting helpers |
| `agent.py` | Orchestrates the two Gemini AI calls |
| `.env` | GEMINI_API_KEY (not committed) |

---

## Current App Behavior
- `/api/generate` returns **hardcoded placeholder data** (no real logic yet)
- UI fully renders: topic tags, prerequisite tree, generated question with MathJax
- Figure display is wired up but hidden (no figure yet)
- Run: `python app.py` → open `http://127.0.0.1:5000`

---

## Build Order (Remaining Steps)

### Step 2 — Data Models & Knowledge Graph (pure logic)
- `models.py`: `Question`, `TopicNode`, `FigureSpec` dataclasses
- `topic_graph.py`: hardcoded topic nodes with prerequisites, graph traversal

### Step 3 — Geometry & Math Rendering (pure logic)
- `geometry_renderer.py`: triangle, circle, quadrilateral, coordinate plane
- `math_formatter.py`: LaTeX wrapping, equation detection

### Step 4 — AI Integration (Gemini)
- `agent.py`: Call A (topic ID) + Call B (question generation)
- Wire into `app.py` `/api/generate` endpoint
- Replace placeholder with real output

---

## Key Design Decisions to Remember
- `figure_spec` is always structured JSON — never raw matplotlib code
- Topic IDs are always from predefined taxonomy — AI never invents new ones
- All AI output is validated against schema before use
- Difficulty is derived from graph depth, not from AI
- Math labels in figures support LaTeX strings (e.g. `"x^2 + 2x"`)
