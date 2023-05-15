
### Module - Airflow Cross-DAG Dependencies (Datasets)

**Background information:**

- DAGs that access the same data now have explicit, visible relationships, and DAGs can be scheduled based on updates to these datasets
- You can define datasets in your Airflow environment and use them to create dependencies between DAGs. To define a dataset, instantiate the `Dataset`class and provide a string to identify the location of the dataset. This string must be in the form of a valid URI
- You can reference the dataset in a task by passing it to the task's `outlets`parameter. When you define a task's `outlets`parameter, Airflow labels the task as **a producer task** that updates the datasets
- Any task that is scheduled with a dataset is considered **a consumer task** even if that task doesn't consume the referenced dataset
- In the following example, we’ll read instructions on how to create and retrieve some informations about cocktails

**Getting Started:**

- [ ]  Add the code snippet below as `dags/datasets_producer_dag.py` - this DAG will look for a cocktail, write the instructions to `include/cocktail_instructions.txt` file and some high-level info to `include/cocktail_info.txt` file

    ```python
    import pendulum
    from datetime import datetime

    from airflow import DAG, Dataset
    from airflow.decorators import task

    API = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    INSTRUCTIONS = Dataset("file://localhost/airflow/include/cocktail_instructions.txt")
    INFO = Dataset("file://localhost/airflow/include/cocktail_info.txt")

    with DAG(
        dag_id="datasets_producer_dag",
        start_date=pendulum.datetime(2022, 10, 1, tz="UTC"),
        schedule=None,
        catchup=False,
    ):

        @task
        def get_cocktail(api):
            import requests

            r = requests.get(api)
            return r.json()

        @task(outlets=[INSTRUCTIONS])
        def write_instructions_to_file(response):
            cocktail_name = response["drinks"][0]["strDrink"]
            cocktail_instructions = response["drinks"][0]["strInstructions"]
            msg = f"See how to prepare {cocktail_name}: {cocktail_instructions}"

            f = open("include/cocktail_instructions.txt", "a")
            f.write(msg)
            f.close()

        @task(outlets=[INFO])
        def write_info_to_file(response):
            import time

            time.sleep(30)
            cocktail_name = response["drinks"][0]["strDrink"]
            cocktail_category = response["drinks"][0]["strCategory"]
            alcohol = response["drinks"][0]["strAlcoholic"]
            msg = f"{cocktail_name} is a(n) {alcohol} cocktail from category {cocktail_category}."
            f = open("include/cocktail_info.txt", "a")
            f.write(msg)
            f.close()

        cocktail = get_cocktail(api=API)

        write_instructions_to_file(cocktail)
        write_info_to_file(cocktail)
    ```

- [ ]  Add the code snippet below as `dags/datasets_consumer_dag.py` - this DAG will read the contents of the files and will run as soon as both Datasets are updated

    ```python
    import pendulum
    from datetime import datetime

    from airflow import DAG, Dataset
    from airflow.decorators import task

    INSTRUCTIONS = Dataset("file://localhost/airflow/include/cocktail_instructions.txt")
    INFO = Dataset("file://localhost/airflow/include/cocktail_info.txt")

    with DAG(
        dag_id="datasets_consumer_dag",
        start_date=pendulum.datetime(2022, 10, 1, tz="UTC"),
        schedule=[INSTRUCTIONS, INFO],  # Scheduled on the Datasets
        tags=["datasets", "cross-DAG dependencies"],
        catchup=False,
    ):

        @task
        def read_about_cocktail():
            cocktail = []
            for filename in ("info", "instructions"):
                with open(f"include/cocktail_{filename}.txt", "r") as f:
    	            contents = f.readlines()
    	            cocktail.append(contents)

            return [item for sublist in cocktail for item in sublist]

        read_about_cocktail()
    ```


**See them in action:**

- [ ]  Unpause `datasets_consumer_dag`. In the Airflow UI notice that:
    - in column `Schedule` you see `Dataset` instead of a CRON expression or a preset
    - `Next Run` states `0 of 2 datasets updated`
- [ ]  Trigger `datasets_producer_dag` (hit the ▶️ `Trigger DAG` button) and observe the behaviour of the second DAG. Key pieces to keep an eye out for:
    - As soon as the task `write_instructions_to_file` is completed, `Next Run` changes to `1 of 2 datasets updated` and the consumer DAG is still not running
    - Task `write_info_to_file` sleeps for 30 seconds, the consumer DAG is still waiting for the second Dataset to be updated
    - As soon as it completes, `dataset_consumer_dag` starts running

**Extras / Reference**

- References


    ### Datasets

    - [Datasets and data-aware scheduling in Airflow | Astronomer Guide](https://docs.astronomer.io/learn/airflow-datasets)
    - [Data Driver Scheduling | Astronomer Webinar](https://www.astronomer.io/events/live/data-driven-scheduling/)
    - [Data-aware scheduling | OSS Airflow Doc](https://airflow.apache.org/docs/apache-airflow/stable/concepts/datasets.html)
