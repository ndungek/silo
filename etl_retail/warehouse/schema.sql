-- Create schemas
CREATE SCHEMA IF NOT EXISTS dim;
CREATE SCHEMA IF NOT EXISTS fact;
CREATE SCHEMA IF NOT EXISTS meta;

----------------------------------------------------
-- Dimension Tables
----------------------------------------------------

-- Products dimension
CREATE TABLE IF NOT EXISTS dim.products (
    product_id       SERIAL PRIMARY KEY,
    sku              TEXT UNIQUE NOT NULL,
    product_name     TEXT NOT NULL,
    category         TEXT NOT NULL,
    brand            TEXT,
    unit_cost        NUMERIC(10,2),
    unit_price       NUMERIC(10,2),
    reorder_level    INT DEFAULT 0,
    last_updated     TIMESTAMP DEFAULT NOW()
);

-- Customers dimension
CREATE TABLE IF NOT EXISTS dim.customers (
    customer_id      SERIAL PRIMARY KEY,
    customer_name    TEXT NOT NULL,
    phone            TEXT,
    join_date        DATE DEFAULT NOW(),
    location         TEXT
);

-- Suppliers dimension
CREATE TABLE IF NOT EXISTS dim.suppliers (
    supplier_id      SERIAL PRIMARY KEY,
    supplier_name    TEXT NOT NULL,
    contact          TEXT,
    phone            TEXT,
    location         TEXT
);

----------------------------------------------------
-- Fact Tables
----------------------------------------------------

-- Sales fact
CREATE TABLE IF NOT EXISTS fact.sales (
    sale_id          SERIAL PRIMARY KEY,
    transaction_id   TEXT NOT NULL,
    product_id       INT REFERENCES dim.products(product_id),
    customer_id      INT REFERENCES dim.customers(customer_id),
    quantity         INT NOT NULL,
    unit_price       NUMERIC(10,2) NOT NULL,
    discount         NUMERIC(10,2) DEFAULT 0,
    total_amount     NUMERIC(10,2) NOT NULL,
    sale_date        TIMESTAMP NOT NULL,
    created_at       TIMESTAMP DEFAULT NOW()
);

-- Inventory movements fact
-- (+) for stock received
-- (-) for stock sold or written-off
CREATE TABLE IF NOT EXISTS fact.inventory_movements (
    movement_id      SERIAL PRIMARY KEY,
    product_id       INT REFERENCES dim.products(product_id),
    supplier_id      INT REFERENCES dim.suppliers(supplier_id),
    movement_type    TEXT NOT NULL, -- purchase, sale, damaged, return
    quantity         INT NOT NULL,
    unit_cost        NUMERIC(10,2),
    movement_date    TIMESTAMP NOT NULL,
    created_at       TIMESTAMP DEFAULT NOW()
);

----------------------------------------------------
-- Metadata
----------------------------------------------------

-- Keeps track of last ETL watermark
CREATE TABLE IF NOT EXISTS meta.etl_markers (
    process_name    TEXT PRIMARY KEY,
    last_run_ts     TIMESTAMP
);

----------------------------------------------------
-- Indexes for performance
----------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_sales_product
    ON fact.sales(product_id);

CREATE INDEX IF NOT EXISTS idx_sales_date
    ON fact.sales(sale_date);

CREATE INDEX IF NOT EXISTS idx_movements_product
    ON fact.inventory_movements(product_id);

CREATE INDEX IF NOT EXISTS idx_movements_date
    ON fact.inventory_movements(movement_date);
