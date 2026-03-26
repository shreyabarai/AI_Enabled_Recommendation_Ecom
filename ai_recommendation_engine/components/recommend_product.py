import reflex as rx

def recommend_product(name):
    return rx.box(
        rx.text(name),
        border="1px solid green",
        padding="10px",
        border_radius="10px"
    )