"""
topic_graph.py — Hardcoded math knowledge graph.

Pure logic only — no AI calls here.
The AI receives topic IDs and descriptions as context;
it never invents new topic IDs at runtime.
"""

from __future__ import annotations
from models import TopicNode, TopicBreakdown, Category

# ── Knowledge graph ────────────────────────────────────────────────────────────
# Each node defines what topics a student must already know (prerequisites).
# Traversing prerequisites from any topic produces the full hint breakdown tree.

TOPICS: dict[str, TopicNode] = {

    # ── Foundations ──────────────────────────────────────────────────────────
    "integer_operations": TopicNode(
        id="integer_operations",
        label="Integer Operations",
        description="Add, subtract, multiply, divide integers; order of operations (PEMDAS).",
        prerequisites=[],
        categories=["SAT", "AMC", "olympiad"],
        difficulty="basic",
    ),
    "fractions_decimals": TopicNode(
        id="fractions_decimals",
        label="Fractions & Decimals",
        description="Simplify, add, subtract, multiply, divide fractions and decimals.",
        prerequisites=["integer_operations"],
        categories=["SAT", "AMC"],
        difficulty="basic",
    ),
    "exponents_radicals": TopicNode(
        id="exponents_radicals",
        label="Exponents & Radicals",
        description="Laws of exponents, square roots, nth roots, rational exponents.",
        prerequisites=["integer_operations"],
        categories=["SAT", "AMC", "olympiad"],
        difficulty="basic",
    ),
    "ratios_proportions": TopicNode(
        id="ratios_proportions",
        label="Ratios & Proportions",
        description="Set up and solve proportions; scale factors; unit rates.",
        prerequisites=["fractions_decimals"],
        categories=["SAT", "AMC"],
        difficulty="basic",
    ),
    "percentages": TopicNode(
        id="percentages",
        label="Percentages",
        description="Percent increase/decrease, percent of a number, reverse percentage.",
        prerequisites=["fractions_decimals"],
        categories=["SAT"],
        difficulty="basic",
    ),

    # ── Algebra ──────────────────────────────────────────────────────────────
    "variables_expressions": TopicNode(
        id="variables_expressions",
        label="Variables & Expressions",
        description="Evaluate and simplify algebraic expressions; combine like terms.",
        prerequisites=["integer_operations"],
        categories=["SAT", "AMC"],
        difficulty="basic",
    ),
    "linear_equations": TopicNode(
        id="linear_equations",
        label="Linear Equations",
        description="Solve one-variable linear equations; isolate unknowns; word problems.",
        prerequisites=["variables_expressions"],
        categories=["SAT", "AMC"],
        difficulty="basic",
    ),
    "linear_inequalities": TopicNode(
        id="linear_inequalities",
        label="Linear Inequalities",
        description="Solve and graph linear inequalities; flip inequality when multiplying by negative.",
        prerequisites=["linear_equations"],
        categories=["SAT", "AMC"],
        difficulty="basic",
    ),
    "systems_linear_equations": TopicNode(
        id="systems_linear_equations",
        label="Systems of Linear Equations",
        description="Solve 2×2 systems by substitution and elimination; no-solution / infinite-solution cases.",
        prerequisites=["linear_equations"],
        categories=["SAT", "AMC"],
        difficulty="intermediate",
    ),
    "factoring": TopicNode(
        id="factoring",
        label="Factoring Polynomials",
        description="Factor out GCF, difference of squares, trinomials (ax²+bx+c).",
        prerequisites=["variables_expressions", "exponents_radicals"],
        categories=["SAT", "AMC"],
        difficulty="intermediate",
    ),
    "quadratic_equations": TopicNode(
        id="quadratic_equations",
        label="Quadratic Equations",
        description="Solve by factoring, completing the square, quadratic formula; discriminant; parabola vertex.",
        prerequisites=["factoring", "exponents_radicals"],
        categories=["SAT", "AMC", "olympiad"],
        difficulty="intermediate",
    ),
    "polynomials": TopicNode(
        id="polynomials",
        label="Polynomials",
        description="Add/subtract/multiply polynomials; polynomial long division; remainder theorem.",
        prerequisites=["factoring", "quadratic_equations"],
        categories=["SAT", "AMC", "olympiad"],
        difficulty="intermediate",
    ),
    "functions": TopicNode(
        id="functions",
        label="Functions",
        description="Function notation f(x); domain and range; composition; inverse functions.",
        prerequisites=["linear_equations"],
        categories=["SAT", "AMC"],
        difficulty="intermediate",
    ),
    "exponential_functions": TopicNode(
        id="exponential_functions",
        label="Exponential & Logarithmic Functions",
        description="Exponential growth/decay; log rules; solving exponential equations.",
        prerequisites=["functions", "exponents_radicals"],
        categories=["SAT", "AMC"],
        difficulty="intermediate",
    ),
    "inequalities_advanced": TopicNode(
        id="inequalities_advanced",
        label="Advanced Inequalities (AM-GM, Cauchy-Schwarz)",
        description="AM-GM inequality, Cauchy-Schwarz, optimization via inequalities.",
        prerequisites=["quadratic_equations", "functions"],
        categories=["AMC", "olympiad"],
        difficulty="advanced",
    ),
    "sequences_series": TopicNode(
        id="sequences_series",
        label="Sequences & Series",
        description="Arithmetic and geometric sequences/series; sigma notation; sum formulas.",
        prerequisites=["linear_equations", "exponents_radicals"],
        categories=["AMC", "olympiad"],
        difficulty="intermediate",
    ),

    # ── Geometry ─────────────────────────────────────────────────────────────
    "angle_concepts": TopicNode(
        id="angle_concepts",
        label="Angle Concepts",
        description="Acute/obtuse/right/straight angles; complementary and supplementary; vertical angles; parallel lines with transversal.",
        prerequisites=["integer_operations"],
        categories=["SAT", "AMC"],
        difficulty="basic",
    ),
    "triangle_angle_sum": TopicNode(
        id="triangle_angle_sum",
        label="Triangle Angle Sum",
        description="Interior angles of a triangle sum to 180°; exterior angle theorem.",
        prerequisites=["angle_concepts"],
        categories=["SAT", "AMC"],
        difficulty="basic",
    ),
    "triangle_similarity_congruence": TopicNode(
        id="triangle_similarity_congruence",
        label="Triangle Similarity & Congruence",
        description="SSS, SAS, ASA, AAS congruence; AA, SAS, SSS similarity; corresponding parts.",
        prerequisites=["triangle_angle_sum", "ratios_proportions"],
        categories=["SAT", "AMC"],
        difficulty="intermediate",
    ),
    "pythagorean_theorem": TopicNode(
        id="pythagorean_theorem",
        label="Pythagorean Theorem",
        description="a²+b²=c² for right triangles; Pythagorean triples; distance formula.",
        prerequisites=["triangle_angle_sum", "exponents_radicals"],
        categories=["SAT", "AMC"],
        difficulty="basic",
    ),
    "area_perimeter": TopicNode(
        id="area_perimeter",
        label="Area & Perimeter",
        description="Formulas for triangles, rectangles, parallelograms, trapezoids.",
        prerequisites=["triangle_angle_sum", "fractions_decimals"],
        categories=["SAT", "AMC"],
        difficulty="basic",
    ),
    "circles": TopicNode(
        id="circles",
        label="Circles",
        description="Area πr², circumference 2πr; arc length; sector area; central and inscribed angles; chords.",
        prerequisites=["angle_concepts", "ratios_proportions"],
        categories=["SAT", "AMC"],
        difficulty="intermediate",
    ),
    "trigonometry": TopicNode(
        id="trigonometry",
        label="Trigonometry",
        description="sin/cos/tan in right triangles; unit circle; law of sines and cosines.",
        prerequisites=["pythagorean_theorem", "ratios_proportions"],
        categories=["SAT", "AMC"],
        difficulty="intermediate",
    ),
    "coordinate_geometry": TopicNode(
        id="coordinate_geometry",
        label="Coordinate Geometry",
        description="Slope; distance formula; midpoint; equations of lines and circles on the coordinate plane.",
        prerequisites=["linear_equations", "pythagorean_theorem"],
        categories=["SAT", "AMC"],
        difficulty="intermediate",
    ),
    "volume_surface_area": TopicNode(
        id="volume_surface_area",
        label="Volume & Surface Area",
        description="Prisms, cylinders, pyramids, cones, spheres — volume and surface area formulas.",
        prerequisites=["area_perimeter"],
        categories=["SAT", "AMC"],
        difficulty="intermediate",
    ),

    # ── Number Theory ─────────────────────────────────────────────────────────
    "number_theory_basics": TopicNode(
        id="number_theory_basics",
        label="Number Theory Basics",
        description="Divisibility rules; prime factorization; identifying primes/composites.",
        prerequisites=["integer_operations"],
        categories=["AMC", "olympiad"],
        difficulty="intermediate",
    ),
    "gcd_lcm": TopicNode(
        id="gcd_lcm",
        label="GCD & LCM",
        description="Greatest common divisor and least common multiple via prime factorization and Euclidean algorithm.",
        prerequisites=["number_theory_basics"],
        categories=["AMC", "olympiad"],
        difficulty="intermediate",
    ),
    "modular_arithmetic": TopicNode(
        id="modular_arithmetic",
        label="Modular Arithmetic",
        description="Congruences mod n; clock arithmetic; solving linear congruences.",
        prerequisites=["number_theory_basics"],
        categories=["AMC", "olympiad"],
        difficulty="advanced",
    ),

    # ── Combinatorics & Probability ───────────────────────────────────────────
    "counting_principles": TopicNode(
        id="counting_principles",
        label="Counting Principles",
        description="Multiplication/addition principles; permutations P(n,r); combinations C(n,r); Pascal's triangle.",
        prerequisites=["integer_operations", "fractions_decimals"],
        categories=["AMC", "olympiad"],
        difficulty="intermediate",
    ),
    "probability": TopicNode(
        id="probability",
        label="Probability",
        description="Basic probability; independent and dependent events; conditional probability; expected value.",
        prerequisites=["counting_principles", "fractions_decimals"],
        categories=["SAT", "AMC"],
        difficulty="intermediate",
    ),

    # ── Statistics ────────────────────────────────────────────────────────────
    "statistics": TopicNode(
        id="statistics",
        label="Statistics",
        description="Mean, median, mode, range; standard deviation concepts; reading charts and data.",
        prerequisites=["integer_operations", "fractions_decimals"],
        categories=["SAT"],
        difficulty="basic",
    ),
}


