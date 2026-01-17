import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import logging
import yfinance as yf
from faker import Faker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManufacturingETL:
    def __init__(self):
        self.engine = create_engine('postgresql://analyst:secure_password@localhost:5432/manufacturing_analytics')
        self.fake = Faker()
        
    def generate_production_data(self, num_days=30):
        """Generate realistic production data"""
        logger.info(f"Generating {num_days} days of production data...")
        
        data = []
        # Get date IDs for the last num_days
        with self.engine.connect() as conn:
            dates_query = """
            SELECT date_id, full_date 
            FROM dim_date 
            ORDER BY full_date DESC 
            LIMIT %s
            """
            dates = pd.read_sql(dates_query, conn, params=(num_days,))
        
        # Get machine and product IDs
        machines = pd.read_sql("SELECT machine_id FROM dim_machine", self.engine)
        products = pd.read_sql("SELECT product_id, cost_price FROM dim_product", self.engine)
        
        for _, date_row in dates.iterrows():
            date_id = date_row['date_id']
            # Generate 5-20 production records per day
            for _ in range(np.random.randint(5, 20)):
                machine_id = np.random.choice(machines['machine_id'])
                product_row = products.sample(1).iloc[0]
                product_id = product_row['product_id']
                
                quantity = np.random.randint(100, 1000)
                defects = np.random.randint(0, int(quantity * 0.05))  # Max 5% defects
                downtime = np.random.randint(0, 120)
                
                # Calculate OEE components (simplified)
                availability = np.random.uniform(0.85, 0.95)
                performance = np.random.uniform(0.88, 0.98)
                quality = 1 - (defects / quantity)
                oee = availability * performance * quality
                
                record = {
                    'date_id': date_id,
                    'machine_id': machine_id,
                    'product_id': product_id,
                    'shift_number': np.random.choice([1, 2, 3]),
                    'operator_id': f'OP{np.random.randint(100, 999):03d}',
                    'quantity_produced': quantity,
                    'defects': defects,
                    'rework_count': np.random.randint(0, int(defects * 0.3)),
                    'downtime_minutes': downtime,
                    'setup_time_minutes': np.random.randint(10, 30),
                    'quality_score': np.random.uniform(85, 99),
                    'inspection_passed': np.random.choice([True, False], p=[0.95, 0.05]),
                    'energy_consumption_kwh': quantity * np.random.uniform(0.1, 0.5),
                    'raw_material_used_kg': quantity * np.random.uniform(0.2, 1.0),
                    'scrap_weight_kg': defects * np.random.uniform(0.1, 0.3),
                    'oee_percentage': round(oee * 100, 2),
                    'availability_percentage': round(availability * 100, 2),
                    'performance_percentage': round(performance * 100, 2),
                    'quality_percentage': round(quality * 100, 2),
                    'start_time': datetime.combine(date_row['full_date'], datetime.min.time()) + timedelta(hours=np.random.randint(8, 16)),
                    'end_time': None
                }
                record['end_time'] = record['start_time'] + timedelta(hours=np.random.uniform(1, 4))
                data.append(record)
        
        return pd.DataFrame(data)
    
    def run_etl(self):
        """Execute complete ETL pipeline"""
        try:
            logger.info("Starting ETL pipeline...")
            
            # 1. Generate production data
            df_production = self.generate_production_data(num_days=90)  # 90 days of data
            
            # 2. Load to database
            logger.info(f"Loading {len(df_production)} records to database...")
            df_production.to_sql('fact_production', self.engine, if_exists='append', index=False)
            
            # 3. Update statistics
            with self.engine.connect() as conn:
                conn.execute(text("ANALYZE fact_production;"))
                conn.commit()
            
            logger.info("ETL completed successfully!")
            
            # Show summary
            summary = pd.read_sql("""
                SELECT 
                    COUNT(*) as total_records,
                    MIN(start_time) as earliest_date,
                    MAX(start_time) as latest_date,
                    SUM(quantity_produced) as total_production,
                    ROUND(AVG(oee_percentage), 2) as avg_oee
                FROM fact_production
            """, self.engine)
            
            print("\n" + "="*50)
            print("ETL SUCCESS SUMMARY")
            print("="*50)
            print(f"Total records: {summary.iloc[0]['total_records']:,}")
            print(f"Date range: {summary.iloc[0]['earliest_date']} to {summary.iloc[0]['latest_date']}")
            print(f"Total production: {summary.iloc[0]['total_production']:,} units")
            print(f"Average OEE: {summary.iloc[0]['avg_oee']}%")
            print("="*50)
            
            return True
            
        except Exception as e:
            logger.error(f"ETL failed: {e}")
            return False

if __name__ == "__main__":
    etl = ManufacturingETL()
    etl.run_etl()