import os
import glob
import pandas as pd
from datetime import datetime
import yaml
import psycopg2

# ---------------------------------------------------------------------
# Load configuration
# ---------------------------------------------------------------------
with open("./config/hardware.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

POS_FOLDER = cfg["etl"]["pos_path"]
CONN_STR = cfg["etl"]["db"]

# ---------------------------------------------------------------------
# Database helper
# ---------------------------------------------------------------------
def connect():
    return psycopg2.connect(CONN_STR)

# ---------------------------------------------------------------------
# Get last processed timestamp
# ---------------------------------------------------------------------
def get_last_processed_ts(cur):
    cur.execute("""
        SELECT last_processed_ts
        FROM meta.etl_markers
        WHERE source_name = 'hardware_pos';
    """)
    row = cur.fetchone()
    return row[0] if row else None

# ---------------------------------------------------------------------
# Update last processed timestamp
# ---------------------------------------------------------------------
def update_last_processed_ts(cur, ts):
    cur.execute("""
        INSERT INTO meta.etl_markers (source_name, last_processed_ts)
        VALUES ('hardware_pos', %s)
        ON CONFLICT (source_name)
        DO UPDATE SET last_processed_ts = excluded.last_processed_ts;
    """, (ts,))

# ---------------------------------------------------------------------
# Load all CSVs incrementally
# ---------------------------------------------------------------------
def load_pos_files(last_ts):
    files = sorted(glob.glob(f"{POS_FOLDER}/*.csv"))
    df_list = []

    for file in files:
        df = pd.read_csv(file, encoding="cp1252")

        df["date"] = pd.to_datetime(df["date"])
        # incremental logic
        if last_ts:
            df = df[df["date"] > last_ts]

        if not df.empty:
            df_list.append(df)

    return pd.concat(df_list) if df_list else pd.DataFrame()

# ---------------------------------------------------------------------
# Transform fields
# ---------------------------------------------------------------------
def transform(df):
    df["total_amount"] = df["quantity"] * (df["unit_price"] - df["discount"])
    df["profit"] = (df["unit_price"] - df["unit_cost"]) * df["quantity"]
    df["date_id"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    return df

# ---------------------------------------------------------------------
# Insert into warehouse
# ---------------------------------------------------------------------
def insert_fact(cur, df):
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO fact.fact_pos_sales (
                sale_id, sale_ts, date_id, sku, quantity, unit_cost, unit_price,
                discount, total_amount, profit, payment_method, employee_id
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (sale_id) DO NOTHING;
        """, (
            row["transaction_id"], row["date"], row["date_id"], row["sku"],
            row["quantity"], row["unit_cost"], row["unit_price"],
            row["discount"], row["total_amount"], row["profit"],
            row["payment_method"], row["employee"]
        ))

# ---------------------------------------------------------------------
# Inventory movement tracking
# ---------------------------------------------------------------------
def insert_inventory_movements(cur, df):
    for _, row in df.iterrows():
        mov_type = "SALE" if row["quantity"] > 0 else "RETURN"
        cur.execute("""
            INSERT INTO fact.fact_inventory_movements (
                sku, movement_ts, movement_type, quantity, reference_id
            ) VALUES (%s,%s,%s,%s,%s);
        """, (
            row["sku"], row["date"], mov_type, row["quantity"], row["transaction_id"]
        ))

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main():
    conn = connect()
    cur = conn.cursor()

    last_ts = get_last_processed_ts(cur)
    df = load_pos_files(last_ts)

    if df.empty:
        print("No new records.")
        return

    df = transform(df)

    insert_fact(cur, df)
    insert_inventory_movements(cur, df)

    # update watermark
    max_ts = df["date"].max()
    update_last_processed_ts(cur, max_ts)

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Loaded {len(df)} records (up to {max_ts}).")

if __name__ == "__main__":
    main()
