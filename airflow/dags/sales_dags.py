import sys
import os
sys.path.append(os.path.abspath("/opt/airflow/etl_scripts"))
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from extract_from_kafka import extract_sales_data
from transform_sales_data import transform_sales_data
from load_to_s3 import load_to_s3


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "email":['deepak.gadde24@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False
}

with DAG(
    dag_id="sales_etl_dag",
    default_args=default_args,
    start_date=datetime(2025, 5, 13),
    schedule_interval="@hourly",
    catchup=False
) as dag:

    def extract_task(**context):
        records = extract_sales_data(batch_size=100)
        context["ti"].xcom_push(key="raw_records", value=records)

    def transform_task(**context):
        raw = context["ti"].xcom_pull(key="raw_records")
        clean = transform_sales_data(raw)
        context["ti"].xcom_push(key="clean_records", value=clean)

    def load_task(**context):
        clean = context["ti"].xcom_pull(key="clean_records")
        load_to_s3(clean)
           

    extract = PythonOperator(task_id="extract", python_callable=extract_task, provide_context=True)
    transform = PythonOperator(task_id="transform", python_callable=transform_task, provide_context=True)
    load = PythonOperator(task_id="load", python_callable=load_task, provide_context=True)

    extract >> transform >> load
