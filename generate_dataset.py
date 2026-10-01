
import random
import csv
from datetime import date, timedelta

random.seed(2026)

REGIONS_ACTIVE = [
    "Hyderabad",
    "Bengaluru",
    "Vijayawada",
    "Visakhapatnam",
    "Warangal",
    "Guntur",
    "Tirupati",
    "Nellore",
    "Karimnagar"
]

REGIONS_MASTER = REGIONS_ACTIVE + ["Kurnool"]

STATES = {
    "Hyderabad": "Telangana",
    "Bengaluru": "Karnataka",
    "Vijayawada": "Andhra Pradesh",
    "Visakhapatnam": "Andhra Pradesh",
    "Warangal": "Telangana",
    "Guntur": "Andhra Pradesh",
    "Tirupati": "Andhra Pradesh",
    "Nellore": "Andhra Pradesh",
    "Karimnagar": "Telangana",
    "Kurnool": "Andhra Pradesh"
}

TIERS = {
    "Hyderabad": "Tier 1",
    "Bengaluru": "Tier 1",
    "Vijayawada": "Tier 2",
    "Visakhapatnam": "Tier 2",
    "Warangal": "Tier 2",
    "Guntur": "Tier 2",
    "Tirupati": "Tier 2",
    "Nellore": "Tier 2",
    "Karimnagar": "Tier 2",
    "Kurnool": "Tier 2"
}

CATEGORIES = [
    "Medicines",
    "Personal Care",
    "Baby Care",
    "Health Devices",
    "Vitamins",
    "Wellness"
]

PRODUCTS = {
    "Medicines": ["Paracetamol", "Antacid", "Cough Syrup"],
    "Personal Care": ["Face Wash", "Shampoo", "Body Lotion"],
    "Baby Care": ["Baby Diapers", "Baby Wipes", "Baby Lotion"],
    "Health Devices": ["Thermometer", "BP Monitor", "Glucometer"],
    "Vitamins": ["Vitamin C", "Multivitamin", "Calcium"],
    "Wellness": ["Protein Powder", "ORS", "Herbal Tea"]
}

BASE_PRICES = {
    "Paracetamol": 120,
    "Antacid": 150,
    "Cough Syrup": 180,
    "Face Wash": 220,
    "Shampoo": 250,
    "Body Lotion": 210,
    "Baby Diapers": 550,
    "Baby Wipes": 180,
    "Baby Lotion": 240,
    "Thermometer": 350,
    "BP Monitor": 1600,
    "Glucometer": 1200,
    "Vitamin C": 300,
    "Multivitamin": 450,
    "Calcium": 280,
    "Protein Powder": 1400,
    "ORS": 100,
    "Herbal Tea": 250
}

REGION_WEIGHTS = {
    "Hyderabad": 0.24,
    "Bengaluru": 0.16,
    "Vijayawada": 0.13,
    "Visakhapatnam": 0.09,
    "Warangal": 0.09,
    "Guntur": 0.09,
    "Tirupati": 0.07,
    "Nellore": 0.07,
    "Karimnagar": 0.06
}

rows = []

start_date = date(2026, 4, 1)

order_number = 1

for month_index in range(3):
    month_start = date(2026, 4 + month_index, 1)

    if month_index == 2:
        next_month = date(2026, 7, 1)
    else:
        next_month = date(2026, 5 + month_index, 1)

    days_in_month = (next_month - month_start).days

    for _ in range(700):

        region = random.choices(
            REGIONS_ACTIVE,
            weights=[REGION_WEIGHTS[r] for r in REGIONS_ACTIVE],
            k=1
        )[0]

        category = random.choice(CATEGORIES)
        product = random.choice(PRODUCTS[category])

        quantity = random.randint(1, 5)

        price = BASE_PRICES[product]
        sales = round(price * quantity * random.uniform(0.85, 1.15), 2)

        margin = random.uniform(0.10, 0.20)
        profit = round(sales * margin, 2)

        order_date = month_start + timedelta(
            days=random.randint(0, days_in_month - 1)
        )

        rows.append([
            f"ORD{order_number:05d}",
            order_date.isoformat(),
            region,
            category,
            product,
            quantity,
            sales,
            profit
        ])

        order_number += 1

# Introduce missing values
for index in random.sample(range(len(rows)), 48):
    rows[index][3] = ""

for index in random.sample(range(len(rows)), 94):
    rows[index][7] = ""

# Introduce messy region names
messy_variants = {
    "Hyderabad": " hyderabad ",
    "Bengaluru": " bengaluru",
    "Vijayawada": "VIJAYAWADA ",
    "Visakhapatnam": " visakhapatnam",
    "Warangal": "WARANGAL",
    "Guntur": " guntur ",
    "Tirupati": "TIRUPATI ",
    "Nellore": " nellore",
    "Karimnagar": " KARIMNAGAR "
}

for index in random.sample(range(len(rows)), 161):
    original = rows[index][2]
    rows[index][2] = messy_variants[original]

# Add 59 exact duplicate rows
rows.extend(random.sample(rows, 59))

assert len(rows) == 2159

with open("pharmeasy_orders_raw.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "order_id",
        "order_date",
        "region",
        "category",
        "product",
        "quantity",
        "sales_inr",
        "profit_inr"
    ])
    writer.writerows(rows)

with open("regions_master.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["region", "state", "tier"])

    for region in REGIONS_MASTER:
        writer.writerow([
            region,
            STATES[region],
            TIERS[region]
        ])

print("Dataset generated successfully")
print("Raw orders:", len(rows))
print("Regions master:", len(REGIONS_MASTER))
