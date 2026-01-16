---Dimension Tables---
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    full_date DATE NOT NULL,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    day_of_week INTEGER,
    is_weekend BOOLEAN,
    fiscal_year INTEGER
);

---Fact Table: Production
CREATE TABLE fact_production (
    production_id SERIAL PRIMARY KEY,
    date_id INTEGER REFERENCES dim_date(date_id),
    machine_id VARCHAR(10),
    product_id VARCHAR(10),
    quantity_produced INTEGER,
    defects INTEGER,
    downtime_minutes INTEGER,
    operator_id VARCHAR(10),
    energy_consumed_kwh DECIMAL(10, 2),
    quality_score DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---Create Indexes for Performance Optimization---
CREATE INDEX idx_fact_production_date ON fact_production(date_id);
CREATE INDEX idx-fact_production_machine ON fact_production(machine_id);
