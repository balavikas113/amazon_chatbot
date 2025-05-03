# train_model.py

import json
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define paths relative to the project root (one level up from script directory)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

DATA_PATH = os.path.join(DATA_DIR, "processed_queries.json")
MODEL_PATH = os.path.join(DATA_DIR, "tfidf_model.joblib")
RESPONSES_PATH = os.path.join(DATA_DIR, "responses.json")

def train():
    print(f"Looking for data file at: {DATA_PATH}")
    # Use utf-8-sig encoding to handle UTF-8 BOM
    with open(DATA_PATH, "r", encoding="utf-8-sig", errors="ignore") as f:
        data = json.load(f)

    queries = [item["query"] for item in data]
    responses = [item["response"] for item in data]

    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(queries)

    # Save the model and data
    joblib.dump(vectorizer, MODEL_PATH)
    with open(RESPONSES_PATH, "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=2)

    print(f"✅ Model trained and saved to '{MODEL_PATH}'")
    print(f"✅ Responses saved to '{RESPONSES_PATH}'")

if __name__ == "__main__":
    train()
