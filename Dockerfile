FROM apache/airflow:2.2.0-python3.8

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY dags/ /opt/airflow/dags/ 
