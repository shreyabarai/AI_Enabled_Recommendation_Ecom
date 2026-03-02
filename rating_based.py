import pandas as pd
def get_top_rated_items(
    data: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:

    average_ratings = (
        data
        .groupby(["Name", "Brand", "ImageURL"], as_index=False)["Rating"]
        .mean()
    )

    top_rated_items = average_ratings.sort_values(
        by="Rating",
        ascending=False
    )

    return top_rated_items.head(top_n)


if __name__ == "__main__":
    from cleaning_data import process_data

    raw_data = pd.read_csv("clean_data.csv")   
    data = process_data(raw_data)

    print(get_top_rated_items(data))