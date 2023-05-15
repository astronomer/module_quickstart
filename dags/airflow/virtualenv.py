
### Dependency Management - Virtualenv

If you encounter an error like:

```
+ grep -Eqx 'apache-airflow\s*[=~>]{1,2}.*' requirements.txt
+ pip install --no-cache-dir -q -r requirements.txt

ERROR: Cannot install apache-airflow, apache-airflow==2.X.Y and ????? because these package versions have conflicting dependencies.
ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/user_guide/#fixing-conflicting-dependencies

The command '/bin/bash -o pipefail -e -u -x -c if grep -Eqx 'apache-airflow\s*[=~>]{1,2}.*' requirements.txt; then     echo >&2 "Do not upgrade by specifying 'apache-airflow' in your requirements.txt, change the base image instead!";  exit 1;   fi;   pip install --no-cache-dir -q -r requirements.txt' returned a non-zero code: 1
Error: command 'docker build -t ??????????/airflow:latest failed: failed to execute cmd: exit status 1
```

One option can be to utilize a “baked” Virtual environment and BashOperator or [PythonVirtualenv](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html#howto-operator-pythonvirtualenvoperator) in your Image.

`requirements.txt`

```
virtualenv
```

`Dockerfile` - note that `dbt_venv` can be called anything here:

```
FROM quay.io/astronomer/astro-runtime:?.?.?

RUN python -m virtualenv dbt_venv && source dbt_venv/bin/activate && pip install dbt-bigquery && deactivate

...
```

`dags/example_venv.py`

```
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(schedule_interval=None, start_date=datetime(1970,1,1)) as dag:
    BashOperator(
        task_id="venv",
        bash_command="source /usr/local/airflow/dbt_venv/bin/activate && dbt --help"
    )
```
