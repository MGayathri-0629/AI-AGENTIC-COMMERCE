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
    if cur.fetchone()[0] == 0:
        products = [
            ("Wireless Headphones", "electronics", 2499, "Comfortable wireless headphones with clear sound and long battery life.", "music audio bluetooth wireless travel"),
            ("Smart Watch", "electronics", 3499, "Fitness-focused smartwatch with notifications and activity tracking.", "fitness watch health sport smartwatch"),
            ("Laptop Backpack", "accessories", 1299, "Water-resistant backpack with a padded laptop compartment.", "bag laptop college travel backpack"),
            ("Running Shoes", "fashion", 1999, "Lightweight running shoes designed for daily workouts.", "running shoes fitness sport walking"),
            ("Cotton T-Shirt", "fashion", 699, "Comfortable everyday cotton T-shirt.", "shirt cotton casual fashion"),
            ("Bluetooth Speaker", "electronics", 1799, "Portable speaker with Bluetooth connectivity and strong battery life.", "speaker music bluetooth portable"),
            ("Study Lamp", "home", 899, "LED desk lamp with adjustable brightness for studying.", "study lamp desk led student"),
            ("Mechanical Keyboard", "electronics", 2999, "Responsive keyboard suitable for coding and gaming.", "keyboard coding gaming computer"),
            ("Water Bottle", "accessories", 599, "Reusable leak-resistant bottle for college and travel.", "bottle water college travel"),
            ("Power Bank", "electronics", 1499, "Portable power bank for charging devices while travelling.", "power bank charging mobile travel")
        ]
        cur.executemany(
            "INSERT INTO products (name, category, price, description, keywords) VALUES (?, ?, ?, ?, ?)",
            products
        )
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.route("/")
def home():
    return render_template("index.html", products=get_all_products())

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    budget = float(data.get("budget", 0) or 0)
    category = data.get("category", "all")
    results = recommend_products(query, budget, category, get_all_products())
    return jsonify(results)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    budget = float(data.get("budget", 0) or 0)
    return jsonify({"reply": chat_response(message, budget, get_all_products())})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
