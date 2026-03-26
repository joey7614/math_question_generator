from flask import Flask, render_template, request, jsonify, send_from_directory
import os

from models import FigureSpec
from geometry_renderer import render_figure
from coordinate_renderer import render_coord_figure

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

    # ── Placeholder figures (both types) ──────────────────────────────────
    # Swap DEMO_MODE to switch which figure shows in the browser.
    # Will be replaced by AI output in Step 4.
    DEMO_MODE = "coordinate"   # "triangle" | "coordinate"

    figure_url = None
    try:
        if DEMO_MODE == "triangle":
            spec = FigureSpec.from_dict({
                "type": "triangle",
                "vertices": {"A": [0, 0], "B": [5, 0], "C": [0, 4]},
                "angle_labels": [
                    {"vertex": "A", "label": "90°"},
                    {"vertex": "B", "label": "$x^2+2x$"},
                    {"vertex": "C", "label": "$-7x$"},
                ],
                "side_labels": [
                    {"from": "B", "to": "C", "label": "a"},
                    {"from": "A", "to": "C", "label": "b"},
                    {"from": "A", "to": "B", "label": "c"},
                ],
                "right_angle_at": "A",
                "extra_labels": [],
            })
            filename  = render_figure(spec)
            figure_url = f"/figures/{filename}"

        elif DEMO_MODE == "coordinate":
            coord_spec = {
                "x_range": [-4, 6],
                "y_range": [-3, 5],
                "show_grid": True,
                "points": [
                    {"label": "A", "x": 1, "y": 4},
                    {"label": "B", "x": 4, "y": -1},
                    {"label": "M", "x": 2.5, "y": 1.5},
                ],
                "segments": [
                    {"from": [1, 4], "to": [4, -1], "label": "$d$"},
                ],
                "lines": [
                    {"slope": -5/3, "intercept": 23/3,
                     "label": "$y = -\\frac{5}{3}x + \\frac{23}{3}$",
                     "style": "dashed"},
                ],
                "slope_triangles": [
                    {"from": [1, 4], "to": [4, -1],
                     "run_label": "3", "rise_label": "$-5$"},
                ],
            }
            filename   = render_coord_figure(coord_spec)
            figure_url = f"/figures/{filename}"

    except Exception as e:
        print(f"[renderer] {e}")

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
            r"Points $A(1, 4)$ and $B(4, -1)$ are on the coordinate plane. "
            r"Find the length of segment $\overline{AB}$ and the equation of "
            r"the line passing through $A$ and $B$."
        ),
        "figure_url": figure_url,
    })


if __name__ == "__main__":
    app.run(debug=True)
