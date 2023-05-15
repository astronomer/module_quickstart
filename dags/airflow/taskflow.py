
### Module - Airflow TaskFlow DAG Writing

**Background information**

The TaskFlow API is a functional API that allows you to explicitly declare message passing while implicitly declaring task dependencies.

If you write most of your DAGs using plain Python code rather than Operators, then the TaskFlow API will make it much easier to author clean DAGs without extra boilerplate, all using the `@task`
 decorator.

**Use decorators**

- [ ]  Add a sample DAG to your `dags/` directory

```python
import requests
from datetime import datetime

from airflow.decorators import dag, task, task_group

@dag(schedule=None, start_date=datetime(2022, 7, 1))
def taskflow_api_example():

    @task(task_id="extract_joke")
    def extract_data():
        API = "https://api.chucknorris.io/jokes/random?category=music"
        return requests.get(API).json()['value']

    extract_data()

taskflow_api_example = taskflow_api_example()
```

- [ ]  Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the logs, you should see something similar:

```python
{python.py:173} INFO - Done. Returned value was: The Drummer for Def Leppard's only got one arm. Chuck Norris needed a back scratcher.
```

**Checkpoint**
At this point you should:

- Understand how to use decorators

**Extras / Reference**

- References


    ### TaskFlow API

    Airflow decorators were introduced as part of the TaskFlow API, which also handles passing data between tasks using XCom and inferring task dependencies automatically.

    - [TaskFlow API in Airflow 2.0 | Astronomer Webinar](https://www.youtube.com/watch?v=DljJg_lXBYQ)
    - [TaskFlow API in Airflow 2.0 | Astronomer Webinar Recap](https://www.astronomer.io/events/recaps/taskflow-api-in-airflow-2-0)
    - [Airflow 2.0 Series - TaskFlow API | Astronomer YouTube](https://www.youtube.com/watch?v=A4kxouVhZWA&list=PLCi-q9vYo4x-PESoBcXN0tXCMgzh5c_Pj&index=4)
    - [Airflow Decorators | Astronomer Guide](https://www.astronomer.io/guides/airflow-decorators)
    - [Astro decorators - GitHub Repo](https://github.com/astro-projects/astro)
    - [Astro Provider | Astronomer Registry](https://registry.astronomer.io/providers/astro)
    - [TaskFlow API | Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html#)
    - [TaskFlow API DAG Example | Astronomer Registry](https://registry.astronomer.io/dags/tutorial-taskflow-api-etl)
