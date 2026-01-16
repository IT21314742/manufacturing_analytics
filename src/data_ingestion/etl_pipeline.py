import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime
import os
from dotenv import load_dotenv