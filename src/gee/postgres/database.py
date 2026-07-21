from gee.execution.sql_executor import SqlExecutor
from gee.execution.function_executor import FunctionExecutor
from gee.execution.procedure_executor import ProcedureExecutor


class DatabaseService:
    def __init__(self, pool):
        self._pool = pool

    @property
    def sql(self):
        return SqlExecutor(self._pool.pool)

    @property
    def function(self):
        return FunctionExecutor(self._pool.pool)

    @property
    def procedure(self):
        return ProcedureExecutor(self._pool.pool)