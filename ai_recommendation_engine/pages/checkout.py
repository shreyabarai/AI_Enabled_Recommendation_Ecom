import reflex as rx
from ai_recommendation_engine.state.cart_state import CartState

def checkout():
    return rx.center(
        rx.vstack(
            rx.heading("Checkout"),
            rx.text(f"Total: ₹{CartState.total}"),

            rx.html(f"""
            <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
            <button id="pay-btn">Pay Now</button>

            <script>
            document.getElementById('pay-btn').onclick = function(e){{
                var options = {{
                    "key": "YOUR_KEY",
                    "amount": "{CartState.total * 100}",
                    "currency": "INR",
                    "name": "AI Store",
                    "handler": function (){{
                        window.location.href = "/payment-status?success=true";
                    }},
                    "modal": {{
                        "ondismiss": function(){{
                            window.location.href = "/payment-status?success=false";
                        }}
                    }}
                }};
                var rzp = new Razorpay(options);
                rzp.open();
                e.preventDefault();
            }}
            </script>
            """)
        )
    )