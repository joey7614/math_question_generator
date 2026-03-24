"""
coordinate_renderer.py — Renders coordinate geometry figures.

Separate from geometry_renderer.py because the drawing model is completely
different: axes, grids, equations of lines/curves vs. polygon vertices/angles.

Pure logic — no AI calls. AI supplies a CoordSpec dict; this file draws it.

Supported elements (all optional, mix and match):
  points       — labeled points on the plane
  segments     — line segments with optional length/midpoint label
  lines        — infinite lines (slope-intercept or two-point), with equation label
  circles      — circle by center + radius
  curves       — parabola (y = ax²+bx+c) or generic function
  slope_triangles — rise/run triangles on a segment
  right_angle_markers — small square between two directions at a vertex
  shaded_regions — shade above/below a line
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import uuid

from math_formatter import ensure_latex

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

matplotlib.rcParams.update({
    "mathtext.fontset": "stix",
    "font.family":      "STIXGeneral",
})

# ── Palette ────────────────────────────────────────────────────────────────────
C_AXIS    = "#2c3e50"
C_GRID    = "#e0e0e0"
C_POINT   = "#c0392b"
C_LINE    = "#2980b9"
C_SEGMENT = "#2c3e50"
C_CURVE   = "#8e44ad"
C_CIRCLE  = "#27ae60"
C_LABEL   = "#1a1a2e"
C_SLOPE   = "#e67e22"
C_SHADE   = "#3498db"


# ── Public spec dataclass (plain dict interface for AI) ────────────────────────

def render_coord_figure(spec: dict, filename: str | None = None) -> str:
    """
    Main entry point.  `spec` is the raw dict from AI (or placeholder).
    Returns the saved filename for URL construction.
    """
    if filename is None:
        filename = f"coord_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    _draw(spec, filepath)
    return filename


# ── Core drawing ───────────────────────────────────────────────────────────────

def _draw(spec: dict, filepath: str):
    x_range = spec.get("x_range", [-6, 6])
    y_range = spec.get("y_range", [-6, 6])
    show_grid = spec.get("show_grid", True)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    _draw_axes(ax, x_range, y_range, show_grid)

    # Draw elements in back-to-front order
    for r in spec.get("shaded_regions", []):
        _draw_shaded_region(ax, r, x_range, y_range)
    for c in spec.get("curves", []):
        _draw_curve(ax, c, x_range)
    for circle in spec.get("circles", []):
        _draw_circle(ax, circle)
    for line in spec.get("lines", []):
        _draw_line(ax, line, x_range, y_range)
    for seg in spec.get("segments", []):
        _draw_segment(ax, seg)
    for st in spec.get("slope_triangles", []):
        _draw_slope_triangle(ax, st)
    for ra in spec.get("right_angle_markers", []):
        _draw_right_angle(ax, ra)
    for pt in spec.get("points", []):
        _draw_point(ax, pt)

    ax.set_xlim(x_range[0] - 0.3, x_range[1] + 0.3)
    ax.set_ylim(y_range[0] - 0.3, y_range[1] + 0.3)

    plt.tight_layout()
    plt.savefig(filepath, dpi=130, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)


# ── Axes ───────────────────────────────────────────────────────────────────────

def _draw_axes(ax, x_range, y_range, show_grid: bool):
    xmin, xmax = x_range
    ymin, ymax = y_range

    for spine in ax.spines.values():
        spine.set_visible(False)

    if show_grid:
        ax.grid(True, color=C_GRID, linewidth=0.7, zorder=0)

    # X axis with arrow
    ax.annotate("", xy=(xmax + 0.2, 0), xytext=(xmin - 0.2, 0),
                arrowprops=dict(arrowstyle="-|>", color=C_AXIS, lw=1.4),
                zorder=2)
    # Y axis with arrow
    ax.annotate("", xy=(0, ymax + 0.2), xytext=(0, ymin - 0.2),
                arrowprops=dict(arrowstyle="-|>", color=C_AXIS, lw=1.4),
                zorder=2)

    # Axis labels
    ax.text(xmax + 0.35, 0, "$x$", ha="left",  va="center", fontsize=13, color=C_AXIS)
    ax.text(0, ymax + 0.35, "$y$", ha="center", va="bottom", fontsize=13, color=C_AXIS)

    # Tick marks and numbers (skip 0)
    tick_size = 0.12
    for x in range(int(xmin), int(xmax) + 1):
        if x == 0:
            continue
        ax.plot([x, x], [-tick_size, tick_size], color=C_AXIS, lw=1, zorder=2)
        ax.text(x, -tick_size * 3, str(x),
                ha="center", va="top", fontsize=8, color=C_AXIS)
    for y in range(int(ymin), int(ymax) + 1):
        if y == 0:
            continue
        ax.plot([-tick_size, tick_size], [y, y], color=C_AXIS, lw=1, zorder=2)
        ax.text(-tick_size * 3, y, str(y),
                ha="right", va="center", fontsize=8, color=C_AXIS)

    # Origin label
    ax.text(-0.25, -0.25, "$O$", ha="right", va="top", fontsize=9, color=C_AXIS)


# ── Points ─────────────────────────────────────────────────────────────────────

def _draw_point(ax, pt: dict):
    x, y = float(pt["x"]), float(pt["y"])
    color = pt.get("color", C_POINT)
    ax.plot(x, y, "o", color=color, markersize=6, zorder=5)

    label = ensure_latex(pt.get("label", ""))
    if label:
        # Smart offset: push label away from origin
        ox = 0.2 if x >= 0 else -0.2
        oy = 0.2
        ha = "left" if x >= 0 else "right"
        ax.text(x + ox, y + oy, label,
                ha=ha, va="bottom", fontsize=12, color=C_LABEL,
                fontweight="bold", zorder=6)


# ── Line segments ──────────────────────────────────────────────────────────────

def _draw_segment(ax, seg: dict):
    x1, y1 = seg["from"]
    x2, y2 = seg["to"]
    style = seg.get("style", "solid")
    color = seg.get("color", C_SEGMENT)
    ls = "--" if style == "dashed" else "-"

    ax.plot([x1, x2], [y1, y2], ls=ls, color=color, lw=2, zorder=3)

    # Midpoint label
    label = ensure_latex(seg.get("label", ""))
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # Perpendicular offset direction
        dx, dy = x2 - x1, y2 - y1
        length = np.hypot(dx, dy) or 1
        px, py = -dy / length * 0.3, dx / length * 0.3
        ax.text(mx + px, my + py, label,
                ha="center", va="center", fontsize=11,
                color=color, zorder=6)

    # Tick marks (equal-length indicator)
    if seg.get("equal_mark"):
        _draw_tick_mark(ax, x1, y1, x2, y2, seg["equal_mark"])


def _draw_tick_mark(ax, x1, y1, x2, y2, count: int = 1):
    """Draw 1, 2, or 3 tick marks at the midpoint of a segment."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    length = np.hypot(dx, dy) or 1
    ux, uy = dx / length, dy / length       # unit along segment
    px, py = -uy * 0.15, ux * 0.15          # perpendicular

    gap = 0.1
    offsets = np.linspace(-(count - 1) * gap / 2, (count - 1) * gap / 2, count)
    for off in offsets:
        sx = mx + ux * off
        sy = my + uy * off
        ax.plot([sx - px, sx + px], [sy - py, sy + py],
                color=C_SEGMENT, lw=1.5, zorder=4)


