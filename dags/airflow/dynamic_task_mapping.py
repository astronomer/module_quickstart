
### Module - Airflow Dynamic Task Mapping

**Background information**

Dynamic Task Mapping allows a way for a workflow to create a number of tasks at runtime based upon current data, rather than the DAG author having to know in advance how many tasks would be needed.

**Create tasks dynamically**

- [ ]  Add a sample DAG to your `dags/` directory

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

default_args = {
        'owner': 'astronomer',
        'retries': 2,
        'retry_delay': timedelta(seconds=15),
    }

with DAG(dag_id='dynamic_task_mapping',
         start_date=datetime(2022, 7, 1),
         schedule=None,
         default_args=default_args,
         tags=['dynamic task mapping'],
         description='''
            This DAG demonstrates dynamic task mapping with a constant parameter based on the known values.
         ''',
         ):

    @task
    def add(x, y):
        return x + y

    # partial(): allows you to pass parameters that remain constant for all tasks
    # expand(): allows you to pass parameters to map over
    added_values = add.partial(x=50).expand(y=[0, 1, 2])
```

- [ ]  Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the graph view, you should see the following graph:

    ![Screenshot 2022-07-18 at 12.54.50.png](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Screenshot_2022-07-18_at_12.54.50.png)

- [ ]  Check the logs of each task, you should see something similar:

```python
{python.py:173} INFO - Done. Returned value was: 50
```

**Checkpoint**
At this point you should:

- Understand how dynamic task mapping works, and how to use expand() and partial()

**Extras / Reference**

- References


    ### Dynamic Task Mapping

    - [Create dynamic Airflow tasks | Astronomer Tutorial](https://docs.astronomer.io/learn/dynamic-tasks)
    - [Dynamic Task Mapping in Airflow | Astronomer Guide](https://www.astronomer.io/blog/apache-airflow-2-3-everything-you-need-to-know/#dynamic-task-mapping-in-airflow)
    - [Dynamic Task Mapping | Airflow Doc](https://airflow.apache.org/docs/apache-airflow/2.3.0/concepts/dynamic-task-mapping.html)
    - [What’s New in Airflow 2.3 | Astronomer Webinars](https://www.astronomer.io/events/recaps/whats-new-in-airflow-2-3/)
    - [Dynamic Task Mapping Tutorial | GitHub Repo](https://github.com/astronomer/dynamic-task-mapping-tutorial)
    - [Dynamic Task Mapping on Multiple Parameters | Astronomer Live](https://www.astronomer.io/events/recaps/dynamic-task-mapping-on-multiple-parameters/)
