from airflow.sdk import dag, task, task_group


@dag
def group():
    @task
    def a():
        print("Task A")

    @task_group
    def my_group():
        @task
        def b():
            print("Task B")

        @task
        def c():
            print("Task C")

        @task_group
        def nested_group():
            @task
            def d():
                print("Task D")

            @task
            def e():
                print("Task E")

            d() >> e()
        
        b() >> c() >> nested_group()

    a() >> my_group()

group()