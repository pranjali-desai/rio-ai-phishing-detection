"""Dataset loading and cleaning functions will go here."""

import pandas as pd

def load_dataset(path="data/raw/new_dataset.csv"):
    df = pd.read_csv(path)
    return df


def clean_dataset(df):
    df = df.copy()

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Remove emails with missing or empty bodies
    df = df.dropna(subset=["body"])
    df = df[df["body"].astype(str).str.strip() != ""]

    # Handle missing values
    for col in ["sender_address", "url", "body"]:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Keep only valid labels
    df = df[df["label"].isin([0, 1])]

    return df
