from ..state.user_state import UserState
from ..components.navbar import navbar
from ..components.footer import footer

def profile_item(label, value, icon):
    return rx.hstack(
        rx.box(
            rx.icon(tag=icon, size=20, color="#10b981"),
            padding="1rem",
            bg="#f0fdf4",
            border_radius="1rem"
        ),
        rx.vstack(
            rx.text(label, size="2", color="#6b7280"),
            rx.text(value, weight="bold", color="#111827", size="4"),
            spacing="0",
            align_items="start"
        ),
        spacing="4",
        padding="1.5rem",
        bg="white",
        border="1px solid #f3f4f6",
        border_radius="1.5rem",
        width="100%",
        align_items="center"
    )

def profile():
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.vstack(
                    rx.box(
                        rx.image(src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix", width="120px", height="120px", border_radius="full"),
                        padding="4px",
                        border="4px solid #10b981",
                        border_radius="full"
                    ),
                    rx.heading(UserState.user_id, size="8", weight="bold", color="#111827", margin_top="4"),
                    rx.badge("Premium Member", color_scheme="teal", variant="soft", radius="full"),
                    align_items="center",
                    spacing="2",
                    margin_bottom="4rem"
                ),

                rx.grid(
                    profile_item("User ID", UserState.user_id, "user"),
                    profile_item("Email Address", UserState.email, "mail"),
                    profile_item("Default Language", "English (US)", "globe"),
                    profile_item("Account Status", "Active", "shield-check"),
                    columns="2",
                    spacing="4",
                    width="100%",
                    max_width="800px"
                ),

                rx.hstack(
                    rx.button(
                        "Edit Profile",
                        variant="outline",
                        color="#111827",
                        border="1px solid #e5e7eb",
                        size="4",
                        radius="full",
                        width="200px"
                    ),
                    rx.button(
                        "Logout",
                        on_click=UserState.logout,
                        size="4",
                        bg="#ef4444",
                        color="white",
                        radius="full",
                        width="200px",
                        _hover={"bg": "#dc2626"}
                    ),
                    spacing="4",
                    margin_top="4rem"
                ),
                
                spacing="0",
                padding="6rem 2rem",
                width="100%",
                align_items="center"
            ),
            width="100%",
            bg="#f9fafb",
            min_height="calc(100vh - 80px)"
        ),
        footer()
    )