import csv
import random
from datetime import datetime, timedelta

# Load products
products = []
with open("./data/products.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        products.append(row)


employees = ["John", "Mary", "Peter", "Lucy"]
payment_methods = ["MPESA", "CASH", "CARD", "BANK_TRANSFER"]

start = datetime(2024, 10, 1)
days = 30  
tx_per_day = (200, 500)

for d in range(days):
    current_date = start + timedelta(days=d)
    filename = f"./data/pos_exports/{current_date.strftime('%Y-%m-%d')}-sales.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "transaction_id","date","sku","product_name",
            "quantity","unit_cost","unit_price","payment_method",
            "supplier","category","employee","discount"
        ])

        tx_count = random.randint(*tx_per_day)

        for n in range(tx_count):
            p = random.choice(products)
            qty = random.randint(1, 10)

            # occasional returns
            if random.random() < 0.02:
                qty *= -1

            discount = random.choice([0, 0, 0, 5, 10])

            ts = current_date + timedelta(
                hours=random.randint(8, 17),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )

            writer.writerow([
                f"{current_date.strftime('%Y%m%d')}-{n:04d}",
                ts.strftime("%Y-%m-%d %H:%M:%S"),
                p["sku"], p["product_name"], qty,
                p["unit_cost"], p["unit_price"],
                random.choice(payment_methods),
                p["supplier"], p["category"],
                random.choice(employees),
                discount
            ])

print("Generated fake POS data.")
