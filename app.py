from flask import Flask, render_template, request, jsonify, send_from_directory
import os

from models import FigureSpec
from geometry_renderer import render_figure

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/figures/<filename>")
def serve_figure(filename: str):
    figures_dir = os.path.join(os.path.dirname(__file__), "output", "figures")
    return send_from_directory(figures_dir, filename)


@app.route("/api/generate", methods=["POST"])
def generate():
    data     = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # ── Placeholder figure spec (triangle example) ─────────────────────────
    # This will be replaced by AI output in Step 4.
    figure_spec_data = {
        "type": "triangle",
        "vertices": {
            "A": [0, 0],
            "B": [5, 0],
            "C": [0, 4],
        },
        "angle_labels": [
            {"vertex": "A", "label": "90°"},
            {"vertex": "B", "label": "$x^2+2x$"},
            {"vertex": "C", "label": "$-7x$"},
        ],
        "side_labels": [
            {"from": "B", "to": "C", "label": "a"},   # opposite A
            {"from": "A", "to": "C", "label": "b"},   # opposite B
            {"from": "A", "to": "B", "label": "c"},   # opposite C
        ],
        "right_angle_at": "A",
        "extra_labels": [],
    }

    # ── Render figure ──────────────────────────────────────────────────────
    figure_url = None
    try:
        spec      = FigureSpec.from_dict(figure_spec_data)
        filename  = render_figure(spec)
        figure_url = f"/figures/{filename}"
    except Exception as e:
        print(f"[geometry_renderer] {e}")

    # ── Placeholder question response ──────────────────────────────────────
    return jsonify({
        "original": question,
        "topics": [
            {"id": "triangle_angle_sum",  "label": "Triangle interior angles = 180°"},
            {"id": "quadratic_equations", "label": "Quadratic equations"},
        ],
        "prerequisites": [
            {"id": "angle_concepts",      "label": "Angle concepts",         "depth": 1},
            {"id": "factoring",           "label": "Factoring polynomials",  "depth": 1},
            {"id": "exponents_radicals",  "label": "Exponents & radicals",   "depth": 1},
            {"id": "integer_operations",  "label": "Integer operations",     "depth": 2},
            {"id": "variables_expressions","label": "Variables & expressions","depth": 2},
        ],
        "generated_question": (
            r"In $\triangle ABC$, $\angle A = 90°$, $\angle B = x^2 + 2x$, "
            r"and $\angle C = -7x$. Find all valid values of $x$."
        ),
        "figure_url": figure_url,
    })


if __name__ == "__main__":
    app.run(debug=True)
