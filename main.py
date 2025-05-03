# main.py

from src.chatbot import get_response

def main():
    print("Amazon Chatbot (Simulated): Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break
        response = get_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    main()
