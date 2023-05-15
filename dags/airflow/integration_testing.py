
### Module - Airflow Integration Testing

**Background information**

Operators might function correctly by themselves, but it’s a combination of multiple operators which often fails. Integration testing in Airflow involves a flow of events between multiple systems.

You need to simulate all systems in your tests, so the feasibility varies depending on your code, security requirements, resources, etc.

It can be helpful to add a few integration tests that use all the common services in your ecosystem (e.g., S3, Snowflake, Vault) but with dummy resources or “dev” accounts.

**Before you start**

- [ ]  Review “Testing Airflow DAGs” guide

[Testing Airflow DAGs - Airflow Guides](https://www.astronomer.io/guides/testing-airflow/#data-integrity-testing)

**Create the metastore**

- [ ]  In order to run the test, you need the local Airflow metastore - to create it automatically for every session with `pytest`, create `conftest.py` in your `tests` directory:

```python
import os
import shutil

import pytest

os.environ["AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS"] = "False"  # Don't want anything to "magically" work
os.environ["AIRFLOW__CORE__LOAD_EXAMPLES"] = "False"  # Don't want anything to "magically" work
os.environ["AIRFLOW__CORE__UNIT_TEST_MODE"] = "True"  # Set default test settings, skip certain actions, etc.
os.environ["AIRFLOW_HOME"] = os.path.dirname(os.path.dirname(__file__))  # Hardcode AIRFLOW_HOME to root of this project

@pytest.fixture(autouse=True, scope="session")
def reset_db():
    """Reset the Airflow metastore for every test session."""
    from airflow.utils import db

    db.resetdb()
    yield

    # Cleanup temp files generated during tests
    os.remove(os.path.join(os.environ["AIRFLOW_HOME"], "unittests.cfg"))
    os.remove(os.path.join(os.environ["AIRFLOW_HOME"], "unittests.db"))
    os.remove(os.path.join(os.environ["AIRFLOW_HOME"], "webserver_config.py"))
    shutil.rmtree(os.path.join(os.environ["AIRFLOW_HOME"], "logs"))
```

**Integration testing**

- [ ]  Create a subdirectory in your `tests` directory called `dags`
- The structure of `tests` folder should mimic the structure outside of this folder (see an example below)

```python
.
├── dags
│   ├── my_dag.py
│   └── my_second_dag.py
├── plugins
│   ├── __init__.py
│   └── no_holidays.py
└──  tests
    ├── conftest.py
    ├── dags
    │   ├── test_complete_dag.py
    │   ├── test_dag_integrity.py
    │   ├── test_my_dag.py
    │   └── test_my_second_dag.py
    └── plugins
		    └── test_no_holidays.py
```

- [ ]  In your new `/tests/dags` directory, create a file called `test_complete_dag.py`:

```python
import pendulum

from airflow.decorators import task
from airflow.executors.debug_executor import DebugExecutor
from airflow.models import DAG, DagRun, TaskInstance
from airflow.operators.bash import BashOperator
from airflow.utils.state import State

def test_dag():
    """Validate a complete DAG."""
    with DAG(
            dag_id="test_complete_dag",
            start_date=pendulum.datetime(2022, 8, 1, tz="UTC"),
            schedule_interval="@daily",
    ) as dag:

        start = BashOperator(task_id="start", bash_command="echo start")

        @task()
        def push_to_xcoms(**kwargs):
            value = "Astronomer"
            kwargs["ti"].xcom_push(key="my_key", value=value)

        @task()
        def pull_from_xcoms(**kwargs):
            pulled_value = kwargs["ti"].xcom_pull(key="my_key", task_ids="push_to_xcoms")
            print("Value = " + str(pulled_value))

        start >> push_to_xcoms() >> pull_from_xcoms()

        dag.clear()
        dag.run(executor=DebugExecutor(), start_date=dag.start_date, end_date=dag.start_date)

        # Validate that DAG Run was successful
        dagruns = DagRun.find(dag_id=dag.dag_id, execution_date=dag.start_date)
        assert len(dagruns) == 1
        assert dagruns[0].state == State.SUCCESS

        # Validate XCom
        pull_from_xcoms_task = dag.get_task("pull_from_xcoms")
        pull_from_xcoms_ti = TaskInstance(task=pull_from_xcoms_task, execution_date=dag.start_date)
        result = pull_from_xcoms_ti.xcom_pull(key="my_key")
        assert result == "Astronomer"
```

<aside>
📚 This test validates if:
1. DAG Run was successful
2. the XCom value received by `pull_from_xcom` task was correct

</aside>

- [ ]  Run `astro dev pytest tests/dags/test_complete_dag.py`. You should see the following message `All Pytests passed!`

**Checkpoint**
At this point you should:

- Understand how to implement integration tests in Airflow

**Extras / Reference**

- References


    ### Testing

    - [Google Slides](https://docs.google.com/presentation/d/1mnR_yRJT7XbCRW0cfqhBp3zcfv6fX-ezbarpUuBlY1I/edit#slide=id.gc4f39c7421_0_10)
    - [GitHub Repo](https://github.com/astronomer/airflow-testing-guide): *Proof-of-concept that shows users how to run DAG validation tests. Pay close attention to the [test_dag_validation.py](https://github.com/astronomer/airflow-testing-guide/blob/main/test_dag_validation.py) script. This script runs tests against the existing DAGs to ensure that they:*
        - *Have no import failures*
        - *Are parameterized for only 2 retries*

    *Script is also called inside of GitHub actions as a CI/CD action (see [here](https://github.com/astronomer/airflow-testing-guide/blob/main/.github/workflows/main.yml#L31))*

    - [Guide](https://www.astronomer.io/guides/testing-airflow): *This guide references the above repository, but also goes into [Unit Testing](https://www.astronomer.io/guides/testing-airflow#unit-testing) as well as [Data Integrity Testing](https://www.astronomer.io/guides/testing-airflow#data-integrity-testing). Here are some resources found in the guide that are referenced:*

    ### Unit Testing

    - *[Testing and Debugging Airflow (Article)](https://godatadriven.com/blog/testing-and-debugging-apache-airflow/): shows how to use Mocking when performing Unit Testing. Article walks users through how to Mock a postgres database. Sometimes you need to fake objects in your tests. For example, when you cannot access the Airflow metastore directly from your laptop and thus cannot read the connections. In these situations, you can mock these objects in your tests.*
    - *[Airflow Tests (GitHub)](https://github.com/apache/airflow/tree/main/tests): Examples of various Airflow tests. Some are examples of mocking, others are just plain unit tests*

    ### Data Integrity Testing

    - [Great Expectations | Astronomer Registry](https://registry.astronomer.io/providers/great-expectations): *The different components of GreatExpectations operators that currently exist in the Airflow OSS project*
    - [Airflow Data Quality Demo | GitHub Repo](https://github.com/astronomer/airflow-data-quality-demo/)
    - [Integrating Airflow and Great Expectations | Astronomer Guide](https://www.astronomer.io/guides/airflow-great-expectations): *Goes in depth on the different types of things you can do with Great Expectations in Airflow*
    - [How to use Great Expectations in an Airflow DAG to perform data quality checks | Astronomer Webinar](https://www.youtube.com/watch?v=5G_jhs8v4nE)
    - [All Data Quality Providers | Astronomer Registry](https://registry.astronomer.io/providers?page=1&categories=Data+Quality): *The different Data Quality providers that currently exist in the Airflow OSS project*
    - [Airflow Data Quality Checks with SQL Operators | Astronomer Guide](https://www.astronomer.io/guides/airflow-sql-data-quality-tutorial)
    - [SQLCheckOperator | Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/modules/sqlcheckoperator): *Perform SQL checks in your data pipelines that can either grind your pipelines to a halt or just notify your team of changes. Check for things like:*
        - *Duplicates*
        - *Nulls*
        - *A list of allowed values*
