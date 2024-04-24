from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from DataProducer import initiate_stream

dag=DAG('DataIngestion',
        description='Getting Data from the Random API',
        schedule_interval='@once',
        start_date=datetime(2024,4,6),
        catchup=False)

Data_ingetion_task = PythonOperator(
    task_id='Data_Ingestion',
    python_callable=initiate_stream,
    dag=dag
)

Data_ingetion_task