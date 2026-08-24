async function getRecommendations() {
    const query = document.getElementById("query").value;
    const budget = document.getElementById("budget").value;
    const category = document.getElementById("category").value;

    const response = await fetch("/recommend", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({query, budget, category})
    });

    const products = await response.json();
    const results = document.getElementById("results");

    if (!products.length) {
        results.innerHTML = "<p>No suitable products found. Try another requirement.</p>";
        return;
    }

    results.innerHTML = products.map(p => `
        <div class="product">
            <div class="icon">🛍️</div>
            <div>
                <h3>${p.name}</h3>
                <p class="price">₹${Number(p.price).toFixed(0)}</p>
                <p>${p.description}</p>
            </div>
        </div>
    `).join("");
}

async function sendMessage() {
    const message = document.getElementById("message").value;
    const budget = document.getElementById("budget").value;
    const chat = document.getElementById("chat");

    if (!message.trim()) return;

    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message, budget})
    });

    const data = await response.json();
    chat.innerHTML = `<strong>Assistant:</strong> ${data.reply}`;
}
