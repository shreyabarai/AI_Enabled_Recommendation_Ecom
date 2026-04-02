import reflex as rx
from ai_recommendation_engine.state.cart_state import CartState
from ai_recommendation_engine.components.navbar import navbar
from ai_recommendation_engine.components.footer import footer

def checkout():
    return rx.box(
        navbar(),
        rx.script(src="https://checkout.razorpay.com/v1/checkout.js"),
        rx.html("""
            <script>
            function openRazorpay(amount) {
                var options = {
                    "key": "rzp_test_SYhaPo3DvVky0n",
                    "amount": amount,
                    "currency": "INR",
                    "name": "ShopHub",
                    "description": "Premium E-commerce Purchase",
                    "handler": function (response){
                        window.location.href = "/payment?success=true";
                    },
                    "modal": {
                        "ondismiss": function(){
                            window.location.href = "/payment?success=false";
                        }
                    },
                    "theme": {
                        "color": "#10b981"
                    }
                };
                var rzp = new Razorpay(options);
                rzp.open();
            }
            </script>
        """),
        rx.center(
            rx.vstack(
                rx.vstack(
                    rx.heading("Checkout", size="9", weight="bold", color="#111827"),
                    rx.text("Securely complete your purchase", color="#6b7280", size="3"),
                    align_items="center",
                    spacing="2",
                    margin_bottom="4rem"
                ),

                rx.grid(
                    # Left: Shipping Info Form
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.heading("Shipping Information", size="5", weight="bold", color="#111827", margin_bottom="1.5rem"),
                                rx.grid(
                                    rx.vstack(rx.text("First Name", size="2", weight="medium"), rx.input(placeholder="John", radius="large", bg="#f9fafb", width="100%"), spacing="2", align_items="start"),
                                    rx.vstack(rx.text("Last Name", size="2", weight="medium"), rx.input(placeholder="Doe", radius="large", bg="#f9fafb", width="100%"), spacing="2", align_items="start"),
                                    columns="2",
                                    spacing="4",
                                    width="100%"
                                ),
                                rx.vstack(rx.text("Email Address", size="2", weight="medium"), rx.input(placeholder="john@example.com", radius="large", bg="#f9fafb", width="100%"), spacing="2", align_items="start", margin_top="4"),
                                rx.vstack(rx.text("Phone Number", size="2", weight="medium"), rx.input(placeholder="+91 98765 43210", radius="large", bg="#f9fafb", width="100%"), spacing="2", align_items="start", margin_top="4"),
                                rx.vstack(rx.text("Shipping Address", size="2", weight="medium"), rx.text_area(placeholder="123, Main Street, Area, City", radius="large", bg="#f9fafb", width="100%", height="100px"), spacing="2", align_items="start", margin_top="4"),
                                width="100%",
                                padding="2.5rem",
                                bg="white",
                                border_radius="2rem",
                                box_shadow="0 4px 6px -1px rgba(0,0,0,0.05)",
                                border="1px solid #f3f4f6"
                            ),
                            width="100%"
                        ),
                        width="100%"
                    ),

                    # Right: Order Summary
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.heading("Order Summary", size="5", weight="bold", color="#111827", margin_bottom="1.5rem"),
                                rx.scroll_area(
                                    rx.vstack(
                                        rx.foreach(
                                            CartState.cart,
                                            lambda item: rx.hstack(
                                                rx.image(src=item["image"], width="60px", height="60px", object_fit="cover", border_radius="lg"),
                                                rx.vstack(
                                                    rx.text(item["name"], weight="bold", size="2", line_clamp=1),
                                                    rx.text("Qty: ", item["qty"], " • ₹", item["price"], size="1", color="#6b7280"),
                                                    spacing="0",
                                                    align_items="start"
                                                ),
                                                rx.spacer(),
                                                rx.text("₹", item["price"].to(int) * item["qty"].to(int), weight="bold", size="2"),
                                                width="100%",
                                                padding="0.75rem 0",
                                                border_bottom="1px solid #f3f4f6"
                                            )
                                        ),
                                        spacing="0",
                                        width="100%"
                                    ),
                                    height="300px",
                                    width="100%"
                                ),
                                rx.vstack(
                                    rx.hstack(rx.text("Subtotal", color="#6b7280"), rx.spacer(), rx.text("₹", CartState.total, ".00", weight="medium"), width="100%"),
                                    rx.hstack(rx.text("Shipping", color="#6b7280"), rx.spacer(), rx.text("FREE", color="#10b981", weight="bold"), width="100%"),
                                    rx.divider(margin_top="1rem", margin_bottom="1rem"),
                                    rx.hstack(rx.text("Total Amount", weight="bold", size="5"), rx.spacer(), rx.text("₹", CartState.total, ".00", weight="bold", size="6", color="#10b981"), width="100%"),
                                    width="100%",
                                    padding_top="1rem"
                                ),
                                
                                # Payment Button
                                rx.button(
                                    "Pay Securely with Razorpay",
                                    on_click=rx.call_script(f"openRazorpay({CartState.total * 100})"),
                                    width="100%",
                                    size="4",
                                    bg="#10b981",
                                    color="white",
                                    radius="full",
                                    margin_top="2rem",
                                    font_weight="bold",
                                    _hover={"bg": "#059669", "transform": "translateY(-2px)"},
                                    transition="all 0.2s",
                                    box_shadow="0 10px 15px -3px rgba(16, 185, 129, 0.3)"
                                ),
                                
                                width="100%",
                                padding="2.5rem",
                                bg="white",
                                border_radius="2rem",
                                box_shadow="0 4px 6px -1px rgba(0,0,0,0.05)",
                                border="1px solid #f3f4f6"
                            ),
                            width="100%"
                        ),
                        width="100%"
                    ),
                    columns="2",
                    spacing="8",
                    width="100%",
                    max_width="1200px"
                ),
                
                spacing="0",
                padding="4rem",
                width="100%",
                align_items="center"
            ),
            width="100%",
            bg="#f9fafb",
            min_height="calc(100vh - 80px)"
        ),
        footer()
    )