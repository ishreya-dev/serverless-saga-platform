from diagram_lib import (
    new_canvas,
    draw_title,
    draw_card,
    draw_database,
    draw_queue,
    draw_arrow,
    draw_section,
    save,
    COLOR_TEXT_MUTED,
)

WIDTH = 11.5
HEIGHT = 7.4

def main():
    fig, ax = new_canvas(WIDTH, HEIGHT)

    draw_title(
        ax,
        0.4,
        HEIGHT - 0.35,
        "Deployment Architecture",
        "AWS serverless infrastructure supporting the Flash Sale Saga platform.",
    )

    # ============================================================
    # Compute Layer
    # ============================================================

    COMPUTE_Y = 5.35
    
    gw = draw_card(
        ax, 0.6, COMPUTE_Y, 1.8, 0.75,
        "API Gateway", "HTTP API"
    )

    payment = draw_card(
        ax, 3.0, COMPUTE_Y, 1.8, 0.75,
        "Payment Service", "AWS Lambda",
        accent=True,
    )

    inventory = draw_card(
        ax, 5.2, COMPUTE_Y, 1.8, 0.75,
        "Inventory Service", "AWS Lambda",
        accent=True,
    )

    rollback = draw_card(
        ax, 7.4, COMPUTE_Y, 1.8, 0.75,
        "Rollback Service", "AWS Lambda",
        accent=True,
    )

    draw_section(
        ax,
        2.8,
        COMPUTE_Y - 0.20,
        6.8,
        1.15,
        "Compute",
    )

    draw_arrow(ax, gw["right"], payment["left"])
    draw_arrow(ax, payment["right"], inventory["left"])
    draw_arrow(ax, inventory["right"], rollback["left"])

    # ============================================================
    # Messaging
    # ============================================================

    payment_q = draw_queue(ax, 3.0, 3.9, 1.8, 0.75,
                           "SQS FIFO",
                           "payment-events.fifo")

    inventory_q = draw_queue(ax, 5.2, 3.9, 1.8, 0.75,
                             "SQS FIFO",
                             "inventory-events.fifo")

    rollback_q = draw_queue(ax, 7.4, 3.9, 1.8, 0.75,
                            "SQS FIFO",
                            "rollback-events.fifo")

    draw_section(ax, 2.8, 3.65, 6.8, 1.15, "Messaging")

    draw_arrow(ax, payment["bottom"], payment_q["top"])
    draw_arrow(ax, inventory["bottom"], inventory_q["top"])
    draw_arrow(ax, rollback["bottom"], rollback_q["top"])

    # ============================================================
    # Dead Letter Queues
    # ============================================================

    payment_dlq = draw_queue(ax, 3.0, 2.2, 1.8, 0.65,
                             "Payment DLQ",
                             "")

    inventory_dlq = draw_queue(ax, 5.2, 2.2, 1.8, 0.65,
                               "Inventory DLQ",
                               "")

    rollback_dlq = draw_queue(ax, 7.4, 2.2, 1.8, 0.65,
                              "Rollback DLQ",
                              "")

    draw_arrow(ax, payment_q["bottom"], payment_dlq["top"])
    draw_arrow(ax, inventory_q["bottom"], inventory_dlq["top"])
    draw_arrow(ax, rollback_q["bottom"], rollback_dlq["top"])

    # ============================================================
    # Persistence
    # ============================================================

    ddb = draw_database(
        ax,
        3.0,
        0.45,
        2.0,
        1.05,
        "Reservation Store",
        "DynamoDB",
    )

    pg = draw_database(
        ax,
        5.6,
        0.45,
        2.0,
        1.05,
        "Payment Ledger",
        "PostgreSQL",
    )

    draw_section(ax, 2.8, 0.2, 5.2, 1.55, "Persistence")

    draw_arrow(ax, inventory["bottom"], ddb["top"], color="#C7CBD1")
    draw_arrow(ax, payment["bottom"], pg["top"], color="#C7CBD1")

    # ============================================================
    # Observability
    # ============================================================

    cw = draw_card(
        ax,
        9.8,
        3.2,
        1.7,
        0.8,
        "CloudWatch",
        "Logs & Alarms",
    )

    draw_arrow(ax, rollback_dlq["right"], cw["left"], color=COLOR_TEXT_MUTED)

    save(fig, "deployment.png")

if __name__ == "__main__":
        main()