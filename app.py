
"""Flask entry point for the phishing email detector."""

from flask import Flask, render_template, request
import joblib
import re
from pathlib import Path
import pandas as pd

app = Flask(__name__)

# Load the newly trained model
MODEL_PATH = Path(__file__).parent / "models" / "new_phishing_model.joblib"
model = joblib.load(MODEL_PATH)


# Patterns for detecting URLs and suspicious wording
URL_PATTERN = re.compile(
    r"https?://[^\s<>\"']+|www\.[^\s<>\"']+",
    re.IGNORECASE
)

URGENT_WORDS = [
    "urgent", "immediately", "verify",
    "suspended", "account", "password",
    "click", "update", "security"
]

URGENT_PATTERN = re.compile(
    r"\b(urgent|immediately|suspended|verify|password|account|"
    r"act now|within 24 hours|final warning|limited time)\b",
    re.IGNORECASE
)

CREDENTIAL_PATTERN = re.compile(
    r"\b(enter|confirm|provide|update|reset|verify)\b.{0,45}"
    r"\b(password|login|credentials|account details|bank details|"
    r"credit card|card number|otp|one[- ]time password)\b"
    r"|\b(password|login credentials|bank details|credit card|otp)\b",
    re.IGNORECASE
)


def extract_sender_domain(sender):
    """Extract the domain from the sender email address."""

    match = re.search(r"@([^>\s]+)", sender)

    return (
        match.group(1).strip(".,;)>").lower()
        if match else "unknown"
    )


def count_urgent_words(email_text):
    """Count the urgency words used during model training."""

    return sum(
        len(re.findall(
            r"\b" + re.escape(word) + r"\b",
            email_text,
            re.IGNORECASE
        ))
        for word in URGENT_WORDS
    )


def build_reasons(email_text, sender, url_count, urgent_matches):
    """Generate rule-based explanations for the user."""

    reasons = []

    if urgent_matches:
        examples = ", ".join(
            sorted(set(word.lower() for word in urgent_matches))[:5]
        )

        reasons.append({
            "title": "Urgent or pressure-based language",
            "detail": (
                f"Detected wording such as: {examples}. "
                "Urgency can be used to pressure recipients."
            )
        })

    if url_count:
        reasons.append({
            "title": "Links are present",
            "detail": (
                f"Found {url_count} URL(s). Links are not automatically "
                "malicious; check their destinations before opening."
            )
        })

    if CREDENTIAL_PATTERN.search(email_text):
        reasons.append({
            "title": "Possible request for sensitive information",
            "detail": (
                "The message appears to ask for passwords, login details, "
                "banking information, or similar credentials."
            )
        })

    sender_domain = extract_sender_domain(sender)

    if sender_domain != "unknown":
        reasons.append({
            "title": "Sender domain to verify",
            "detail": (
                f"The supplied sender domain is {sender_domain}. "
                "Confirm it matches the organisation's official domain."
            )
        })

    if not reasons:
        reasons.append({
            "title": "No obvious warning indicators found",
            "detail": (
                "The simple checks found no obvious warning signs. "
                "This does not guarantee the email is safe."
            )
        })

    return reasons


@app.route("/")
def index():
    return render_template(
        "index.html",
        email_text="",
        sender=""
    )


@app.route("/analyze", methods=["POST"])
def analyze():

    # Get submitted email and sender
    email_text = request.form.get("email_text", "")
    sender = request.form.get("sender", "").strip()

    if not email_text.strip():
        return render_template(
            "index.html",
            email_text=email_text,
            sender=sender,
            error="Please paste email content before analysing."
        )

    # Extract features
    sender_domain = extract_sender_domain(sender)

    urls = URL_PATTERN.findall(email_text)
    url_count = len(urls)

    urgent_matches = URGENT_PATTERN.findall(email_text)
    urgent_count = count_urgent_words(email_text)

    email_length = len(email_text)

    # Prepare input in the exact format used during training
    input_data = pd.DataFrame([{
        "body": email_text,
        "sender_domain": sender_domain,
        "url_count": url_count,
        "urgent_word_count": urgent_count,
        "email_length": email_length
    }])

    # Predict email category and probability
    prediction = int(model.predict(input_data)[0])

    probabilities = model.predict_proba(input_data)[0]

    risk_score = round(float(probabilities[1]) * 100, 2)

    # Assign presentation risk level
    if risk_score <= 30:
        risk_level = "low"
        risk_label = "Low risk"

    elif risk_score <= 70:
        risk_level = "medium"
        risk_label = "Medium risk"

    else:
        risk_level = "high"
        risk_label = "High risk"

    model_label = (
        "Phishing / Spam"
        if prediction == 1
        else "Legitimate"
    )

    result = {
        "prediction": prediction,
        "model_label": model_label,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_label": risk_label,
        "url_count": url_count,
        "urgent_count": urgent_count,
        "reasons": build_reasons(
            email_text,
            sender,
            url_count,
            urgent_matches
        ),
        "message": (
            "The model found patterns associated with phishing or spam."
            if prediction == 1
            else "The model classified this email as legitimate."
        )
    }

    return render_template(
        "index.html",
        result=result,
        email_text=email_text,
        sender=sender
    )


if __name__ == "__main__":

    # Development server only
    app.run(debug=True)
