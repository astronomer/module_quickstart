### Module - Airflow DAG Writing Best Practices

**Before You Start**

- [ ]  Review the “Airflow Best Practices” education module

[Airflow Best Practices](https://academy.astronomer.io/airflow-best-practices)

**Write a DAG**

- [ ]  Create a file in your `dags/` directory called `best_practices.py`
- [ ]  Start each DAG with importing all necessary modules and [providers](https://airflow.apache.org/docs/apache-airflow-providers/)

```python
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
```

- [ ]  Add your variables and/or functions if needed. At least define a set of parameters common to all tasks (`default_args`)
    - Make sure to avoid top-level code (meaning any code that isn’t part of your DAG or operator instantiation, particularly code making requests to external systems) -  Airflow executes all code in the `dags/` folder on every `min_file_process_interval`, which defaults to 30 seconds. Because of this, top-level code that makes requests to external systems, like an API or a database, or makes function calls outside of your tasks can cause performance issues since these requests and connections are being made every 30 seconds rather than only when the DAG is scheduled to run

```python
default_args = {
    'owner': 'cs',  # You can filter DAGs in the UI by owner
    'retries': 3,  # Number of retries that should be performed before failing the task
    'retry_delay': timedelta(seconds=45),  # Delay between retries
}
```

<aside>
💡 Default arguments can be overwritten at task level.

</aside>

- [ ]  Instantiate the DAG using `with DAG() as dag:` statement

```python
with DAG(
    dag_id="best_practices",  # Each DAG needs to have a unique dag_id
    default_args=default_args,
    start_date=pendulum.datetime(2022, 7, 1, tz="UTC"),  # DAG's first data interval, keep it static
    schedule='@daily',  # Use CRON expressions/presets or timedelta objects
    catchup=False,  # If set to False, Scheduler won't trigger DAG Runs that haven't been run since the last data interval
    max_active_runs=4,  # Define how many running concurrent instances of a DAG there are allowed to be; crucial when catchup=True
    description="This DAG demonstrates some of the best practices.",  # A way to define a description of the DAG
    tags=["best practices"],  # You can filter DAGs in the UI by tags
) as dag:
```

<aside>
🔥 Everything coming after DAG instantiation needs to be indented.

</aside>

- [ ]  Define your tasks
    - Make sure to keep them atomic - each task should be responsible for one operation that can be re-run independently of others
    - Use [decorators](https://www.astronomer.io/guides/airflow-decorators/) where possible to simplify your code
    - Use template fields, [variables, and macros](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html) - it helps keep your DAGs **idempotent** (a DAG is considered idempotent if rerunning the same DAG Run (with the same inputs) multiple times has the same effect as running it only once), and ensures you are not executing functions on every Scheduler heartbeat
    - Break out your pipelines into incremental extracts and loads wherever possible (e.g., using “last modified” date or a sequence or incrementing ID)

```python
	start = EmptyOperator(task_id="start")

	@task(retries=4)
  def print_next_execution_date(**kwargs):
      return "Next execution date is {0}".format(kwargs["next_ds"])

	end = EmptyOperator(task_id="end")
```

<aside>
💡 As a DAG in Airflow is simply a Python script, you can use loops to create your tasks.

For the example above, you could create `start` and `finish` tasks with a single line of code:

</aside>

```python
	start, finish = [EmptyOperator(task_id=tid) for tid in ['start', 'finish']]
```

- [ ]  Set [dependencies](https://www.astronomer.io/guides/managing-dependencies/#basic-dependencies) between your tasks
    - Make sure to use a consistent method for task dependencies - preferably `>>` and `<<` , over `set_upstream()` and `set_downstream()`

```python
	start >> print_next_execution_date() >> finish
```

- [ ]  Put the DAG together, run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the logs of `print_next_execution_date` task, you should see something similar:

```python
{python.py:173} INFO - Done. Returned value was: Next execution date is 2022-07-20
```

**Checkpoint**

At this point you should:

- Be able to identify and implement the most important DAG writing best practices

**Extras / Reference**

- References


    - [Airflow Best Practices | Astronomer Academy](https://academy.astronomer.io/airflow-best-practices)
    - [Intro to Apache Airflow DAGs | Astronomer Guide](https://www.astronomer.io/guides/dags)
    - [DAG Writing Best Practices | Astronomer Guide](https://www.astronomer.io/guides/dag-best-practices)
    - [Hooks 101 | Astronomer Guide](https://www.astronomer.io/guides/what-is-a-hook)
    - [Sensors 101 | Astronomer Guide](https://www.astronomer.io/guides/what-is-a-sensor)
    - [Operators 101 | Astronomer Guide](https://www.astronomer.io/guides/what-is-an-operator)
    - [Airflow 101: Essential Tips for Beginners by Astronomer | Astronomer Webinar](https://www.youtube.com/watch?v=2jhcTmZlU4k)
    - [Best Practices For Writing DAGs in Airflow 2.0 | Astronomer Webinar](https://www.youtube.com/watch?v=zVzBVpbgw1A&t=35s)
    - [Introduction to Apache Airflow | Astronomer Webinar](https://www.youtube.com/watch?v=GIztRAHc3as)
    - [10 Airflow Best Practices | Astronomer Blog](https://www.astronomer.io/blog/10-airflow-best-practices/)
    - [Create DAG documentation in Apache Airflow | Astronomer Tutorial](https://docs.astronomer.io/learn/custom-airflow-ui-docs-tutorial)
