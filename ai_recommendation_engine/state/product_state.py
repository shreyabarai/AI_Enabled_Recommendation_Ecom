import reflex as rx
import pandas as pd
import random
from ai_recommendation_engine.backend.content_based import get_user_recommendations
from typing import List, Dict

class ProductState(rx.State):
    products: List[Dict] = [
        {
            "id": 0,
            "name": "Initial Loading...",
            "image": "",
            "desc": "Loading products from dataset",
            "category": "All",
            "price": 0,
            "rating": "0.0",
            "reviews": "0",
            "discount": "0",
            "badge_text": "LOADING",
        }
    ]
    recommended: List[Dict] = []
    popular: List[Dict] = []
    categories: List[str] = ["All"]
    selected_category: str = "All"
    search_query: str = ""
    selected_product: Dict = {}
    user_history: List[str] = []
    wishlist: List[Dict] = []
    is_loading: bool = False
    
    def toggle_wishlist(self, product_id: int):
        """Toggle a product in the wishlist by ID."""
        # Find product in self.products
        product = next((p for p in self.products if p["id"] == product_id), None)
        if not product:
            return

        if any(p["id"] == product_id for p in self.wishlist):
            self.wishlist = [p for p in self.wishlist if p["id"] != product_id]
        else:
            self.wishlist = self.wishlist + [product]

    @rx.var
    def wishlist_ids(self) -> List[int]:
        return [p["id"] for p in self.wishlist]

    def set_category(self, category: str):
        self.selected_category = category

    def set_search_query(self, query: str):
        self.search_query = query

    def handle_search(self):
        """Redirect to products page if searching from elsewhere, or just ensure search is active."""
        if self.search_query:
            return rx.redirect("/home") # Home now shows search results prominently
        return None

    def handle_search_key(self, key: str):
        """Handle Enter key press in search bar."""
        if key == "Enter":
            return self.handle_search()

    @rx.var
    def filtered_products(self) -> List[Dict]:
        filtered = self.products
        if self.selected_category != "All":
            filtered = [
                p for p in filtered 
                if p.get("category") == self.selected_category
            ]
        if self.search_query:
            query = self.search_query.lower()
            filtered = [
                p for p in filtered
                if query in p.get("name", "").lower() or query in p.get("desc", "").lower()
            ]
        return filtered
    
    def load_products(self):
        print("DEBUG: Starting load_products...")
        if len(self.products) > 1:
            return
        
        self.is_loading = True
        try:
            import os
            import pandas as pd
            file_path = os.path.join(os.getcwd(), "clean_data.csv")
            
            if not os.path.exists(file_path):
                file_path = "clean_data.csv"
                if not os.path.exists(file_path):
                    return

            df = pd.read_csv(file_path)
            df.columns = [c.strip() for c in df.columns]
            
            # Extract categories
            unique_cats = set()
            if "Category" in df.columns:
                for cat_str in df["Category"].dropna():
                    main_cat = str(cat_str).split(",")[0].strip().title()
                    if main_cat:
                        unique_cats.add(main_cat)
            self.categories = ["All"] + sorted(list(unique_cats))
            
            # Load all products
            new_products = []
            for i, row in df.head(200).iterrows():
                new_products.append({
                    "id": i,
                    "name": str(row.get("Name", "Unknown")),
                    "image": str(row.get("ImageURL", "")),
                    "desc": str(row.get("Description", "")),
                    "category": str(row.get("Category", "")).split(",")[0].strip().title(),
                    "price": random.randint(300, 5000),
                    "rating": str(round(random.uniform(3.5, 5.0), 1)),
                    "reviews": str(random.randint(50, 10000)),
                    "discount": str(random.randint(10, 40)),
                    "badge_text": random.choice(["DEAL", "BEST SELLER", "NEW", "TRENDING"]),
                })
            self.products = new_products
            
            # Set popular products (top rated)
            self.popular = sorted(self.products, key=lambda x: float(x["rating"]), reverse=True)[:8]
            
            # Set initial recommendations
            if self.products:
                self.recommended = random.sample(self.products, min(len(self.products), 8))
                
        except Exception as e:
            print(f"ERROR: {str(e)}")
        finally:
            self.is_loading = False

    def set_product(self, product):
        self.selected_product = product

        # 🔥 track view
        self.user_history = self.user_history + [product["name"]]

        return rx.redirect("/product-details")

    def load_product_by_id(self):
        """Load a product into selected_product based on the 'id' query parameter."""
        # Ensure products are loaded first
        if len(self.products) <= 1:
            self.load_products()

        query_params = self.router.page.params
        product_id = query_params.get("id")
        
        if product_id is not None:
            try:
                pid = int(product_id)
                # Find product in self.products
                for p in self.products:
                    if p["id"] == pid:
                        self.selected_product = p
                        return
                
                # If not found in current products, we might need to load it from CSV
                # but for now let's assume it's in the first 200 loaded products
            except (ValueError, TypeError):
                pass

    def recommend(self):
        if not self.user_history:
            # If no history, just show some random products from the list
            self.recommended = random.sample(self.products, min(len(self.products), 8))
        else:
            self.recommended = get_user_recommendations(self.user_history)