### Handy Debugging/Exploration DAG

```python
from datetime import datetime

from airflow import DAG
from airflow.models import Param
from airflow.operators.bash import BashOperator

with DAG('bash', schedule=None, start_date=datetime(2023, 1, 1), params={"cmd": Param(default="echo hi")}):
    BashOperator(
        task_id='bash',
        bash_command="{{ params.cmd }}"
    )
```
