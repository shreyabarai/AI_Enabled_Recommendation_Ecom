import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def normalize_text(text):
    return (
        str(text)
        .lower()
        .strip()
        .replace(",", " ")
        .replace("-", " ")
    )

def shorten_text(text, max_len):
    text = str(text)
    return text[:max_len - 3] + "..." if len(text) > max_len else text


def content_based_filtering(df, product_name, top_n=5):

    df.columns = df.columns.str.strip().str.lower()

    if "name" in df.columns:
        product_col = "name"
    elif "product_name" in df.columns:
        product_col = "product_name"
    else:
        raise KeyError("Product name column not found")

    for col in ["tags", "description", "category"]:
        if col in df.columns:
            text_col = col
            break
    else:
        raise KeyError("Tags/description/category column not found")

    df = df[[product_col, text_col]].dropna().reset_index(drop=True)

    df["name_norm"] = df[product_col].apply(normalize_text)
    query_norm = normalize_text(product_name)

    matches = df[df["name_norm"].str.contains(query_norm, regex=False)]

    if matches.empty:
        print(f"\n❌ No product found for: {product_name}")
        return []

    product_index = matches.index[0]
    print(f"\n Using product: {df.loc[product_index, product_col]}")

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df[text_col])

    cosine_sim = cosine_similarity(tfidf_matrix)
    scores = list(enumerate(cosine_sim[product_index]))
    scores.sort(key=lambda x: x[1], reverse=True)

    scores = scores[1: top_n + 1]
    indices = [i[0] for i in scores]

    return df.loc[indices, [product_col, text_col]].values.tolist()

if __name__ == "__main__":

    print("\n📌 Content-Based Recommendation System")

    df = pd.read_csv("cleaned_data_final.csv")
    query = input("\nEnter Product Name: ").strip()

    results = content_based_filtering(df, query)

    if results:
        print("\n🔹 Recommended Products:\n")

        NAME_WIDTH = 75
        TAG_WIDTH = 80

        print(f"{'Product Name':<{NAME_WIDTH}}  {'Description / Tags':<{TAG_WIDTH}}")
        print("-" * (NAME_WIDTH + TAG_WIDTH + 2))

        for name, tags in results:
            name = shorten_text(name, NAME_WIDTH)
            tags = shorten_text(tags, TAG_WIDTH)
            print(f"{name:<{NAME_WIDTH}}  {tags:<{TAG_WIDTH}}")