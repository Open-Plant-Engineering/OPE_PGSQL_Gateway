import asyncpg


class FunctionExecutor:
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def execute(
        self,
        schema: str,
        function_name: str,
        *params,
    ):
        placeholders = [
            f"${idx + 1}"
            for idx in range(len(params))
        ]

        sql = (
            f"SELECT * "
            f"FROM {schema}.{function_name}"
            f"({','.join(placeholders)})"
        )

        async with self._pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)

        return rows