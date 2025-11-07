import psycopg2
import pandas as pd

conn = psycopg2.connect("dbname=silo user=postgres password=postgres host=localhost")
cur = conn.cursor()


cur.execute("""
    SELECT sku, current_stock
    FROM fact.vw_inventory_position
    WHERE current_stock < 50;
""")
rows = cur.fetchall()

for sku, stock in rows:
    cur.execute("""
        INSERT INTO alerts.alert_log (alert_type, sku, description, severity, current_value, threshold)
        VALUES ('LOW_STOCK', %s, 'Stock below safety level', 'HIGH', %s, 50);
    """, (sku, stock))

cur.execute("""
    SELECT sku, SUM(profit) AS total_profit
    FROM fact.fact_pos_sales
    GROUP BY sku
    HAVING SUM(profit) < 0;
""")
rows = cur.fetchall()

for sku, profit in rows:
    cur.execute("""
        INSERT INTO alerts.alert_log (alert_type, sku, description, severity, current_value, threshold)
        VALUES ('NEGATIVE_MARGIN', %s, 'Selling below cost', 'CRITICAL', %s, 0);
    """, (sku, profit))

cur.execute("""
    SELECT p.sku
    FROM dim.dim_products p
    LEFT JOIN fact.fact_pos_sales f ON p.sku = f.sku
           AND f.sale_ts >= NOW() - INTERVAL '14 days'
    GROUP BY p.sku
    HAVING COUNT(f.sale_id) = 0;
""")
rows = cur.fetchall()

for sku, in rows:
    cur.execute("""
        INSERT INTO alerts.alert_log (alert_type, sku, description, severity)
        VALUES ('SLOW_MOVING', %s, 'No sales in the past 14 days', 'MEDIUM');
    """, (sku,))

cur.execute("""
    WITH stats AS (
        SELECT
            sku,
            SUM(CASE WHEN quantity < 0 THEN ABS(quantity) ELSE 0 END) AS returns,
            SUM(CASE WHEN quantity > 0 THEN quantity ELSE 0 END) AS sales
        FROM fact.fact_pos_sales
        GROUP BY sku
    )
    SELECT sku, returns::float / sales AS ratio
    FROM stats
    WHERE sales > 0 AND (returns::float / sales) > 0.08;
""")
rows = cur.fetchall()

for sku, ratio in rows:
    cur.execute("""
        INSERT INTO alerts.alert_log (alert_type, sku, description, severity, current_value, threshold)
        VALUES ('HIGH_RETURN_RATE', %s, 'High customer return ratio', 'MEDIUM', %s, 0.08);
    """, (sku, ratio))


conn.commit()
cur.close()
conn.close()

print("Alerts generated!")
