from airflow.sdk import asset, Asset, Context
import requests


@asset(
    schedule= "@daily",
    uri= "https://randomuser.me/api/",
    extra= {"description": "Fetches a random user from the API"}
)
def user(self) -> dict[str]:
    r = requests.get(self.uri)
    return r.json()

@asset.multi(
        schedule= user,
        outlets= [
           Asset("user_location"),
           Asset("login_data") 
        ]
)
def user_info(user: Asset, context: Context) -> list[dict[str]]:
    user_data = context['ti'].xcom_pull(
        dag_id= user.name,
        task_ids= user.name,
        include_prior_dates=True
    )
    return {
        user_data['results'][0]['location'],
        user_data['results'][0]['login']
    }

# @asset(
#     schedule=user
# )
# def user_location(user: Asset, context: Context) -> dict[str]:
#     user_data = context['ti'].xcom_pull(
#         dag_id= user.name,
#         task_ids= user.name,
#         include_prior_dates=True
#     )
#     return user_data['results'][0]['location']

# @asset(
#     schedule= user
# )
# def login_data(user: Asset, context: Context) -> dict[str]:
#     user_data = context['ti'].xcom_pull(
#         dag_id= user.name,
#         task_ids= user.name,
#         include_prior_dates=True
#     )
#     return user_data['results'][0]['login']