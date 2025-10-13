import os
import sqlite3
import random
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta

DATABASE = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "tps.db"))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")


def get_conn():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS customers (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          email TEXT UNIQUE
        );
        CREATE TABLE IF NOT EXISTS products (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          price REAL NOT NULL CHECK(price >= 0),
          stock INTEGER NOT NULL CHECK(stock >= 0)
        );
        CREATE TABLE IF NOT EXISTS sales (
          id INTEGER PRIMARY KEY,
          customer_id INTEGER NOT NULL,
          total REAL NOT NULL,
          created_at TEXT NOT NULL,
          FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
        CREATE TABLE IF NOT EXISTS sale_items (
          id INTEGER PRIMARY KEY,
          sale_id INTEGER NOT NULL,
          product_id INTEGER NOT NULL,
          qty INTEGER NOT NULL CHECK(qty > 0),
          unit_price REAL NOT NULL,
          FOREIGN KEY (sale_id) REFERENCES sales(id),
          FOREIGN KEY (product_id) REFERENCES products(id)
        );
        CREATE TABLE IF NOT EXISTS txn_log (
          id INTEGER PRIMARY KEY,
          type TEXT NOT NULL,
          payload TEXT,
          status TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        """
    )
    conn.commit()

    # Seed básico de clientes y productos
    basic_seed(conn)
    # Generar ventas si no existen para el dashboard
    seed_sales(conn, only_if_empty=True)
    conn.close()


@app.route("/")
def index():
    conn = get_conn()
    products = conn.execute("SELECT * FROM products").fetchall()
    customers = conn.execute("SELECT * FROM customers").fetchall()
    sales = conn.execute(
        "SELECT s.id, c.name AS customer, s.total, s.created_at FROM sales s JOIN customers c ON c.id = s.customer_id ORDER BY s.id DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", products=products, customers=customers, sales=sales)


def create_sale(conn, customer_id, items, created_at_override=None):
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        total = 0.0
        # Validar stock y calcular total
        for pid, qty in items:
            row = cur.execute("SELECT price, stock FROM products WHERE id = ?", (pid,)).fetchone()
            if not row:
                raise ValueError("Producto inexistente")
            price, stock = row
            if stock < qty:
                raise ValueError("Stock insuficiente")
            total += price * qty
        # Registrar venta
        created_at = created_at_override or datetime.utcnow().isoformat()
        cur.execute(
            "INSERT INTO sales(customer_id,total,created_at) VALUES(?,?,?)",
            (customer_id, total, created_at),
        )
        sale_id = cur.lastrowid
        # Registrar ítems y actualizar stock
        for pid, qty in items:
            unit_price = cur.execute("SELECT price FROM products WHERE id = ?", (pid,)).fetchone()[0]
            cur.execute(
                "INSERT INTO sale_items(sale_id,product_id,qty,unit_price) VALUES(?,?,?,?)",
                (sale_id, pid, qty, unit_price),
            )
            cur.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, pid))
        conn.commit()
        cur.execute(
            "INSERT INTO txn_log(type,payload,status,created_at) VALUES (?,?,?,?)",
            (
                "sale",
                str({"customer_id": customer_id, "items": items}),
                "committed",
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        return {"sale_id": sale_id, "total": total}
    except Exception as e:
        conn.rollback()
        cur.execute(
            "INSERT INTO txn_log(type,payload,status,created_at) VALUES (?,?,?,?)",
            (
                "sale",
                str({"customer_id": customer_id, "items": items}),
                f"rolled_back: {str(e)}",
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        return {"error": str(e)}


def basic_seed(conn):
    cur = conn.cursor()
    # Clientes
    cur.execute("SELECT COUNT(*) AS c FROM customers")
    if cur.fetchone()["c"] == 0:
        cur.executemany(
            "INSERT INTO customers(name,email) VALUES (?,?)",
            [
                ("Cliente Demo", "demo@example.com"),
                ("Alice", "alice@example.com"),
                ("Bob", "bob@example.com"),
                ("Carlos", "carlos@example.com"),
                ("Diana", "diana@example.com"),
            ],
        )
    # Productos
    cur.execute("SELECT COUNT(*) AS c FROM products")
    if cur.fetchone()["c"] < 10:
        products = [
            ("Café Molido 250g", 4.50, 200),
            ("Té Verde 100g", 3.20, 180),
            ("Azúcar 1kg", 1.90, 300),
            ("Arroz 1kg", 2.10, 250),
            ("Aceite 1L", 5.75, 220),
            ("Leche 1L", 1.30, 260),
            ("Pan Integral", 2.40, 150),
            ("Huevos Docena", 2.80, 190),
            ("Queso 500g", 6.50, 140),
            ("Yogur 1L", 3.10, 170),
        ]
        cur.executemany("INSERT INTO products(name,price,stock) VALUES (?,?,?)", products)
    conn.commit()


def seed_sales(conn, only_if_empty=False, num_days=10, sales_per_day=3):
    cur = conn.cursor()
    if only_if_empty:
        cnt = cur.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        if cnt > 0:
            return
    customers = [r[0] for r in cur.execute("SELECT id FROM customers").fetchall()]
    products = [(r[0], r[1]) for r in cur.execute("SELECT id, price FROM products").fetchall()]
    if not customers or not products:
        return
    random.seed(42)
    start = datetime.utcnow() - timedelta(days=num_days)
    for d in range(num_days):
        day = start + timedelta(days=d)
        for _ in range(sales_per_day):
            customer_id = random.choice(customers)
            num_items = random.randint(1, 3)
            items = []
            chosen = random.sample(products, k=min(num_items, len(products)))
            for pid, _price in chosen:
                qty = random.randint(1, 5)
                items.append((pid, qty))
            create_sale(conn, customer_id, items, created_at_override=day.isoformat())
    conn.commit()


@app.route("/sale", methods=["POST"]) 
def sale():
    customer_id = int(request.form.get("customer_id"))
    items = []
    for key in request.form.keys():
        if key.startswith("qty_"):
            pid = int(key.split("_")[1])
            qty_str = request.form.get(key)
            try:
                qty = int(qty_str)
            except ValueError:
                qty = 0
            if qty > 0:
                items.append((pid, qty))
    conn = get_conn()
    result = create_sale(conn, customer_id, items)
    conn.close()
    if "error" in result:
        flash(f"Error: {result['error']}")
    else:
        flash(f"Venta registrada (ID {result['sale_id']}) Total: {result['total']}")
    return redirect(url_for("index"))


@app.route("/api/products")
def api_products():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/sales")
def api_sales():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM sales ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# --- Estadísticas y Dashboard ---
@app.route("/api/stats/summary")
def api_stats_summary():
    conn = get_conn()
    cur = conn.cursor()
    total_sales, total_revenue = cur.execute(
        "SELECT COUNT(*) AS c, COALESCE(SUM(total),0) AS r FROM sales"
    ).fetchone()
    products_count = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    customers_count = cur.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    conn.close()
    return jsonify(
        {
            "total_sales": total_sales,
            "total_revenue": total_revenue,
            "products_count": products_count,
            "customers_count": customers_count,
        }
    )


@app.route("/api/stats/sales_by_date")
def api_stats_sales_by_date():
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT substr(created_at,1,10) AS date,
               COUNT(*) AS count,
               COALESCE(SUM(total),0) AS revenue
        FROM sales
        GROUP BY date
        ORDER BY date
        """
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/stats/top_products")
def api_stats_top_products():
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT p.name AS product,
               COALESCE(SUM(si.qty),0) AS qty,
               COALESCE(SUM(si.qty*si.unit_price),0) AS revenue
        FROM sale_items si
        JOIN products p ON p.id = si.product_id
        GROUP BY si.product_id
        ORDER BY qty DESC
        LIMIT 5
        """
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/stats/stock")
def api_stats_stock():
    conn = get_conn()
    rows = conn.execute("SELECT name AS product, stock FROM products ORDER BY stock DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/seed")
def seed_endpoint():
    conn = get_conn()
    seed_sales(conn, only_if_empty=False, num_days=14, sales_per_day=5)
    conn.close()
    flash("Datos de ejemplo generados correctamente.")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))