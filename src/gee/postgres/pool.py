import asyncpg


class PostgresPool:

    def __init__(
        self,
        settings,
    ):
        self._settings = settings

        self._connection_pool = None

    async def connect(self):
    
        postgres = (
            self._settings.postgres
        )
    
        self._connection_pool = (
            await asyncpg.create_pool(
                host=postgres.host,
                port=postgres.port,
                database=postgres.database,
                user=postgres.user,
                password=postgres.password,
                min_size=postgres.min_pool_size,
                max_size=postgres.max_pool_size,
            )
        )

    async def close(
        self,
    ):

        if self._connection_pool:

            await self._connection_pool.close()

    @property
    def pool(
        self,
    ):
        return self._connection_pool