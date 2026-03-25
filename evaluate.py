# evaluate.py

import pandas as pd
from cleaning_data import process_data
from content_based import content_based_filtering


def evaluate_content_based_metrics(data, item_name, top_n=10):
    print(f"\n=== FULL METRICS: CONTENT-BASED (Top {top_n}) ===")

    # 1. CHECK ITEM EXISTS
    item_matches = data[data['Name'] == item_name]

    if item_matches.empty:
        print(f"Item '{item_name}' NOT FOUND!")
        return None

    item_data = item_matches.iloc[0]
    item_category = item_data.get('Category', None)
    item_brand = item_data.get('Brand', 'Unknown')

    print(f"\nInput: {item_name}")
    print(f"Category: {item_category}, Brand: {item_brand}")

    # 2. GROUND TRUTH
    relevant_items = set()

    if item_category:
        relevant_items.update(
            data[data['Category'] == item_category]['Name'].values
        )

    relevant_items.update(
        data[data['Brand'] == item_brand]['Name'].values
    )

    # Remove the item itself
    relevant_items.discard(item_name)

    total_relevant = len(relevant_items)
    print(f"Total relevant items in dataset: {total_relevant}")

    # 3. GET RECOMMENDATIONS (returns list)
    recs = content_based_filtering(data, item_name, top_n)

    if not recs:
        print("No recommendations!")
        return None

    # Extract only product names from list of [name, tags]
    recommended_names = set([item[0] for item in recs])

    # 4. METRICS
    true_positives = len(recommended_names & relevant_items)

    precision = true_positives / top_n if top_n > 0 else 0
    recall = true_positives / total_relevant if total_relevant > 0 else 0
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0 else 0
    )

    # 5. RESULTS
    print(f"\nMETRICS@{top_n}:")
    print(f"Precision: {precision:.3f} ({true_positives}/{top_n})")
    print(f"Recall:    {recall:.3f} ({true_positives}/{total_relevant})")
    print(f"F1-Score:  {f1:.3f}")

    matches = list(recommended_names & relevant_items)
    print(f"\nMatches: {matches[:3]}...")

    return {
        'precision': precision,
        'recall': recall,
        'f1': f1
    }


# ✅ MAIN BLOCK (FIXED)
if __name__ == "__main__":
    print("Running evaluation...")

    raw_data = pd.read_csv("clean_data.csv")
    data = process_data(raw_data)

    item_name = data['Name'].iloc[0]

    evaluate_content_based_metrics(data, item_name, top_n=10)