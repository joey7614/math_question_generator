"""
geometry_renderer.py — Converts a FigureSpec into a matplotlib PNG.
Pure logic — no AI calls. AI never generates matplotlib code directly.
"""

import matplotlib
matplotlib.use("Agg")   # headless — no display required
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import uuid

from models import FigureSpec, AngleLabel, SideLabel
from math_formatter import ensure_latex
import coordinate_renderer

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Math font — STIX matches LaTeX Computer Modern appearance ──────────────────
matplotlib.rcParams.update({
    "mathtext.fontset": "stix",
    "font.family":      "STIXGeneral",
})

# ── Colour palette ─────────────────────────────────────────────────────────────
C_FILL   = "#dce8fb"    # polygon fill
C_EDGE   = "#2c3e50"    # polygon edges
C_ANGLE  = "#c0392b"    # angle label (red)
C_SIDE   = "#27ae60"    # side label (green)
C_VERTEX = "#1a1a2e"    # vertex name
C_EXTRA  = "#555577"    # extra labels
C_AXIS   = "#888899"    # coordinate axes


# ── Vector helpers ─────────────────────────────────────────────────────────────

def _unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n > 1e-10 else v


def _bisector(vertex: list, adj1: list, adj2: list) -> np.ndarray:
    """Inward unit bisector at vertex between the two adjacent vertices."""
    v  = np.array(vertex, dtype=float)
    d1 = _unit(np.array(adj1, dtype=float) - v)
    d2 = _unit(np.array(adj2, dtype=float) - v)
    b  = d1 + d2
    return _unit(b) if np.linalg.norm(b) > 1e-10 else np.array([-d1[1], d1[0]])


def _right_angle_marker(ax, vertex: list, adj1: list, adj2: list, size: float):
    """Draw a small square at a right-angle vertex."""
    v  = np.array(vertex, dtype=float)
    u1 = _unit(np.array(adj1, dtype=float) - v) * size
    u2 = _unit(np.array(adj2, dtype=float) - v) * size
    p1, p2, p3 = v + u1, v + u1 + u2, v + u2
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C_EDGE, lw=1.2, zorder=3)
    ax.plot([p2[0], p3[0]], [p2[1], p3[1]], color=C_EDGE, lw=1.2, zorder=3)


# ── Public entry point ─────────────────────────────────────────────────────────

def render_figure(spec: FigureSpec, filename: str | None = None) -> str:
    """
    Render a FigureSpec to a PNG in output/figures/.
    Returns the filename (used to build the /figures/<filename> URL).
    """
    if filename is None:
        filename = f"fig_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    dispatch = {
        "triangle":         _render_polygon,
        "quadrilateral":    _render_polygon,
        "circle":           _render_circle,
    }

    # Coordinate plane is handled by its dedicated renderer
    if spec.type == "coordinate_plane":
        return coordinate_renderer.render_coord_figure(
            spec.__dict__ | {"type": "coordinate_plane"},
            filename,
        )

    fn = dispatch.get(spec.type)
    if fn is None:
        raise ValueError(f"Unknown figure type: {spec.type!r}")

    fn(spec, filepath)
    return filename


# ── Triangle / quadrilateral ───────────────────────────────────────────────────

