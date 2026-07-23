import asyncpg


class SqlExecutor:

    def __init__(
        self,
        connection_pool: asyncpg.Pool,
        batch_size: int,
    ):
        self._connection_pool = (
            connection_pool
        )
        self._batch_size = batch_size

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
    ):

        async with (
            self._connection_pool.acquire()
        ) as connection:

            async with connection.transaction():

                cursor = connection.cursor(
                    sql,
                    *parameters,
                    prefetch=self._batch_size,
                )

                current_batch = []

                async for row in cursor:

                    current_batch.append(
                        row
                    )

                    if (
                        len(current_batch)
                        >= self._batch_size
                    ):

                        yield current_batch

                        current_batch = []

                if current_batch:

                    yield current_batch