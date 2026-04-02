import reflex as rx
from ..state.theme_state import ThemeState
from ..state.cart_state import CartState
from ..state.product_state import ProductState

def navbar():
    return rx.hstack(
        # Logo
        rx.hstack(
            rx.icon(tag="shopping-bag", color="#10b981", size=30),
            rx.heading("ShopHub", size="7", weight="bold", color="#1f2937"),
            spacing="2",
            align_items="center",
            cursor="pointer",
            on_click=lambda: rx.redirect("/home")
        ),

        # Search Bar
        rx.hstack(
            rx.input(
                placeholder="What are you looking for today?",
                value=ProductState.search_query,
                on_change=ProductState.set_search_query,
                on_key_down=ProductState.handle_search_key,
                width="100%",
                variant="soft",
                radius="full",
                padding_left="1rem",
                bg="white",
                border="1px solid #e5e7eb"
            ),
            rx.icon_button(
                rx.icon(tag="search", size=20),
                on_click=ProductState.handle_search,
                color_scheme="teal",
                radius="full",
                variant="solid",
                bg="#10b981",
                cursor="pointer"
            ),
            width="50%",
            spacing="0",
            position="relative"
        ),

        # Right Icons
        rx.hstack(
            rx.icon_button(
                rx.icon(tag=rx.cond(ThemeState.dark_mode, "sun", "moon"), size=20),
                variant="ghost",
                color="#1f2937",
                on_click=ThemeState.toggle_theme,
                cursor="pointer"
            ),
            rx.box(
                rx.icon_button(
                    rx.icon(tag="heart", size=20),
                    variant="ghost",
                    color="#1f2937",
                    cursor="pointer",
                    on_click=lambda: rx.redirect("/wishlist")
                ),
                rx.cond(
                    ProductState.wishlist.length() > 0,
                    rx.badge(
                        ProductState.wishlist.length(),
                        color_scheme="red",
                        variant="solid",
                        radius="full",
                        position="absolute",
                        top="-2px",
                        right="-2px",
                        size="1"
                    )
                ),
                position="relative"
            ),
            rx.icon_button(
                rx.icon(tag="log-out", size=20),
                variant="ghost",
                color="#1f2937",
                on_click=lambda: rx.redirect("/login"),
                cursor="pointer"
            ),
            rx.box(
                rx.icon_button(
                    rx.icon(tag="shopping-cart", size=20),
                    variant="ghost",
                    color="#1f2937",
                    cursor="pointer",
                    on_click=CartState.toggle_cart
                ),
                rx.badge(
                    CartState.total_items,
                    color_scheme="orange",
                    variant="solid",
                    radius="full",
                    position="absolute",
                    top="-2px",
                    right="-2px",
                    size="1"
                ),
                position="relative"
            ),
            spacing="4"
        ),

        justify="between",
        width="100%",
        padding="1rem 4rem",
        bg="white",
        border_bottom="1px solid #f3f4f6",
        position="sticky",
        top="0",
        z_index="100"
    )