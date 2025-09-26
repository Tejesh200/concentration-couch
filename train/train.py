import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_model():
    # Load dataset
    df = pd.read_csv("dataset.csv")

    # If no title column, just use URL
    if "title" in df.columns:
        df["text"] = df["title"].fillna("") + " " + df["url"]
    else:
        df["text"] = df["url"]

    X = df["text"]
    y = df["label"]

    # Split with stratify
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # TF-IDF
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Random Forest
    clf = RandomForestClassifier(n_estimators=300, random_state=42)
    clf.fit(X_train_tfidf, y_train)

    # Evaluate
    y_pred = clf.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.2f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Save
    joblib.dump(clf, "model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")

if __name__ == "__main__":
    train_model()
