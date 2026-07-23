from gee.execution.sql_executor import SqlExecutor
from gee.execution.function_executor import FunctionExecutor
from gee.execution.procedure_executor import (
    ProcedureExecutor,
)


class DatabaseService:

    def __init__(
        self,
        connection_pool,
    ):
        self._connection_pool = (
            connection_pool
        )

        self._sql_executor = SqlExecutor(
            self._connection_pool.pool
        )

        self._function_executor = (
            FunctionExecutor(
                self._connection_pool.pool
            )
        )

        self._procedure_executor = (
            ProcedureExecutor(
                self._connection_pool.pool
            )
        )

    @property
    def sql(
        self,
    ) -> SqlExecutor:
        return self._sql_executor

    @property
    def function(
        self,
    ) -> FunctionExecutor:
        return self._function_executor

    @property
    def procedure(
        self,
    ) -> ProcedureExecutor:
        return self._procedure_executor