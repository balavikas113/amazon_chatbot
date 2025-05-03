from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load processed data
try:
    with open("data/processed_queries.json", "r", encoding="utf-8-sig") as f:
        processed_data = json.load(f)
except FileNotFoundError:
    logging.error("The file 'processed_queries.json' was not found. Please check the path.")
    raise

try:
    with open("data/responses.json", "r", encoding="utf-8-sig") as f:
        responses = json.load(f)
except FileNotFoundError:
    logging.error("The file 'responses.json' was not found. Please check the path.")
    raise

# --- Vectorization ---
vectorizer = TfidfVectorizer(stop_words=None)
queries = [item["query"] for item in processed_data]

if not queries:
    raise ValueError("No queries found in processed data.")

query_vectors = vectorizer.fit_transform(queries)

# --- Multilingual Placeholders ---
def detect_language(text):
    # Placeholder: Always English; integrate with langdetect or fasttext later
    return "en"

def translate_to_english(text, lang):
    # Placeholder: Add real translation logic later
    return text

def translate_from_english(text, lang):
    # Placeholder: Add real translation logic later
    return text

# --- Chain of Thought Reasoning ---
def apply_chain_of_thought(query):
    steps = []
    
    if "order" in query:
        steps.append("The customer wants to know about their order.")
        steps.append("First, identify the order number.")
        steps.append("Then, check order status and tracking.")
        steps.append("Finally, summarize delivery status.")
    elif "return" in query:
        steps.append("The customer is asking about a return.")
        steps.append("First, verify the item and order.")
        steps.append("Then, explain the return window and process.")
    elif "refund" in query:
        steps.append("The customer inquired about a refund.")
        steps.append("Start by checking the return/refund status.")
        steps.append("Then, explain refund timelines.")
    elif "gift card" in query:
        steps.append("The customer asked about a gift card.")
        steps.append("First, identify the gift card number or account.")
        steps.append("Then, retrieve the balance.")
    else:
        steps.append("Analyzing the request step by step.")
        steps.append("Trying to understand user intent and possible actions.")

    return "\n".join(steps)

# --- Response Logic ---
def get_response(user_input):
    logging.debug(f"Received user input: {user_input}")
    
    original_lang = detect_language(user_input)
    translated_input = translate_to_english(user_input, original_lang)
    user_input_clean = translated_input.strip().lower()

    greetings = ["hi", "hello", "hey", "greetings"]
    if user_input_clean in greetings:
        return translate_from_english("Hello! How can I help you today?", original_lang)

    # Exact match first
    for query in queries:
        if user_input_clean == query.lower():
            return translate_from_english(responses.get(query, "Sorry, I couldn't find a response."), original_lang)

    # TF-IDF similarity
    user_vector = vectorizer.transform([user_input_clean])
    similarities = cosine_similarity(user_vector, query_vectors)
    best_match_index = np.argmax(similarities)
    best_score = similarities[0][best_match_index]

    if best_score < 0.1:
        return translate_from_english("Sorry, I didn't understand that. Could you rephrase?", original_lang)

    matched_query = queries[best_match_index]
    response = responses.get(matched_query, "Sorry, I couldn't find a response.")

    # Chain of Thought
    cot_steps = apply_chain_of_thought(user_input_clean)
    full_response = f"[Chain of Thought Reasoning]\n{cot_steps}\n\n[Final Response]\n{response}"
    
    return translate_from_english(full_response, original_lang)

# --- API Endpoint ---
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("query")
    
    if not user_input:
        return jsonify({"response": "No input provided."}), 400
    
    response = get_response(user_input)
    return jsonify({"response": response})

# --- Run the Flask app ---
if __name__ == "__main__":
    app.run(debug=True)  # Set debug=True for development
