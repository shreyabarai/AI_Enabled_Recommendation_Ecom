import reflex as rx
from ..state.product_state import ProductState
from ..components.product_card import product_card
from ..components.navbar import navbar
from ..components.footer import footer

def wishlist():
    return rx.box(
        navbar(),
        rx.vstack(
            rx.vstack(
                rx.heading("My Wishlist", size="9", weight="bold", color="#111827"),
                rx.text("Keep track of the products you love", color="#374151"),
                align_items="start",
                spacing="2",
                padding="4rem 4rem 2rem 4rem"
            ),
            
            rx.cond(
                ProductState.wishlist.length() == 0,
                rx.center(
                    rx.vstack(
                        rx.icon(tag="heart", size=60, color="#d1d5db"),
                        rx.text("Your wishlist is empty.", size="5", color="#6b7280"),
                        rx.button(
                            "Continue Shopping",
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
                    rx.foreach(ProductState.wishlist, product_card),
                    columns="4",
                    spacing="6",
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
