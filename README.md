#  SILO — Retail Data Engineering & BI Pipeline

SILO is a production-style data engineering and business intelligence system built for
retail hardware stores. It demonstrates end-to-end capabilities across:

- ETL pipelines
- Incremental loading (watermarking)
- Dimensional modeling (Kimball)
- Fact/Dimension warehouse design
- Inventory movement tracking
- Business anomaly alerts
- Power BI analytics
- Python + SQL data automation

Designed to simulate the analytics needs of a real store: stock control, profitability,
supplier performance, and sales trends.

---

## Architecture Overview


Core schemas:

- `fact.fact_pos_sales` — line-level sales fact
- `fact.fact_inventory_movements` — granular stock movements
- `dim.dim_date` — calendar/time intelligence
- `dim.dim_products` — category, supplier, unit price/cost
- `dim.dim_employees` — staff dimension
- `meta.etl_markers` — incremental checkpointing

---

## Star Schema (Dimensional Model)

                 dim_date
                     |
                     |
dim_products — fact_pos_sales — dim_employees
                     |
                     |
          fact_inventory_movements


This supports:

- Stock valuation
- Profitability
- Employee performance
- SKU trends
- Returns behavior

---

## ETL Pipeline Features

- Incremental ingestion using a watermark
- Deduplication via transaction identifiers
- Return handling (negative quantities)
- Profit contribution calculations
- Surrogate keys for date dimension
- Movement codes (IN/OUT) for stock

Built with Python and PostgreSQL using `pandas` and `psycopg2`.

---

## Automated Business Alerts

Script monitors operational risks and logs anomalies to
`alerts.alert_log`.

Alerts include:

- Low stock risk
- Negative margin sales
- Slow-moving items (no sales for the last 14 days)
- Excessive returns (>8%)

Useful for:

- Store managers
- Inventory planners
- BI dashboards

---

## Power BI Integration

Connected warehouse tables enable dashboards such as:

- Stock aging
- Category profitability
- Supplier contribution
- Employee sales ranking
- Return behavior
- Payment method distribution

Analysis is driven by the fact and dimension tables populated by the pipeline.

---

## Date Intelligence

The calendar dimension supports:

- Year/Quarter/Month breakdowns
- Weekend analysis
- Holiday segmentation
- Time-series trends

A standard data warehouse time backbone.

---

## Inventory Movement Logic

Every sale generates:

- `OUT` movement (quantity sold)
- Optional `IN` for returns (negative quantities)

This enables live ending stock calculations:


---

## Synthetic Data Generation

The system ships with a Python generator that produces realistic sales logs:

- Randomized timestamps
- Negative quantities (returns)
- Varying discounts
- Product catalog lookup
- Employee attribution
- Supplier/category context

Exported as daily CSV files under:



---

## Tech Stack

- Python
- Pandas
- PostgreSQL
- psycopg2
- YAML configuration
- Power BI
- Dimensional Modeling (Kimball)

---

## Project Structure
SILO/
├── dashboard/                     # Power BI / BI artifacts (visual analytics)
│
├── data/                          # Warehouse landing folders (optional external data)
│
├── etl_retail/                    # Retail-specific ETL domain
│   ├── alerts/                    # Data quality / business rule alert scripts
│   │   └── run_alerts.py          # Example alert trigger
│   │
│   ├── config/
│   │   └── hardware.yaml          # ETL configuration (DB, paths, credentials)
│   │
│   ├── data/                      # Raw + processed operational data
│   │   ├── products.csv           # Product master used when generating POS files
│   │   └── pos_exports/           # Daily exported POS transactions (CSV)
│   │
│   ├── etl_hardware/              # Hardware store pipeline logic
│   │   ├── generate_pos_data.py   # Synthetic retail POS generator (daily files)
│   │   ├── pipeline.py            # Orchestrated incremental ETL load
│   │   ├── load_dim_date.py       # Populate date dimension table
│   │   ├── load_dim_employees.py  # Populate employee dimension table
│   │   └── load_dim_products.py   # Populate product dimension table
│
├── warehouse/                     # Warehouse DDL & schemas
│   └── schema.sql                 # Star schema: facts, dimensions, metadata tables
│
├── extract.py                     # Base extract orchestrator for generic data sources
├── load.py                        # Generic data warehouse loader utilities
├── transform.py                   # Cleaning, standardization & enrichment utilities
│
├── .gitignore                     # Ignore sensitive & local-only artifacts
├── requirements.txt               # Python dependency lock
└── README.md                      # You are here ✅

## Author

👩‍💻 **Maureen Kitang'a**  
Data Engineer | BI Developer  
---
