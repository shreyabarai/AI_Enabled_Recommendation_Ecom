import reflex as rx
from ai_recommendation_engine.state.product_state import ProductState
from ai_recommendation_engine.components.product_card import product_card
from ai_recommendation_engine.components.navbar import navbar

def home():
    return rx.vstack(
        navbar(),

        rx.heading("Recommended For You"),

        rx.button(
            "Load Products",
            on_click=lambda: [ProductState.load_products(), ProductState.recommend()]
        ),

        rx.grid(
            rx.foreach(ProductState.recommended, product_card),
            columns="4",
            spacing="6"
        )
    )