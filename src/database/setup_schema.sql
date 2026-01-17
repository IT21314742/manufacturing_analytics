-- ============================================
-- MANUFACTURING ANALYTICS DATABASE SCHEMA
-- Complete setup script
-- ============================================

-- Drop existing tables if they exist
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
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    fiscal_year INTEGER NOT NULL,
    month_name VARCHAR(20),
    qarter_name VARCHAR(10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dim_date IS 'Time dimension table for all date-based analysis';

-- Machine Dimension
CREATE TABLE dim_machine(
    machine_id VARCHAR(20) PRIMARY KEY,
    machine_name VARCHAR(100) NOT NULL,
    machine_type VARCHAR(50),
    location VARCHAR(100),
    installation_date DATE,
    manufacturer VARCHAR(100),
)