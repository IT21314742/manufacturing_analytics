-- ============================================
-- MANUFACTURING ANALYTICS DATABASE SCHEMA
-- Complete setup script
-- ============================================

-- Drop existing tables (if you want fresh start)
DROP TABLE IF EXISTS fact_production CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS dim_machine CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;
DROP TABLE IF EXISTS dim_supplier CASCADE;

-- ============================================
-- DIMENSION TABLES
-- ============================================

-- Date Dimension (Critical for time-based analysis)
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,  -- 1=Monday, 7=Sunday
    is_weekend BOOLEAN NOT NULL,
    fiscal_year INTEGER NOT NULL,
    month_name VARCHAR(20),
    quarter_name VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dim_date IS 'Time dimension table for all date-based analytics';

-- Machine Dimension
CREATE TABLE dim_machine (
    machine_id VARCHAR(20) PRIMARY KEY,
    machine_name VARCHAR(100) NOT NULL,
    machine_type VARCHAR(50),
    location VARCHAR(100),
    installation_date DATE,
    manufacturer VARCHAR(100),
    capacity_per_hour DECIMAL(10,2),
    maintenance_interval_days INTEGER,
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dim_machine IS 'Manufacturing machines and equipment details';

-- Product Dimension
CREATE TABLE dim_product (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    product_category VARCHAR(100),
    unit_price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL,
    material_cost DECIMAL(10,2),
    labor_cost DECIMAL(10,2),
    weight_kg DECIMAL(10,2),
    target_production_time_minutes INTEGER,
    quality_standard VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dim_product IS 'Product catalog with pricing and cost information';

-- Supplier Dimension
CREATE TABLE dim_supplier (
    supplier_id VARCHAR(20) PRIMARY KEY,
    supplier_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    country VARCHAR(50),
    lead_time_days INTEGER DEFAULT 7,
    reliability_score DECIMAL(5,2) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dim_supplier IS 'Raw material and component suppliers';

-- ============================================
-- FACT TABLES
-- ============================================

-- Production Fact Table (Main transactional data)
CREATE TABLE fact_production (
    production_id SERIAL PRIMARY KEY,
    date_id INTEGER NOT NULL,
    machine_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    shift_number INTEGER,
    operator_id VARCHAR(50),
    
    -- Production metrics
    quantity_produced INTEGER NOT NULL,
    defects INTEGER DEFAULT 0,
    rework_count INTEGER DEFAULT 0,
    downtime_minutes INTEGER DEFAULT 0,
    setup_time_minutes INTEGER DEFAULT 0,
    
    -- Quality metrics
    quality_score DECIMAL(5,2),
    inspection_passed BOOLEAN,
    
    -- Resource usage
    energy_consumption_kwh DECIMAL(10,2),
    raw_material_used_kg DECIMAL(10,2),
    scrap_weight_kg DECIMAL(10,2),
    
    -- Calculated fields (can be computed or stored)
    oee_percentage DECIMAL(5,2),  -- Overall Equipment Effectiveness
    availability_percentage DECIMAL(5,2),
    performance_percentage DECIMAL(5,2),
    quality_percentage DECIMAL(5,2),
    
    -- Timestamps
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_date FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    CONSTRAINT fk_machine FOREIGN KEY (machine_id) REFERENCES dim_machine(machine_id),
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    
    -- Data validation
    CONSTRAINT chk_quantity CHECK (quantity_produced >= 0),
    CONSTRAINT chk_defects CHECK (defects >= 0 AND defects <= quantity_produced),
    CONSTRAINT chk_oee CHECK (oee_percentage >= 0 AND oee_percentage <= 100)
);

COMMENT ON TABLE fact_production IS 'Daily production transactions with quality and efficiency metrics';

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Date-based queries (most common)
CREATE INDEX idx_fact_production_date ON fact_production(date_id);
CREATE INDEX idx_fact_production_machine_date ON fact_production(machine_id, date_id);
CREATE INDEX idx_fact_production_product_date ON fact_production(product_id, date_id);

-- For filtering and grouping
CREATE INDEX idx_fact_production_oee ON fact_production(oee_percentage);
CREATE INDEX idx_fact_production_quality ON fact_production(quality_score);

-- Dimension table indexes
CREATE INDEX idx_dim_date_full_date ON dim_date(full_date);
CREATE INDEX idx_dim_machine_status ON dim_machine(status);
CREATE INDEX idx_dim_product_category ON dim_product(product_category);

-- ============================================
-- SAMPLE DATA INSERTION
-- ============================================

-- Insert sample machines
INSERT INTO dim_machine (machine_id, machine_name, machine_type, location, capacity_per_hour) VALUES
('M001', 'Injection Molder A', 'Plastic', 'Line 1', 500.00),
('M002', 'CNC Machine B', 'Metal', 'Line 2', 120.00),
('M003', 'Assembly Robot C', 'Assembly', 'Line 3', 300.00),
('M004', 'Packaging Line D', 'Packaging', 'Line 4', 1000.00),
('M005', 'Quality Scanner E', 'Inspection', 'QC Area', 800.00);

-- Insert sample products
INSERT INTO dim_product (product_id, product_name, product_category, unit_price, cost_price) VALUES
('P001', 'Smartphone Case', 'Consumer Electronics', 15.99, 8.50),
('P002', 'Automotive Bracket', 'Automotive', 45.50, 22.75),
('P003', 'Medical Device Housing', 'Medical', 120.00, 65.00),
('P004', 'Toy Action Figure', 'Toys', 9.99, 4.25),
('P005', 'Industrial Valve', 'Industrial', 89.99, 45.00);

-- Insert sample suppliers
INSERT INTO dim_supplier (supplier_id, supplier_name, country, lead_time_days) VALUES
('S001', 'Plastic Raw Materials Ltd.', 'Sri Lanka', 5),
('S002', 'Precision Components Inc.', 'Germany', 14),
('S003', 'Electronics Assembly Co.', 'China', 21),
('S004', 'Local Packaging Solutions', 'Sri Lanka', 3),
('S005', 'Quality Certification Services', 'USA', 7);

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- View for daily production summary
CREATE VIEW vw_daily_production_summary AS
SELECT 
    d.full_date,
    COUNT(DISTINCT fp.machine_id) as active_machines,
    SUM(fp.quantity_produced) as total_production,
    SUM(fp.defects) as total_defects,
    ROUND(AVG(fp.oee_percentage), 2) as avg_oee,
    SUM(fp.downtime_minutes) as total_downtime
FROM fact_production fp
JOIN dim_date d ON fp.date_id = d.date_id
GROUP BY d.full_date
ORDER BY d.full_date DESC;

-- View for machine performance ranking
CREATE VIEW vw_machine_performance AS
SELECT 
    m.machine_id,
    m.machine_name,
    m.machine_type,
    COUNT(fp.production_id) as production_days,
    SUM(fp.quantity_produced) as total_production,
    ROUND(AVG(fp.oee_percentage), 2) as avg_oee,
    ROUND((SUM(fp.defects) * 100.0 / NULLIF(SUM(fp.quantity_produced), 0)), 2) as defect_rate_percentage,
    SUM(fp.downtime_minutes) as total_downtime_minutes
FROM dim_machine m
LEFT JOIN fact_production fp ON m.machine_id = fp.machine_id
GROUP BY m.machine_id, m.machine_name, m.machine_type
ORDER BY avg_oee DESC NULLS LAST;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

SELECT 'Schema created successfully!' as status;

SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;



-- Check all tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Should return:
-- dim_date
-- dim_machine  
-- dim_product
-- dim_supplier
-- fact_production

-- Check row counts
SELECT 'dim_date' as table, COUNT(*) as rows FROM dim_date
UNION ALL
SELECT 'dim_machine', COUNT(*) FROM dim_machine
UNION ALL
SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL
SELECT 'dim_supplier', COUNT(*) FROM dim_supplier
UNION ALL
SELECT 'fact_production', COUNT(*) FROM fact_production;









-- Populate dim_date for 2023-2024
INSERT INTO dim_date (full_date, day, month, year, quarter, day_of_week, is_weekend, fiscal_year, month_name, quarter_name)
SELECT 
    datum AS full_date,
    EXTRACT(DAY FROM datum) AS day,
    EXTRACT(MONTH FROM datum) AS month,
    EXTRACT(YEAR FROM datum) AS year,
    EXTRACT(QUARTER FROM datum) AS quarter,
    EXTRACT(ISODOW FROM datum) AS day_of_week,
    CASE WHEN EXTRACT(ISODOW FROM datum) IN (6, 7) THEN true ELSE false END AS is_weekend,
    CASE WHEN EXTRACT(MONTH FROM datum) >= 4 THEN EXTRACT(YEAR FROM datum) 
         ELSE EXTRACT(YEAR FROM datum) - 1 END AS fiscal_year,
    TO_CHAR(datum, 'Month') AS month_name,
    'Q' || EXTRACT(QUARTER FROM datum) AS quarter_name
FROM generate_series(
    '2023-01-01'::DATE,
    '2024-12-31'::DATE,
    '1 day'::INTERVAL
) AS datum;









-- Connect to manufacturing_analytics database as postgres user
-- (You might need to use the default postgres superuser)

-- Grant ALL permissions to analyst user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO analyst;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO analyst;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO analyst;

-- Grant future permissions too
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO analyst;

-- Make sure analyst can connect
GRANT CONNECT ON DATABASE manufacturing_analytics TO analyst;

-- Verify permissions
SELECT 
    grantee,
    table_name,
    privilege_type
FROM information_schema.table_privileges 
WHERE table_schema = 'public'
AND grantee = 'analyst'
ORDER BY table_name;




-- Connect to manufacturing_analytics database
-- Run these commands:

-- 1. First, see current permissions for analyst
SELECT 
    grantee,
    table_catalog,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges 
WHERE grantee = 'analyst'
ORDER BY table_name, privilege_type;

-- 2. Grant USAGE on schema (THIS IS WHAT'S MISSING!)
GRANT USAGE ON SCHEMA public TO analyst;

-- 3. Grant SELECT on all tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst;

-- 4. Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO analyst;

-- 5. Also grant USAGE on sequences if any
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO analyst;

-- 6. Verify permissions
SELECT 
    has_schema_privilege('analyst', 'public', 'USAGE') as can_use_schema,
    has_table_privilege('analyst', 'dim_date', 'SELECT') as can_select_dates,
    has_table_privilege('analyst', 'fact_production', 'SELECT') as can_select_production;