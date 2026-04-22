# ✈️ Apache Airflow 3.0 — Certification Prep

A hands-on learning repository for mastering **Apache Airflow 3.0** concepts, built while preparing for the Airflow certification. It covers core DAG patterns, the TaskFlow API, Celery workers, XComs, Asset-based scheduling, and custom provider SDK development.

---

## 📁 Project Structure

```
airflow/
├── dags/                    # Example DAGs covering key Airflow concepts
│   ├── user_processing.py   # End-to-end pipeline: API → CSV → PostgreSQL
│   ├── branch.py            # BranchPythonOperator / @task.branch pattern
│   ├── celery.py            # Multi-worker Celery queue routing
│   ├── group.py             # TaskGroup & nested TaskGroup organisation
│   ├── xcoms.py             # XCom push/pull between tasks
│   ├── sql.py               # @task.sql decorator with PostgreSQL
│   └── user.py              # Asset-based scheduling (@asset, @asset.multi)
├── my-sdk/                  # Custom Airflow provider SDK
│   └── my_sdk/
│       ├── __init__.py      # Provider entry-point registration
│       └── decorators/
│           └── sql.py       # Custom @task.sql decorator implementation
├── config/
│   └── airflow.cfg          # Airflow configuration file
├── snippets/
│   └── assets.py            # Asset API reference snippets
├── notes/
│   └── basics.md            # Study notes on Airflow fundamentals
├── Dockerfile               # Custom Airflow image with my-sdk pre-installed
├── docker-compose.yaml      # Full CeleryExecutor stack (Postgres + Redis)
└── pyproject.toml           # Python project metadata & dependencies
```

---

## 🧠 Concepts Covered

| Concept | File |
|---|---|
| TaskFlow API (`@dag`, `@task`) | All DAGs |
| Sensors (`@task.sensor`) | `user_processing.py` |
| SQL Operators & Hooks | `user_processing.py`, `sql.py` |
| Branching (`@task.branch`) | `branch.py` |
| Celery queue routing (`queue=`) | `celery.py` |
| TaskGroups & nesting | `group.py` |
| XCom push/pull | `xcoms.py` |
| Asset-based scheduling | `user.py` |
| Custom Provider / SDK | `my-sdk/` |
| Docker + CeleryExecutor setup | `Dockerfile`, `docker-compose.yaml` |

---

## 🏗️ Architecture

The `docker-compose.yaml` spins up a full production-like **CeleryExecutor** stack:

```
┌────────────────────────────────────────────────────┐
│                  Airflow Services                  │
│                                                    │
│  API Server (:8080)  ←→  Scheduler                 │
│       ↓                      ↓                     │
│  DAG Processor          Triggerer                  │
│       ↓                                            │
│  Worker 1 (default queue)                          │
│  Worker 2 (high_cpu queue)                         │
│                                                    │
│  Celery Flower (:5555) [optional --profile flower] │
└────────────────────────────────────────────────────┘
         ↓                         ↓
    PostgreSQL :5432          Redis :6379
   (metadata DB +           (Celery broker)
    Celery result backend)
```

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python ≥ 3.12 (for local development)

### 1. Start the Stack

```bash
# Set the Airflow UID (Linux only — skip on macOS)
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Initialise and start all services
docker compose up airflow-init
docker compose up -d
```

The Airflow UI will be available at **http://localhost:8080**  
Default credentials: `airflow` / `airflow`

### 2. Optional: Enable Celery Flower

```bash
docker compose --profile flower up -d
```

Flower dashboard: **http://localhost:5555**

### 3. Tear Down

```bash
docker compose down --volumes --remove-orphans
```

---

## 🔌 Custom SDK (`my-sdk`)

A minimal custom Airflow **provider package** that demonstrates how to extend the TaskFlow API with a custom decorator.

**Registered decorator:** `@task.sql` — executes a SQL string returned from a Python function against a configured connection.

The provider is installed into the Airflow image at build time via the `Dockerfile`:

```dockerfile
FROM apache/airflow:3.0.0
COPY my-sdk /opt/airflow/my-sdk
RUN pip install -e /opt/airflow/my-sdk
```

---

## 📦 DAG Summaries

### `user_processing` — End-to-End Pipeline
Demonstrates a real-world ETL pipeline:
1. **`create_table`** — Creates a `users` table in PostgreSQL if it doesn't exist
2. **`is_api_available`** — Sensor that polls a fake user API until it responds
3. **`extract_user`** — Extracts relevant fields from the API response
4. **`process_user`** — Writes user data to a CSV file
5. **`store_user`** — Bulk-loads the CSV into PostgreSQL via `COPY`

### `branch` — Conditional Branching
Uses `@task.branch` to route execution based on a random integer — demonstrates how Airflow handles conditional task skipping.

### `celery` — Queue-Based Task Routing
Shows how to assign tasks to specific Celery queues (`high_cpu`) so they are only picked up by designated workers.

### `group` — Task Groups
Demonstrates `@task_group` for logical grouping of tasks, including **nested task groups**.

### `xcoms` — Cross-Task Communication
Simple chain showing XCom push/pull: `t1` returns `42` → `t2` doubles it → `t3` adds 3 and prints the final value.

### `sql` — SQL Task Decorator
Uses the `@task.sql` decorator to execute a raw SQL query (`SELECT COUNT(*) FROM xcom`) against a PostgreSQL connection.

### `user` — Asset-Based Scheduling
Demonstrates the **Airflow 3.0 Asset API**:
- `@asset` fetches a random user daily from an external API
- `@asset.multi` consumes that asset and produces two downstream assets (`user_location`, `login_data`)

---

## 🛠️ Local Development

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

---

## 📚 Dependencies

| Package | Version |
|---|---|
| `apache-airflow` | `3.0.0` |
| `apache-airflow-providers-postgres` | `6.1.3` |
| Python | `≥ 3.12` |