# ── Infinite lines ─────────────────────────────────────────────────────────────

def _draw_line(ax, line: dict, x_range, y_range):
    xmin, xmax = x_range
    color = line.get("color", C_LINE)
    ls = "--" if line.get("style") == "dashed" else "-"

    # Determine slope and intercept
    if "slope" in line and "intercept" in line:
        m, b = float(line["slope"]), float(line["intercept"])
        xs = np.array([xmin - 1, xmax + 1])
        ys = m * xs + b
    elif "from" in line and "to" in line:
        x1, y1 = line["from"]
        x2, y2 = line["to"]
        dx = x2 - x1
        if abs(dx) < 1e-10:
            # Vertical line
            ax.axvline(x=x1, color=color, lw=1.8, ls=ls, zorder=2)
            label = ensure_latex(line.get("label", ""))
            if label:
                ax.text(x1 + 0.2, (y_range[0] + y_range[1]) / 2, label,
                        fontsize=10, color=color, zorder=6)
            return
        m = (y2 - y1) / dx
        b = y1 - m * x1
        xs = np.array([xmin - 1, xmax + 1])
        ys = m * xs + b
    else:
        return

    ax.plot(xs, ys, ls=ls, color=color, lw=1.8, zorder=2)

    label = ensure_latex(line.get("label", ""))
    if label:
        # Place label near right end of visible range
        lx = xmax * 0.75
        ly = m * lx + b
        ax.text(lx + 0.15, ly + 0.15, label,
                fontsize=10, color=color, zorder=6)


# ── Circles ────────────────────────────────────────────────────────────────────

