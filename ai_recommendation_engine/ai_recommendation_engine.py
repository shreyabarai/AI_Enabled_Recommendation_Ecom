import reflex as rx

from ai_recommendation_engine.pages.login import login
from ai_recommendation_engine.pages.home import home
from ai_recommendation_engine.pages.products import products
from ai_recommendation_engine.pages.product_details import product_details
from ai_recommendation_engine.pages.cart import cart
from ai_recommendation_engine.pages.wishlist import wishlist
from ai_recommendation_engine.pages.checkout import checkout
from ai_recommendation_engine.pages.payment import payment, PaymentState

from ai_recommendation_engine.state.product_state import ProductState

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="teal",
    ),
)

app.add_page(login, route="/")
app.add_page(home, route="/home", on_load=ProductState.load_products)
app.add_page(products, route="/products")
app.add_page(product_details, route="/product-details", on_load=ProductState.load_product_by_id)
app.add_page(cart, route="/cart")
app.add_page(wishlist, route="/wishlist")
app.add_page(checkout, route="/checkout")
app.add_page(payment, route="/payment", on_load=PaymentState.on_load)