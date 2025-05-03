import re
import json
import os

# Paths
INPUT_PATH = "../data/queries.txt"
OUTPUT_PATH = "../data/processed_queries.json"

# Intent detection rules
INTENT_KEYWORDS = {
    "track_order": ["track", "where", "status", "dónde", "état", "commande", "pedido"],
    "return_item": ["return", "devolver", "retourner"],
    "cancel_order": ["cancel", "cancelar", "annuler"],
    "product_info": ["details", "information", "about", "producto", "produit"],
    "contact_support": ["help", "support", "contact", "soporte", "assistance"]
}

def detect_intent(text):
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(word in text.lower() for word in keywords):
            return intent
    return "unknown"

def detect_language(raw_line):
    if raw_line.startswith("[en]"):
        return "en"
    elif raw_line.startswith("[es]"):
        return "es"
    elif raw_line.startswith("[fr]"):
        return "fr"
    return "unknown"

def clean_query(query):
    query = query.lower()
    query = re.sub(r"[^a-zA-Z0-9áéíóúüñçàèâêîôûäëïöüœ'\s#]", "", query)
    query = query.strip()
    return query

def preprocess_queries():
    processed = []

    with open(INPUT_PATH, "r", encoding="utf-16") as f:
        for line in f:
            lang = detect_language(line)
            text = re.sub(r"\[\w+\]\s*", "", line).strip()
            cleaned = clean_query(text)
            intent = detect_intent(cleaned)

            processed.append({
                "language": lang,
                "original_query": text,
                "cleaned_query": cleaned,
                "intent": intent
            })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as out_file:
        json.dump(processed, out_file, indent=2, ensure_ascii=False)

    print(f"Processed {len(processed)} queries and saved to '{OUTPUT_PATH}'")

if __name__ == "__main__":
    preprocess_queries()