def _render_polygon(spec: FigureSpec, filepath: str):
    keys   = list(spec.vertices.keys())
    coords = np.array([spec.vertices[k] for k in keys], dtype=float)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # ── filled polygon ──────────────────────────────────────────────────────
    poly = plt.Polygon(coords, closed=True,
                       facecolor=C_FILL, edgecolor=C_EDGE, linewidth=2, zorder=1)
    ax.add_patch(poly)

    centroid = coords.mean(axis=0)

    # ── vertex names (A, B, C …) ────────────────────────────────────────────
    for key, coord in zip(keys, coords):
        outward = _unit(coord - centroid) * 0.32
        ax.text(coord[0] + outward[0], coord[1] + outward[1], key,
                ha="center", va="center",
                fontsize=15, fontweight="bold", color=C_VERTEX, zorder=4)

    # ── right-angle marker ──────────────────────────────────────────────────
    if spec.right_angle_at and spec.right_angle_at in spec.vertices:
        ra   = spec.right_angle_at
        idx  = keys.index(ra)
        adjs = [keys[(idx - 1) % len(keys)], keys[(idx + 1) % len(keys)]]
        size = min(
            np.linalg.norm(coords[(idx + 1) % len(keys)] - coords[idx]),
            np.linalg.norm(coords[(idx - 1) % len(keys)] - coords[idx]),
        ) * 0.10
        _right_angle_marker(ax,
                             spec.vertices[ra],
                             spec.vertices[adjs[0]],
                             spec.vertices[adjs[1]],
                             size)

    # ── angle labels ────────────────────────────────────────────────────────
    angle_map = {al.vertex: al.label for al in spec.angle_labels}
    for i, key in enumerate(keys):
        if key not in angle_map:
            continue
        adj = [keys[(i - 1) % len(keys)], keys[(i + 1) % len(keys)]]
        bis = _bisector(spec.vertices[key],
                        spec.vertices[adj[0]],
                        spec.vertices[adj[1]])
        avg_side = np.mean([
            np.linalg.norm(coords[(i + 1) % len(keys)] - coords[i]),
            np.linalg.norm(coords[(i - 1) % len(keys)] - coords[i]),
        ])
        pos = np.array(spec.vertices[key], dtype=float) + bis * avg_side * 0.26
        label = ensure_latex(angle_map[key])
        ax.text(pos[0], pos[1], label,
                ha="center", va="center",
                fontsize=13, color=C_ANGLE, zorder=4)

    # ── side labels ─────────────────────────────────────────────────────────
    for sl in spec.side_labels:
        if sl.from_vertex not in spec.vertices or sl.to_vertex not in spec.vertices:
            continue
        p1  = np.array(spec.vertices[sl.from_vertex], dtype=float)
        p2  = np.array(spec.vertices[sl.to_vertex],   dtype=float)
        mid = (p1 + p2) / 2
        toward_centroid = _unit(centroid - mid)
        pos = mid + toward_centroid * np.linalg.norm(p2 - p1) * 0.12
        label = ensure_latex(sl.label)
        ax.text(pos[0], pos[1], label,
                ha="center", va="center",
                fontsize=13, color=C_SIDE, zorder=4)

    # ── extra labels ────────────────────────────────────────────────────────
    for el in spec.extra_labels:
        ax.text(el.x, el.y, ensure_latex(el.label),
                ha="center", va="center", fontsize=10, color=C_EXTRA, zorder=4)

    # ── axis limits with padding ─────────────────────────────────────────────
    xs, ys = coords[:, 0], coords[:, 1]
    span   = max(xs.max() - xs.min(), ys.max() - ys.min())
    pad    = span * 0.45
    ax.set_xlim(xs.min() - pad, xs.max() + pad)
    ax.set_ylim(ys.min() - pad, ys.max() + pad)

    _save(fig, filepath)


# ── Circle ─────────────────────────────────────────────────────────────────────

def _render_circle(spec: FigureSpec, filepath: str):
    cx, cy = (spec.center or [0, 0])
    r      = spec.radius or 1.0

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    circle = plt.Circle((cx, cy), r,
                         facecolor=C_FILL, edgecolor=C_EDGE, linewidth=2, zorder=1)
    ax.add_patch(circle)

    # Centre dot
    ax.plot(cx, cy, "o", color=C_EDGE, markersize=4, zorder=3)

    # Extra labels (e.g. arc / sector labels)
    for el in spec.extra_labels:
        ax.text(el.x, el.y, ensure_latex(el.label),
                ha="center", va="center", fontsize=10, color=C_EXTRA, zorder=4)

    pad = r * 0.3
    ax.set_xlim(cx - r - pad, cx + r + pad)
    ax.set_ylim(cy - r - pad, cy + r + pad)

    _save(fig, filepath)


# ── Coordinate plane ───────────────────────────────────────────────────────────

def _render_coordinate_plane(spec: FigureSpec, filepath: str):
    points = spec.points or []

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    # Grid lines
    ax.grid(True, color="#eeeeee", linewidth=0.8, zorder=0)
    ax.axhline(0, color=C_AXIS, linewidth=1.4, zorder=1)
    ax.axvline(0, color=C_AXIS, linewidth=1.4, zorder=1)
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Points
    for pt in points:
        x, y = float(pt["x"]), float(pt["y"])
        ax.plot(x, y, "o", color=C_ANGLE, markersize=6, zorder=3)
        lbl = ensure_latex(pt.get("label", ""))
        if lbl:
            ax.text(x + 0.15, y + 0.15, lbl,
                    fontsize=10, color=C_VERTEX, zorder=4)

    # Auto-range
    if points:
        xs = [float(p["x"]) for p in points]
        ys = [float(p["y"]) for p in points]
        pad = max(max(xs) - min(xs), max(ys) - min(ys), 2) * 0.3
        ax.set_xlim(min(xs) - pad, max(xs) + pad)
        ax.set_ylim(min(ys) - pad, max(ys) + pad)
    else:
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)

    _save(fig, filepath)


# ── Shared save helper ─────────────────────────────────────────────────────────

def _save(fig, filepath: str):
    plt.tight_layout()
    plt.savefig(filepath, dpi=130, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
