"""Model training and evaluation code will go here."""

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from preprocess import load_dataset, clean_dataset
from features import extract_features


# 1. Load and prepare dataset
df = load_dataset()
df = clean_dataset(df)
df = extract_features(df)

# 2. Select input features and target
X = df[[
    "body",
    "sender_domain",
    "url_count",
    "urgent_word_count",
    "email_length"
]]

y = df["label"]

# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4. Prepare feature transformers
preprocessor = ColumnTransformer(
    transformers=[
        ("text", TfidfVectorizer(
            max_features=10000,
            stop_words="english",
            ngram_range=(1, 2)
        ), "body"),

        ("sender", OneHotEncoder(
            handle_unknown="ignore"
        ), ["sender_domain"]),

        ("numeric", StandardScaler(), [
            "url_count",
            "urgent_word_count",
            "email_length"
        ])
    ]
)

# 5. Create and train model
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

print("Training model...")
model.fit(X_train, y_train)

# 6. Evaluate model
predictions = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# 7. Save model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/new_phishing_model.joblib")

print("\nModel saved successfully!")
