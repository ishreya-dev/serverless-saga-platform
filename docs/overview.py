"""
overview.py -> overview.png

The 30-second version of the system. No AWS, no databases, no queues --
just the shape of the request path a customer triggers when they buy a
flash-sale ticket. This is the first thing a recruiter or a new
contributor should see.
"""

from diagram_lib import (
    new_canvas, draw_title, draw_card, draw_arrow, save, GRID,
    COLOR_ACCENT,
)

WIDTH, HEIGHT = 11.5, 5.6
CARD_W, CARD_H = 1.9, 0.85
ROW_GAP = 1.55
COL_GAP = 0.55

STEPS_ROW_1 = ["Customer", "API Gateway", "Saga\nInitiator", "Payment\nService"]
STEPS_ROW_2 = ["Frontend", "Status\nService", "Rollback\nService", "Inventory\nService"]


def row_x_positions(start_x, count):
    return [start_x + i * (CARD_W + COL_GAP) for i in range(count)]


def main():
    fig, ax = new_canvas(WIDTH, HEIGHT)
    draw_title(
        ax, 0.4, HEIGHT - 0.35,
        "Flash Sale Saga -- System Overview",
        "One customer request, seven services, one confirmed booking.",
    )

    top_y = HEIGHT - 2.2
    bottom_y = top_y - ROW_GAP
    start_x = 0.5
    xs = row_x_positions(start_x, 4)

    # Row 1: Customer -> API Gateway -> Saga Initiator -> Payment Service
    anchors_top = []
    for label, x in zip(STEPS_ROW_1, xs):
        accent = label == "Customer"
        anchors_top.append(draw_card(ax, x, top_y, CARD_W, CARD_H, label, accent=accent))

    for i in range(len(anchors_top) - 1):
        draw_arrow(ax, anchors_top[i]["right"], anchors_top[i + 1]["left"])

    # Row 2 sits directly under row 1, but reads right-to-left so the
    # story flows in a single continuous snake: down, then left.
    anchors_bottom = []
    for label, x in zip(STEPS_ROW_2, xs):
        accent = label == "Frontend"
        anchors_bottom.append(draw_card(ax, x, bottom_y, CARD_W, CARD_H, label, accent=accent))

    draw_arrow(ax, anchors_top[-1]["bottom"], anchors_bottom[-1]["top"])
    for i in range(len(anchors_bottom) - 1, 0, -1):
        draw_arrow(ax, anchors_bottom[i]["left"], anchors_bottom[i - 1]["right"])

    # A short caption instead of clutter -- keeps the "what is this" answer explicit.
    ax.text(
        0.5, bottom_y - 0.55,
        "Payment, inventory, and rollback are decoupled services coordinated\n"
        "through a saga, not a single monolithic transaction.",
        fontsize=8.5, color="#6E7681", ha="left", va="top", family="DejaVu Sans",
    )

    save(fig, "overview.png")


if __name__ == "__main__":
    main()