import pandas as pd
import numpy as np

def clean_data(file_path):
    
    data = pd.read_csv(file_path)

    # Fix invalid numeric IDs
    if 'ProdID' in data.columns:
        data['ProdID'] = data['ProdID'].replace(-2147483648, np.nan)

    if "User's ID" in data.columns:
        data["User's ID"] = data["User's ID"].replace(-2147483648, np.nan)

    # Drop rows with missing critical IDs (if present)
    critical_ids = [c for c in ["User's ID", "ProdID"] if c in data.columns]
    if critical_ids:
        data = data.dropna(subset=critical_ids)

    # Convert IDs to int
    if "User's ID" in data.columns:
        data["User's ID"] = data["User's ID"].astype("int64")

    if "ProdID" in data.columns:
        data["ProdID"] = data["ProdID"].astype("int64")

    # Review Count cleanup
    if "Review Count" in data.columns:
        data["Review Count"] = data["Review Count"].fillna(0).astype("int64")

    # Clean text columns
    text_columns = ["Brand", "Description", "Tags", "Name"]
    for col in text_columns:
        if col in data.columns:
            data[col] = (
                data[col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    # CATEGORY FIX - FILL MISSING WITH TAGS OR UNKNOWN
    if "Category" in data.columns:
        data["Category"] = (
            data["Category"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        data.loc[data["Category"] == "", "Category"] = "Unknown"

        if "Tags" in data.columns:
            mask = data["Category"] == "Unknown"
            data.loc[mask, "Category"] = (
                data.loc[mask, "Tags"]
                .fillna("")
                .str.split(",")
                .str[0]
                .str.strip()
                .replace("", "Unknown")
            )
            
    # IMAGE URL CLEANING 
    if "ImageURL" in data.columns:
        data["ImageURL"] = (
            data["ImageURL"]
            .fillna("")
            .astype(str)
            .str.split(r"\s*\|\s*")  # correct pipe handling
            .str[0]
            .str.strip()
        )

    # REMOVE BLANK / BROKEN ROWS
    essential_cols = [c for c in ["Name", "Brand", "ImageURL"] if c in data.columns]

    if essential_cols:
        for col in essential_cols:
            data = data[data[col] != ""]

    # Remove rows that are mostly empty
    data = data.dropna(thresh=int(len(data.columns) * 0.4))

    return data


if __name__ == "__main__":
    cleaned_data = clean_data("clean_data.csv")
    cleaned_data.to_csv("cleaned_data_final.csv", index=False)

    print("✅ Data cleaned successfully")
    print(f"📊 Final rows count: {len(cleaned_data)}")







