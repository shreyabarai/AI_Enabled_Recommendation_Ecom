import reflex as rx
import pandas as pd
import random
import os

from ..backend.content_based import content_based_filtering
from ..backend.collaborative_based import collaborative_filtering_recommendations

class RecommendationState(rx.State):
    query: str = ""
    content_results: list[dict] = []
    collaborative_results: list[dict] = []
    is_loading: bool = False

    def set_query(self, value: str):
        self.query = value

    def generate_recommendations(self):
        self.is_loading = True
        yield
        
        try:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            file_path = os.path.join(BASE_DIR, "clean_data.csv")
            df = pd.read_csv(file_path)

            # 1. Content-based (Because you viewed/searched)
            if self.query:
                recs_content = content_based_filtering(df, self.query, top_n=8)
                for item in recs_content:
                    item["price"] = random.randint(300, 5000)
                    item["discount"] = str(random.randint(10, 40))
                    item["badge_text"] = "MATCH"
                self.content_results = recs_content
            else:
                # Default content recs if no query
                self.content_results = random.sample(self.content_results if self.content_results else [], 0)

            # 2. Collaborative-based (Users like you liked)
            # Mocking a user ID for demo purposes
            mock_user_id = df['ID'].iloc[0] if not df.empty else 0
            recs_collab = collaborative_filtering_recommendations(df, mock_user_id, top_n=8)
            
            if not recs_collab.empty:
                collab_list = recs_collab.to_dict('records')
                for item in collab_list:
                    item["price"] = random.randint(300, 5000)
                    item["discount"] = str(random.randint(10, 40))
                    item["badge_text"] = "POPULAR"
                    # Rename keys to match UI product_card
                    item["name"] = item.get("Name", "Unknown")
                    item["image"] = item.get("ImageURL", "")
                    item["rating"] = str(item.get("Rating", "0.0"))
                    item["reviews"] = str(item.get("ReviewCount", "0"))
                self.collaborative_results = collab_list

        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            self.is_loading = False
            yield