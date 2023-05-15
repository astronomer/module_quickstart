
### Module - Airflow TaskGroups

**Background information**

A TaskGroup is a collection of closely related tasks in one DAG that should be grouped together in the graph view.

**Use** **TaskGroups**

- [ ]  Add a sample DAG to your `dags/` directory

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

default_args = {
        'owner': 'astronomer',
        'retries': 2,
        'retry_delay': timedelta(seconds=15),
    }

with DAG(dag_id='task_groups',
         start_date=datetime(2022, 7, 1),
         schedule=None,
         default_args=default_args,
         tags=['task groups'],
         description='''
            This DAG demonstrates task groups - a UI grouping concept.
         ''',
         ) as dag:

		groups = []

		for g_id in range(1, 4):
        tg_id = f'group_{g_id}'
        with TaskGroup(group_id=tg_id) as tg1:
            t1 = EmptyOperator(task_id='task1')

            t2 = EmptyOperator(task_id='task2')

            t1 >> t2

            if tg_id == 'group_3':  # Additional task for one of the TaskGroups
                t3 = EmptyOperator(task_id='task3')

                t1 >> t3

            groups.append(tg1)

    [groups[0], groups[1]] >> groups[2]  # Set dependencies between TaskGroups
```

- [ ]  Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the graph view, you should see the following graph:

    ![Screenshot 2022-07-18 at 12.31.22.png](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Screenshot_2022-07-18_at_12.31.22.png)

    And after expanding each TaskGroup:

    ![Screenshot 2022-07-18 at 12.32.14.png](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Screenshot_2022-07-18_at_12.32.14.png)


**Checkpoint**
At this point you should:

- Understand how to use TaskGroups

**Extras / Reference**

- References


    ### TaskGroups

    - [Airflow 2.0 Series - Task Groups | Astronomer YouTube](https://www.youtube.com/watch?v=e81DIxUmeYA)
    - [Using Task Groups in Airflow | Astronomer Guide](https://www.astronomer.io/guides/task-groups)
