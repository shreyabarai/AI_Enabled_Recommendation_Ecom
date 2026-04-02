import reflex as rx
from ai_recommendation_engine.state.product_state import ProductState
from ai_recommendation_engine.state.cart_state import CartState
import random

def product_card(product):
    # Calculations moved into state or done via Var expressions
    badge_color = rx.cond(
        product["badge_text"] == "DEAL", 
        "red", 
        rx.cond(product["badge_text"] == "BEST SELLER", "blue", "green")
    )
    
    # Calculate original price using Var expression
    original_price = product["price"].to(int) * 1.2
    
    # Check if in wishlist using the computed var
    is_in_wishlist = ProductState.wishlist_ids.contains(product["id"])

    return rx.box(
        rx.vstack(
            # Image Container with Badge
            rx.box(
                rx.image(
                    src=product["image"],
                    width="100%",
                    height="220px",
                    object_fit="cover",
                    border_radius="1rem",
                ),
                rx.badge(
                    product["badge_text"],
                    variant="solid",
                    color_scheme=badge_color,
                    position="absolute",
                    top="1rem",
                    left="1rem",
                    radius="medium",
                    size="1"
                ),
                rx.icon_button(
                    rx.icon(
                        tag="heart", 
                        size=18, 
                        fill=rx.cond(is_in_wishlist, "red", "none"),
                        color=rx.cond(is_in_wishlist, "red", "gray")
                    ),
                    variant="soft",
                    color_scheme=rx.cond(is_in_wishlist, "red", "gray"),
                    radius="full",
                    position="absolute",
                    top="1rem",
                    right="1rem",
                    bg="white",
                    on_click=ProductState.toggle_wishlist(product["id"]),
                    _hover={"color": "red", "transform": "scale(1.1)"},
                    transition="all 0.2s"
                ),
                # Buttons Overlay on Hover
                rx.box(
                    rx.vstack(
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="shopping-cart", size=18),
                                rx.text("Add to Cart"),
                                spacing="2"
                            ),
                            width="100%",
                            bg="#10b981",
                            color="white",
                            radius="full",
                            on_click=lambda: CartState.add_to_cart(product),
                            _hover={"bg": "#059669"}
                        ),
                        rx.button(
                            "View Details",
                            width="100%",
                            variant="outline",
                            bg="white",
                            color="#111827",
                            border="1px solid #e5e7eb",
                            radius="full",
                            on_click=lambda: ProductState.set_product(product),
                            _hover={"bg": "#f9fafb"}
                        ),
                        spacing="2",
                        width="90%"
                    ),
                    position="absolute",
                    bottom="1.5rem",
                    left="5%",
                    width="100%",
                    opacity="0",
                    _group_hover={"opacity": "1", "bottom": "2rem"},
                    transition="all 0.3s ease-out"
                ),
                position="relative",
                width="100%",
                overflow="hidden",
                role="group",
                border_radius="1rem"
            ),

            # Content
            rx.vstack(
                rx.text(
                    product["name"],
                    weight="bold",
                    size="3",
                    line_clamp=2,
                    height="3rem",
                    color="#111827"
                ),
                # Ratings
                rx.hstack(
                    rx.hstack(
                        rx.icon(tag="star", size=12, fill="#f59e0b", color="#f59e0b"),
                        rx.icon(tag="star", size=12, fill="#f59e0b", color="#f59e0b"),
                        rx.icon(tag="star", size=12, fill="#f59e0b", color="#f59e0b"),
                        rx.icon(tag="star", size=12, fill="#f59e0b", color="#f59e0b"),
                        rx.icon(tag="star", size=12, fill="#f59e0b", color="#f59e0b"),
                        spacing="1"
                    ),
                    rx.text(product["rating"], " (", product["reviews"], ")", size="1", color="#374151"),
                    align_items="center",
                    spacing="2"
                ),
                # Price
                rx.hstack(
                    rx.text("₹", product["price"], weight="bold", size="5", color="#111827"),
                    rx.text("₹", original_price.to(int), text_decoration="line-through", size="2", color="#4b5563"),
                    rx.badge("-", product["discount"], "%", variant="soft", color_scheme="red", size="1"),
                    align_items="center",
                    spacing="2"
                ),
                spacing="2",
                align_items="start",
                width="100%",
                padding_top="0.5rem"
            ),
            spacing="1",
            width="100%"
        ),
        padding="1rem",
        bg="white",
        border_radius="1.5rem",
        border="1px solid #f3f4f6",
        _hover={"box_shadow": "0 10px 15px -3px rgba(0,0,0,0.1)", "transform": "translateY(-4px)"},
        transition="all 0.3s",
        cursor="pointer",
        on_click=lambda: ProductState.set_product(product),
        width="100%"
    )
