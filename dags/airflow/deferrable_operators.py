
### Module - Airflow Deferrable Operators

**Before you start:**

- To use deferrable operators both in a local Airflow environment and on Astro, you must have:
    - An [Astro project](https://docs.astronomer.io/astro/create-project) running [Astro Runtime 4.2.0+](https://docs.astronomer.io/astro/runtime-release-notes#astro-runtime-420).
    - The [Astro CLI v1.1.0+](https://docs.astronomer.io/astro/cli-release-notes#v110) installed.
- This example will showcase using `ExternalTaskSensorAsync` rather than the traditional `ExternalTaskSensor`

**Add the DAGs to your project:**

- [ ]  Add the following 2 DAGs to your `/dags` folder
    - DAG 1 - This DAG contains several `BashOperator` tasks that sleep for 10 seconds each.

        ```python
        from airflow import DAG
        from airflow.operators.empty import EmptyOperator
        from datetime import datetime, timedelta
        from airflow.operators.bash import BashOperator

        with DAG(dag_id='deferrable_sleep_dag'
                 schedule_interval="@daily",
                 start_date=datetime(2022, 1, 1),
                 catchup=False) as dag:

            start = EmptyOperator(
                task_id='start')

            sleep_task_1 = BashOperator(
                task_id='sleep_task_1',
                bash_command='sleep 10s'
            )

            sleep_task_2 = BashOperator(
                task_id='sleep_task_2',
                bash_command='sleep 10s'
            )

            sleep_task_3 = BashOperator(
                task_id='sleep_task_3',
                bash_command='sleep 10s'
            )

            finish = EmptyOperator(
                task_id='finish')

            start >> sleep_task_1 >> sleep_task_2 >> sleep_task_3 >> finish
        ```

    - DAG 2 - This DAG contains a task using `ExternalTaskSensorAsync` which will sense when `sleep_task_2` from DAG 1 has finished running.

        ```python
        from airflow import DAG
        from datetime import timedelta
        from airflow.operators.empty import EmptyOperator
        from airflow.utils.timezone import datetime

        from astronomer.providers.core.sensors.external_task import ExternalTaskSensorAsync

        with DAG(
            dag_id="deferrable_operator_dag",
            start_date=datetime(2022, 1, 1),
            schedule_interval='@daily',
            catchup=False
        ) as dag:

            start = EmptyOperator(task_id="start")

            external_task_async = ExternalTaskSensorAsync(
                task_id="external_task_async",
                external_task_id="sleep_task_2",
                external_dag_id="deferrable_sleep_dag",
            )

            finish = EmptyOperator(task_id="finish")

            start >> external_task_async >> finish
        ```


**Spin up your local astro project & unpause DAGs:**

- [ ]  In your local project, run `astro dev start`
    - This will spin up 4 Docker containers, one of which runs the **Triggerer** service, which is responsible for running Triggers, a requirement for using async operators.
- [ ]  Unpause the two DAGs at the same time and monitor the deferred `external_task_async` in DAG 2 to see it defer its execution until `sleep_task_2` has succeeded.

<aside>
💡 **Note:** As with the traditional `ExternalTaskSensor`, in order for the `ExternalTaskSensorAsync` to succeed, the `execution_date` of both DAG 1 & DAG 2 must be the same. Both DAGs have a schedule of `@daily` and `Catchup=False` which means that once they are both unpaused, they will both perform a single scheduled run with the same `execution_date` in order to showcase the async task. If you manually trigger them at different times, the sensor will not succeed. If you wish to re-run the DAGs to see them in action, simply clear them both from the first task so that they re-run with the same **scheduled** `execution_date`.

</aside>

**See the DAGs in action:**

To illustrate this, both DAGs are running with the same `execution_date` of `2022-06-28 00:00:00+00:00` (as shown in red boxes) and the `external_task_async` task in the 2nd DAG is deferring and sensing to check when `sleep_task_2` completes (as shown in orange boxes):

![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%207.png)

**Checkpoint**

- You have now successfully implemented and observed the `ExternalTaskSensorAsync` deferrable sensor in action.

Next Steps:

- [ ]  [View available async/deferrable](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst) operators and keep up with new ones being released. On this same page, example DAGs are available for each new operator being released.
- [ ]  Implement async/deferrable operators rather than traditional versions wherever available.
    - For example, if you currently use `[DatabricksSubmitRunOperator](https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/_api/airflow/providers/databricks/operators/databricks/index.html#airflow.providers.databricks.operators.databricks.DatabricksSubmitRunOperator)`, consider replacing with `[DatabricksSubmitRunDeferrableOperator](https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/_api/airflow/providers/databricks/operators/databricks/index.html#airflow.providers.databricks.operators.databricks.DatabricksSubmitRunDeferrableOperator)`

    <aside>
    💡 Since async/deferrable operators take all of the same parameters as the traditional versions of the operators, you can simply re-alias the operator’s import statement to avoid making further changes DAGs.
    For example:
    **Before:** `from astronomer.providers.databricks.operators.databricks import DatabricksRunNowOperatorAsync`
    **After:**
    `from astronomer.providers.databricks.operators.databricks import DatabricksRunNowOperatorAsync **as DatabricksRunNowOperator**`

    </aside>

- Reference


    ### Deferrable Operators

    > In general, deferrable operators should be used whenever you have tasks that occupy a worker slot while polling for a condition in an external system. This can include sensors and long-running tasks. There are numerous benefits to using deferrable operators. Some of the most notable are:
    >
    >
    > > **Reduced resource consumption:** Depending on the available resources and the workload of your triggers, you can run hundreds to thousands of deferred tasks in a single Triggerer process. This can lead to a reduction in the number of workers needed to run tasks during periods of high concurrency. With less workers needed, you are able to scale down the underlying infrastructure of your Airflow environment
    > >
    - [Deferrable Operators & Triggers | Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/concepts/deferring.html#:~:text=A%20deferrable%20operator%20is%20one,to%20something%20called%20a%20Trigger.)
    - [Deferrable Operators | Astronomer Guide](https://www.astronomer.io/guides/deferrable-operators)
    - [Deferrable Operators | Google Slides](https://docs.google.com/presentation/d/1ATtvBecqG5017TvIId1e3Qa3uozPUeL1QRnVSj0Z0eg/edit?usp=sharing)
    - [Deferrable Operators - Change log (which Operators are available)](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst)
    - [Everything you Need to Know About Airflow 2.2 | Astronomer Webinar](https://youtu.be/SwN1D9JHAiw?t=1238)
    - [Astronomer Provider (Deferrable Operators from Astronomer) | Repo](https://github.com/astronomer/astronomer-providers/blob/main/README.rst)
