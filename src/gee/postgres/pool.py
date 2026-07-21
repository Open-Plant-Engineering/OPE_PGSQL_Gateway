import asyncpg


class PostgresPool:

    def __init__(self):
        self._pool = None

    async def connect(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ):
        self._pool = await asyncpg.create_pool(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            min_size=5,
            max_size=20,
        )

    @property
    def pool(self):
        return self._pool