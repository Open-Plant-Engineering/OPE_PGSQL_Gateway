import asyncpg


class ProcedureExecutor:

    def __init__(
        self,
        connection_pool: asyncpg.Pool,
    ):
        self._connection_pool = (
            connection_pool
        )

    async def execute(
        self,
        schema_name: str,
        procedure_name: str,
        *procedure_parameters,
    ):

        parameter_placeholders = [
            f"${index + 1}"
            for index in range(
                len(procedure_parameters)
            )
        ]

        sql = (
            f"CALL {schema_name}.{procedure_name}"
            f"({','.join(parameter_placeholders)})"
        )

        async with (
            self._connection_pool.acquire()
        ) as connection:

            await connection.execute(
                sql,
                *procedure_parameters,
            )

        return True