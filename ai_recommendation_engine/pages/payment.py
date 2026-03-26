import reflex as rx

class PaymentState(rx.State):
    success: bool = True  # default

def payment_status():
    return rx.center(
        rx.vstack(
            rx.heading("Payment Status"),

            rx.cond(
                PaymentState.success,
                rx.text("✅ Payment Successful"),
                rx.text("❌ Payment Failed")
            ),

            rx.text("Your order will arrive in 3-5 days 🚚"),

            rx.button(
                "Go Home",
                on_click=lambda: rx.redirect("/home")
            ),

            spacing="4"
        ),
        height="100vh"
    )