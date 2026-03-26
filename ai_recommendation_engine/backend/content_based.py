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

def get_user_recommendations(history):
    import pandas as pd

    df = pd.read_csv("clean_data.csv")

    # If no history → default recommendations
    if not history:
        return [
            {
                "id": i,
                "name": str(row["Name"]),
                "image": str(row["ImageURL"]),
                "desc": str(row.get("Description", "")),
                "price": 500
            }
            for i, row in df.head(6).iterrows()
        ]

    # Match products user interacted with
    matched = df[df["Name"].isin(history)]

    if matched.empty:
        return df.head(6).to_dict("records")

    # Use category-based similarity
    category = matched.iloc[0]["category"]

    recs = df[df["category"] == category].head(6)

    return [
        {
            "id": i,
            "name": str(row["Name"]),
            "image": str(row["ImageURL"]),
            "desc": str(row.get("Description", "")),
            "price": 500
        }
        for i, row in recs.iterrows()
    ]

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