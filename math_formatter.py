"""
math_formatter.py — LaTeX label helpers.
Pure logic — no AI calls.
"""

import re


def ensure_latex(label: str) -> str:
    """
    Wrap a math expression in $...$ if it looks like math and isn't already.

    Rules:
    - Already wrapped ($...$)  → return as-is
    - Single letter (a, b, x)  → math variable → wrap
    - Contains math characters  → expression → wrap
    - Plain text (90°, 'cm')   → leave as-is
    """
    label = label.strip()
    if not label:
        return label
    # Already wrapped
    if label.startswith("$") and label.endswith("$"):
        return label
    # Single letter → math italic variable (e.g. a, b, c, x, y)
    if re.match(r"^[a-zA-Z]$", label):
        return f"${label}$"
    # Expression with math characters → wrap
    math_signals = re.compile(r"[+\-*/^_\\{}]|[a-zA-Z]\d|\d[a-zA-Z]")
    if math_signals.search(label):
        return f"${label}$"
    return label


def strip_latex(label: str) -> str:
    """Remove surrounding $...$ delimiters."""
    label = label.strip()
    if label.startswith("$") and label.endswith("$"):
        return label[1:-1]
    return label


def format_question_text(text: str) -> str:
    """
    Ensure all inline math in a question string uses $...$ delimiters.
    Leaves already-delimited segments alone.
    """
    return text  # MathJax on the frontend handles $...$ natively
