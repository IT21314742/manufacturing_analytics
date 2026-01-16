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