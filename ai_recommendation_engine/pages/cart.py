import reflex as rx
from ai_recommendation_engine.state.cart_state import CartState
from ai_recommendation_engine.components.navbar import navbar


def cart():
    return rx.vstack(
        navbar(),

        rx.heading("Your Cart", size="6"),

        # ✅ CORRECT FOREACH (NO key access)
        rx.foreach(
            CartState.cart.to(list),
            lambda item: rx.box(

                rx.hstack(

                    # 🖼️ Image
                    rx.image(
                        src=item["image"],
                        width="100px",
                        height="100px",
                        border_radius="8px"
                    ),

                    # 📦 Details
                    rx.vstack(
                        rx.text(item["name"], font_weight="bold"),

                        rx.text(f"₹{item['price']}", color="green"),

                        # ➕ ➖ buttons
                        rx.hstack(
                            rx.button(
                                "-",
                                on_click=lambda: CartState.decrease(item)
                            ),

                            rx.text(item["qty"]),

                            rx.button(
                                "+",
                                on_click=lambda: CartState.increase(item)
                            ),
                        ),

                        rx.button(
                            "Remove",
                            color_scheme="red",
                            on_click=lambda: CartState.remove(item)
                        ),

                        align="start"
                    ),

                    rx.spacer(),

                    # 💰 total per item
                    rx.text(
                        f"₹{item['price'] * item['qty']}",
                        font_weight="bold"
                    ),

                    width="100%",
                    align="center"
                ),

                padding="16px",
                border_radius="12px",
                background="#111827",
                margin_bottom="12px"
            )
        ),

        # 💵 total
        rx.box(
            rx.hstack(
                rx.text("Total:", font_weight="bold"),
                rx.spacer(),
                rx.text(f"₹{CartState.total}", color="green"),
            ),
            padding="16px",
            background="#1f2937",
            border_radius="12px",
            width="100%"
        ),

        rx.button(
            "Proceed to Checkout",
            width="100%",
            on_click=lambda: rx.redirect("/checkout")
        ),

        max_width="800px",
        margin="auto",
        padding="2em",
        spacing="4"
    )