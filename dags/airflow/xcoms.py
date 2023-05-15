
### Module - Airflow XComs

**Background information**

XComs (short for “cross-communications”) are a mechanism that let tasks talk to each other, as by default tasks are entirely isolated and may be running on entirely different machines.

An XCom is identified by a `key`(essentially its name), as well as the `task_id` and `dag_id` it came from. They can have any (serializable) value, but they are only designed for small amounts of data or metadata; do not use them to pass around large values, like dataframes or file contents - however you can pass the name of a file in cloud storage to another task.

**Push and pull XComs**

- [ ]  Add this file to `dags/example_xcom.py`

```python
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(
    dag_id='example_xcoms',
    start_date=datetime(1970, 1, 1),
    schedule=None,
    catchup=False
) as dag:
    xcom_push = BashOperator(
        task_id="xcom_push",
        bash_command="echo hello!"
    )

    # Using jinja templating to access an XCOM
    xcom_pull_bash = BashOperator(
        task_id="xcom_pull_bash",
        bash_command="echo {{ ti.xcom_pull(task_ids='xcom_push') }}"
    )

    # Using Python Operator to access an XCOM, via context passed in as kwargs
    def _print(ti):
        print(ti.xcom_pull(task_ids='xcom_push'))

    xcom_pull_python = PythonOperator(
        task_id='xcom_pull_python',
        python_callable=_print
    )

    xcom_push >> [xcom_pull_python, xcom_pull_bash]
```

- [ ]  Trigger the DAG and look at the Logs of the later two tasks to see the XCOM pushed from the first task

**Checkpoint**

At this point you should understand how to push and pull XComs with both Jinja Templating and PythonOperators

**Extras / Reference**

- The [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/concepts/taskflow.html) is a newer way to write `PythonOperator` in Airflow, and makes it easy to exchange XComs between tasks
- References


    ### XComs

    - [Custom Backends | Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/concepts/xcoms.html#custom-backends)
    - [Custom XCom Backends | Astronomer Tutorial](https://docs.astronomer.io/learn/xcom-backend-tutorial)
    - [Passing Data Between Airflow Tasks | Astronomer Guide](https://www.astronomer.io/guides/airflow-passing-data-between-tasks)
    - [Example DAG | Astronomer Registry](https://registry.astronomer.io/dags/example-xcom)