def _draw_circle(ax, circle: dict):
    cx, cy = circle["center"]
    r      = float(circle["radius"])
    color  = circle.get("color", C_CIRCLE)

    patch = mpatches.Circle((cx, cy), r,
                             facecolor="none", edgecolor=color,
                             linewidth=2, zorder=3)
    ax.add_patch(patch)
    ax.plot(cx, cy, "+", color=color, markersize=8, mew=1.5, zorder=4)

    # Radius label
    label = ensure_latex(circle.get("label", ""))
    if label:
        ax.text(cx + r / 2, cy + 0.15, label,
                ha="center", va="bottom", fontsize=11, color=color, zorder=6)
        ax.plot([cx, cx + r], [cy, cy], "-", color=color, lw=1.2, zorder=3)


# ── Curves ────────────────────────────────────────────────────────────────────

def _draw_curve(ax, curve: dict, x_range):
    xmin, xmax = x_range
    color = curve.get("color", C_CURVE)
    xs = np.linspace(xmin, xmax, 400)

    curve_type = curve.get("type", "parabola")
    if curve_type == "parabola":
        a = float(curve.get("a", 1))
        b = float(curve.get("b", 0))
        c = float(curve.get("c", 0))
        ys = a * xs**2 + b * xs + c
    else:
        return   # unknown curve type — skip safely

    ax.plot(xs, ys, color=color, lw=2, zorder=3)

    label = ensure_latex(curve.get("label", ""))
    if label:
        # Label near the right side of the curve
        lx = xmax * 0.6
        if curve_type == "parabola":
            ly = a * lx**2 + b * lx + c
        ax.text(lx + 0.15, ly + 0.2, label,
                fontsize=10, color=color, zorder=6)


# ── Slope triangles ────────────────────────────────────────────────────────────

def _draw_slope_triangle(ax, st: dict):
    """
    Draw a rise/run right triangle under a line segment to illustrate slope.
    """
    x1, y1 = st["from"]
    x2, y2 = st["to"]
    color = st.get("color", C_SLOPE)

    # Corner of the triangle
    cx, cy = x2, y1   # horizontal then vertical

    # Draw the two legs (dashed)
    ax.plot([x1, cx], [y1, cy], "--", color=color, lw=1.4, zorder=3)
    ax.plot([cx, x2], [cy, y2], "--", color=color, lw=1.4, zorder=3)

    # Right angle at corner
    size = abs(x2 - x1) * 0.08
    sx = -np.sign(x2 - x1) * size
    sy =  np.sign(y2 - y1) * size
    ax.plot([cx + sx, cx + sx, cx], [cy, cy + sy, cy + sy],
            color=color, lw=1.2, zorder=4)

    # Labels
    run_label  = ensure_latex(st.get("run_label",  "run"))
    rise_label = ensure_latex(st.get("rise_label", "rise"))
    mx_run  = (x1 + cx) / 2
    mx_rise = (cx + x2) / 2
    ax.text(mx_run,  cy - 0.3 * np.sign(y2 - y1), run_label,
            ha="center", va="center", fontsize=10, color=color, zorder=6)
    ax.text(cx + 0.3 * np.sign(x2 - x1), (cy + y2) / 2, rise_label,
            ha="center", va="center", fontsize=10, color=color, zorder=6)


# ── Right angle between two lines ──────────────────────────────────────────────

def _draw_right_angle(ax, ra: dict):
    vertex = np.array(ra["vertex"], dtype=float)
    adj1   = np.array(ra["adj1"],   dtype=float)
    adj2   = np.array(ra["adj2"],   dtype=float)
    size   = float(ra.get("size", 0.25))

    def unit(v):
        n = np.linalg.norm(v)
        return v / n if n > 1e-10 else v

    u1 = unit(adj1 - vertex) * size
    u2 = unit(adj2 - vertex) * size
    p1, p2, p3 = vertex + u1, vertex + u1 + u2, vertex + u2
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C_AXIS, lw=1.2, zorder=4)
    ax.plot([p2[0], p3[0]], [p2[1], p3[1]], color=C_AXIS, lw=1.2, zorder=4)


# ── Shaded regions ─────────────────────────────────────────────────────────────

def _draw_shaded_region(ax, region: dict, x_range, y_range):
    """Shade area above or below a line y = mx + b."""
    xmin, xmax = x_range
    ymin, ymax = y_range
    m = float(region.get("slope", 1))
    b = float(region.get("intercept", 0))
    above = region.get("above", True)
    color = region.get("color", C_SHADE)
    alpha = float(region.get("alpha", 0.15))

    xs = np.array([xmin, xmax])
    ys = m * xs + b

    if above:
        ax.fill_between(xs, ys, ymax, alpha=alpha, color=color, zorder=1)
    else:
        ax.fill_between(xs, ymin, ys, alpha=alpha, color=color, zorder=1)
