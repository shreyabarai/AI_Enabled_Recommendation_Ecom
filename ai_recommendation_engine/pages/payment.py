import reflex as rx
from ai_recommendation_engine.components.navbar import navbar
from ai_recommendation_engine.components.footer import footer

class PaymentState(rx.State):
    payment_success: bool = False

    def on_load(self):
        """Check query parameters for payment status."""
        query_params = self.router.page.params
        status = query_params.get("success")
        if status == "true":
            self.payment_success = True
        else:
            self.payment_success = False

def payment():
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.box(
                    rx.cond(
                        PaymentState.payment_success,
                        rx.vstack(
                            rx.box(
                                rx.icon(tag="circle-check", size=80, color="#10b981"),
                                padding="2rem",
                                bg="#f0fdf4",
                                border_radius="full"
                            ),
                            rx.heading("Payment Successful!", size="9", weight="bold", color="#111827", margin_top="2rem"),
                            rx.text("Thank you for your purchase. Your order is being processed and will be delivered shortly.", color="#6b7280", text_align="center", size="4"),
                            rx.vstack(
                                rx.hstack(rx.text("Order ID:", color="#6b7280"), rx.text("#SH-98231", weight="bold"), spacing="2"),
                                rx.hstack(rx.text("Delivery Expectation:", color="#6b7280"), rx.text("3-5 Business Days", weight="bold"), spacing="2"),
                                margin_top="2rem",
                                spacing="2",
                                align_items="center"
                            ),
                            spacing="4",
                            align_items="center"
                        ),
                        rx.vstack(
                            rx.box(
                                rx.icon(tag="circle-x", size=80, color="#ef4444"),
                                padding="2rem",
                                bg="#fef2f2",
                                border_radius="full"
                            ),
                            rx.heading("Payment Failed", size="9", weight="bold", color="#111827", margin_top="2rem"),
                            rx.text("Something went wrong with your transaction. Please check your payment details and try again.", color="#6b7280", text_align="center", size="4"),
                            spacing="4",
                            align_items="center"
                        )
                    ),
                    bg="white",
                    padding="5rem",
                    border_radius="3rem",
                    box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1)",
                    max_width="700px",
                    width="100%",
                    text_align="center",
                    border="1px solid #f3f4f6"
                ),
                rx.hstack(
                    rx.button(
                        "Download Invoice",
                        variant="outline",
                        color="#111827",
                        border="1px solid #e5e7eb",
                        size="4",
                        radius="full",
                        padding="0 2rem"
                    ),
                    rx.button(
                        "Continue Shopping",
                        on_click=lambda: rx.redirect("/home"),
                        size="4",
                        bg="#10b981",
                        color="white",
                        radius="full",
                        padding="0 2rem",
                        _hover={"bg": "#059669", "transform": "scale(1.05)"}
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