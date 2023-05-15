
### Module - Airflow SQL Data Quality Checks

**Before you start**

- [ ]  Review “Data quality and Airflow” guide

[Data quality and Airflow - Airflow Guides](https://www.astronomer.io/guides/data-quality/)

**Install Common SQL and Postgres provider**

- [ ]  Add `apache-airflow-providers-common-sql` to your `requirements.txt` file

```bash
$ cat requirements.txt
apache-airflow-providers-common-sql
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that the provider is installed. You can restart your project using `astro dev restart`.

</aside>

**Create an Airflow Connection**

- [ ]  [Follow this guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) to create an [Airflow Connection](https://airflow.apache.org/docs/apache-airflow/stable/concepts/connections.html)
    - the specifics will vary greatly based on what database you are integrating with

<aside>
🛠 Specifics for creating your connection should be inserted here

</aside>

**Use SQL check operators**

- [ ]  Test out SQL check operators
- Create the following DAG (add `sql_data_quality.py` file to your `dags/` directory)

<aside>
💡 If you have an existing table that you can use for this exercise, feel free to remove first two tasks and update the checks to reflect your setup.

</aside>

```python
docs = """
Connection used in this example: \n
- Connection ID: sqlite_default \n
- Connection Type: Sqlite \n
- Host: /tmp/sqlite.db \n
Make sure to add apache-airflow-providers-sqlite to your requirements.txt file.
"""
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator, SQLTableCheckOperator
from airflow.providers.sqlite.operators.sqlite import SqliteOperator

_CONN_ID = "sqlite_default"
_TABLE_NAME = "employees"

default_args = {
    "owner": "cs",
    "retries": 3,
    "retry_delay": timedelta(seconds=15),
    }

with DAG(
    dag_id="sql_data_quality",
    start_date=pendulum.datetime(2022, 10, 1, tz="UTC"),
    default_args=default_args,
    schedule=None,
    doc_md=docs,
) as dag:

    create_table = SqliteOperator(
        task_id="create_table",
        sqlite_conn_id=_CONN_ID,
        sql=f"""
        CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (
            employee_name VARCHAR NOT NULL,
            employment_year INT NOT NULL
        );
        """
    )

    populate_data = SqliteOperator(
        task_id="populate_data",
        sqlite_conn_id=_CONN_ID,
        sql=f"""
            INSERT INTO {_TABLE_NAME} (employee_name, employment_year) VALUES
                ('Mary', 2021),
                ('Patricia', 2022),
                ('Susan', 2020);
        """,
    )

    check_row_count = SQLTableCheckOperator(
        task_id="check_row_count",
        conn_id=_CONN_ID,
        table=_TABLE_NAME,
        checks={
            "row_count_check": {"check_statement": "COUNT(*) >= 3"}
        },
    )

    check_employee_data = SQLColumnCheckOperator(
        task_id="check_employee_data",
        conn_id=_CONN_ID,
        table=_TABLE_NAME,
        column_mapping={
            "employment_year": {"max": {"less_than": 2023}}
        },
    )

    create_table >> populate_data >> [check_row_count, check_employee_data]
```

- [ ]  Run it locally - hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Change the check statement in the  `check_row_count` task and trigger the DAG again:

```python
checks={
    "row_count_check": {"check_statement": "COUNT(*) >= 10"}
},
```

- [ ]  Go to the logs of `check_row_count` task, you should see the following:

```python
The following tests have failed:
	Check: row_count_check,
	Check Values: {'check_statement': 'COUNT(*) >= 10', 'success': False}
```

- [ ]  Change the check in the `check_employee_data` task and trigger the DAG again:

```python
column_mapping={
    "employment_year": {"max": {"less_than": 2022}}
},
```

- [ ]  Go to the logs of `check_employee_data` task, you should see the following:

```python
The following tests have failed:
	Check: max,
	Check Values: {'less_than': 2022, 'result': 2022, 'success': False}
```

**Checkpoint**

At this point you should:

- Understand and be able to use SQL check operators

**Extras / Reference**

- References


    ### SQL Data Quality Checks

    - [Data quality and Airflow | Astronomer Guide](https://www.astronomer.io/guides/data-quality/)
    - [15-min live on SQLColumnCheckOperator | Astronomer Live](https://www.astronomer.io/events/live/the-sql-column-check-operator/)
    - [15-min live on SQLTableCheckOperator | Astronomer Live](https://www.astronomer.io/events/live/the-sql-table-check-operator/)
    - [SQLColumnCheckOperator | Astronomer Registry](https://registry.astronomer.io/providers/common-sql/modules/sqlcolumncheckoperator)
    - [SQLTableCheckOperator | Astronomer Registry](https://registry.astronomer.io/providers/common-sql/modules/sqltablecheckoperator)
