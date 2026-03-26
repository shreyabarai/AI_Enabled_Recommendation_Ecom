import reflex as rx

def footer():
    return rx.box(
        rx.text("© 2026 AI Recommendation System"),
        text_align="center",
        padding="10px",
        bg="lightgray"
    )