import reflex as rx
from ai_recommendation_engine.components.product_card import product_card
from ai_recommendation_engine.state.product_state import ProductState
from ai_recommendation_engine.components.navbar import navbar

def products():
    return rx.vstack(
        navbar(),

        rx.heading("All Products", size="7"),

        rx.grid(
            rx.foreach(ProductState.filtered_products, product_card),
            columns="4",
            spacing="6"
        ),
        padding="2em"
    )