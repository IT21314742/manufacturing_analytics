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
    