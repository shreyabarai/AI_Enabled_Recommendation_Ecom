import reflex as rx
import pandas as pd
import random
from ai_recommendation_engine.backend.content_based import get_user_recommendations
from typing import List, Dict

class ProductState(rx.State):
    products: List[Dict] = []
    recommended: List[Dict] = []
    selected_product: Dict = {}
    user_history: List[str] = []
    
    def load_products(self):
        df = pd.read_csv("clean_data.csv")

        self.products = [
        {
            "id": i,
            "name": str(row["Name"]),               # ✅ FIXED
            "image": str(row["ImageURL"]),          # ✅ FIXED
            "desc": str(row.get("Description", "")),
            "price": random.randint(300, 2000)
        }
        for i, row in df.iterrows()
    ]

    def set_product(self, product):
        self.selected_product = product

        # 🔥 track view
        self.user_history = self.user_history + [product["name"]]

        return rx.redirect("/product-details")

    def recommend(self):
        self.recommended = get_user_recommendations(self.user_history)