from airflow.sdk import dag, task
import random

@dag
def branch():
    @task
    def a():
        return random.randint(1, 2)

    @task.branch
    def b(val: int):
        if val == 1:
            return "equal_1"
        else:
            return "other_than_1"

    @task
    def equal_1():
        print("Value is equal to 1")

    @task
    def other_than_1():
        print("Value is other than 1")

    val = a()

    b(val) >> [equal_1(), other_than_1()]

branch()