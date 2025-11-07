import pandas as pd
import psycopg2
import glob

files = glob.glob("./data/pos_exports/*.csv")
df = pd.concat([pd.read_csv(f, encoding="cp1252") for f in files])

dim = df[["sku","product_name","category","supplier"]].drop_duplicates()

conn = psycopg2.connect("dbname=silo user=postgres password=postgres host=localhost")
cur = conn.cursor()

for _, row in dim.iterrows():
    cur.execute("""
        INSERT INTO dim.dim_products (sku, product_name, category, supplier)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT (sku)
        DO NOTHING;
    """, tuple(row))

conn.commit()
cur.close()
conn.close()

print("dim_products loaded!")
