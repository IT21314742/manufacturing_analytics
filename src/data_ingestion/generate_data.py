import pandas as pd
from faker import Faker
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

def generate_manufacturing_data(start_date='2023-01-01', end_date='2024-01-01'):
    """Generate synthetic manufacturing data."""
    fake = Faker()
    dates = pd.date_range(start=start_date, end=end_date, freq='D')