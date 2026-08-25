import re


STOP_WORDS = {
    "i", "need", "want", "a", "an", "the", "for",
    "under", "with", "my", "me", "to", "and",
    "please", "buy", "looking", "something",
    "show", "give", "find", "get", "in", "on",
    "is", "of", "within", "budget"
}


CATEGORY_KEYWORDS = {
    "laptop": [
        "laptop", "notebook", "computer", "pc"
    ],

    "smartphone": [
        "smartphone", "phone", "mobile",
        "android", "iphone"
    ],

    "headphones": [
        "headphone", "headphones",
        "earphone", "earphones",
        "headset", "earbuds"
    ],

    "keyboard": [
        "keyboard", "mechanical keyboard"
    ],

    "mouse": [
        "mouse", "wireless mouse", "gaming mouse"
    ],

    "monitor": [
        "monitor", "display", "screen"
    ],

    "tablet": [
        "tablet", "ipad"
    ],

    "power bank": [
        "powerbank", "power bank",
        "portable charger"
    ],

    "speaker": [
        "speaker", "bluetooth speaker",
        "portable speaker"
    ],

    "smartwatch": [
        "smartwatch", "smart watch"
    ],

    "shoes": [
        "shoes", "running shoes",
        "footwear"
    ],

    "fashion": [
        "shirt", "t-shirt", "clothes",
        "fashion", "dress"
    ],

    "home": [
        "lamp", "study lamp",
        "home", "desk"
    ],

    "accessories": [
        "bag", "backpack", "bottle",
        "accessory", "accessories"
    ]
}


def tokenize(text):
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [word for word in words if word not in STOP_WORDS]


def detect_category(query):
    query_lower = query.lower()

    # Check longer phrases first
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in query_lower:
                return category

    return "all"


def category_matches(product, category):

    if category == "all":
        return True

    product_name = product["name"].lower()
    product_category = product["category"].lower()
    product_keywords = product["keywords"].lower()

    # Electronics means all electronic products
    if category == "electronics":
        electronic_categories = {
            "laptop",
            "smartphone",
            "headphones",
            "keyboard",
            "mouse",
            "monitor",
            "tablet",
            "power bank",
            "speaker",
            "smartwatch"
        }

        return product_category in electronic_categories

    # Direct category match
    if product_category == category:
        return True

    # Check category keywords against product information
    if category in CATEGORY_KEYWORDS:

        for keyword in CATEGORY_KEYWORDS[category]:

            if keyword in product_name:
                return True

            if keyword in product_category:
                return True

            if keyword in product_keywords:
                return True

    return False


def recommend_products(query, budget, category, products):

    query_words = set(tokenize(query))

    # Automatically detect category from user's text
    detected_category = detect_category(query)

    if detected_category != "all":
        category = detected_category

    scored = []

    for product in products:

        # Category filtering
        if not category_matches(product, category):
            continue

        # Budget filtering
        if budget > 0 and product["price"] > budget:
            continue

        searchable_text = (
            f'{product["name"]} '
            f'{product["category"]} '
            f'{product["description"]} '
            f'{product["keywords"]}'
        ).lower()

        searchable_words = set(tokenize(searchable_text))

        # Count matching keywords
        matches = query_words.intersection(searchable_words)

        score = len(matches) * 10

        # Strong category bonus
        if detected_category != "all":
            if category_matches(product, detected_category):
                score += 50

        # Exact product-name bonus
        if product["name"].lower() in query.lower():
            score += 50

        # Budget preference
        if budget > 0:

            difference = budget - product["price"]

            if difference >= 0:

                budget_score = 5 - (
                    difference / max(budget, 1) * 5
                )

                score += max(0, budget_score)

        # Only show relevant products
        if score > 0:

            scored.append(
                (score, product)
            )

    # Nothing found
    if not scored:
        return []

    # Highest score first
    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        product
        for _, product in scored[:4]
    ]


def chat_response(message, budget, products):

    msg = message.lower().strip()

    # Greeting
    if msg in ["hello", "hi", "hey", "hai"]:

        return (
            "Hello! 👋 Tell me the product you need "
            "and your budget. For example: "
            "'I need a laptop under 50000'."
        )

    results = recommend_products(
        message,
        budget,
        "all",
        products
    )

    if not results:

        return (
            "I could not find a suitable product. "
            "Please try another product or increase your budget."
        )

    names = ", ".join(
        product["name"]
        for product in results[:3]
    )

    return (
        f"Based on your requirement, I recommend: {names}. "
        "These products were selected based on your "
        "product type, keywords, and budget."
    )
