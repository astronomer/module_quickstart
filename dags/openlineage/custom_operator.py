OpenLineage - Extracting information for Custom Operators

**Before You Start**

- Have an understanding of OpenLineage, and it’s [interface in Astronomer](https://docs.astronomer.io/astro/data-lineage) Cloud
- Have an existing Connection and an existing Custom Operator

**(optional) Add OpenLineage to your project**

************************this is optional, as `openlineage-airflow` will already be in the `astro-runtime` image, but it is a good practice to be explicit that you are depending on it.*
****

- [ ]  Add line the following to your `requirements.txt`

    ```bash
    openlineage-airflow
    ```


**************************************************************Add an Custom Extractor from an Existing Extractor**************************************************************

To view the basics of adding a custom extractor, that inherits from an existing extractor:

- Add the following DAG to your project at `dags/test_lineage.py`

```bash
from datetime import datetime
from typing import List
from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from openlineage.airflow.extractors.snowflake_extractor import SnowflakeExtractor

# This is an example of a Custom Operator
class CustomSnowflakeOperator(SnowflakeOperator):
    pass

# This is an example of an Extractor for our Custom Operator,
# we are utilizing the SnowflakeExtractor as a base
# view other pre-existing Airflow extractors here:
# https://github.com/OpenLineage/OpenLineage/tree/main/integration/airflow#bundled-extractors
class CustomSnowflakeExtractor(SnowflakeExtractor):
    @classmethod
    def get_operator_classnames(cls) -> List[str]:
        return ["CustomSnowflakeOperator"]

# NOTE: It is better practice to place both your custom operator
# and custom extractor in files in the /include folder
# to keep your DAG code clean

with DAG(
	dag_id="test_lineage",
	start_date=datetime(1970, 1, 1),
	schedule=None
) as dag:
    CustomSnowflakeOperator(task_id="custom_snowflake_operator", sql="select 1;")
```

- [ ]  add the following to your `.env` **and** as an [Environment Variable in Astronomer](https://docs.astronomer.io/astro/environment-variables) for any deployments you will deploy this to

    ```bash
    OPENLINEAGE_EXTRACTORS=dags.test_lineage.CustomSnowflakeExtractor
    ```

    <aside>
    💡 If you need to add multiple custom extractor module paths to OpenLineage, you can do so separating them with a `;` like:

    ```bash
    OPENLINEAGE_EXTRACTORS=my.first.CustomExtractor;my.other.OtherExtractor
    ```

    </aside>

- [ ]  Deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Go to the `Lineage` tab in Astronomer and search for `custom_snowflake_operator`

    ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2068.png)


**Checkpoint**

You should now successfully have instrumented a Custom Operator with OpenLineage
****

**Next Steps**

- Instrument your existing custom operators with Custom OpenLineage Extractors
- Read this post describing the topic in more detail

    [Methods of Extracting Data Lineage from Apache Airflow - Astronomer](https://www.astronomer.io/blog/3-ways-to-extract-data-lineage-from-airflow/)

