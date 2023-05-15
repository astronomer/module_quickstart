
### Module - Airflow REST API

**Background Information:**

To facilitate management, Apache Airflow supports a range of [REST API endpoints](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) across its objects. You can use a third party client, such as [curl](https://curl.haxx.se/), [HTTPie](https://httpie.org/), [Postman](https://www.postman.com/) or [the Insomnia rest client](https://insomnia.rest/) to test the Apache Airflow API. Note that you will need to pass credentials data.

In the following example, we’ll use [Postman](https://www.postman.com/) to test and build a sample API request to [list DAGs](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_dags) in a deployment.

**Before you start:**

In order to follow along with this guide, you’ll need:

- [ ]  A free [Postman](https://www.postman.com/) account and download the [Postman Desktop App](https://www.postman.com/downloads/)
- [ ]  An Astro deployment

**Download and add the Airflow REST API into Postman**

- [ ]  Download the OpenAPI specification located at the top of the [Airflow REST API page](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html)
- [ ]  Create a workspace in Postman:

    ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%208.png)


- [ ]  Import the downloaded Airflow API into your new workspace:

    ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%209.png)


- You should now see a menu containing the same API endpoints available on the [Airflow REST API doc page](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html):

    ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2010.png)


**Build an API request:**

- [ ]  In the API endpoint list, select the `dags` dropdown, then select `List DAGs` :

    ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2011.png)


- [ ]  In the `GET` field, replace the pre-populated URL with your Airflow deployment’s URL which can be found when viewing your Airflow UI:

    ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2012.png)

    - Remove `/home` from the end of your Airflow URL
    - Add the desired endpoint to the end of the URL
        - It will be in the format `/api/v1/{desired_endpoint}` which can also be found in the Airflow Rest API docs:

            ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2013.png)

        - For this example, the endpoint for listing DAGs will be: `/api/v1/dags`
    - **To summarize,** if your Airflow UI URL is: `https://mycompany.astronomer.run/d55x5h33/home`,
    - It will become: `https://mycompany.astronomer.run/d55x5h33/api/v1/dags` (reminder, note the removal of `/home` from the deployment URL)
        - Example showing the updated `GET` field:

            ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2014.png)


- [ ]  For simplicity in this example, uncheck the pre-selected Query Params:

    ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2015.png)


- [ ]  Retrieve an [Access Token](https://docs.astronomer.io/astro/airflow-api#step-1-retrieve-an-access-token-and-deployment-url) to authorize the API request:
    - For a one-time use token, visit [https://cloud.astronomer.io/token](https://cloud.astronomer.io/token) and copy the access token
    - In Postman, click `Authorization` and select `Type: Bearer Token`
        - Paste the access token obtained in the previous steps:

            ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2016.png)


- [ ]  Click `Send` to submit the API request. The results of the request will be shown below. In this example, since we used the `List DAGs` endpoint, we receive json output containing information about all of the DAGs in the deployment:

    ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2017.png)


**Checkpoint**

- You have now successfully built and made an Airflow REST API request to retrieve information about DAGs in your deployment

**Next Steps**

- [ ]  View the full API request being made:
    - Postman provides the API request you just made in many forms so that you can modify or re-use them. On the right-hand side of the page, click the `code` icon to see these:

    ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2018.png)

    - For example, you can obtain the `cURL` version of this API request to be used directly in your CLI:

        ![Untitled](ADE%20Modules%20&%20Knowledge%20Base%20%5BDEPRECATING%5D%20395fc8c6c2e74faaa859c326369eeb50/Untitled%2019.png)


- [ ]  Explore and get familiar with the other available [endpoints](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) in the API, for example, [Trigger a new DAG run](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run)

- [ ]  If you have an automated [CI/CD process](https://docs.astronomer.io/astro/ci-cd) configured, we recommend including logic to generate a [fresh access token](https://docs.astronomer.io/astro/airflow-api#step-1-retrieve-an-access-token-and-deployment-url). If you add a step to your CI/CD pipeline that automatically generates an API access token, for example, you can avoid having to generate the token manually.

**Extras / Reference**

- Reference


    - [Airflow Rest API | Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html)
    - [Make Requests to the Airflow REST API | Astronomer Doc](https://docs.astronomer.io/astro/airflow-api)
    - [Airflow 2.0 Series - Stable REST API | Astronomer Youtube](https://www.youtube.com/watch?v=LODs9yTpMlo&list=PLCi-q9vYo4x-PESoBcXN0tXCMgzh5c_Pj&index=3)
