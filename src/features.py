"""Text, URL, sender, and metadata feature extraction will go here."""

import re
import pandas as pd
from urllib.parse import urlparse

def extract_features(df):
    df = df.copy()

    # Email body features
    df["body"] = df["body"].fillna("").astype(str)
    df["email_length"] = df["body"].str.len()

    # Count URLs
    df["url_count"] = df["url"].fillna("").apply(
        lambda x: 0 if x.strip().upper() == "NO_URL"
        else len(x.split("|"))
    )

    # Count urgent words
    urgent_words = [
        "urgent", "immediately", "verify",
        "suspended", "account", "password",
        "click", "update", "security"
    ]

    df["urgent_word_count"] = df["body"].apply(
        lambda text: sum(
            len(re.findall(r"\b" + word + r"\b", text, re.IGNORECASE))
            for word in urgent_words
        )
    )

    # Extract sender domain
    df["sender_domain"] = df["sender_address"].fillna("").apply(
        lambda x: x.split("@")[-1].lower()
        if "@" in x else "unknown"
    )

    return df
