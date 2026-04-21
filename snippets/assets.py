from airflow.sdk import asset

@asset(
    name = "my_asset",
    schedule="@daily",
    uri=  "file://path/to/my/asset",
    extra= {"size_mb": 2},
    group= "the_assets"
)
def my_asset():
    return "This is my asset content"