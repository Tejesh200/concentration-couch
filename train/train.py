import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import shuffle
import joblib
import re

def extract_domain(url):
    """Extract domain name from URL."""
    if not url or pd.isna(url):
        return ""
    url = str(url).lower()
    # Remove protocol
    url = re.sub(r'^https?://', '', url)
    # Remove www.
    url = re.sub(r'^www\.', '', url)
    # Extract domain (first part before /)
    domain = url.split('/')[0]
    # Remove port numbers
    domain = domain.split(':')[0]
    return domain

def clean_text(text):
    """Improved text cleaning that preserves domain names."""
    text = str(text).lower()
    
    # Extract domain from URL before removing it
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    domains = [extract_domain(url) for url in urls]
    domain_text = ' '.join(domains)
    
    # Remove URLs but keep domain names
    text = re.sub(r'https?://\S+', '', text)
    
    # Combine domain names with title
    text = domain_text + ' ' + text
    
    # Remove symbols/numbers but keep domain dots
    text = re.sub(r'[^a-z\s\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    text = re.sub(r'\b(productive|distracting)\b', '', text)  # remove label words
    return text.strip()

def train_model():
    # Load dataset
    df = pd.read_csv("dataset.csv")

    # Combine title + URL
    if "title" in df.columns:
        df["text"] = df["title"].fillna("") + " " + df["url"]
    else:
        df["text"] = df["url"]

    # Clean the text
    df["text"] = df["text"].apply(clean_text)

    X = df["text"]
    y = df["label"]

    # Remove noise - train on clean labels for better accuracy
    # Shuffle the data
    df_shuffled = shuffle(df, random_state=42)
    X = df_shuffled["text"]
    y = df_shuffled["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # TF-IDF with better parameters
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),  # Include bigrams to capture domain patterns
        stop_words="english",
        sublinear_tf=True,
        min_df=1,
        max_df=0.95
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Random Forest with better parameters for accuracy
    clf = RandomForestClassifier(
        n_estimators=200,  # More trees for better accuracy
        max_depth=20,  # Deeper trees
        min_samples_split=3,  # Less restrictive
        min_samples_leaf=1,
        random_state=42,
        class_weight='balanced'  # Handle class imbalance
    )
    clf.fit(X_train_tfidf, y_train)

    # Evaluate
    y_pred = clf.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.2f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Save model + vectorizer
    joblib.dump(clf, "model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")

if __name__ == "__main__":
    train_model()
