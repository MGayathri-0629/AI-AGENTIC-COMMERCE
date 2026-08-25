async function getRecommendations() {

    const query = document
        .getElementById("query")
        .value
        .trim();

    const budget = document
        .getElementById("budget")
        .value;

    const category = document
        .getElementById("category")
        .value;

    const results = document.getElementById("results");

    if (!query) {

        results.innerHTML =
            "<p>Please enter a product you are looking for.</p>";

        return;
    }

    results.innerHTML =
        "<p>Finding the best products for you...</p>";

    try {

        const response = await fetch("/recommend", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                query: query,
                budget: budget,
                category: category
            })
        });

        const data = await response.json();

        if (!response.ok) {

            console.error(data);

            throw new Error(
                data.error || "Server error"
            );
        }

        const products = data;

        if (!products.length) {

            results.innerHTML =
                "<p>No suitable products found. Try another requirement or increase your budget.</p>";

            return;
        }

        results.innerHTML = products.map(p => `

            <div class="product">

                <div class="icon">🛍️</div>

                <div>

                    <h3>${p.name}</h3>

                    <p class="price">
                        ₹${Number(p.price).toFixed(0)}
                    </p>

                    <p>${p.description}</p>

                </div>

            </div>

        `).join("");

    } catch (error) {

        console.error(error);

        results.innerHTML =
            `<p>Unable to get recommendations.</p>
             <p>Error: ${error.message}</p>`;
    }
}


async function sendMessage() {

    const message = document
        .getElementById("message")
        .value
        .trim();

    const budget = document
        .getElementById("budget")
        .value;

    const chat = document.getElementById("chat");

    if (!message) {
        return;
    }

    chat.innerHTML =
        "<strong>Assistant:</strong> Thinking...";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message,
                budget: budget
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Server error");
        }

        chat.innerHTML =
            `<strong>Assistant:</strong> ${data.reply}`;

    } catch (error) {

        console.error(error);

        chat.innerHTML =
            `<strong>Assistant:</strong>
             Sorry, something went wrong: ${error.message}`;
    }
}
