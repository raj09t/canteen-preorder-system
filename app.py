from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from pathlib import Path
from functools import wraps
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-before-deployment"
DB_PATH = Path(__file__).with_name("canteen.db")

DEFAULT_MENU = [
    ("Ham and cheese sandwich", 5.50, "Sandwiches"),
    ("Chicken wrap", 6.50, "Sandwiches"),
    ("Veggie wrap", 6.00, "Sandwiches"),
    ("Cheese toastie", 4.50, "Hot food"),
    ("Fruit cup", 3.00, "Snacks"),
    ("Muffin", 3.50, "Snacks"),
    ("Water", 2.00, "Drinks"),
    ("Orange juice", 3.00, "Drinks"),
]

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL CHECK(price >= 0),
            category TEXT NOT NULL,
            available INTEGER NOT NULL DEFAULT 1
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            student_name TEXT NOT NULL,
            student_class TEXT NOT NULL,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Received',
            created_at TEXT NOT NULL
        )""")
        count = db.execute("SELECT COUNT(*) FROM menu").fetchone()[0]
        if count == 0:
            db.executemany(
                "INSERT INTO menu (name, price, category) VALUES (?, ?, ?)",
                DEFAULT_MENU
            )

def staff_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("staff_logged_in"):
            flash("Please log in as canteen staff first.", "warning")
            return redirect(url_for("staff_login"))
        return view(*args, **kwargs)
    return wrapped

@app.route("/")
def home():
    with connect_db() as db:
        menu = db.execute(
            "SELECT * FROM menu WHERE available = 1 ORDER BY category, name"
        ).fetchall()
    return render_template("index.html", menu=menu)

@app.route("/place-order", methods=["POST"])
def place_order():
    student_name = request.form.get("student_name", "").strip()
    student_class = request.form.get("student_class", "").strip()
    quantities = request.form.getlist("quantity")

    if not student_name or not student_class:
        flash("Please enter your name and class before submitting.", "error")
        return redirect(url_for("home"))

    order_items = []
    total = 0.0
    with connect_db() as db:
        menu = db.execute("SELECT * FROM menu WHERE available = 1").fetchall()
        for item in menu:
            try:
                qty = int(request.form.get(f"item_{item['id']}", "0"))
            except ValueError:
                qty = 0
            if qty < 0:
                qty = 0
            if qty > 0:
                line_total = item["price"] * qty
                total += line_total
                order_items.append(
                    f"{item['name']} x {qty} (${line_total:.2f})"
                )

        if not order_items:
            flash("Please choose at least one menu item.", "error")
            return redirect(url_for("home"))

        order_number = "CAN-" + secrets.token_hex(3).upper()
        db.execute(
            """INSERT INTO orders
            (order_number, student_name, student_class, items, total, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (order_number, student_name, student_class, "; ".join(order_items),
             total, "Received", datetime.now().strftime("%d %b %Y, %I:%M %p"))
        )

    return render_template("confirmation.html", order_number=order_number,
                           student_name=student_name, total=total,
                           order_items=order_items)

@app.route("/staff/login", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # Demo-only login. Replace with securely stored accounts for a real system.
        if username == "staff" and password == "ChangeMe123!":
            session["staff_logged_in"] = True
            flash("You are now logged in.", "success")
            return redirect(url_for("dashboard"))
        flash("Incorrect username or password.", "error")
    return render_template("login.html")

@app.route("/staff/logout")
def staff_logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@app.route("/staff")
@staff_required
def dashboard():
    with connect_db() as db:
        orders = db.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
        menu = db.execute("SELECT * FROM menu ORDER BY category, name").fetchall()
    return render_template("dashboard.html", orders=orders, menu=menu)

@app.route("/staff/order/<int:order_id>/status", methods=["POST"])
@staff_required
def update_status(order_id):
    status = request.form.get("status", "")
    allowed = {"Received", "Preparing", "Ready for collection", "Collected"}
    if status not in allowed:
        flash("That order status is not valid.", "error")
    else:
        with connect_db() as db:
            db.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
        flash("Order status updated.", "success")
    return redirect(url_for("dashboard"))

@app.route("/staff/menu/add", methods=["POST"])
@staff_required
def add_menu_item():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    try:
        price = float(request.form.get("price", ""))
    except ValueError:
        price = -1
    if not name or not category or price < 0:
        flash("Enter a valid item name, category and price.", "error")
    else:
        with connect_db() as db:
            db.execute("INSERT INTO menu (name, price, category) VALUES (?, ?, ?)",
                       (name, price, category))
        flash("Menu item added.", "success")
    return redirect(url_for("dashboard"))

@app.route("/staff/menu/<int:item_id>/availability", methods=["POST"])
@staff_required
def toggle_menu_item(item_id):
    with connect_db() as db:
        db.execute("UPDATE menu SET available = CASE available WHEN 1 THEN 0 ELSE 1 END WHERE id = ?",
                   (item_id,))
    flash("Menu availability updated.", "success")
    return redirect(url_for("dashboard"))

@app.route("/health")
def health():
    return {"status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(debug=True)
