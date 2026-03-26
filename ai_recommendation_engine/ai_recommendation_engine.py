import reflex as rx

from ai_recommendation_engine.pages.login import login
from ai_recommendation_engine.pages.home import home
from ai_recommendation_engine.pages.products import products
from ai_recommendation_engine.pages.product_details import product_details
from ai_recommendation_engine.pages.cart import cart
from ai_recommendation_engine.pages.checkout import checkout
from ai_recommendation_engine.pages.payment import payment_status

from ai_recommendation_engine.state.product_state import ProductState

app = rx.App()

# Load data once
ProductState.load_products()
ProductState.recommend()

app.add_page(login, route="/")
app.add_page(home, route="/home")
app.add_page(products, route="/products")
app.add_page(product_details, route="/product-details")
app.add_page(cart, route="/cart")
app.add_page(checkout, route="/checkout")
app.add_page(payment_status, route="/payment-status")