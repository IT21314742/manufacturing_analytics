#! /user/bin/env python
"""
Database setup script for manufacturing analytics Projects
Creates all necessary tables and schemas in PostgreSQL.
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
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def create_database():
    """Create the manufacturing_analytics database if it doesn't exist."""

    # Default connection parameters
    params = {
        'host': 'localhost',
        'user': 'postgres', # Default PostgreDQL superuser
        'password': 'vihan',
        'port': 5432
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
        cur.execute("SELECT 1 FROM pg-catalog.pg_database WHERE datname = 'manufacturing_analytics'")
        exists = cur.fetchone()

        if not exists:
            logger.info("Creating database 'manufacturing_analytics'...")
            cur.execute(sql.SQL("CREATE DATABASE manufacturing_analytics"))
            logger.info("Database created successfully!")
        else:
            logger.info("Database 'manufacturing_analytics' already exists.")

        # Create analyst user (If not exists)
        try:
            cur.execute("""
"""))