import reflex as rx
from ai_recommendation_engine.state.user_state import UserState

def profile():
    return rx.vstack(
        rx.heading("👤 Profile"),

        rx.text(f"User ID: {UserState.user_id}"),
        rx.text(f"Email: {UserState.email}"),

        rx.button("Logout", on_click=UserState.logout)
    )