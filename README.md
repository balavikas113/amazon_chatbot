Intelligent Customer Service Chatbot for Amazon Retail

Project Purpose
---------------
This project automates Amazon customer service by building an AI-powered chatbot that handles common customer inquiries such as order tracking, product returns, cancellations, and support requests. The chatbot leverages AWS Bedrock Agents and Cohere Command using advanced Chain of Thought (CoT) prompting to generate context-aware, accurate, and multilingual (English, Spanish, French) responses in real-time. The goal is to reduce query resolution time by 40%, improving customer satisfaction and operational efficiency during peak shopping seasons.

Setup Instructions
------------------
1. Clone the repository:
   git clone <repository-url>
   cd Amazon_Chatbot

2. Install dependencies (Python 3.8+):
   pip install -r requirements.txt

3. Configure AWS credentials:
   Run
     aws configure
   and enter your AWS access key, secret key, region, and output format.
   Ensure the credentials allow access to AWS Bedrock services.

4. Set up Cohere API key:
   Obtain your Cohere API key from https://dashboard.cohere.ai/
   Export it as an environment variable:
     export COHERE_API_KEY='your-cohere-api-key'

Run Command
-----------
To query the chatbot, use the main script with a text query and language code (en, es, or fr):

Example:
  python src/main.py --query "Dónde está mi pedido?" --lang "es"

This will process the Spanish query "Where is my order?" and return an AI-generated response.

Project Structure
-----------------
Amazon_Chatbot/
├── data/
│   ├── queries.txt            # Sample queries (10 each for en, es, fr)
│   ├── orders.json            # Mock order data with order IDs and statuses
│   └── responses/             # Generated response text files per query
├── src/
│   ├── preprocess.py          # Cleans and tags queries with intent & language
│   ├── chatbot.py             # Core chatbot: intent detection, CoT prompting, response gen
│   ├── aws_bedrock.py         # AWS Bedrock & Cohere Command API integration
│   └── main.py                # Runs the chatbot pipeline
├── tests/
│   ├── test_preprocess.py     # Unit tests for preprocessing
│   └── test_queries.py        # Unit tests for chatbot responses
├── docs/
│   ├── README.md              # Project overview and instructions
│   └── test_results.md        # Test case results (accuracy, latency)
├── requirements.txt           # Python dependencies
└── demo_video.mp4             # 2-minute demonstration video

For detailed documentation and additional help, please refer to the docs/ directory.

---

If you need more details or any other assistance, just let me know!
