import os
import pandas as pd
from datetime import datetime

# Define paths
RAW_PATH = os.path.join("data", "raw", "retail_orders.json")
PROCESSED_DIR = os.path.join("data", "processed")
PROCESSED_PATH = os.path.join(PROCESSED_DIR, "retail_orders_clean.csv")

# Ensure processed directory exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

def load_data(path):
    print(f"📥 Loading data from {path}...")
    df = pd.read_json(path)
    print(f"✅ Loaded {len(df)} records")
    return df

def clean_transform(df):
    print("🛠️ Cleaning and transforming data...")

    # Combine first & last name
    df["customer_name"] = df["first_name"].str.strip().str.title() + " " + df["last_name"].str.strip().str.title()

    # Normalize strings
    df["product_name"] = df["product_name"].str.strip().str.title()
    df["category"] = df["category"].str.strip().str.title()

    # Convert order_date to datetime
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Ensure 'total' is numeric
    df["total"] = pd.to_numeric(df["total"], errors="coerce")

    # Add order_month for reporting
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

    # Flag high value orders
    df["is_high_value"] = df["total"] > 500

    # Drop unnecessary columns
    df.drop(columns=["first_name", "last_name"], inplace=True)

    print("✅ Transformation complete")
    return df


def save_data(df, path):
    df.to_json(path, orient="records", indent=2, date_format="iso")
    print(f"💾 Saved cleaned data to {path}")

def main():
    df = load_data(RAW_PATH)
    df_clean = clean_transform(df)
    save_data(df_clean, PROCESSED_PATH)

if __name__ == "__main__":
    main()
