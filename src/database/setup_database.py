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