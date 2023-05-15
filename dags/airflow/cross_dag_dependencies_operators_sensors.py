
### Module - Airflow Cross-DAG Dependencies (TriggerDagRunOperator, ExternalTaskSensor)

**Background information:**

<aside>
💡 When two DAGs have [dependency relationships](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external_task_sensor.html), it is worth considering combining them into a single DAG, which is usually simpler to understand. However, it is not always practical to put all related tasks on the same DAG due to different schedule intervals, a DAG depending on tasks in another DAG, etc.

</aside>

- In the following example, we’ll use `TriggerDagRunOperator` in the `cross_dag_dependency_trigger_dag` DAG  (aka the "Trigger" DAG), to trigger the `cross_dag_dependency_triggered_dag` DAG, aka (the "Triggered" DAG), and `ExternalTaskSensor`in the Trigger to check when a task in the Triggered DAG has finished running.

**Getting Started:**

- [ ]  Add the code snippet below as `dags/cross_dag_dependency_trigger_dag.py` - this DAG will trigger the other DAG

    ```python
    from datetime import datetime
    from airflow import DAG
    from airflow.sensors.external_task import ExternalTaskSensor
    from airflow.operators.trigger_dagrun import TriggerDagRunOperator
    from airflow.operators.empty import EmptyOperator

    with DAG(dag_id='cross_dag_dependency_trigger_dag',
             schedule="@once",
             start_date=datetime(2022, 1, 1),
             catchup=False) \
            as dag:
        trigger_another_dag = TriggerDagRunOperator(
            task_id="trigger_another_dag",
            trigger_dag_id="cross_dag_dependency_triggered_dag",  # Ensure this equals the dag_id of the DAG to trigger
            execution_date="{{ execution_date }}",
            conf={"message": "Sending greetings from the trigger DAG!"},
        )

        check_external_task = ExternalTaskSensor(
            task_id="check_external_task",
            external_task_id="print_with_bash", # Ensure this equals the task_id of the task in the External DAG
            external_dag_id="cross_dag_dependency_triggered_dag", # Ensure this equals the dag_id of the External DAG
            poke_interval=5
        )
    		trigger_another_dag >> check_external_task
    ```

- [ ]  Add the code snippet below as `dags/cross_dag_dependency_trigger_dag.py` - this DAG will be triggered

    ```python
    from datetime import datetime
    from airflow import DAG
    from airflow.operators.bash import BashOperator
    from airflow.operators.empty import EmptyOperator

    with DAG(dag_id='cross_dag_dependency_triggered_dag',
             schedule=None,
             start_date=datetime(2022, 1, 1),
             catchup=False) \
            as dag:

        BashOperator(
            task_id="print_with_bash",
            bash_command='echo "Here is the message: $message"',
            env={'message': '{{ dag_run.conf["message"] if dag_run else "" }}'},
        )
    ```


**See them in action:**

- [ ]  Unpause both DAGs and observe their behavior. Key pieces to keep an eye out for:
    - The `trigger_another_dag` task in the Trigger DAG (blue box in screenshot below) will automatically trigger a run of the Triggered DAG, despite the Triggered DAG having a `schedule_interval=None`
    - The `check_external_task` task in the Trigger DAG (pink box in screenshot below) will poke every 5 seconds (adjustable in the parameter `poke_interval=5`) to check when the `print_with_bash` task in the Triggered DAG has completed running
    - In this example, we are passing `execution_date="{{ execution_date }}"`in the `TriggerDagRunOperator` which causes both of these DAGs to have the same `execution_date` (red boxes in screenshot below)
        - This is especially important for the `ExternalTaskSensor`, which requires the same `execution_date` as the DAG that triggered. Otherwise, you can use [optional parameters](https://airflow.apache.org/docs/apache-airflow/2.3.2/_api/airflow/sensors/external_task/index.html#airflow.sensors.external_task.ExternalTaskSensor) such as `execution_delta` or `execution_date_fn` to specify acceptable timeframes for checking a task’s success.

        ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%206.png)


**Next Steps**

- [ ]  Add cross-DAG dependencies into your workflows when their use is justified.
    - See Extras/References section below for further reading and more fine-grain control over these dependencies.

- **Extras/References**


    ### Cross-DAG Dependencies

    - [Cross-DAG Dependencies | Astronomer Guide](https://www.astronomer.io/guides/cross-dag-dependencies/)
    - [Cross-DAG Dependencies | Apache Docs](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external_task_sensor.html)
    - [ExternalTaskSensor | Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/modules/externaltasksensor)
    - [TriggerDagRunOperator | Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/modules/triggerdagrunoperator)
