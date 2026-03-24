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
| `requirements.txt` | ✅ Done | flask, python-dotenv, matplotlib, numpy |
| `app.py` | ✅ Done | Flask app, `/api/generate` + `/figures/<file>` routes |
| `templates/index.html` | ✅ Done | Full UI with MathJax, sidebar, input/output panels |
| `static/css/style.css` | ✅ Done | Dark theme, card layout, topic tags, spinner |
| `static/js/app.js` | ✅ Done | Fetch, MathJax re-render, category selector, Ctrl+Enter |
| `models.py` | ✅ Done | Question, TopicNode, FigureSpec, TopicBreakdown dataclasses |
| `topic_graph.py` | ✅ Done | 31-topic knowledge graph, BFS traversal, difficulty derivation |
| `geometry_renderer.py` | ✅ Done | matplotlib renderer: triangle, circle, quad, coord plane |
| `math_formatter.py` | ✅ Done | ensure_latex(): wraps expressions + single letters in $...$ |
| `output/figures/` | ✅ Done | Generated PNGs served at /figures/<filename> |

### Files NOT Yet Created
| File | Description |
|------|-------------|
| `agent.py` | Orchestrates the two Gemini AI calls |
| `.env` | GEMINI_API_KEY (never committed) |

---

## Current App Behavior
- `/api/generate` returns **hardcoded placeholder data** (triangle question)
- Triangle renders with: STIX math fonts, right-angle marker, correct a/b/c convention
  (side `a` opposite vertex A, `b` opposite B, `c` opposite C)
- Angle labels render as proper LaTeX math ($x^2+2x$, $-7x$)
- Single letter side labels (a, b, c) auto-wrapped in $...$ → math italic
- Run: `python app.py` → open `http://127.0.0.1:5000`

---

## Build Order (Remaining)

### Step 4 — AI Integration (Gemini) ← NEXT
- `agent.py`: Call A (topic identification, Gemini Flash, structured JSON)
- `agent.py`: Call B (question generation, returns question + figure_spec JSON)
- Wire into `app.py` to replace placeholder
- Add `google-generativeai` to requirements.txt
- Create `.env` with GEMINI_API_KEY

---

## Key Design Decisions to Remember
- `figure_spec` is always structured JSON — never raw matplotlib code
- Topic IDs are always from predefined taxonomy — AI never invents new ones
- All AI output is validated against schema before use
- Difficulty is derived from graph depth, not from AI
- Math labels in figures support LaTeX strings (e.g. `"x^2 + 2x"`)
