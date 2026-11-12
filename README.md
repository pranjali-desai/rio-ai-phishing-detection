# RIO – AI-Based Phishing Email Detection

An AI-powered web application that analyses email content and sender information to identify potentially **Legitimate** or **Phishing/Spam** emails. It displays a risk score, risk level and warning indicators to help users identify suspicious emails.

**Project Status:** Phase 1 – Approximately 70% Complete

## 1. Features

- Email content and sender address input.
- AI-based email classification.
- Risk score with Low, Medium and High risk levels.
- Warning indicators for suspicious email content.
- Email input retention after analysis.
- Option to clear email content.

## 2. Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Frontend | HTML, CSS, JavaScript |
| Backend | Flask |
| ML Library | Scikit-learn |
| ML Algorithm | Logistic Regression |
| Text Feature Extraction | TF-IDF |
| Data Processing | Pandas |
| Model Storage | Joblib |
| IDE | Visual Studio Code |

## 3. How It Works

1. User enters the email content and sender address.
2. The application extracts relevant email features.
3. TF-IDF and other preprocessing techniques convert the data into model-ready features.
4. Logistic Regression predicts whether the email is Legitimate or Phishing/Spam.
5. The application displays the prediction, risk score and warning indicators.

## 4. Dataset

The project uses a combined email dataset containing **134,614 records**.

**Dataset columns:**
- `sender_address`
- `url`
- `body`
- `label`

**Label mapping:**
- `0` – Legitimate
- `1` – Phishing/Spam

Note: The current model combines phishing and spam into one category. It does not yet distinguish between them.

## 5. Model Performance

- Algorithm: Logistic Regression
- Training and testing split: 80:20
- Test records: 26,923
- Reported accuracy: **98.41%**

The accuracy is based on a random holdout split from the same dataset. Real-world performance requires further independent testing.

## 6. Project Structure

```text
AI Phishing Detection/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── src/
│   ├── clean_data.py
│   ├── features.py
│   ├── preprocess.py
│   ├── train.py
│   └── predict.py
│
├── static/
├── templates/
├── notebooks/
├── docs/
└── tests/
```

## 7. Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/rio-ai-phishign-detection.git
cd rio-ai-phishign-detection
```

Replace `YOUR-USERNAME` with your GitHub username.

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Install dependencies

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Step 4: Add the dataset

Place `new_dataset.csv` inside:

```text
data/raw/
```

### Step 5: Train the model

```bash
.venv\Scripts\python.exe src/train.py
```

This generates the trained model:

```text
models/new_phishing_model.joblib
```

### Step 6: Run the application

```bash
.venv\Scripts\python.exe app.py
```

Open the local Flask address displayed in the terminal, usually:

`http://127.0.0.1:5000`

**Note:** The dataset and trained model are excluded from GitHub through `.gitignore`. They must be added locally before running the application.

## 8. Current Limitations

- Phishing and ordinary spam are not yet classified separately.
- False positives need further reduction.
- URL reputation and attachment analysis are not implemented.
- Independent real-world validation is still required.

## 9. Phase 2 – Future Enhancements

- Develop a browser extension for automatic email analysis and direct integration with an email service such as Gmail.
- Introduce multi-class classification to distinguish phishing from spam and improve detection accuracy.

## 10. Disclaimer

This project is an academic prototype developed for educational purposes. Its predictions should not be treated as a guarantee that an email is safe or malicious.