# ── Traversal helpers ──────────────────────────────────────────────────────────

def get_topic(topic_id: str) -> TopicNode | None:
    return TOPICS.get(topic_id)


def get_topics_for_category(category: Category) -> list[TopicNode]:
    """Return all topics that appear on a given exam category."""
    return [t for t in TOPICS.values() if category in t.categories]


def get_prerequisite_tree(topic_ids: list[str], max_depth: int = 4) -> list[dict]:
    """
    BFS traversal: given immediate topic IDs, return all prerequisite topics
    as a flat list with depth info, deduplicated.

    Returns: [{"id": str, "label": str, "depth": int}, ...]
    """
    visited: set[str] = set(topic_ids)   # exclude immediate topics from results
    result:  list[dict] = []
    queue:   list[tuple[str, int]] = [(tid, 1) for tid in topic_ids]

    while queue:
        current_id, depth = queue.pop(0)
        if depth > max_depth:
            continue
        node = TOPICS.get(current_id)
        if not node:
            continue
        for prereq_id in node.prerequisites:
            if prereq_id not in visited:
                visited.add(prereq_id)
                prereq_node = TOPICS.get(prereq_id)
                if prereq_node:
                    result.append({
                        "id":    prereq_id,
                        "label": prereq_node.label,
                        "depth": depth,
                    })
                    queue.append((prereq_id, depth + 1))

    return result


