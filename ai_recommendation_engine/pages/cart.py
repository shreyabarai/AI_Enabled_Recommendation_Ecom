import reflex as rx
from ai_recommendation_engine.state.cart_state import CartState
from ai_recommendation_engine.components.navbar import navbar


from ai_recommendation_engine.state.cart_state import CartState
from ai_recommendation_engine.components.navbar import navbar
from ai_recommendation_engine.components.footer import footer

def cart():
    return rx.box(
        navbar(),
        rx.vstack(
            rx.vstack(
                rx.heading("Shopping Cart", size="9", weight="bold", color="#111827"),
                rx.text(rx.cond(CartState.total_items > 0, f"You have {CartState.total_items} items in your cart", "Your cart is currently empty"), color="#374151"),
                align_items="start",
                spacing="2",
                padding="4rem 4rem 2rem 4rem"
            ),

            rx.cond(
                CartState.total_items == 0,
                rx.center(
                    rx.vstack(
                        rx.icon(tag="shopping-bag", size=60, color="#d1d5db"),
                        rx.text("Your cart is empty.", size="5", color="#6b7280"),
                        rx.button(
                            "Start Shopping",
                            on_click=lambda: rx.redirect("/home"),
                            bg="#10b981",
                            color="white",
                            radius="full",
                            margin_top="1rem"
                        ),
                        spacing="4",
                        padding="6rem"
                    ),
                    width="100%"
                ),
                rx.grid(
                    # Cart Items List
                    rx.vstack(
                        rx.foreach(
                            CartState.cart,
                            lambda item: rx.box(
                                rx.hstack(
                                    # 🖼️ Image
                                    rx.image(
                                        src=item["image"],
                                        width="120px",
                                        height="120px",
                                        object_fit="cover",
                                        border_radius="1rem"
                                    ),

                                    # 📦 Details
                                    rx.vstack(
                                        rx.text(item["name"], weight="bold", size="4", color="#111827"),
                                        rx.text(item["category"], size="2", color="#6b7280"),
                                        rx.text("₹", item['price'], color="#10b981", weight="bold"),
                                        
                                        # ➕ ➖ buttons
                                        rx.hstack(
                                            rx.button(
                                                rx.icon(tag="minus", size=14),
                                                on_click=lambda: CartState.decrease(item),
                                                variant="soft",
                                                color_scheme="gray",
                                                radius="full",
                                                size="1"
                                            ),
                                            rx.text(item["qty"], weight="bold", padding="0 0.5rem"),
                                            rx.button(
                                                rx.icon(tag="plus", size=14),
                                                on_click=lambda: CartState.increase(item),
                                                variant="soft",
                                                color_scheme="gray",
                                                radius="full",
                                                size="1"
                                            ),
                                            spacing="1",
                                            align_items="center",
                                            bg="#f3f4f6",
                                            padding="0.25rem",
                                            border_radius="full",
                                            margin_top="0.5rem"
                                        ),
                                        align_items="start",
                                        spacing="1",
                                        padding_left="1rem"
                                    ),

                                    rx.spacer(),

                                    # 💰 total per item & Remove
                                    rx.vstack(
                                        rx.text(
                                            "₹", (item['price'].to(int) * item['qty'].to(int)),
                                            weight="bold",
                                            size="5",
                                            color="#111827"
                                        ),
                                        rx.button(
                                            rx.icon(tag="trash-2", size=16),
                                            variant="ghost",
                                            color_scheme="red",
                                            on_click=lambda: CartState.remove(item),
                                            size="1"
                                        ),
                                        align_items="end",
                                        spacing="4"
                                    ),

                                    width="100%",
                                    align_items="center"
                                ),
                                padding="1.5rem",
                                border_radius="1.5rem",
                                bg="white",
                                border="1px solid #f3f4f6",
                                margin_bottom="1rem",
                                width="100%",
                                _hover={"box_shadow": "0 4px 6px -1px rgba(0,0,0,0.05)"}
                            )
                        ),
                        width="100%"
                    ),
                    
                    # Cart Summary Card
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.heading("Order Summary", size="5", weight="bold", color="#111827", margin_bottom="1rem"),
                                rx.hstack(
                                    rx.text("Subtotal", color="#4b5563"),
                                    rx.spacer(),
                                    rx.text("₹", CartState.total, weight="medium"),
                                    width="100%"
                                ),
                                rx.hstack(
                                    rx.text("Shipping", color="#4b5563"),
                                    rx.spacer(),
                                    rx.text("FREE", color="#10b981", weight="bold"),
                                    width="100%"
                                ),
                                rx.divider(margin="1rem 0"),
                                rx.hstack(
                                    rx.text("Total", weight="bold", size="5"),
                                    rx.spacer(),
                                    rx.text("₹", CartState.total, weight="bold", size="6", color="#10b981"),
                                    width="100%"
                                ),
                                rx.button(
                                    "Proceed to Checkout",
                                    width="100%",
                                    size="4",
                                    bg="#10b981",
                                    color="white",
                                    radius="full",
                                    margin_top="2rem",
                                    on_click=lambda: rx.redirect("/checkout"),
                                    _hover={"transform": "scale(1.02)", "bg": "#059669"},
                                    transition="all 0.2s"
                                ),
                                rx.button(
                                    "Continue Shopping",
                                    variant="ghost",
                                    width="100%",
                                    color="#6b7280",
                                    on_click=lambda: rx.redirect("/home"),
                                    margin_top="0.5rem"
                                ),
                                align_items="start",
                                width="100%"
                            ),
                            padding="2rem",
                            bg="white",
                            border_radius="2rem",
                            border="1px solid #f3f4f6",
                            box_shadow="0 10px 15px -3px rgba(0,0,0,0.05)",
                            position="sticky",
                            top="120px"
                        ),
                        width="100%"
                    ),
                    columns="2",
                    spacing="8",
                    width="100%",
                    padding="0 4rem 6rem 4rem"
                )
            ),
            footer(),
            width="100%",
            spacing="0",
            bg="#f9fafb"
        )
    )