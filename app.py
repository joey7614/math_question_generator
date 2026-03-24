from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Placeholder response — will be replaced with real logic
    return jsonify({
        "original": question,
        "topics": [
            {"id": "triangle_angle_sum", "label": "Triangle interior angles sum to 180°"},
            {"id": "quadratic_equations", "label": "Solve quadratic equations"},
        ],
        "prerequisites": [
            {"id": "linear_equations", "label": "Solve linear equations", "depth": 1},
            {"id": "integer_operations", "label": "Integer operations", "depth": 2},
        ],
        "generated_question": (
            r"In triangle $ABC$, angle $A = 90°$, angle $B = x^2 + 2x$, "
            r"and angle $C = -7x$. Find all valid values of $x$."
        ),
        "figure_spec": None,
    })


if __name__ == "__main__":
    app.run(debug=True)
