
### Module - Airflow Branching with BranchPythonOperator

**Background information**

Sometimes you need a workflow to branch, or only go down a certain path based on an arbitrary condition which is typically related to something that happened in an upstream task. One way to do this is by using the `BranchPythonOperator`.

The `BranchPythonOperator` is much like the PythonOperator except that it expects a `python_callable` that returns a `task_id` (or list of `task_ids`). The `task_id` returned is followed, and all of the other paths are skipped. The `task_id` returned by the Python function has to be referencing a task directly downstream from the `BranchPythonOperator` task.

**Use branching**

- [ ]  Add a sample DAG to your `dags/` directory

```python
import random
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.edgemodifier import Label

default_args = {
        'owner': 'astronomer',
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
    }

options = ['branch_a', 'branch_b', 'branch_c', 'branch_d']

with DAG(dag_id='branching_branch_python_operator',
         start_date=datetime(2022, 7, 1),
         schedule=None,
         default_args=default_args,
         tags=['branching'],
         description='''
             This DAG demonstrates the usage of the BranchPythonOperator.
         ''',
         ) as dag:

    start = EmptyOperator(
        task_id='start',
    )

    branching = BranchPythonOperator(
        task_id='branching',
        python_callable=lambda: random.choice(options),
    )

    start >> branching

    end = EmptyOperator(
        task_id='end',
        trigger_rule='none_failed_min_one_success',  # All upstream tasks have not failed or upstream_failed,
        # and at least one upstream task has succeeded.
    )

    for option in options:

        empty_follow = EmptyOperator(
            task_id=option,
        )

        # Label() is used in order to label the dependency edges between different tasks in the Graph view.
        # It can be especially useful for branching,
        # so you can label the conditions under which certain branches might run.
        branching >> Label(option) >> empty_follow >> end
```

- [ ]  Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button a couple of times to see different results
- [ ]  Check the graph view, you should see the following graph:

    ![Screenshot 2022-07-18 at 12.47.28.png](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Screenshot_2022-07-18_at_12.47.28.png)


**Checkpoint**
At this point you should:

- Understand how branching with `BranchPythonOperator`works

**Extras / Reference**

- Reference


    ### Branching

    - [Branching in Airflow | Astronomer Guide](https://www.astronomer.io/guides/airflow-branch-operator)
    - [BranchDateTimeOperator | Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/modules/branchdatetimeoperator)
    - [BranchDayOfWeekOperator | Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/modules/branchdayofweekoperator)
    - [BranchPythonOperator | Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/modules/branchpythonoperator)
    - [BranchSQLOperator | Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/modules/branchsqloperator)
    - [The Airflow BranchPythonOperator for Beginners in 10 mins | YouTube](https://www.youtube.com/watch?v=aRfuZ4DVqUU)
    - [ShortCircuitOperator | Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/modules/shortcircuitoperator)
