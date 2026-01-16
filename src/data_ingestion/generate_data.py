import pandas as pd
from faker import Faker
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

def generate_manufacturing_data(start_date='2023-01-01', end_date='2024-01-01'):
    """Generate synthetic manufacturing data."""
    fake = Faker()
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    data = []
    for date in dates:
        for _ in range(np.random.randint(5, 15)):  # Random number of entries per day
            data.append({
                'date': date.date(),
                'machine_id': f"M{np.random.randint(1, 100):03d}",
                'product_id': f"P{np.random.randint(1, 500):03d}",
                'quantity': np.random.randint(100, 10000),
                'defects': np.random.randint(0, 50),
                'downtime_minutes': np.random.randint(0, 120),
                'operator': fake.name(),
                'energy_consumption_kwh': np.random.uniform(100, 500)
            })

    return pd.DataFrame(data)