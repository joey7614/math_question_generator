from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal
from datetime import datetime
import uuid

# ── Constrained type aliases ───────────────────────────────────────────────────
Category   = Literal["SAT", "AMC", "olympiad"]
Difficulty = Literal["basic", "intermediate", "advanced"]
FigureType = Literal["triangle", "circle", "quadrilateral", "coordinate_plane"]


# ── Knowledge graph node ───────────────────────────────────────────────────────
@dataclass
class TopicNode:
    id:            str
    label:         str               # Human-readable name
    description:   str               # What this topic covers (fed to AI as context)
    prerequisites: list[str]         # List of topic IDs that must be known first
    categories:    list[Category]    # Which exams test this topic
    difficulty:    Difficulty        # Derived from graph depth, not AI


# ── Geometry figure spec ───────────────────────────────────────────────────────
# AI outputs this JSON; renderer converts it to a matplotlib PNG.
# All label strings support LaTeX (e.g. "$x^2 + 2x$").

@dataclass
class AngleLabel:
    vertex: str    # e.g. "A"
    label:  str    # e.g. "90°" or "$x^2 + 2x$"

@dataclass
class SideLabel:
    from_vertex: str   # e.g. "A"
    to_vertex:   str   # e.g. "B"
    label:       str   # e.g. "5" or "$\\sqrt{2}$"

@dataclass
class ExtraLabel:
    x:     float
    y:     float
    label: str

@dataclass
class FigureSpec:
    type:           FigureType
    # Triangle / quadrilateral: named vertex → [x, y]
    vertices:       dict[str, list[float]] = field(default_factory=dict)
    angle_labels:   list[AngleLabel]       = field(default_factory=list)
    side_labels:    list[SideLabel]        = field(default_factory=list)
    right_angle_at: str | None             = None   # vertex name or None
    extra_labels:   list[ExtraLabel]       = field(default_factory=list)
    # Circle-specific
    center:         list[float] | None     = None   # [x, y]
    radius:         float | None           = None
    # Coordinate plane: list of points to highlight
    points:         list[dict] | None      = None   # [{"label":"A","x":1,"y":2}, ...]

    @staticmethod
    def from_dict(d: dict) -> FigureSpec:
        """Parse and validate AI-supplied figure_spec JSON into a FigureSpec."""
        allowed_types = {"triangle", "circle", "quadrilateral", "coordinate_plane"}
        fig_type = d.get("type", "")
        if fig_type not in allowed_types:
            raise ValueError(f"Invalid figure type: {fig_type!r}")

        angle_labels = [
            AngleLabel(vertex=a["vertex"], label=a["label"])
            for a in d.get("angle_labels", [])
        ]
        side_labels = [
            SideLabel(from_vertex=s["from"], to_vertex=s["to"], label=s["label"])
            for s in d.get("side_labels", [])
        ]
        extra_labels = [
            ExtraLabel(x=e["position"][0], y=e["position"][1], label=e["label"])
            for e in d.get("extra_labels", [])
        ]
        return FigureSpec(
            type           = fig_type,
            vertices       = d.get("vertices", {}),
            angle_labels   = angle_labels,
            side_labels    = side_labels,
            right_angle_at = d.get("right_angle_at"),
            extra_labels   = extra_labels,
            center         = d.get("center"),
            radius         = d.get("radius"),
            points         = d.get("points"),
        )


# ── Topic breakdown (result of graph traversal) ────────────────────────────────
@dataclass
class TopicBreakdown:
    immediate:     list[TopicNode]             # Topics directly needed
    prerequisites: list[dict]                  # [{"id":..,"label":..,"depth":1,2,3}]


# ── Final question object ──────────────────────────────────────────────────────
@dataclass
class Question:
    id:         str            = field(default_factory=lambda: str(uuid.uuid4())[:8])
    category:   Category       = "SAT"
    topic_ids:  list[str]      = field(default_factory=list)
    text:       str            = ""      # Question body (LaTeX)
    answer:     str            = ""      # Answer / solution hint (LaTeX)
    difficulty: Difficulty     = "intermediate"
    figure_spec: FigureSpec | None = None
    breakdown:  TopicBreakdown | None = None
    created_at: datetime       = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        """Serialize to a JSON-safe dict for the API response."""
        return {
            "id":         self.id,
            "category":   self.category,
            "topic_ids":  self.topic_ids,
            "text":       self.text,
            "answer":     self.answer,
            "difficulty": self.difficulty,
            "topics": [
                {"id": t.id, "label": t.label}
                for t in (self.breakdown.immediate if self.breakdown else [])
            ],
            "prerequisites": (
                self.breakdown.prerequisites if self.breakdown else []
            ),
            "figure_spec": None,  # renderer fills figure_url separately
        }
