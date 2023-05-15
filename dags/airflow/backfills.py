- Airflow has a CLI which can be utilized to execute and monitor a backfill via a `BashOperator`
    - [Reference](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#backfill)

```python
from airflow import DAG
from datetime import datetime

with DAG(dag_id="my_dag_backfill", start_date=datetime(1970,1,1), schedule=None) as dag:
    BashOperator(
        task_id="backfill",
        bash_command="airflow dags backfill -s 2022-01-01 -e 2022-02-01 my_dag"
    )
```
