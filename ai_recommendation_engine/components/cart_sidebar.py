import reflex as rx
from ..state.cart_state import CartState

def cart_item(item):
    return rx.hstack(
        rx.box(
            rx.image(
                src=item["image"],
                width="80px",
                height="80px",
                object_fit="cover",
                border_radius="0.75rem",
                bg="#f3f4f6"
            ),
            position="relative"
        ),
        rx.vstack(
            rx.text(item["name"], weight="bold", size="3", line_clamp=1, color="#111827"),
            rx.text(item.get("category", "General"), size="1", color="#6b7280"),
            rx.hstack(
                rx.hstack(
                    rx.icon_button(
                        rx.icon(tag="minus", size=14),
                        size="1",
                        variant="soft",
                        color_scheme="gray",
                        on_click=lambda: CartState.decrease(item)
                    ),
                    rx.text(item["qty"], size="2", weight="medium", width="20px", text_align="center"),
                    rx.icon_button(
                        rx.icon(tag="plus", size=14),
                        size="1",
                        variant="soft",
                        color_scheme="gray",
                        on_click=lambda: CartState.increase(item)
                    ),
                    bg="#f3f4f6",
                    border_radius="full",
                    padding="2px",
                    align_items="center"
                ),
                rx.spacer(),
                rx.text("₹", (item["price"].to(int) * item["qty"].to(int)).to(str), weight="bold", size="3", color="#10b981"),
                width="100%",
                align_items="center"
            ),
            spacing="1",
            align_items="start",
            flex_grow="1"
        ),
        rx.icon_button(
            rx.icon(tag="trash-2", size=16),
            variant="ghost",
            color_scheme="red",
            on_click=lambda: CartState.remove(item),
            _hover={"bg": "#fee2e2"}
        ),
        width="100%",
        padding="1rem",
        bg="white",
        border_radius="1rem",
        border="1px solid #f3f4f6",
        spacing="3",
        align_items="center",
        _hover={"border_color": "#10b981"}
    )

def cart_sidebar():
    return rx.drawer.root(
        rx.drawer.overlay(bg="rgba(0,0,0,0.4)", backdrop_filter="blur(4px)"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Shopping Cart", size="6", color="#111827"),
                            rx.text(f"{CartState.total_items} items in your cart", size="2", color="#6b7280"),
                            spacing="0",
                            align_items="start"
                        ),
                        rx.spacer(),
                        rx.drawer.close(
                            rx.icon_button(
                                rx.icon(tag="x", size=20),
                                variant="ghost",
                                color="#111827",
                                _hover={"bg": "#f3f4f6"}
                            )
                        ),
                        width="100%",
                        padding="1.5rem 2rem",
                        border_bottom="1px solid #f3f4f6",
                        align_items="center"
                    ),
                    
                    # Content
                    rx.scroll_area(
                        rx.vstack(
                            rx.cond(
                                CartState.total_items == 0,
                                rx.center(
                                    rx.vstack(
                                        rx.box(
                                            rx.icon(tag="shopping-bag", size=60, color="#d1d5db"),
                                            padding="2rem",
                                            bg="#f9fafb",
                                            border_radius="full"
                                        ),
                                        rx.text("Your cart is feeling lonely", weight="bold", size="4", color="#111827"),
                                        rx.text("Add some items to get started!", color="#6b7280"),
                                        rx.button(
                                            "Start Shopping",
                                            on_click=CartState.toggle_cart,
                                            variant="solid",
                                            bg="#10b981",
                                            color="white",
                                            radius="full",
                                            margin_top="1rem"
                                        ),
                                        spacing="3",
                                        padding="4rem 0"
                                    ),
                                    width="100%"
                                ),
                                rx.foreach(CartState.cart, cart_item)
                            ),
                            spacing="4",
                            padding="1.5rem 2rem"
                        ),
                        height="calc(100vh - 280px)",
                        width="100%"
                    ),

                    # Footer
                    rx.vstack(
                        rx.divider(),
                        rx.vstack(
                            rx.hstack(
                                rx.text("Subtotal", color="#374151"),
                                rx.spacer(),
                                rx.text("₹", CartState.total, ".00", weight="bold", size="4", color="#111827"),
                                width="100%"
                            ),
                            rx.hstack(
                                rx.text("Shipping", color="#374151"),
                                rx.spacer(),
                                rx.text("Calculated at checkout", color="#6b7280", size="2"),
                                width="100%"
                            ),
                            spacing="2",
                            width="100%",
                            padding="1rem 0"
                        ),
                        rx.button(
                            rx.hstack(
                                rx.text("Proceed to Checkout"),
                                rx.spacer(),
                                rx.text("₹", CartState.total, ".00"),
                                width="100%",
                                align_items="center"
                            ),
                            width="100%",
                            size="4",
                            bg="#10b981",
                            color="white",
                            radius="large",
                            on_click=lambda: rx.redirect("/checkout"),
                            disabled=CartState.total_items == 0,
                            _hover={"bg": "#059669", "transform": "translateY(-2px)"},
                            transition="all 0.2s"
                        ),
                        rx.button(
                            "Continue Shopping",
                            variant="ghost",
                            width="100%",
                            color="#6b7280",
                            on_click=CartState.toggle_cart,
                            _hover={"bg": "transparent", "color": "#111827"}
                        ),
                        spacing="4",
                        padding="1.5rem 2rem",
                        width="100%",
                        bg="white",
                        border_top="1px solid #f3f4f6"
                    ),
                    height="100vh",
                    bg="white",
                    spacing="0"
                ),
                top="0",
                right="0",
                width="450px",
                height="100vh",
                bg="white",
                box_shadow="-10px 0 15px -3px rgba(0,0,0,0.1)"
            )
        ),
        open=CartState.is_open,
        on_open_change=CartState.set_is_open,
        direction="right"
    )
