import reflex as rx
import pandas as pd
import random
import os

from ..backend.content_based import content_based_filtering


class RecommendationState(rx.State):

    query: str = ""
    results: list[dict] = []   # ✅ FIXED TYPE

    def set_query(self, value: str):
        self.query = value

    def generate(self):

        if not self.query:
            return rx.window_alert("Enter something")

        try:
            # ✅ LOAD DATASET PROPERLY
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            file_path = os.path.join(BASE_DIR, "clean_data.csv")

            df = pd.read_csv(file_path)

            # ✅ ML CALL
            recs = content_based_filtering(df, self.query, top_n=6)

            # 🔥 ADD PRICE (since dataset doesn't have it)
            for item in recs:
                item["price"] = random.randint(199, 4999)

            # ✅ STORE RESULTS
            self.results = recs

        except Exception as e:
            return rx.window_alert(f"Error: {str(e)}")