"""
storage.py -> storage.png

How state is actually persisted. PostgreSQL owns the source of truth
for money (the payment ledger, keyed by an idempotency key). DynamoDB
owns the fast-moving saga state that the choreography reads and writes
at high concurrency. This diagram exists to answer "why two databases?"
"""

from diagram_lib import (
    COLOR_TEXT_MUTED,
    draw_arrow,
    draw_badge,
    draw_card,
    draw_database,
    draw_section,
    draw_title,
    new_canvas,
    save,
)

WIDTH, HEIGHT = 11.5, 7.6


def main():
    fig, ax = new_canvas(WIDTH, HEIGHT)
    draw_title(
        ax,
        0.4,
        HEIGHT - 0.35,
        "Persistence Model",
        "Financial records live in PostgreSQL. Saga state is maintained in DynamoDB.",
    )

    # ---- PostgreSQL: system of record for payment ------------------------
    pg_x, pg_y = 0.8, 3.15
    ledger = draw_database(ax, pg_x, pg_y, 2.6, 1.4, "Payment Ledger", "PostgreSQL")
    draw_section(ax, pg_x - 0.3, pg_y - 0.35, 3.2, 2.05, "Financial Records")
    ax.text(
        pg_x,
        pg_y - 0.05,
        "UNIQUE(idempotency_key)\nFK(saga_id)",
        fontsize=7.5,
        color=COLOR_TEXT_MUTED,
        ha="left",
        va="top",
        family="DejaVu Sans",
    )

    # ---- DynamoDB: fast-moving saga state, one table per concern ---------
    ddb_x = 5.1
    ddb_labels = [
        ("Reservation", "TTL Hold"),
        ("Inventory", "Available Seats"),
        ("Status", "Saga State"),
        ("Recovery", "Replay Marker"),
    ]
    step_gap = 1.28
    top_y = HEIGHT - 2.95
    ddb_anchors = []
    for i, (label, sub) in enumerate(ddb_labels):
        y = top_y - i * step_gap
        ddb_anchors.append(draw_card(ax, ddb_x, y, 2.9, 0.8, label, sub))

    draw_section(
        ax,
        ddb_x - 0.3,
        ddb_anchors[-1]["bottom"][1] - 0.35,
        3.5,
        top_y + 0.8 - (ddb_anchors[-1]["bottom"][1] - 0.3) + 0.35,
        "Saga State (DynamoDB)",
    )

    for i in range(len(ddb_anchors) - 1):
        draw_arrow(ax, ddb_anchors[i]["bottom"], ddb_anchors[i + 1]["top"], label="same saga_id" if i == 0 else None)

    # ---- the join: idempotency_key ties the ledger to the saga record ----
    ax.text(
        4.65,
        4.95,
        "shared saga_id",
        fontsize=8,
        color=COLOR_TEXT_MUTED,
        ha="center",
        family="DejaVu Sans",
    )

    draw_arrow(
        ax,
        ledger["right"],
        ddb_anchors[0]["left"],
    )

    draw_badge(
        ax,
        0.8,
        1.0,
        "Idempotent Retries\nNo Duplicate Charges",
    )

    save(fig, "storage.png")


if __name__ == "__main__":
    main()
