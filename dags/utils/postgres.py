from airflow.providers.postgres.hooks.postgres import PostgresHook

from .tw_logger import logger
from .minio_io import read_csv, PROCESSED_BUCKET


POSTGRES_TW_CONN = "postgres_tw"

insert_query = """
    INSERT INTO comments (postId , id, name, email, body)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
"""


def load_data_to_postgres(run_id: str):
    logger.info("Loading data to Postgres")
    data = read_csv(PROCESSED_BUCKET, run_id, "processed_data.csv")
    if data is not None:
        try:
            hook = PostgresHook(postgres_conn_id=POSTGRES_TW_CONN)
            connection = hook.get_conn()
            cursor = connection.cursor()
            for index, row in data.iterrows():
                cursor.execute(
                    insert_query,
                    (row["postId"], row["id"], row["name"], row["email"], row["body"]),
                )
            connection.commit()
            cursor.close()
            connection.close()
            logger.info("Data loaded to Postgres")
        except Exception as e:
            logger.error(f"Error loading data to Postgres: {e}")
            raise ValueError("Cannot load data to Postgres")
    else:
        raise ValueError("No data found to load to Postgres")
