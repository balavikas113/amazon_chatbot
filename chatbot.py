# src/chatbot.py

import re

# Define intent categories and sample patterns
INTENTS = {
    "order_status": ["where is my order", "track my order", "order status"],
    "cancel_order": ["cancel my order", "how to cancel", "stop order"],
    "return_item": ["return item", "how do i return", "return process"],
    "refund_status": ["where is my refund", "refund status", "when will i get my money back"]
}

# Chain-of-thought templates for each intent
COT_TEMPLATES = {
    "order_status": "The customer wants to know the status of their order. First, I will identify the order. Then, I will retrieve tracking info. Finally, I’ll provide a summary.",
    "cancel_order": "The user wants to cancel their order. I will first check if the order is eligible. Then, I’ll guide them through cancellation.",
    "return_item": "The customer wishes to return an item. I will explain the return eligibility and provide steps to return.",
    "refund_status": "The user is asking about a refund. I’ll verify if the refund is processed and explain the timeline."
}

# Mock Cohere API Response (to be replaced with real call)
def mock_cohere_response(prompt: str) -> str:
    return f"[Simulated Response]\n{prompt}\n[End of Response]"

# Intent detection using simple keyword match
def detect_intent(user_input: str) -> str:
    user_input = user_input.lower()
    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            if pattern in user_input:
                return intent
    return "unknown"

# Main function to handle chatbot response
def get_response(user_input: str) -> str:
    intent = detect_intent(user_input)
    
    if intent == "unknown":
        return "Sorry, I didn’t understand that. Can you rephrase?"

    # Build the CoT-style prompt
    cot_prompt = COT_TEMPLATES[intent]
    full_prompt = f"{cot_prompt}\n\nUser Query: {user_input}"

    # Simulate calling Cohere
    response = mock_cohere_response(full_prompt)
    return response
