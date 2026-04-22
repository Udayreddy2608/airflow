from typing import Any

__version__ = "0.1.0"
__all__ = ["sql"]

def get_provider_info() -> dict[str, Any]:
    return {
        "package-name": "my-sdk",
        "name": "My SDK",
        "description": "A simple SDK for demonstration purposes.",
        "versions": [__version__],
        "task-decorators": [
            {
                "name": "sql",
                "class-name": "my_sdk.decorators.sql.sql_task",
            }
        ],
    }