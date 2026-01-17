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