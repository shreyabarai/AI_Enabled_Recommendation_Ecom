import reflex as rx
from ai_recommendation_engine.state.product_state import ProductState

def product_card(product):
    return rx.box(
        rx.vstack(
            rx.image(src=product["image"], height="180px"),

            rx.text(product["name"], font_weight="bold"),
            rx.text(f"₹{product['price']}", color="green"),

            rx.button(
                "View Details",
                width="100%",
                on_click=lambda: ProductState.set_product(product)
            ),
        ),
        padding="1em",
        border_radius="15px",
        box_shadow="0 6px 20px rgba(0,0,0,0.1)",
        _hover={"transform": "scale(1.05)", "transition": "0.3s"}
    )
