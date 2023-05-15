
- Currently (as of May 2022), there is no direct backfill API endpoint.
- A workaround is possible by triggering a `backfill_trigger_dag` via the API and using `dag_run.conf` to pass in parameters such as `start_date`, `end_date`, and `dag_id` for the required backfill.
    - the `backfill_trigger_dag` will then trigger the backfill for the desired *target* DAG
        - ensure the `backfill_trigger_dag` is unpaused, with a schedule of `None` so that it can be triggered as needed but does not run on an interval

- [API Endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) to use: [`https://airflow.apache.org/api/v1/dags/{dag_id}/dagRuns`](https://airflow.apache.org/api/v1/dags/%7Bdag_id%7D/dagRuns)

**In the below example, we will use two DAGs:**

1. The `**backfill_trigger_dag**` - this DAG uses a `BashOperator` to run the Airflow CLI command `airflow dags backfill` and pulls in the `dag_run.conf` values from the API call being made to populate `start_date`, `end_date`, `dag_id`, etc.
    1. This is the dag_id (i.e. the DAG’s name)to be included in the POST request - such as (bolded):

    ```
    curl --location --request POST 'http://localhost:8080/api/v1/dags/**backfill_trigger_dag**/dagRuns' \
    ...
    ```

2. The `**dag_to_be_triggered**` - this is the DAG the backfill is being performed on (i.e. the *target* DAG).
    1. this is the DAG name to be included in the json `conf` such as (bolded):

    ```
    ...
    --data-raw '{
        "conf": {"dag_id": "**example_dag_basic**", "date_start": 20220425, "date_end": 20220430}
    }'
    ```


**The DAG responsible for triggering the backfill:**

**`backfill_trigger_dag`:**

<aside>
💡 **Note:** The commented `trigger_backfill` task shows how you would hard-code these parameters to perform a backfill without using the API.

Instead, we will use the un-commented task which uses Jinja templates to pull in the `dag_run.conf` values from the API call:

</aside>

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(dag_id='backfill_trigger_dag',
         schedule=None,
         start_date=datetime(2022, 1, 1),
         tags=['backfill-trigger-cli'],
         catchup=False) as dag:

    # Method 1: Trigger a backfill using hard-coded dates & dag_id:
    # trigger_backfill = BashOperator(
    #     task_id='trigger_backfill',
    #     bash_command='airflow dags backfill --reset-dagruns -y -s 20220401 -e 20220410 example_dag_basic',
    # )

    # Method 2: Use the REST API or trigger a DAG run with conf to trigger a backfill, passing in start/end dates and dag_id etc:
    trigger_backfill = BashOperator(
        task_id='trigger_backfill',
        bash_command="airflow dags backfill --reset-dagruns -y -s {{ dag_run.conf['date_start'] }} -e {{ dag_run.conf['date_end'] }} {{ dag_run.conf['dag_id'] }}"
    )

    trigger_backfill
```

**Example cURL request using localhost:**

```bash
curl --location --request POST 'http://localhost:8080/api/v1/dags/backfill_trigger_dag/dagRuns' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46YWRtaW4=' \
--data-raw '{
    "conf": {"dag_id": "example_dag_basic", "date_start": 20220425, "date_end": 20220430}
}'
```

**Example Python/Requests using localhost:**

```python
import requests
import json

url = "http://localhost:8080/api/v1/dags/backfill_trigger_dag/dagRuns"

payload = json.dumps({
  "conf": {
    "dag_id": "example_dag_basic",
    "date_start": 20220425,
    "date_end": 20220430
  }
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic YWRtaW46YWRtaW4='
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
