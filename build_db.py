
import sqlite3
import csv

DB_FILE = "pharmeasy.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS regions_master")
cur.execute("DROP TABLE IF EXISTS orders_clean")

cur.execute("""
CREATE TABLE regions_master (
    region TEXT,
    state TEXT,
    tier TEXT
)
""")

cur.execute("""
CREATE TABLE orders_clean (
    order_id TEXT,
    order_date TEXT,
    region TEXT,
    category TEXT,
    product TEXT,
    quantity INTEGER,
    sales_inr REAL,
    profit_inr REAL
)
""")

with open("regions_master.csv", newline="") as f:
    reader = csv.DictReader(f)
    cur.executemany(
        "INSERT INTO regions_master VALUES (?, ?, ?)",
        [(r["region"], r["state"], r["tier"]) for r in reader]
    )

with open("orders_clean.csv", newline="") as f:
    reader = csv.DictReader(f)
    cur.executemany(
        "INSERT INTO orders_clean VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                r["order_id"],
                r["order_date"],
                r["region"],
                r["category"],
                r["product"],
                int(r["quantity"]),
                float(r["sales_inr"]),
                float(r["profit_inr"])
            )
            for r in reader
        ]
    )

conn.commit()
conn.close()

print("pharmeasy.db created successfully")
