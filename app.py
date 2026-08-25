from flask import Flask, render_template, request, jsonify
import sqlite3

from recommender import recommend_products, chat_response


app = Flask(__name__)

DB = "products.db"


def init_db():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL,
            keywords TEXT NOT NULL
        )
    """)

    cur.execute("SELECT COUNT(*) FROM products")

    count = cur.fetchone()[0]

    if count == 0:

        products = [

            (
                "HP Laptop",
                "laptop",
                45000,
                "Powerful laptop suitable for coding, studying and everyday work.",
                "laptop computer notebook coding programming student"
            ),

            (
                "Dell Laptop",
                "laptop",
                55000,
                "Reliable laptop for programming, office work and college students.",
                "laptop computer notebook coding programming college"
            ),

            (
                "Samsung Smartphone",
                "smartphone",
                18000,
                "Android smartphone with a large display and good battery life.",
                "smartphone phone mobile android samsung"
            ),

            (
                "OnePlus Smartphone",
                "smartphone",
                28000,
                "Fast smartphone with excellent performance and battery life.",
                "smartphone phone mobile android oneplus"
            ),

            (
                "Wireless Headphones",
                "headphones",
                2499,
                "Comfortable wireless headphones with clear sound and long battery life.",
                "headphones headphone music audio bluetooth wireless"
            ),

            (
                "Smart Watch",
                "smartwatch",
                3499,
                "Fitness-focused smartwatch with notifications and activity tracking.",
                "smartwatch watch fitness sport tracking"
            ),

            (
                "Laptop Backpack",
                "accessories",
                1999,
                "Water-resistant backpack with a padded laptop compartment.",
                "bag laptop college travel backpack"
            ),

            (
                "Running Shoes",
                "fashion",
                1999,
                "Lightweight running shoes designed for daily workouts.",
                "running shoes fitness sport walking"
            ),

            (
                "Cotton T-Shirt",
                "fashion",
                699,
                "Comfortable everyday cotton T-shirt.",
                "shirt cotton casual fashion"
            ),

            (
                "Bluetooth Speaker",
                "speaker",
                1799,
                "Portable speaker with Bluetooth connectivity and strong battery life.",
                "speaker bluetooth music portable audio"
            ),

            (
                "Study Lamp",
                "home",
                899,
                "LED desk lamp with adjustable brightness for studying.",
                "study lamp desk led student"
            ),

            (
                "Mechanical Keyboard",
                "keyboard",
                2999,
                "Responsive keyboard suitable for coding and gaming.",
                "keyboard mechanical coding gaming computer"
            ),

            (
                "Wireless Mouse",
                "mouse",
                999,
                "Wireless mouse suitable for laptops, computers and office work.",
                "mouse wireless computer laptop office"
            ),

            (
                "Water Bottle",
                "accessories",
                599,
                "Reusable leak-resistant bottle for college and travel.",
                "bottle water college travel"
            ),

            (
                "Power Bank",
                "power bank",
                1499,
                "Portable power bank for charging mobile devices while travelling.",
                "power bank charging mobile phone portable"
            )
        ]

        cur.executemany("""
            INSERT INTO products
            (name, category, price, description, keywords)
            VALUES (?, ?, ?, ?, ?)
        """, products)

    conn.commit()
    conn.close()


def get_all_products():

    conn = sqlite3.connect(DB)

    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        "SELECT * FROM products ORDER BY id"
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.route("/")
def home():

    return render_template(
        "index.html",
        products=get_all_products()
    )


@app.route("/recommend", methods=["POST"])
def recommend():

    try:

        data = request.get_json() or {}

        query = data.get("query", "").strip()

        budget = float(
            data.get("budget", 0) or 0
        )

        category = data.get(
            "category",
            "all"
        )

        products = get_all_products()

        results = recommend_products(
            query,
            budget,
            category,
            products
        )

        return jsonify(results)

    except Exception as e:

        print("Recommendation error:", e)

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json() or {}

        message = data.get(
            "message",
            ""
        ).strip()

        budget = float(
            data.get("budget", 0) or 0
        )

        products = get_all_products()

        reply = chat_response(
            message,
            budget,
            products
        )

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print("Chat error:", e)

        return jsonify({
            "reply": "Sorry, something went wrong."
        }), 500


if __name__ == "__main__":

    init_db()

    app.run(debug=True)