def build_breakdown(topic_ids: list[str], max_depth: int = 4) -> TopicBreakdown:
    """
    Given a list of topic IDs (from AI), build the full TopicBreakdown:
    - immediate: the TopicNode objects for each ID
    - prerequisites: BFS prerequisite tree with depth info
    """
    from models import TopicBreakdown

    immediate = [TOPICS[tid] for tid in topic_ids if tid in TOPICS]
    prerequisites = get_prerequisite_tree(topic_ids, max_depth=max_depth)

    return TopicBreakdown(immediate=immediate, prerequisites=prerequisites)


def derive_difficulty(topic_ids: list[str]) -> str:
    """
    Derive difficulty from the hardest topic in the list.
    Order: basic < intermediate < advanced
    """
    order = {"basic": 0, "intermediate": 1, "advanced": 2}
    max_level = 0
    for tid in topic_ids:
        node = TOPICS.get(tid)
        if node:
            max_level = max(max_level, order.get(node.difficulty, 0))
    return ["basic", "intermediate", "advanced"][max_level]


def topic_ids_for_prompt(category: Category) -> list[str]:
    """
    Return the list of valid topic IDs for a given category.
    This is sent to the AI so it can only pick from known IDs.
    """
    return [t.id for t in get_topics_for_category(category)]


def topic_context_for_prompt(topic_ids: list[str]) -> str:
    """
    Build a human-readable description of selected topics to include in the AI prompt.
    """
    lines = []
    for tid in topic_ids:
        node = TOPICS.get(tid)
        if node:
            lines.append(f"- {node.label}: {node.description}")
    return "\n".join(lines)
