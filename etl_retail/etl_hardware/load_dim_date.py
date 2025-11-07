import pandas as pd
import psycopg2
from datetime import datetime

start = datetime(2024, 10, 1)
end = datetime(2024, 11, 30)

dates = pd.date_range(start, end)

df = pd.DataFrame({
    "date_id": dates.strftime("%Y%m%d").astype(int),
    "full_date": dates,
    "year": dates.year,
    "quarter": dates.quarter,
    "month": dates.month,
    "month_name": dates.strftime("%B"),
    "day": dates.day,
    "day_of_week": dates.strftime("%A"),
})

df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])

conn = psycopg2.connect("dbname=silo user=postgres password=postgres host=localhost")
cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO dim.dim_date (
            date_id, full_date, year, quarter, month, month_name,
            day, day_of_week, is_weekend
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (date_id) DO NOTHING;
    """, tuple(row))

conn.commit()
cur.close()
conn.close()

print("dim_date loaded!")
