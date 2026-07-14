from diagram_lib import (
    draw_arrow,
    draw_card,
    draw_dashed_arrow,
    draw_legend,
    draw_section,
    draw_title,
    new_canvas,
    save,
)

WIDTH, HEIGHT = 11.5, 6.6
CARD_W, CARD_H = 2.5, 0.72

HAPPY_PATH = [
    "Payment Requested",
    "Payment Success",
    "Inventory Reserve",
    "Reservation Success",
    "Booking Confirmed",
]

ROLLBACK_PATH = [
    "Inventory Failure",
    "Rollback Queue",
    "Refund Issued",
    "Saga Complete",
]


def main():
    fig, ax = new_canvas(WIDTH, HEIGHT)
    draw_title(
        ax,
        0.4,
        HEIGHT - 0.35,
        "Flash Sale Saga -- Choreography",
        "Every service reacts to the previous event; there is no central orchestrator.",
    )

    # ---- Happy path: a single vertical chain on the left -------------
    left_x = 0.7
    top_y = HEIGHT - 1.7
    step_gap = 0.98

    happy_anchors = []
    for i, label in enumerate(HAPPY_PATH):
        y = top_y - i * step_gap
        happy_anchors.append(draw_card(ax, left_x, y, CARD_W, CARD_H, label, accent=(i == len(HAPPY_PATH) - 1)))

    for i in range(len(happy_anchors) - 1):
        draw_arrow(ax, happy_anchors[i]["bottom"], happy_anchors[i + 1]["top"])

    # ---- Rollback path: branches off "Inventory Reserve" -------------
    right_x = left_x + CARD_W + 2.3
    branch_index = 2  # "Inventory Reserve"
    branch_y = top_y - branch_index * step_gap

    rollback_anchors = []
    for i, label in enumerate(ROLLBACK_PATH):
        y = branch_y - i * step_gap
        rollback_anchors.append(draw_card(ax, right_x, y, CARD_W, CARD_H, label, muted=(i < 3)))

    # dashed arrow from the fork point across to the failure branch
    draw_dashed_arrow(
        ax,
        happy_anchors[branch_index]["right"],
        rollback_anchors[0]["left"],
        label="on reservation failure",
    )
    for i in range(len(rollback_anchors) - 1):
        draw_dashed_arrow(ax, rollback_anchors[i]["bottom"], rollback_anchors[i + 1]["top"])

    draw_section(
        ax,
        left_x - 0.25,
        happy_anchors[-1]["bottom"][1] - 0.35,
        CARD_W + 0.5,
        top_y + CARD_H - (happy_anchors[-1]["bottom"][1] - 0.35) + 0.15,
        "success path",
    )
    draw_section(
        ax,
        right_x - 0.25,
        rollback_anchors[-1]["bottom"][1] - 0.35,
        CARD_W + 0.5,
        branch_y + CARD_H - (rollback_anchors[-1]["bottom"][1] - 0.35) + 0.15,
        "compensation path",
    )

    draw_legend(
        ax,
        0.7,
        0.35,
        [("solid", "event -> next service"), ("dashed", "compensating action")],
    )

    save(fig, "workflow.png")


if __name__ == "__main__":
    main()
