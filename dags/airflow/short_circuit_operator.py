
### Module - Airflow Branching with ShortCircuitOperator

**Background information**

Sometimes you need a workflow to branch, or only go down a certain path based on an arbitrary condition which is typically related to something that happened in an upstream task. One way to do this is by using the `ShortCircuitOperator`.

The `ShortCircuitOperator` is much like the PythonOperator except that it expects a `python_callable` that returns `True`or `False`based on logic implemented for your use case. If `True` is returned, the DAG will continue, and if `False` is returned, all downstream tasks will be skipped.

The short-circuiting can be configured to either respect or ignore the **`trigger_rule`**
 set for downstream tasks. If **`ignore_downstream_trigger_rules`**
 is set to True (default), all downstream tasks are skipped without considering the **`trigger_rule`**
 defined for tasks. However, if this parameter is set to False, the direct downstream tasks are skipped but the specified **`trigger_rule`** for other subsequent downstream tasks are respected.

**Use branching**

- [ ]  Add a sample DAG to your `dags/` directory

```python
import random
from datetime import timedelta
import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import ShortCircuitOperator

default_args = {
    "owner": "cs",
    "retries": 3,
    "retry_delay": timedelta(seconds=15),
    }

with DAG(
    dag_id="branching_short_circuit_operator",
    default_args=default_args,
    start_date=pendulum.datetime(2022, 8, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    description="This DAG demonstrates the usage of the ShortCircuitOperator.",
    tags=["branching"],
) as dag:

    start = EmptyOperator(task_id="start")

    check_condition = ShortCircuitOperator(
        task_id='check_condition',
        python_callable=lambda: random.choice([True, False]),
        ignore_downstream_trigger_rules=False,
    )

    @task()
    def print_execution_date(**kwargs):
        return "The execution date is {0}".format(kwargs["execution_date"])

    end = EmptyOperator(task_id="end", trigger_rule="all_done")

    start >> check_condition >> print_execution_date() >> end
```

- [ ]  Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button a couple of times to see different results
- [ ]  Check the logs of `check_condition` task, if you see:
- `{python.py:173} INFO - Done. Returned value was: True`, the grid view should look as follows:

    ![Screenshot 2022-08-02 at 09.31.23.png](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Screenshot_2022-08-02_at_09.31.23.png)

- `{python.py:173} INFO - Done. Returned value was: False`, the grid view should look as follows:

    ![Screenshot 2022-08-02 at 09.33.31.png](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Screenshot_2022-08-02_at_09.33.31.png)


**Checkpoint**
At this point you should:

- Understand how branching with `ShortCircuitOperator` works

**Extras / Reference**

- Reference
