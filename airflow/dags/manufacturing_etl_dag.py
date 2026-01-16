# airflow/dags/manufacturing_etl_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'vihan',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'manufacturing_data_pipeline',
    default_args=default_args,
    description='Daily ETL for manufacturing analytics',
    schedule_interval='0 2 * * *',
    catchup=False,
)

def run_etl():
    from src.data_ingestion.etl_pipeline import ETLPipeline
    pipeline = ETLPipeline()
    return pipeline.run_pipeline()

etl_task = PythonOperator(
    task_id='run_etl_pipeline',
    python_callable=run_etl,
    dag=dag,
)

data_quality_check = BashOperator(
    task_id='data_quality_check',
    bash_command='python src/data_quality/validate_data.py'
    dag=dag,
)

etl_task >> data_quality_check