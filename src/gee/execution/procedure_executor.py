import asyncpg


class ProcedureExecutor:
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def execute(
        self,
        schema: str,
        procedure_name: str,
        *params,
    ):
        placeholders = [
            f"${idx + 1}"
            for idx in range(len(params))
        ]

        sql = (
            f"CALL {schema}.{procedure_name}"
            f"({','.join(placeholders)})"
        )

        async with self._pool.acquire() as conn:
            await conn.execute(sql, *params)

        return True