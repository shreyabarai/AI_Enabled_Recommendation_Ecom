import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 🔹 Clean text
def normalize_text(text):
    return (
        str(text)
        .lower()
        .strip()
        .replace(",", " ")
        .replace("-", " ")
    )

# 🔹 Main recommendation function (FINAL)
def content_based_filtering(df, query, top_n=5):

    # ✅ Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # ✅ Detect product column
    if "name" in df.columns:
        product_col = "name"
    elif "product_name" in df.columns:
        product_col = "product_name"
    else:
        raise KeyError("❌ Product name column not found")

    # ✅ Detect text column
    text_col = None
    for col in ["tags", "description", "category"]:
        if col in df.columns:
            text_col = col
            break

    if not text_col:
        raise KeyError("❌ No text column (tags/description/category) found")

    # ✅ Keep required columns
    df = df[[product_col, text_col]].dropna().reset_index(drop=True)

    # ✅ Normalize names
    df["name_norm"] = df[product_col].apply(normalize_text)
    query_norm = normalize_text(query)

    # 🔥 Create combined text (better recommendations)
    df["combined"] = df[product_col].astype(str) + " " + df[text_col].astype(str)

    # 🔥 TF-IDF
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(df["combined"])

    # 🔥 If product exists → use it
    matches = df[df["name_norm"].str.contains(query_norm, regex=False)]

    if not matches.empty:
        idx = matches.index[0]
        query_vec = matrix[idx]
    else:
        # 🔥 Otherwise use query text
        query_vec = tfidf.transform([query])

    # 🔥 Similarity
    similarity = cosine_similarity(query_vec, matrix).flatten()

    # 🔥 Top results
    indices = similarity.argsort()[-(top_n + 1):][::-1]

    results = []

    for i in indices:
        item = {
            "product_name": df.loc[i, product_col],
            "category": df.loc[i, text_col],
            "score": float(similarity[i])
        }

        results.append(item)

    # ❗ Remove first item if it's same product
    if results and normalize_text(results[0]["product_name"]) == query_norm:
        results = results[1:]

    return results[:top_n]

def get_user_recommendations(history, df_all=None):
    """
    Get content-based recommendations based on user history.
    Uses TF-IDF and Cosine Similarity for robust matching.
    """
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import random

    if df_all is None:
        try:
            df = pd.read_csv("clean_data.csv")
        except:
            return []
    else:
        df = df_all.copy()

    # Clean data
    df.columns = [c.strip() for c in df.columns]
    df = df.fillna("")

    # If no history → return popular/random products
    if not history:
        # Just return first few products formatted correctly
        recs = df.head(8)
        return _format_results(recs)

    # Combine text for TF-IDF
    # We use Name, Category, and Description for better similarity
    df["combined_features"] = df["Name"].astype(str) + " " + \
                              df["Category"].astype(str) + " " + \
                              df["Description"].astype(str)

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["combined_features"])

    # Create a profile for the user based on their history
    # We search for the indices of products in the history
    history_indices = []
    for product_name in history:
        idx = df[df["Name"] == product_name].index
        if not idx.empty:
            history_indices.append(idx[0])

    if not history_indices:
        # If none of the history products found, return random
        return _format_results(df.sample(min(len(df), 8)))

    # Average the TF-IDF vectors of the products in the user's history
    user_profile = tfidf_matrix[history_indices].mean(axis=0)
    
    # Convert to array for cosine_similarity
    import numpy as np
    user_profile = np.asarray(user_profile)

    # Calculate cosine similarity between user profile and all products
    cosine_sim = cosine_similarity(user_profile, tfidf_matrix).flatten()

    # Get indices of products with highest similarity
    # Exclude products already in history
    related_indices = cosine_sim.argsort()[::-1]
    
    top_indices = []
    history_names = [name.lower() for name in history]
    
    for idx in related_indices:
        if df.iloc[idx]["Name"].lower() not in history_names:
            top_indices.append(idx)
        if len(top_indices) >= 8:
            break

    recs = df.iloc[top_indices]
    return _format_results(recs)

def _format_results(df_recs):
    """Helper to format dataframe rows into the dict structure used by the app."""
    import random
    results = []
    for i, row in df_recs.iterrows():
        results.append({
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
    return results

# 🔹 CLI testing (optional)
if __name__ == "__main__":

    print("\n📌 Content-Based Recommendation System")

    df = pd.read_csv("clean_data.csv")
    query = input("\nEnter Product Name: ").strip()

    results = content_based_filtering(df, query)

    if results:
        print("\n🔹 Recommended Products:\n")

        for item in results:
            print(f"{item['product_name']}  |  {item['category']}")