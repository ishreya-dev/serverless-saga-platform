"""
diagram_lib.py

Small set of reusable drawing primitives shared by the four
Flash Sale Saga diagrams (overview, workflow, deployment, storage).

The goal is not a generic diagramming framework -- it's just enough
shared code that each diagram script stays short and reads like a
description of the system rather than a pile of matplotlib calls.
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Rectangle
from matplotlib.path import Path
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------
# Palette
#
# One accent colour, everything else is grayscale. Kept in one place so a
# future edit ("make the accent green") only touches this block.
# ---------------------------------------------------------------------------
COLOR_BG = "#FFFFFF"
COLOR_BORDER = "#D6D9DE"
COLOR_BORDER_STRONG = "#9AA1AC"
COLOR_TEXT = "#1F2328"
COLOR_TEXT_MUTED = "#6E7681"
COLOR_ACCENT = "#4F46E5"
COLOR_ACCENT_SOFT = "#EEF0FD"
COLOR_FAIL = "#B45309"
COLOR_FAIL_SOFT = "#FBEFE1"

# Grid unit. Every position/size below is expressed as a multiple of this
# so spacing stays consistent without hardcoding pixel-ish numbers.
GRID = 0.35

FONT_TITLE = {"family": "DejaVu Sans", "weight": "bold"}
FONT_BODY = {"family": "DejaVu Sans", "weight": "normal"}


def new_canvas(width, height, dpi=200):
    """Create a figure/axes pair with a clean coordinate system."""
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    return fig, ax


def draw_title(ax, x, y, text, subtitle=None):
    """Page header: a bold title and an optional muted subtitle beneath it."""
    ax.text(x, y, text, fontsize=17, color=COLOR_TEXT, ha="left", va="top", **FONT_TITLE)
    if subtitle:
        ax.text(x, y - GRID * 1.3, subtitle, fontsize=10.5, color=COLOR_TEXT_MUTED,
                 ha="left", va="top", **FONT_BODY)


def draw_card(ax, x, y, w, h, label, sublabel=None, accent=False, muted=False):
    """
    A rounded rectangle representing a service or component.
    Returns (left_mid, right_mid, top_mid, bottom_mid) anchor points so
    callers can wire arrows to/from it without recomputing geometry.
    """
    face = COLOR_ACCENT_SOFT if accent else COLOR_BG
    edge = COLOR_ACCENT if accent else (COLOR_TEXT_MUTED if muted else COLOR_BORDER_STRONG)
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=0.08",
        linewidth=1.1,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(box)

    text_color = COLOR_TEXT if not muted else COLOR_TEXT_MUTED
    if sublabel:
        ax.text(x + w / 2, y + h * 0.60, label, fontsize=10, color=text_color,
                 ha="center", va="center", **FONT_TITLE)
        ax.text(x + w / 2, y + h * 0.30, sublabel, fontsize=8, color=COLOR_TEXT_MUTED,
                 ha="center", va="center", **FONT_BODY)
    else:
        ax.text(x + w / 2, y + h / 2, label, fontsize=10, color=text_color,
                 ha="center", va="center", **FONT_TITLE)

    return {
        "left": (x, y + h / 2), "right": (x + w, y + h / 2),
        "top": (x + w / 2, y + h), "bottom": (x + w / 2, y),
        "center": (x + w / 2, y + h / 2),
    }


def draw_database(ax, x, y, w, h, label, engine=None):
    """A cylinder shape for a datastore. Anchors returned like draw_card."""
    cap_h = h * 0.16
    body = Rectangle((x, y + cap_h / 2), w, h - cap_h, linewidth=1.1,
                      edgecolor=COLOR_BORDER_STRONG, facecolor=COLOR_BG)
    ax.add_patch(body)
    bottom_cap = Ellipse((x + w / 2, y + cap_h / 2), w, cap_h,
                          linewidth=1.1, edgecolor=COLOR_BORDER_STRONG, facecolor=COLOR_BG)
    top_cap = Ellipse((x + w / 2, y + h - cap_h / 2), w, cap_h,
                       linewidth=1.1, edgecolor=COLOR_BORDER_STRONG, facecolor=COLOR_BG)
    ax.add_patch(bottom_cap)
    ax.add_patch(top_cap)

    ax.text(x + w / 2, y + h * 0.42, label, fontsize=9.5, color=COLOR_TEXT,
             ha="center", va="center", **FONT_TITLE)
    if engine:
        ax.text(x + w / 2, y + h * 0.20, engine, fontsize=7.5, color=COLOR_TEXT_MUTED,
                 ha="center", va="center", **FONT_BODY)

    return {
        "left": (x, y + h / 2), "right": (x + w, y + h / 2),
        "top": (x + w / 2, y + h), "bottom": (x + w / 2, y),
        "center": (x + w / 2, y + h / 2),
    }


def draw_queue(ax, x, y, w, h, label, sublabel=None):
    """A rectangle with a stacked-lines glyph to signal 'queue'."""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.06",
                          linewidth=1.1, edgecolor=COLOR_BORDER_STRONG, facecolor=COLOR_BG)
    ax.add_patch(box)

    # three short lines in the left margin of the card = queue glyph
    glyph_x = x + w * 0.10
    for i, frac in enumerate((0.65, 0.5, 0.35)):
        ax.plot([glyph_x, glyph_x + w * 0.10], [y + h * frac, y + h * frac],
                 color=COLOR_ACCENT, linewidth=1.6, solid_capstyle="round")

    text_x = x + w * 0.30
    if sublabel:
        ax.text(text_x, y + h * 0.60, label, fontsize=9, color=COLOR_TEXT,
                 ha="left", va="center", **FONT_TITLE)
        ax.text(text_x, y + h * 0.32, sublabel, fontsize=7.5, color=COLOR_TEXT_MUTED,
                 ha="left", va="center", **FONT_BODY)
    else:
        ax.text(text_x, y + h / 2, label, fontsize=9, color=COLOR_TEXT,
                 ha="left", va="center", **FONT_TITLE)

    return {
        "left": (x, y + h / 2), "right": (x + w, y + h / 2),
        "top": (x + w / 2, y + h), "bottom": (x + w / 2, y),
        "center": (x + w / 2, y + h / 2),
    }


def draw_arrow(ax, p1, p2, label=None, color=COLOR_BORDER_STRONG, label_offset=0.14):
    """A solid arrow between two anchor points, with an optional caption."""
    arrow = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=11,
                             linewidth=1.2, color=color, shrinkA=2, shrinkB=2)
    ax.add_patch(arrow)
    if label:
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        ax.text(mx, my + label_offset, label, fontsize=7.5, color=COLOR_TEXT_MUTED,
                 ha="center", va="bottom", **FONT_BODY)


def draw_dashed_arrow(ax, p1, p2, label=None, color=COLOR_FAIL, label_offset=0.14):
    """A dashed arrow -- reserved for rollback / failure paths only."""
    arrow = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=11,
                             linewidth=1.2, color=color, linestyle=(0, (4, 2.5)),
                             shrinkA=2, shrinkB=2)
    ax.add_patch(arrow)
    if label:
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        ax.text(mx, my + label_offset, label, fontsize=7.5, color=color,
                 ha="center", va="bottom", **FONT_BODY)


def draw_section(ax, x, y, w, h, label):
    """A faint bounding box used to group a cluster of cards under a heading."""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.10",
                          linewidth=1, edgecolor=COLOR_BORDER, facecolor="none",
                          linestyle=(0, (3, 3)))
    ax.add_patch(box)
    ax.text(x + GRID * 0.3, y + h + GRID * 0.12, label, fontsize=8.5,
             color=COLOR_TEXT_MUTED, ha="left", va="bottom", **FONT_TITLE)


def draw_badge(ax, x, y, text, fail=False):
    """A small pill used for short status labels like 'sync' / 'async'."""
    color = COLOR_FAIL if fail else COLOR_ACCENT
    soft = COLOR_FAIL_SOFT if fail else COLOR_ACCENT_SOFT
    w = GRID * (0.9 + 0.16 * len(text))
    h = GRID * 0.7
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.35",
                          linewidth=0.9, edgecolor=color, facecolor=soft)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, fontsize=7, color=color,
             ha="center", va="center", **FONT_TITLE)
    return w


def draw_legend(ax, x, y, items):
    """items: list of (swatch_style, label). swatch_style is 'solid' or 'dashed'."""
    cursor = x
    for style, label in items:
        color = COLOR_FAIL if style == "dashed" else COLOR_BORDER_STRONG
        ls = (0, (4, 2.5)) if style == "dashed" else "solid"
        ax.plot([cursor, cursor + GRID * 0.8], [y, y], color=color, linewidth=1.4, linestyle=ls)
        ax.text(cursor + GRID * 0.95, y, label, fontsize=7.5, color=COLOR_TEXT_MUTED,
                 ha="left", va="center", **FONT_BODY)
        cursor += GRID * 0.95 + GRID * (0.55 + 0.13 * len(label))


def save(fig, path):
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.25)
    print(f"wrote {path}")