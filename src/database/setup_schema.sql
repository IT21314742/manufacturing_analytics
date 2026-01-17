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
)