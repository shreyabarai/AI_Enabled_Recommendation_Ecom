import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from cleaning_data import process_data

data = pd.read_csv("clean_data.csv")
data = process_data(data)


def collaborative_filtering_recommendations(data, target_user_id, top_n=10):
    
    # Check if user exists
    if target_user_id not in data['ID'].values:
        print("Target user ID not found in dataset")
        return pd.DataFrame()

    # Create User-Item Matrix
    user_item_matrix = data.pivot_table(
        index='ID',
        columns='ProdID',
        values='Rating',
        aggfunc='mean'
    ).fillna(0)

    # Compute Cosine Similarity between users
    user_similarity = cosine_similarity(user_item_matrix)

    similarity_df = pd.DataFrame(
        user_similarity,
        index=user_item_matrix.index,
        columns=user_item_matrix.index
    )

    user_similarities = similarity_df[target_user_id]

    user_similarities = user_similarities.drop(index=target_user_id)

    similar_users = user_similarities.sort_values(ascending=False).head(20).index

    target_user_ratings = user_item_matrix.loc[target_user_id]

    # Collect recommended products
    recommended_products = set()

    for user in similar_users:
        similar_user_ratings = user_item_matrix.loc[user]

        products_to_recommend = similar_user_ratings[
            (similar_user_ratings > 0) & (target_user_ratings == 0)
        ].index

        recommended_products.update(products_to_recommend)

    # Limit to top_n
    recommended_products = list(recommended_products)[:top_n]

    recommendations = data[data['ProdID'].isin(recommended_products)][
        ['ProdID', 'Name', 'Brand', 'Rating', 'ReviewCount', 'ImageURL']
    ].drop_duplicates()

    return recommendations


if __name__ == "__main__":
    print("\n Collaborative Filtering Recommendation System")

    user_id = int(input("Enter User ID: "))

    results = collaborative_filtering_recommendations(data, user_id, top_n=10)

    if not results.empty:
        print("\n Recommended Products:\n")
        print(results.to_string(index=False))
    else:
        print("No recommendations found.")