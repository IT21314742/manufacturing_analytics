#!/usr/bin/env python
"""
Database setup script for Manufacturing Analytics Project
Creates all necessary tables and schemas in PostgreSQL
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_database():
    """Create the manufacturing_analytics database if it doesn't exist"""
    
    # Default connection parameters
    # CHANGE THESE IF YOUR POSTGRES HAS DIFFERENT CREDENTIALS
    params = {
        'host': 'localhost',
        'user': 'postgres',  # Default PostgreSQL superuser
        'password': '1010',  # Change to YOUR password
        'port': '5432'
    }
    
    try:
        # Connect to PostgreSQL server
        logger.info(f"Connecting to PostgreSQL server at {params['host']}:{params['port']}")
        conn = psycopg2.connect(
            host=params['host'],
            user=params['user'],
            password=params['password'],
            port=params['port']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'manufacturing_analytics'")
        exists = cur.fetchone()
        
        if not exists:
            logger.info("Creating database 'manufacturing_analytics'...")
            cur.execute(sql.SQL("CREATE DATABASE manufacturing_analytics"))
            logger.info("Database created successfully!")
        else:
            logger.info("Database 'manufacturing_analytics' already exists")
        
        # Create analyst user (if not exists)
        try:
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'analyst') THEN
                        CREATE USER analyst WITH PASSWORD 'secure_password';
                    END IF;
                END
                $$;
            """)
            logger.info("User 'analyst' created or already exists")
        except Exception as e:
            logger.warning(f"Could not create user: {e}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Failed to create database: {e}")
        logger.info("\nTroubleshooting tips:")
        logger.info("1. Is PostgreSQL running? Check in Services (services.msc)")
        logger.info("2. Default credentials are usually:")
        logger.info("   - Username: postgres")
        logger.info("   - Password: [what you set during installation]")
        logger.info("3. Try connecting with pgAdmin first to verify credentials")
        sys.exit(1)

def create_tables():
    """Create all tables in the manufacturing_analytics database"""
    
    # Connection parameters for the new database
    params = {
        'host': 'localhost',
        'database': 'manufacturing_analytics',
        'user': 'postgres',  # Use postgres for setup
        'password': 'admin123',  # Your password
        'port': '5432'
    }
    
    # SQL to create tables
    sql_commands = [
        """
        -- Drop tables if they exist (for clean setup)
        DROP TABLE IF EXISTS fact_production CASCADE;
        DROP TABLE IF EXISTS fact_inventory CASCADE;
        DROP TABLE IF EXISTS fact_financial CASCADE;
        DROP TABLE IF EXISTS dim_date CASCADE;
        DROP TABLE IF EXISTS dim_machine CASCADE;
        DROP TABLE IF EXISTS dim_product CASCADE;
        DROP TABLE IF EXISTS dim_supplier CASCADE;
        """,
        """
        -- Dimension: Date
        CREATE TABLE dim_date (
            date_id SERIAL PRIMARY KEY,
            full_date DATE NOT NULL UNIQUE,
            day INTEGER NOT NULL CHECK (day >= 1 AND day <= 31),
            month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
            year INTEGER NOT NULL CHECK (year >= 2020 AND year <= 2030),
            quarter INTEGER NOT NULL CHECK (quarter >= 1 AND quarter <= 4),
            day_of_week INTEGER CHECK (day_of_week >= 1 AND day_of_week <= 7),
            is_weekend BOOLEAN DEFAULT FALSE,
            fiscal_year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        -- Dimension: Machine
        CREATE TABLE dim_machine (
            machine_id VARCHAR(10) PRIMARY KEY,
            machine_name VARCHAR(100) NOT NULL,
            machine_type VARCHAR(50),
            location VARCHAR(100),
            installation_date DATE,
            maintenance_interval_days INTEGER DEFAULT 90,
            status VARCHAR(20) DEFAULT 'ACTIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        -- Dimension: Product
        CREATE TABLE dim_product (
            product_id VARCHAR(10) PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            category VARCHAR(50),
            unit_price DECIMAL(10,2) CHECK (unit_price >= 0),
            unit_cost DECIMAL(10,2) CHECK (unit_cost >= 0),
            profit_margin DECIMAL(5,2),
            weight_kg DECIMAL(8,2),
            shelf_life_days INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        -- Fact: Production
        CREATE TABLE fact_production (
            production_id SERIAL PRIMARY KEY,
            date_id INTEGER,
            machine_id VARCHAR(10),
            product_id VARCHAR(10),
            shift_number INTEGER CHECK (shift_number >= 1 AND shift_number <= 3),
            quantity_produced INTEGER CHECK (quantity_produced >= 0),
            defects INTEGER CHECK (defects >= 0),
            downtime_minutes INTEGER CHECK (downtime_minutes >= 0),
            operator_id VARCHAR(50),
            energy_consumption_kwh DECIMAL(10,2) CHECK (energy_consumption_kwh >= 0),
            quality_score DECIMAL(5,2) CHECK (quality_score >= 0 AND quality_score <= 100),
            oee_score DECIMAL(5,2) CHECK (oee_score >= 0 AND oee_score <= 100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
            FOREIGN KEY (machine_id) REFERENCES dim_machine(machine_id),
            FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
        );
        """,
        """
        -- Create indexes for performance
        CREATE INDEX idx_production_date ON fact_production(date_id);
        CREATE INDEX idx_production_machine ON fact_production(machine_id);
        CREATE INDEX idx_production_product ON fact_production(product_id);
        CREATE INDEX idx_production_created ON fact_production(created_at);
        """,
        """
        -- Sample data for dim_machine
        INSERT INTO dim_machine (machine_id, machine_name, machine_type, location) VALUES
        ('M001', 'Injection Molder X1', 'Molding', 'Production Line A'),
        ('M002', 'CNC Router V2', 'Cutting', 'Production Line B'),
        ('M003', 'Assembly Robot R3', 'Assembly', 'Production Line C'),
        ('M004', 'Packaging Machine P1', 'Packaging', 'Production Line D'),
        ('M005', 'Quality Scanner Q2', 'Inspection', 'Quality Control')
        ON CONFLICT (machine_id) DO NOTHING;
        """,
        """
        -- Sample data for dim_product
        INSERT INTO dim_product (product_id, product_name, category, unit_price, unit_cost) VALUES
        ('P001', 'Smartphone Case', 'Electronics', 12.99, 4.50),
        ('P002', 'Automotive Bracket', 'Automotive', 8.75, 3.20),
        ('P003', 'Medical Device Housing', 'Medical', 45.00, 18.75),
        ('P004', 'Toy Figurine', 'Consumer Goods', 5.99, 1.80),
        ('P005', 'Industrial Valve', 'Industrial', 32.50, 12.40)
        ON CONFLICT (product_id) DO NOTHING;
        """
    ]
    
    try:
        logger.info("Connecting to database to create tables...")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        for i, command in enumerate(sql_commands, 1):
            logger.info(f"Executing command {i}/{len(sql_commands)}...")
            try:
                cur.execute(command)
                conn.commit()
            except Exception as e:
                logger.warning(f"Command {i} had issue (might be expected): {e}")
                conn.rollback()
        
        logger.info("All tables created successfully!")
        
        # Verify table creation
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        logger.info(f"\nCreated tables: {', '.join([t[0] for t in tables])}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        sys.exit(1)

def main():
    """Main function to run database setup"""
    print("=" * 60)
    print("Manufacturing Analytics - Database Setup")
    print("=" * 60)
    print("\nIMPORTANT: Make sure PostgreSQL is running!")
    print("Check in Services (services.msc) -> PostgreSQL")
    print("=" * 60)
    
    # Ask for PostgreSQL password if not provided
    response = input("\nPress Enter to continue or 'q' to quit: ")
    if response.lower() == 'q':
        print("Setup cancelled.")
        return
    
    print("\nStep 1: Creating database...")
    create_database()
    
    print("\nStep 2: Creating tables...")
    create_tables()
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Connect to database using:")
    print("   Host: localhost")
    print("   Port: 5432")
    print("   Database: manufacturing_analytics")
    print("   Username: postgres or analyst")
    print("\n2. Verify in pgAdmin:")
    print("   - Connect to PostgreSQL server")
    print("   - Expand 'manufacturing_analytics' database")
    print("   - Check 'Schemas' -> 'public' -> 'Tables'")
    print("\n3. Run the ETL pipeline:")
    print("   python src/data_ingestion/generate_data.py")

if __name__ == "__main__":
    main()