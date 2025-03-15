from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from utils.postgres import load_data_to_postgres
import pytz

from utils.data_processing import collect_raw_data, process_raw_data


# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


dag = DAG(
    "trust_wallet_jsonplaceholder_api_data",
    default_args=default_args,
    description="Dag to collect data from JSONPlaceholder API",
    schedule_interval=timedelta(minutes=30), # run every 30 minutes
    start_date=datetime(2025, 3, 15, tzinfo=pytz.UTC),
    catchup=False,
    tags=["company", "trust-wallet"],
)


collect_raw_data_task = PythonOperator(
    task_id="raw_data_collection_task",
    python_callable=collect_raw_data,
    provide_context=True,
    op_kwargs={
        "api_url": "https://jsonplaceholder.typicode.com/comments",
        "bucket_name": "raw-data",
        "run_id": "{{ dag_run.run_id }}",
    },
    dag=dag,
)

process_data_task = PythonOperator(
    task_id="raw_data_processing_task",
    python_callable=process_raw_data,
    provide_context=True,
    op_kwargs={
        "bucket_name": "processed-data",
        "run_id": "{{ dag_run.run_id }}",
    },
    dag=dag,
)

create_comments_table_task = PostgresOperator(
    task_id="create_comments_table_task",
    postgres_conn_id="postgres_tw",
    sql="sql/comments.sql",
    dag=dag,
)

load_data_to_postgres_task = PythonOperator(
    task_id="load_process_data_to_postgres",
    python_callable=load_data_to_postgres,
    provide_context=True,
    op_kwargs={
        "run_id": "{{ dag_run.run_id }}",
    },
    dag=dag,
)

(
    collect_raw_data_task
    >> process_data_task
    >> create_comments_table_task
    >> load_data_to_postgres_task
)
