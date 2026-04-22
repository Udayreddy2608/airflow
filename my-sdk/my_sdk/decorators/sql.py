from airflow.sdk.bases.decorator import DecoratedOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.definitions._internal.types import SET_DURING_EXECUTION
from airflow.utils.context import context_merge
from airflow.utils.operator_helpers import determine_kwargs
from airflow.sdk.definitions.context import Context
from airflow.sdk.bases.decorator import task_decorator_factory, TaskDecorator

from typing import Any, ClassVar, Collection, Mapping, Callable
from collections.abc import Sequence
import warnings





class _SQLDECORATEDOPERATOR(DecoratedOperator, SQLExecuteQueryOperator):
    template_fields : Sequence[str] = (*DecoratedOperator.template_fields,
                                        *SQLExecuteQueryOperator.template_fields)
    
    template_field_renderers: ClassVar[dict[str, str]] = {
        **DecoratedOperator.template_fields_renderers,
        **SQLExecuteQueryOperator.template_fields_renderers
    }

    custom_operator_name: str = "@task.sql"
    overwrite_rtif_after_execution: bool = True

    def __init__(
        self,
        *,
        python_callable= Callable,
        op_args: Collection[Any] | None = None,
        op_kwargs: Mapping[str, Any] | None = None,
        **kwargs,
    ) -> None:
        
        if kwargs.pop(
            "multiple_outputs", None
        ):
            warnings.warn(
                "The 'multiple_outputs' argument is not supported in @task.sql and will be ignored.",
                UserWarning,
                stacklevel=3
            )
        
        super().__init__(
            python_callable=python_callable,
            op_args=op_args,
            op_kwargs=op_kwargs,
            multiple_outputs=False,
            sql = SET_DURING_EXECUTION,
            **kwargs
        )
    
    def execute(self, context: Context) -> Any:
        context_merge(context, self.op_kwargs)
        kwargs = determine_kwargs(self.python_callable, self.op_args, context)
        
        self.sql = self.python_callable(*self.op_args,**kwargs)
        
        if not isinstance(self.sql, str) or self.sql.strip() == "":
            raise ValueError("The python_callable must return a string representing the SQL query.")
        context["ti"].render_templates()

        return super().execute(context)


def sql_task(
        python_callable: Callable | None = None,
        **kwargs
) -> TaskDecorator:
    
    return task_decorator_factory(
        python_callable=python_callable,
        decorated_operator_class=_SQLDECORATEDOPERATOR,
        **kwargs
    )
