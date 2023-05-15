
### Module - Airflow Parametrized DAG

**Background information**

- In order to parametrize your DAG, you can use an Airflow concept of providing runtime configuration to tasks - [Params](https://airflow.apache.org/docs/apache-airflow/stable/concepts/params.html)
- Parameters can use [JSONSchema validation](https://airflow.apache.org/docs/apache-airflow/stable/concepts/params.html#json-schema-validation)
- Params can be modified before the DAGRun starts when you trigger a DAG manually
- To add Params to a DAG, initialize it with the `params`kwarg. Use a dictionary that maps Param names to either a Param or an object indicating the parameter’s default value
- You can access params:
    - by referencing them in a template
    - via a tasks’s `context` kwargs

**Create an example DAG**

- [ ]  Test out params
- Create the following DAG (add `params.py` file to your `dags/` directory)

```python
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.models.param import Param
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="params",
    start_date=pendulum.datetime(2022, 10, 1, tz="UTC"),
    schedule=None,
    params={
        "my_param": Param("this will be used if you do not overwrite param", type="string")
    }
):
    BashOperator(
        task_id="bash_task",
        bash_command='echo "Here is my param: {{ params.my_param }}"',
    )

    @task
    def python_task(**context):
        print(context["params"]["my_param"])

    python_task()
```

- [ ]  Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the logs of `bash_task`, you should see the following:

```python
{subprocess.py:75} INFO - Running command: ['/bin/bash', '-c', 'echo "Here is my param: this will be used if you do not overwrite param"']
{subprocess.py:86} INFO - Output:
{subprocess.py:93} INFO - Here is my param: this will be used if you do not overwrite param
```

- [ ]  Check the logs of `python_task`, you should see the following:

```python
{logging_mixin.py:117} INFO - this will be used if you do not overwrite param
```

- [ ]  Trigger your DAG using `Trigger DAG w/config` option and provide the configuration JSON as shown below:

```json
{
    "my_param": "overwriting the default value"
}
```

- [ ]  Check the logs of both tasks and verify if you see the change in the logs

**Checkpoint**
At this point you should:

- Understand how to parametrize your DAG
