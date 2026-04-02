import reflex as rx
from ..state.user_state import UserState
from ..state.product_state import ProductState

class LoginState(rx.State):
    def login(self):
        # Mock login
        return [ProductState.load_products, rx.redirect("/home")]

def login():
    return rx.box(
        rx.hstack(
            # Left side: Image/Branding
            rx.vstack(
                rx.box(
                    rx.icon(tag="shopping-bag", size=40, color="white"),
                    padding="1rem",
                    bg="#10b981",
                    border_radius="1.5rem",
                    margin_bottom="2rem"
                ),
                rx.heading("ShopHub AI", size="9", weight="bold", color="white"),
                rx.text("Your personalized shopping destination powered by intelligent recommendations.", size="4", color="rgba(255,255,255,0.8)", text_align="center", max_width="400px"),
                width="50%",
                height="100vh",
                bg="#111827",
                padding="4rem",
                align_items="center",
                justify_content="center",
                display=rx.cond(rx.breakpoints({"sm": "none", "md": "flex"}), "flex", "none")
            ),
            
            # Right side: Form
            rx.vstack(
                rx.vstack(
                    rx.heading("Welcome Back", size="8", weight="bold", color="#111827"),
                    rx.text("Enter your credentials to access your account", color="#6b7280", size="3"),
                    align_items="start",
                    spacing="2",
                    margin_bottom="3rem"
                ),
                
                rx.vstack(
                    rx.vstack(
                        rx.text("Email Address", size="2", weight="medium", color="#374151"),
                        rx.input(
                            placeholder="name@example.com",
                            on_change=UserState.set_email,
                            width="100%",
                            size="3",
                            radius="large",
                            bg="#f9fafb"
                        ),
                        spacing="2",
                        width="100%",
                        align_items="start"
                    ),
                    rx.vstack(
                        rx.text("Password", size="2", weight="medium", color="#374151"),
                        rx.input(
                            placeholder="••••••••",
                            type="password",
                            on_change=UserState.set_password,
                            width="100%",
                            size="3",
                            radius="large",
                            bg="#f9fafb"
                        ),
                        spacing="2",
                        width="100%",
                        align_items="start",
                        margin_top="4"
                    ),
                    rx.button(
                        "Sign In",
                        on_click=LoginState.login,
                        width="100%",
                        size="4",
                        bg="#10b981",
                        color="white",
                        radius="large",
                        margin_top="6",
                        _hover={"bg": "#059669"}
                    ),
                    rx.hstack(
                        rx.text("Don't have an account?", color="#6b7280", size="2"),
                        rx.link("Create Account", href="/signup", color="#10b981", weight="bold", size="2"),
                        spacing="2",
                        margin_top="4"
                    ),
                    width="100%",
                    max_width="400px"
                ),
                width=rx.cond(rx.breakpoints({"sm": "100%", "md": "50%"}), "100%", "50%"),
                height="100vh",
                padding="4rem",
                align_items="center",
                justify_content="center",
                bg="white"
            ),
            width="100%",
            spacing="0"
        ),
        on_mount=ProductState.load_products,
        width="100%",
        height="100vh",
        overflow="hidden"
    )