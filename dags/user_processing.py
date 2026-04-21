from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.bases.sensor import PokeReturnValue
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import requests
import csv

@dag(
    schedule=None,
    catchup=False,
    start_date=datetime(2024, 1, 1),
    is_paused_upon_creation=False
)
def user_processing():

    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        sql="""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            firstname VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""",
        conn_id="postgres")

    @task.sensor(poke_interval=30, timeout=300)
    def is_api_available() -> PokeReturnValue:
        response = requests.get("https://raw.githubusercontent.com/marclamberti/datasets/main/fakeuser.json")
        if response.status_code == 200:
            return PokeReturnValue(is_done=True, xcom_value=response.json())
        return PokeReturnValue(is_done=False, xcom_value=None)

    @task
    def extract_user(fake_user: dict) -> dict:
        return {
            "id": fake_user["id"],
            "firstname": fake_user["personalInfo"]["firstName"],
            "lastname": fake_user["personalInfo"]["lastName"],
            "email": fake_user["personalInfo"]["email"]
        }

    @task
    def process_user(user_info: dict) -> str:
        filepath = "/tmp/userinfo.csv"
        with open(filepath, "w") as f:
            writer = csv.DictWriter(f, fieldnames=user_info.keys())
            writer.writeheader()
            writer.writerow(user_info)
        return filepath

    @task
    def store_user(filepath: str):
        hook = PostgresHook(postgres_conn_id="postgres")
        hook.copy_expert(
            sql="COPY users (id, firstname, lastname, email) FROM STDIN WITH CSV HEADER",
            filename=filepath
        )

    store_user(process_user(extract_user(create_table >> is_api_available())))

user_processing()