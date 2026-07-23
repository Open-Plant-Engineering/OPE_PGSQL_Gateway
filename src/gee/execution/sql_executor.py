import asyncpg


class SqlExecutor:

    def __init__(
        self,
        connection_pool: asyncpg.Pool,
    ):
        self._connection_pool = (
            connection_pool
        )

    async def execute(
        self,
        sql: str,
        *parameters,
    ):

        async with (
            self._connection_pool.acquire()
        ) as connection:

            rows = await connection.fetch(
                sql,
                *parameters,
            )

        return rows

    async def stream(
        self,
        sql: str,
        *parameters,
        batch_size: int = 1000,
    ):

        async with (
            self._connection_pool.acquire()
        ) as connection:

            async with connection.transaction():

                cursor = connection.cursor(
                    sql,
                    *parameters,
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