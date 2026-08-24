import re

STOP_WORDS = {
    "i", "need", "want", "a", "an", "the", "for", "under", "with",
    "my", "me", "to", "and", "please", "buy", "looking", "something"
}

def tokenize(text):
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [w for w in words if w not in STOP_WORDS]

def recommend_products(query, budget, category, products):
    query_words = set(tokenize(query))
    scored = []

    for p in products:
        if category != "all" and p["category"].lower() != category.lower():
            continue
        if budget > 0 and p["price"] > budget:
            continue

        searchable = set(tokenize(
            f'{p["name"]} {p["category"]} {p["description"]} {p["keywords"]}'
        ))
        matches = len(query_words.intersection(searchable))
        score = matches * 10

        if budget > 0:
            # Prefer products that fit comfortably within the budget.
            score += max(0, 5 - (budget - p["price"]) / max(budget, 1) * 5)

        if matches > 0:
            scored.append((score, p))

    # If no keyword matches, show affordable products as fallback.
    if not scored:
        candidates = [
            p for p in products
            if (category == "all" or p["category"].lower() == category.lower())
            and (budget <= 0 or p["price"] <= budget)
        ]
        candidates.sort(key=lambda x: x["price"])
        return candidates[:4]

    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:4]]

def chat_response(message, budget, products):
    msg = message.lower()

    if any(word in msg for word in ["hello", "hi", "hey"]):
        return "Hello! Tell me what product you need, your preferred category, and your budget."

    results = recommend_products(message, budget, "all", products)
    if not results:
        return "I could not find a suitable product. Try a different requirement or increase your budget."

    names = ", ".join(p["name"] for p in results[:3])
    return f"Based on your requirement, I recommend: {names}. These suggestions are ranked using your keywords and budget."
