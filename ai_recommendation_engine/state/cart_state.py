import reflex as rx
from typing import Dict, List, Any


class CartState(rx.State):
    # ✅ typed cart (IMPORTANT)
    cart: list[dict[str, Any]] = []
    is_open: bool = False

    def toggle_cart(self):
        self.is_open = not self.is_open

    def add_to_cart(self, item: dict):
        if not item: return
        self.is_open = True
        
        # Check if item already exists
        for i, cart_item in enumerate(self.cart):
            if cart_item["name"] == item["name"]:
                # Create a copy of the item and update qty
                new_item = cart_item.copy()
                new_item["qty"] += 1
                # Replace the old item in the list
                self.cart[i] = new_item
                # Re-assign to trigger update
                self.cart = self.cart
                return
        
        # Add new item
        new_item = item.copy()
        new_item["qty"] = 1
        self.cart = self.cart + [new_item]


    def increase(self, item: dict):
        for i, cart_item in enumerate(self.cart):
            if cart_item["name"] == item["name"]:
                new_item = cart_item.copy()
                new_item["qty"] += 1
                self.cart[i] = new_item
                self.cart = self.cart
                break


    def decrease(self, item: dict):
        for i, cart_item in enumerate(self.cart):
            if cart_item["name"] == item["name"]:
                if cart_item["qty"] > 1:
                    new_item = cart_item.copy()
                    new_item["qty"] -= 1
                    self.cart[i] = new_item
                    self.cart = self.cart
                else:
                    self.cart = [
                        ci for ci in self.cart 
                        if ci["name"] != item["name"]
                    ]
                break


    def remove(self, item: dict):
        self.cart = [
            cart_item for cart_item in self.cart
            if cart_item["name"] != item["name"]
        ]

    @rx.var
    def total(self) -> int:
        return sum(item["price"] * item["qty"] for item in self.cart)

    # ✅ ADD THIS (fixes your error)
    @rx.var
    def total_items(self) -> int:
        return sum(item["qty"] for item in self.cart)
    
