import asyncpg


class FunctionExecutor:

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
        function_name: str,
        *function_parameters,
    ):

        parameter_placeholders = [
            f"${index + 1}"
            for index in range(
                len(function_parameters)
            )
        ]

        sql = (
            f"SELECT * "
            f"FROM {schema_name}.{function_name}"
            f"({','.join(parameter_placeholders)})"
        )

        async with (
            self._connection_pool.acquire()
        ) as connection:

            rows = await connection.fetch(
                sql,
                *function_parameters,
            )

        return rows

    async def stream(
        self,
        schema_name: str,
        function_name: str,
        *function_parameters,
        batch_size: int = 1000,
    ):

        parameter_placeholders = [
            f"${index + 1}"
            for index in range(
                len(function_parameters)
            )
        ]

        sql = (
            f"SELECT * "
            f"FROM {schema_name}.{function_name}"
            f"({','.join(parameter_placeholders)})"
        )

        async with (
            self._connection_pool.acquire()
        ) as connection:

            async with connection.transaction():

                cursor = connection.cursor(
                    sql,
                    *function_parameters,
                    prefetch=batch_size,
                )

                current_batch = []

                async for row in cursor:

                    current_batch.append(
                        row
                    )

                    if (
                        len(current_batch)
                        >= batch_size
                    ):

                        yield current_batch

                        current_batch = []

                if current_batch:

                    yield current_batch