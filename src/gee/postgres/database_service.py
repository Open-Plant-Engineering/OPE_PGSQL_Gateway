from gee.execution.sql_executor import SqlExecutor
from gee.execution.function_executor import FunctionExecutor
from gee.execution.procedure_executor import (
    ProcedureExecutor,
)


class DatabaseService:

    def __init__(
        self,
        connection_pool,
        settings,
    ):
        self._settings = settings
        batch_size = (
            self._settings.streaming.batch_size
        )

        self._connection_pool = (
            connection_pool
        )

        self._sql_executor = SqlExecutor(
            self._connection_pool.pool,
            batch_size=batch_size
        )

        self._function_executor = (
            FunctionExecutor(
                self._connection_pool.pool,
                batch_size=batch_size
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