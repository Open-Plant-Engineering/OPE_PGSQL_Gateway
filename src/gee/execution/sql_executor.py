import asyncpg


class SqlExecutor:
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def execute(
        self,
        sql: str,
        *params,
    ):
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                sql,
                *params,
            )

        return rows

    async def stream(
        self,
        sql: str,
        *params,
        batch_size: int = 1000,
    ):
        async with self._pool.acquire() as conn:

            async with conn.transaction():

                cursor = conn.cursor(
                    sql,
                    *params,
                    prefetch=batch_size,
                )

                batch = []

                async for row in cursor:

                    batch.append(row)

                    if len(batch) >= batch_size:
                        yield batch
                        batch = []

                if batch:
                    yield batch