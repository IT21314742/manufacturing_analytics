import pandas as pd
from sqlalchemy import create_engine, text

# Try different connection strings
connections = [
    'postgresql://postgres:postgres@localhost:5432/manufacturing_analytics',
    'postgresql://analyst:secure_password@localhost:5432/manufacturing_analytics'
]

for conn_str in connections:
    print(f"\nTrying: {conn_str.split('@')[0]}****")
    try:
        engine = create_engine(conn_str)
        with engine.connect() as conn:
            # List tables
            tables = pd.read_sql("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """, conn)
            
            print("Tables found:")
            for table in tables['table_name']:
                print(f"  - {table}")
                
            # Test row count
            for table in tables['table_name'][:3]:  # First 3 tables
                count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table}", conn)
                print(f"  {table}: {count.iloc[0]['cnt']} rows")
                
    except Exception as e:
        print(f"  ERROR: {e}")