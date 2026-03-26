import pandas as pd
import numpy as np


def process_data(data: pd.DataFrame) -> pd.DataFrame:

    # Standardize Column Names
    if "User's ID" in data.columns:
        data = data.rename(columns={"User's ID": "ID"})

    if "Review Count" in data.columns:
        data = data.rename(columns={"Review Count": "ReviewCount"})

    # Replace invalid values
    if 'ProdID' in data.columns:
        data['ProdID'] = data['ProdID'].replace(-2147483648, np.nan)

    if 'ID' in data.columns:
        data['ID'] = data['ID'].replace(-2147483648, np.nan)

    # Convert to numeric
    if 'ID' in data.columns:
        data['ID'] = pd.to_numeric(data['ID'], errors='coerce')

    if 'ProdID' in data.columns:
        data['ProdID'] = pd.to_numeric(data['ProdID'], errors='coerce')

    # Drop missing IDs
    data = data.dropna(subset=['ID', 'ProdID'])

    # Remove zero IDs
    data = data[(data['ID'] != 0) & (data['ProdID'] != 0)]

    # Convert to int
    data['ID'] = data['ID'].astype('int64')
    data['ProdID'] = data['ProdID'].astype('int64')

    # Clean Rating
    if 'Rating' in data.columns:
        data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce')
        data['Rating'] = data['Rating'].fillna(0)

    # Clean ReviewCount
    if 'ReviewCount' in data.columns:
        data['ReviewCount'] = pd.to_numeric(
            data['ReviewCount'], errors='coerce'
        ).fillna(0).astype('int64')

    # Clean text columns
    for col in ['Category', 'Brand', 'Description', 'Tags', 'Name']:
        if col in data.columns:
            data[col] = data[col].fillna('').astype(str).str.strip()

    # Clean ImageURL
    if 'ImageURL' in data.columns:
        data['ImageURL'] = (
            data['ImageURL']
            .fillna('')
            .astype(str)
            .str.split('|')
            .str[0]
            .str.strip()
        )

    # Drop unwanted column
    if 'Unnamed: 0' in data.columns:
        data = data.drop(columns=['Unnamed: 0'])

    data.reset_index(drop=True, inplace=True)

    return data







