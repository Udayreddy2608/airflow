from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.bases.sensor import PokeReturnValue
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests
import csv


    
@dag
def user_processing():

    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        sql="""CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""",
        conn_id="postgres")
    
    @task.sensor(poke_interval=30, timeout= 300)
    def is_api_available() -> PokeReturnValue:
        response = requests.get("https://raw.githubusercontent.com/marclamberti/datasets/main/fakeuser.json")
        if response.status_code == 200:
            fake_user = response.json()
            return PokeReturnValue(is_done=True, xcom_value= fake_user)
        else:
            fake_user = None
            return PokeReturnValue(is_done=False,xcom_value= fake_user)
    
    @task
    def extract_user(fake_user: dict) -> dict:
        return {
            "id": fake_user["id"],
            "firstname": fake_user["personalInfo"]["firstName"],
            "lastname": fake_user["personalInfo"]["lastName"],
            "email": fake_user["personalInfo"]["email"]
        }

    @task
    def process_user(user_info: dict):
        print(f"Processing user: {user_info['firstname']} {user_info['lastname']} with email: {user_info['email']}")
        with open("/tmp/userinfo.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames= user_info.keys())
            writer.writeheader()
            writer.writerow(user_info)
    
    @task
    def store_user():
        hook = PostgresHook(postgres_conn_id="postgres")
        hook.copy_expert(
            sql="COPY users FROM STDIN WITH CSV HEADER",
            filename="/tmp/userinfo.csv"
        )

    fake_user = is_api_available()
    user_info = extract_user(fake_user)
    process_user(user_info)
    store_user()

user_processing()


# command to test a task: airflow tasks test user_processing create_table