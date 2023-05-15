
### Module - Airflow Templating

**Background information**

Templating in Airflow works exactly the same as templating with [Jinja](https://www.notion.so/Resource-Glossary-a45cce63a5c7468b922454fd937d4a5c) in Python: define your to-be-evaluated code between double curly braces, and the expression will be evaluated at runtime.

Templates cannot be applied to all arguments of an operator. Two attributes in the BaseOperator define limitations on templating:

- `template_fields`: Defines which fields are templateable
- `template_ext`: Defines which file extensions are templateable.

Airflow includes [many variables which can be used for templating](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html). Some of the most used variables are:

- `{{ ds }}`: The DAG Run’s logical date as `YYYY-MM-DD`
- `{{ ds_nodash }}`: The DAG run’s logical date as `YYYYMMDD`
- `{{ data_interval_start }}`: Start of the data interval
- `{{ data_interval_end }}`: End of the data interval

- **Use built-in variables accessible in all templates**
    - [ ]  Add a sample DAG to your `dags/` directory

    ```python
    import pendulum
    from datetime import timedelta

    from airflow import DAG
    from airflow.decorators import task
    from airflow.operators.bash import BashOperator

    default_args = {
        'owner': 'cs',
        'retries': 3,
        'retry_delay': timedelta(seconds=15),
        }

    with DAG(dag_id='templating',
             start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
             schedule_interval="@monthly",
             default_args=default_args,
             catchup=False,
             ) as dag:

        @task
        def print_logical_date_with_python(ds=None):
            print("The DAG Run's logical date is " + ds)

        print_next_logical_date_with_bash = BashOperator(
            task_id='print_next_logical_date_with_bash',
            bash_command='echo "Next DAG Run\'s logical date is {{ next_ds }}"',
        )

        [print_logical_date_with_python(), print_next_logical_date_with_bash]
    ```

    - [ ]  Unpause the DAG
    - [ ]  Check the logs of `print_logical_date_with_python` task, you should see something similar:

    ```python
    {logging_mixin.py:115} INFO - The DAG Run's logical date is 2022-07-01
    ```

    - [ ]  Check the logs of `print_next_logical_date_with_bash` task, you should see something similar:

    ```python
    {subprocess.py:74} INFO - Running command: ['bash', '-c', 'echo "Next DAG Run\'s logical date is 2022-08-01"']
    {subprocess.py:85} INFO - Output:
    {subprocess.py:92} INFO - Next DAG Run's logical date is 2022-08-01
    ```

- **Retrieve Airflow Variables**
    - [ ]  Add a dummy Variable `templating_test`- go to Airflow UI, click on Admin >> Variables and add a new record as shown below

    ![Screenshot 2022-08-09 at 10.03.35.png](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Screenshot_2022-08-09_at_10.03.35.png)

    - [ ]  Add a new task to your DAG

    ```python
        retrieve_variable = BashOperator(
            task_id='retrieve_variable',
            bash_command='echo {{ var.value.templating_test }}',
        )
    ```

    - [ ]  Update the task dependencies

    ```python
        [print_logical_date_with_python(), print_next_logical_date_with_bash] >> retrieve_variable
    ```

    - [ ]  Trigger the DAG manually - hit the ▶️ `Trigger DAG` button to see a successful run
    - [ ]  Check the logs of `retrieve_variable` task, you should see the following:

    ```python
    {subprocess.py:74} INFO - Running command: ['bash', '-c', 'echo This is the value of my variable.']
    {subprocess.py:85} INFO - Output:
    {subprocess.py:92} INFO - This is the value of my variable.
    ```

- **Retrieve Airflow Connections**
    - [ ]  Add a dummy connection `test_conn`- go to Airflow UI, click on Admin >> Connections and add a new record as shown below

    ![Screenshot 2022-08-09 at 10.31.29.png](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Screenshot_2022-08-09_at_10.31.29.png)

    - [ ]  Add new tasks to your DAG

    ```python
        retrieve_connection = BashOperator(
            task_id='retrieve_connection',
            bash_command='echo {{ conn.test_conn }}',
        )

        retrieve_field_from_conn = BashOperator(
            task_id='retrieve_field_from_conn',
            bash_command='echo "This is the login: {{ conn.test_conn.login }}"',
        )
    ```

    - [ ]  Update the task dependencies

    ```python
        [print_logical_date_with_python(), print_next_logical_date_with_bash] >> \
        retrieve_variable >> \
        [retrieve_connection, retrieve_field_from_conn]
    ```

    - [ ]  Trigger the DAG manually - hit the ▶️ `Trigger DAG` button to see a successful run
    - [ ]  Check the logs of both new tasks, you should see the following:
    - `retrieve_connection`:

    ```python
    {subprocess.py:74} INFO - Running command: ['bash', '-c', 'echo test_conn']
    {subprocess.py:85} INFO - Output:
    {subprocess.py:92} INFO - test_conn
    ```

    - `retrieve_field_from_conn`:

    ```python
    {subprocess.py:74} INFO - Running command: ['bash', '-c', 'echo "This is the login: my_login"']
    {subprocess.py:85} INFO - Output:
    {subprocess.py:92} INFO - This is the login: my_login
    ```


**Checkpoint**
At this point you should:

- Understand how to apply Jinja templates in your code

**Extras / Reference**

- References


    ### Templating

    - [Templates Reference | Apache Airflow Doc](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html)
    - [Templating in Airflow | Astronomer Guide](https://www.astronomer.io/guides/templating)
