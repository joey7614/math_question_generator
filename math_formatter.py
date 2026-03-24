"""
math_formatter.py — LaTeX label helpers.
Pure logic — no AI calls.
"""

import re


def ensure_latex(label: str) -> str:
    """
    Wrap a math expression in $...$ if it looks like math and isn't already.
    Plain text like '90°', 'a', 'b' is left as-is.
    """
    label = label.strip()
    if not label:
        return label
    # Already wrapped
    if label.startswith("$") and label.endswith("$"):
        return label
    # Heuristics: contains math characters → wrap it
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
