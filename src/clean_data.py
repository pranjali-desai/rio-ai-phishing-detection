import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/new_dataset.csv")

print("Original shape:", df.shape)

# Remove exact duplicate rows
df = df.drop_duplicates()

# Remove rows with empty email bodies
df = df.dropna(subset=["body"])
df = df[df["body"].astype(str).str.strip() != ""]

# Clean text columns
for col in ["sender_address", "url", "body"]:
    df[col] = df[col].fillna("").astype(str).str.strip()

# Keep only valid labels
df = df[df["label"].isin([0, 1])]

# Save cleaned dataset
df.to_csv("data/processed/cleaned_dataset.csv", index=False)

print("Cleaned shape:", df.shape)
print("\nLabel distribution:")
print(df["label"].value_counts())

print("\nDataset cleaned successfully!")