from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Dummy order database
orders = {
    "113": {
        "status": "shipped",
        "tracking_number": "1Z999AA10123456784",
        "estimated_delivery": "2025-05-06"
    },
    "077": {
        "status": "processing",
        "tracking_number": "ilsiufeiugfsbsdfg",
        "estimated_delivery": "under process"
    },
    "123": {
        "status": "shipped",
        "tracking_number": "TRK1234567890",
        "estimated_delivery": "2025-05-08"
    },
    "456": {
        "status": "delivered",
        "tracking_number": "under process",
        "estimated_delivery": "under process"
    },
    "789": {
        "status": "pending",
        "tracking_number": "under process",
        "estimated_delivery": "under process"
    },
    "101": {
        "status": "cancelled",
        "tracking_number": "under process",
        "estimated_delivery": "under process"
    },
    "102": {
        "status": "shipped",
        "tracking_number": "TRK0987654321",
        "estimated_delivery": "2025-05-07"
    },
    "103": {
        "status": "processing",
        "tracking_number": "under process",
        "estimated_delivery": "under process"
    },
    "104": {
        "status": "delivered",
        "tracking_number": "under process",
        "estimated_delivery": "under process"
    },
    "105": {
        "status": "pending",
        "tracking_number": "under process",
        "estimated_delivery": "under process"
    },
    "106": {
        "status": "shipped",
        "tracking_number": "TRK5647382910",
        "estimated_delivery": "2025-05-09"
    },
    "107": {
        "status": "delivered",
        "tracking_number": "under process",
        "estimated_delivery": "under process"
    }
}

# Predefined responses for common queries
common_queries = {
    "Where is my order?": "You can track your order in the 'Your Orders' section of your Amazon account. You'll find tracking details there.",
    "I want to return a product": "You can return most items within 30 days by visiting the Returns Center on Amazon.",
    "How do I cancel my order?": "To cancel an order, visit 'Your Orders' in your Amazon account. If the item hasn't shipped yet, you can cancel it directly.",
    "Can I change my shipping address?": "If your order hasn't shipped yet, you can update your shipping address in 'Your Orders'. If the item has already shipped, the address cannot be changed.",
    "What is the status of my delivery?": "You can check the delivery status of your order by visiting 'Your Orders' and selecting the relevant order to view tracking updates.",
    "How do I track my order?": "To track your order, go to 'Your Orders' and click on the 'Track Package' option for real-time updates.",
    "I received a damaged item": "We apologize for the inconvenience. You can request a return or replacement through 'Your Orders'. Please select the item and choose the return/replacement option.",
    "I need help with payment": "For payment-related issues, visit the 'Help & Customer Service' section on Amazon, or check your order details to ensure your payment was processed correctly.",
    "Where is my refund?": "Refunds usually take 3-5 business days to process. You can check the status in 'Your Orders' under the refund section.",
    "The product I received is wrong": "We apologize for sending the wrong product. Please visit 'Your Orders' and select the 'Return or Replace' option to resolve this issue.",
    "Hi": "Hello! How can I assist you today?"
}

@app.route('/track_order', methods=['POST'])
def track_order():
    data = request.json
    order_id = data.get("order_id")

    if not order_id:
        return jsonify({"status": "error", "message": "Order ID not provided"}), 400

    order = orders.get(order_id)

    if order:
        return jsonify({
            "status": "success",
            "tracking_number": order["tracking_number"],
            "estimated_delivery": order["estimated_delivery"]
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Order not found"
        }), 404

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"status": "error", "message": "Question not provided"}), 400

    response = common_queries.get(question, "I'm sorry, I don't have an answer for that.")
    return jsonify({"status": "success", "response": response})

if __name__ == '__main__':
    app.run(debug=True)
