import reflex as rx
from ai_recommendation_engine.state.product_state import ProductState
from ai_recommendation_engine.state.cart_state import CartState
from ai_recommendation_engine.components.navbar import navbar

def product_details():
    p = ProductState.selected_product

    return rx.vstack(
        navbar(),

        rx.hstack(
            rx.image(src=p["image"], width="400px"),

            rx.vstack(
                rx.heading(p["name"]),
                rx.text(p["desc"]),
                rx.text(f"₹{p['price']}"),

                rx.button(
                    "Add to Cart",
                    on_click=lambda: CartState.add(p)
                )
            ),
            spacing="8"
        ),
        padding="2em"
    )