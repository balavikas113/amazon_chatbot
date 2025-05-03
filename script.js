document.getElementById("chat-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("user-input");
    const message = input.value.trim().toLowerCase();
    addMessage("user", message);

    let orderId = null;

    if (message.includes("where is my order") || message.includes("track order")) {
        // You can use regex to extract order ID if present
        orderId = "12345"; // demo fallback
    }

    if (!orderId) {
        addMessage("bot", "Sorry, I didn't understand that.");
        input.value = "";
        return;
    }

    try {
        const response = await fetch("/track_order", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ order_id: orderId })
        });
        const data = await response.json();
        if (data.status === "success") {
            addMessage("bot", `Tracking Number: ${data.tracking_number}\nEstimated Delivery: ${data.estimated_delivery}`);
        } else {
            addMessage("bot", "Sorry, we couldn't find your order.");
        }
    } catch (err) {
        console.error(err);
        addMessage("bot", "Error: Failed to fetch");
    }

    input.value = "";
});
