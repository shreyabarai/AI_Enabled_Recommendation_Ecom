# ==========================================
# CONTENT-BASED RECOMMENDATION SYSTEM
# ==========================================

import re
from difflib import get_close_matches

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_text(value):
    value = str(value).casefold().strip()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return value.strip()


def content_based_filtering(cleaned_data, product_name, top_n=5):

    # Normalize column names
    cleaned_data.columns = cleaned_data.columns.str.strip().str.lower()

    print("\nAvailable columns:")
    print(list(cleaned_data.columns))

    # -------------------------------
    # Detect product name column
    # -------------------------------
    if "name" in cleaned_data.columns:
        product_col = "name"
    elif "product_name" in cleaned_data.columns:
        product_col = "product_name"
    elif "product name" in cleaned_data.columns:
        product_col = "product name"
    else:
        raise KeyError("Product name column not found")

    # -------------------------------
    # Detect tags column
    # -------------------------------
    possible_tag_cols = ["tags", "description", "category"]
    tag_col = None

    for col in possible_tag_cols:
        if col in cleaned_data.columns:
            tag_col = col
            break

    if tag_col is None:
        raise KeyError("Tags/Description column not found")

    # -------------------------------
    # Clean required data
    # -------------------------------
    cleaned_data = cleaned_data[[product_col, tag_col]].copy()
    cleaned_data.dropna(inplace=True)
    cleaned_data[tag_col] = cleaned_data[tag_col].astype(str)
    cleaned_data = cleaned_data.reset_index(drop=True)

    # -------------------------------
    # Resolve product name robustly
    # -------------------------------
    original_names = cleaned_data[product_col].astype(str)
    normalized_to_original = {
        normalize_text(name): name for name in original_names
    }

    if product_name in original_names.values:
        selected_product_name = product_name
    else:
        normalized_input = normalize_text(product_name)

        # Case/punctuation/spacing-insensitive exact match
        if normalized_input in normalized_to_original:
            selected_product_name = normalized_to_original[normalized_input]
            print(f"Using normalized match: {selected_product_name}")
        else:
            # Fuzzy fallback for near matches
            normalized_candidates = list(normalized_to_original.keys())
            close_normalized = get_close_matches(
                normalized_input, normalized_candidates, n=5, cutoff=0.55
            )

            if not close_normalized:
                print(f"Product '{product_name}' not found.")
                return pd.DataFrame()

            selected_product_name = normalized_to_original[close_normalized[0]]
            print("Exact product not found.")
            print(f"Using closest match: {selected_product_name}")

            if len(close_normalized) > 1:
                print("\nSimilar products:")
                for suggestion in close_normalized[1:]:
                    print(f"- {normalized_to_original[suggestion]}")

    # -------------------------------
    # TF-IDF
    # -------------------------------
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(cleaned_data[tag_col])

    # -------------------------------
    # Cosine Similarity
    # -------------------------------
    cosine_sim = cosine_similarity(tfidf_matrix)

    product_index = cleaned_data[
        cleaned_data[product_col] == selected_product_name
    ].index[0]

    similarity_scores = list(enumerate(cosine_sim[product_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    similarity_scores = similarity_scores[1 : top_n + 1]
    recommended_indices = [i[0] for i in similarity_scores]

    return cleaned_data.iloc[recommended_indices]


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":

    print("\nContent-Based Recommendation System")
    print("----------------------------------------")

    df = pd.read_csv("cleaned_data_final.csv")

    product_name = input("\nEnter Product Name: ").strip()

    result = content_based_filtering(df, product_name, top_n=5)

    if not result.empty:
        print("\nRecommended Products:\n")
        print(result)
