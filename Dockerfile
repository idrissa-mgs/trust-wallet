FROM apache/airflow:2.7.1
ENV AIRFLOW_VAR_MINIO_ROOT_USER minioadmin
ENV AIRFLOW_VAR_MINIO_ROOT_PASSWORD minioadmin
COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt
