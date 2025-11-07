import pandas as pd
import psycopg2
import glob

files = glob.glob("./data/pos_exports/*.csv")
df = pd.concat([pd.read_csv(f, encoding="cp1252") for f in files])

dim = df[["employee"]].drop_duplicates()
dim["employee_id"] = dim["employee"]

conn = psycopg2.connect("dbname=silo user=postgres password=postgres host=localhost")
cur = conn.cursor()

for _, row in dim.iterrows():
    cur.execute("""
        INSERT INTO dim.dim_employees (employee_id, employee_name)
        VALUES (%s,%s)
        ON CONFLICT (employee_id)
        DO NOTHING;
    """, (row["employee"], row["employee"]))

conn.commit()
cur.close()
conn.close()

print("dim_employees loaded!")
