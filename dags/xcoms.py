from airflow.sdk import dag, task, Context


@dag
def xcom_dag():

    @task
    def t1():
        return 42

    @task
    def t2(val):
        return val * 2
    
    @task
    def t3(val):
        print(f"Final value: {val + 3}")

    t3(t2(t1()))

xcom_dag()