
import sqlite3

DB_FILE = "pharmeasy.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

print("=== JOIN VALIDATION ===")

cur.execute("""
SELECT COUNT(*)
FROM regions_master r
LEFT JOIN orders_clean o
ON r.region = o.region
""")
print("LEFT JOIN rows:", cur.fetchone()[0])

cur.execute("""
SELECT COUNT(*)
FROM regions_master r
INNER JOIN orders_clean o
ON r.region = o.region
""")
print("INNER JOIN rows:", cur.fetchone()[0])

cur.execute("""
SELECT order_id, COUNT(*)
FROM orders_clean
GROUP BY order_id
HAVING COUNT(*) > 1
""")
duplicate_order_ids = cur.fetchall()
print("Duplicate order_id groups:", len(duplicate_order_ids))

print("\n=== REGION ORDER COUNTS ===")

cur.execute("""
SELECT
    r.region,
    COUNT(o.order_id) AS order_count
FROM regions_master r
LEFT JOIN orders_clean o
ON r.region = o.region
GROUP BY r.region
ORDER BY order_count, r.region
""")

for row in cur.fetchall():
    print(row)

print("\n=== MONTHLY SALES BY REGION ===")

cur.execute("""
SELECT
    region,
    substr(order_date, 1, 7) AS month,
    ROUND(SUM(sales_inr), 2) AS sales
FROM orders_clean
GROUP BY region, month
ORDER BY region, month
""")

for row in cur.fetchall():
    print(row)

conn.close()
