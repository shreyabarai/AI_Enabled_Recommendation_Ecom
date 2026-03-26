import reflex as rx
from typing import Dict


class CartState(rx.State):
    # ✅ typed cart (IMPORTANT)
    cart: list = []

    def add(self, item: dict):
        for cart_item in self.cart:
            if cart_item["name"] == item["name"]:
                cart_item["qty"] += 1
                return
        self.cart.append({**item, "qty": 1})


    def increase(self, item: dict):
        for cart_item in self.cart:
            if cart_item["name"] == item["name"]:
                cart_item["qty"] += 1


    def decrease(self, item: dict):
        for cart_item in self.cart:
            if cart_item["name"] == item["name"]:
                if cart_item["qty"] > 1:
                    cart_item["qty"] -= 1
                else:
                    self.cart.remove(cart_item)


    def remove(self, item: dict):
        self.cart = [
            cart_item for cart_item in self.cart
            if cart_item["name"] != item["name"]
        ]

    @rx.var
    def total(self) -> int:
        return sum(item["price"] * item["qty"] for item in self.cart.values())

    # ✅ ADD THIS (fixes your error)
    @rx.var
    def total_items(self) -> int:
        return sum(item["qty"] for item in self.cart.values())
    
