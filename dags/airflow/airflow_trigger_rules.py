
### Module - Airflow Trigger Rules

**Background information**

All operators have a `trigger_rule` argument which defines the rule by which the generated task gets triggered. The default value for `trigger_rule`is `all_success`and can be defined as “trigger this task when all directly upstream tasks have succeeded”. Other available rules:

- `all_success`: (default) The task runs only when all upstream tasks have succeeded.
- `all_failed`: The task runs only when all upstream tasks are in a failed or upstream_failed state.
- `all_done`: The task runs once all upstream tasks are done with their execution.
- `all_skipped`: The task runs only when all upstream tasks have been skipped.
- `one_failed`: The task runs as soon as at least one upstream task has failed.
- `one_success`: The task runs as soon as at least one upstream task has succeeded.
- `none_failed`: The task runs only when all upstream tasks have succeeded or been skipped.
- `none_failed_min_one_success`: The task runs only when all upstream tasks have not failed or upstream_failed, and at least one upstream task has succeeded.
- `none_skipped`: The task runs only when no upstream task is in a skipped state.
- `always`: The task runs at any time.
- `dummy`: Dependencies are just for show, trigger at will.

**Use Trigger Rules**

- [ ]  Add a sample DAG to your `dags/` directory

```python
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator

default_args = {
        'owner': 'astronomer',
        'retries': 2,
        'retry_delay': timedelta(seconds=15),
    }

with DAG(
    dag_id="trigger_rules",
    schedule=None,
    start_date=datetime(2022, 7, 1),
    default_args=default_args,
) as dag:

    run_this_first = EmptyOperator(task_id="run_this_first")

    branching = BranchPythonOperator(task_id="branching", python_callable=lambda: "branch_a")

    branch_a = EmptyOperator(task_id="branch_a")

    follow_branch_a = EmptyOperator(task_id="follow_branch_a")

    branch_false = EmptyOperator(task_id="branch_false")

    join = EmptyOperator(task_id="join")

    run_this_first >> branching
    branching >> branch_a >> follow_branch_a >> join
    branching >> branch_false >> join
```

- [ ]  Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the graph view, you should see that the `join` task was skipped - `trigger_rule` is set to `all_success` by default, and the skip caused by the branching operation cascades down to skip a task marked as `all success`

    ![Screenshot 2022-07-18 at 13.04.08.png](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Screenshot_2022-07-18_at_13.04.08.png)

- [ ]  Change `trigger_rule` to `none_failed_min_one_success` in the `join` task, and trigger the DAG

```python
join = EmptyOperator(task_id="join", trigger_rule="none_failed_min_one_success")
```

- [ ]  Check the graph view, `join` task should be marked as `success`

    ![Screenshot 2022-07-18 at 13.06.11.png](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Screenshot_2022-07-18_at_13.06.11.png)


**Checkpoint**
At this point you should:

- Understand how Trigger Rules work and can impact your pipelines

**Extras / Reference**

- References


    ### Trigger Rules

    - [Trigger Rules | Airflow Doc](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html#trigger-rules)
    - [Trigger Rules | Astronomer Guide](https://www.astronomer.io/guides/managing-dependencies/#trigger-rules)
