import reflex as rx
from ..state.user_state import UserState

def signup():
    return rx.vstack(
        rx.heading("Signup"),

        rx.input(placeholder="Email", on_change=UserState.set_email),
        rx.input(placeholder="Password", type="password", on_change=UserState.set_password),

        rx.button("Signup", on_click=UserState.signup)
    )