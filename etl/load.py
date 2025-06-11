# etl/load.py

import os
import pandas as pd

def load_to_files(df, filename="retail_orders_clean"):
    output_dir = os.path.join("data", "processed")
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, f"{filename}.csv")
    json_path = os.path.join(output_dir, f"{filename}.json")

    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2)

    print(f"✅ Saved CSV to: {csv_path}")
    print(f"✅ Saved JSON to: {json_path}")

def main():
    input_path = os.path.join( "data", "processed", "retail_orders_clean.json")
    
    if not os.path.exists(input_path):
        print("❌ Transformed data not found. Run transform.py first.")
        return

    df = pd.read_json(input_path)
    load_to_files(df)

if __name__ == "__main__":
    main()
