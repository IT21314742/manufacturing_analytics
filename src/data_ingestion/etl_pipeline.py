import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handlers=[
        logging.FileHandler("etl_pipeline.log"),
        logging.StreamHandler()

    ]
)
logger = logging.getLogger(__name__)

class ETLPipeline:
    def __init__(self):
        load_dotenv()
        self.db_connection = self.create_db_connection()
    
    def _create_db_connection(self):
        """Create database connection with error handling"""
        try:
            #Get Credentials from environment variables
            db_user = os.getenv('DB_USER', 'vihan')
            db_password = os.getenv('DB_PASSWORD', 'Vihan')
            db_host = os.getenv('DB_HOST', 'localhost')
            db_port = os.getenv('DB_PORT', '5432')
            db_name = os.getenv('DB_NAME', 'manufacturing_analytics')

            connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            engine = create_engine(connection_string)

            #Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            logger.info("Database connection established successfully.")
            return engine
        
        except SQLAlchemyError as e:
            logger.error(f"Database Connection Failed: {e}")
            raise
    
    def extract(self):
        """Extract data from various sources"""
        logger.info("Starting data extraction...")

        #generate manufacturing data
        manufacturing_df = self.generate_manufacturing_data()
        