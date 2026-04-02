import reflex as rx
from ..state.product_state import ProductState
from ..state.cart_state import CartState
from ..components.navbar import navbar

from ..components.footer import footer
from ..components.product_card import product_card

def product_details():
    p = ProductState.selected_product
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                # Breadcrumbs
                rx.hstack(
                    rx.link("Home", href="/home", color="#6b7280", size="2"),
                    rx.text("/", color="#d1d5db", size="2"),
                    rx.link(p["category"], href="/home", color="#6b7280", size="2"),
                    rx.text("/", color="#d1d5db", size="2"),
                    rx.text(p["name"], color="#111827", size="2", weight="medium"),
                    spacing="2",
                    width="100%",
                    margin_bottom="2rem"
                ),
                
                # Main Product Layout
                rx.grid(
                    # Left: Image Gallery
                    rx.vstack(
                        rx.box(
                            rx.image(src=p["image"], width="100%", height="500px", object_fit="cover", border_radius="2rem"),
                            position="relative",
                            overflow="hidden",
                            box_shadow="0 10px 15px -3px rgba(0,0,0,0.1)"
                        ),
                        rx.hstack(
                            rx.box(
                                rx.image(src=p["image"], width="100px", height="100px", object_fit="cover", border_radius="1rem"),
                                cursor="pointer",
                                border="2px solid transparent",
                                _hover={"border_color": "#10b981"}
                            ),
                            rx.box(
                                rx.image(src=p["image"], width="100px", height="100px", object_fit="cover", border_radius="1rem"),
                                cursor="pointer",
                                border="2px solid transparent",
                                _hover={"border_color": "#10b981"}
                            ),
                            rx.box(
                                rx.image(src=p["image"], width="100px", height="100px", object_fit="cover", border_radius="1rem"),
                                cursor="pointer",
                                border="2px solid transparent",
                                _hover={"border_color": "#10b981"}
                            ),
                            rx.box(
                                rx.image(src=p["image"], width="100px", height="100px", object_fit="cover", border_radius="1rem"),
                                cursor="pointer",
                                border="2px solid transparent",
                                _hover={"border_color": "#10b981"}
                            ),
                            spacing="4",
                            margin_top="1rem"
                        ),
                        width="100%"
                    ),
                    
                    # Right: Product Info
                    rx.vstack(
                        rx.badge(p["badge_text"], color_scheme="teal", variant="solid", radius="full", size="2"),
                        rx.heading(p["name"], size="9", weight="bold", color="#111827", margin_top="1rem"),
                        
                        rx.hstack(
                            rx.hstack(
                                rx.icon(tag="star", size=18, fill="#f59e0b", color="#f59e0b"),
                                rx.icon(tag="star", size=18, fill="#f59e0b", color="#f59e0b"),
                                rx.icon(tag="star", size=18, fill="#f59e0b", color="#f59e0b"),
                                rx.icon(tag="star", size=18, fill="#f59e0b", color="#f59e0b"),
                                rx.icon(tag="star", size=18, fill="#f59e0b", color="#f59e0b"),
                                spacing="1"
                            ),
                            rx.text(p["rating"], weight="bold", color="#111827"),
                            rx.text("(", p["reviews"], " Reviews)", color="#6b7280"),
                            spacing="3",
                            align_items="center",
                            margin_top="0.5rem"
                        ),
                        
                        rx.divider(margin_top="2rem", margin_bottom="2rem"),
                        
                        rx.vstack(
                            rx.hstack(
                                rx.text("₹", p["price"], size="9", weight="bold", color="#10b981"),
                                rx.text("₹", (p["price"].to(int) * 1.3).to(int), text_decoration="line-through", color="#9ca3af", size="4"),
                                rx.badge("-30%", color_scheme="red", variant="soft", size="2"),
                                align_items="baseline",
                                spacing="4"
                            ),
                            rx.text("Inclusive of all taxes", color="#6b7280", size="2"),
                            align_items="start"
                        ),
                        
                        rx.text(
                            rx.cond(
                                p["desc"],
                                p["desc"],
                                "No description available for this product."
                            ),
                            color="#374151",
                            line_height="1.8",
                            margin_top="2rem"
                        ),
                        
                        rx.hstack(
                            rx.button(
                                rx.hstack(rx.icon(tag="shopping-cart"), rx.text("Add to Cart")),
                                on_click=lambda: CartState.add_to_cart(p),
                                size="4",
                                bg="white",
                                color="#10b981",
                                border="2px solid #10b981",
                                radius="full",
                                width="100%",
                                _hover={"bg": "#f0fdf4"}
                            ),
                            rx.button(
                                "Buy Now",
                                on_click=lambda: [CartState.add_to_cart(p), rx.redirect("/checkout")],
                                size="4",
                                bg="#10b981",
                                color="white",
                                radius="full",
                                width="100%",
                                _hover={"bg": "#059669", "transform": "scale(1.02)"},
                                transition="all 0.2s"
                            ),
                            spacing="4",
                            width="100%",
                            margin_top="3rem"
                        ),
                        
                        rx.vstack(
                            rx.hstack(rx.icon(tag="truck", size=18), rx.text("Free Delivery on orders above ₹500", size="2"), spacing="3"),
                            rx.hstack(rx.icon(tag="rotate-ccw", size=18), rx.text("7 Days easy return policy", size="2"), spacing="3"),
                            rx.hstack(rx.icon(tag="shield-check", size=18), rx.text("100% Authentic Products", size="2"), spacing="3"),
                            align_items="start",
                            spacing="3",
                            margin_top="3rem",
                            color="#4b5563"
                        ),
                        
                        align_items="start",
                        width="100%",
                        padding_left="4rem"
                    ),
                    columns="2",
                    width="100%"
                ),
                
                # Similar Products Section
                rx.vstack(
                    rx.heading("Similar Products", size="7", weight="bold", color="#111827", margin_top="6rem", margin_bottom="2rem"),
                    rx.grid(
                        rx.foreach(ProductState.recommended, product_card),
                        columns="4",
                        spacing="6",
                        width="100%"
                    ),
                    width="100%",
                    align_items="start"
                ),
                
                padding="4rem",
                max_width="1400px",
                width="100%"
            ),
            width="100%",
            bg="white"
        ),
        footer()
    )