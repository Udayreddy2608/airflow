## 1. What is Airflow?
A: Airflow is an open source platform to programmatically auhor, schedule and monitor workflows. It helps you to create, organize and keep track of your data tasks automatically. Its like a smart to-do list of you data work that runs itself.

## 2. What are the benefits of using Airflow?
1. Airflow can adapt and change on what's happening. 
2. Airflow can handle both small and large amounts of work.
3. Fully functional UI.
4. Can add new features or connect Airflow to other tools easily.

## 3. Core components of Airflow
#### Component 1: The Metadata Database
This is the database that stores information about your tasks and their statuses.
#### Component 2: Scheduler
The scheduler is responsible for determining when tasks should run.
#### Component 3: The DAG File Processor
This parses DAG files and serializes them into metadata database
#### Component 4: Executor
The executor determines how the tasks will be run.
#### Component 4: The API Server
The API server provides endpoints for task operations and serving the UI.
#### Component 5: The Worker
Worker is the component that actually executes the tasks in processes.
#### Component 6: The Queue
The queue is a list of tasks waiting to be executed
#### Component 7: The triggerer
The triggerer is responsible for managing deferrable tasks - tasks that wait for external events.


# 4. Core concepts
#### Concept 1: The DAG (Directed Acyclic Graph)
A DAG is a collection of all the tasks you want to run, organized in a way that reflects their dependencies. It helps you define the structure of your entire workflow, showing which tasks needs to happen before the others.
#### Concept 2: Operator
An operator defines a single, ideally idempotent, task in your DAG.
#### Concept 3: Task/Task Instance
A task is a specific instance of an operator, when an operator is assigned to a DAG, it becomes a task.
#### Concept 4: Workflow
A workflow is the process defined by your DAG, including all tasks and their dependencies. It represents the entire data pipeline.


# The different architectures

#### 1. Single node architecture
A 'node' is a single computer or server.
In single node architecture all components of Airflow are running on one machine.

#### 2. Multi Node Architecture
Multi-node' refers to running Airflow across multiple computers or servers.




