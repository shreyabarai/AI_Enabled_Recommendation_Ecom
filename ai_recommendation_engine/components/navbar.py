import reflex as rx
from ..state.theme_state import ThemeState
from ..state.cart_state import CartState

def navbar():
    return rx.hstack(
        rx.heading("🛍 AI Shop", size="6"),

        rx.input(
            placeholder="Search...",
            width="40%",
            border_radius="20px"
        ),

        rx.hstack(
            rx.link("Home", href="/"),
            rx.link("Products", href="/products"),

            rx.box(
                rx.link("Cart", href="/cart"),
                rx.badge(CartState.total_items),
            ),

            rx.link("Profile", href="/profile"),
        ),

        rx.button(
            rx.cond(ThemeState.dark_mode, "🌙", "☀️"),
            on_click=ThemeState.toggle_theme
        ),

        justify="between",
        width="100%",
        padding="15px",
        bg="rgba(30,41,59,0.6)",
        backdrop_filter="blur(10px)",
        border_radius="12px"
    )