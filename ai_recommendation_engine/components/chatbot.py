import reflex as rx

def chatbot():
    return rx.box(
        rx.vstack(
            rx.heading("💬 Shopping Assistant"),

            rx.box(
                rx.text("Hi 👋 how can I help you shop!"),
                height="400px",
                width="100%",
                bg="#1e293b",
                padding="10px",
                border_radius="10px"
            ),

            rx.input(placeholder="Ask something..."),

            rx.button("Send", width="100%"),

        ),

        width="300px",
        height="100vh",
        padding="15px",
        bg="#020617",
        border_right="1px solid #334155",
        position="sticky",
        top="0"
    )