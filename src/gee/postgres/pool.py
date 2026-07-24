import asyncpg
import logging

logger = logging.getLogger(__name__)

class PostgresPool:

    def __init__(
        self,
        settings,
    ):
        self._settings = settings

        self._connection_pool = None

    async def connect(self):
    
        logger.info(
            "Connecting to PostgreSQL"
        )
    
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

        logger.info(
            "PostgreSQL Connected"
        )
    

        logger.info(
            "Host=%s",
            self._settings.postgres.host,
        )

        logger.info(
            "Port=%s",
            self._settings.postgres.port,
        )

        logger.info(
            "Database=%s",
            self._settings.postgres.database,
        )

        logger.info(
            "MinPoolSize=%s",
            self._settings.postgres.min_pool_size,
        )

        logger.info(
            "MaxPoolSize=%s",
            self._settings.postgres.max_pool_size,
        )

    async def close(
        self,
    ):

        if self._connection_pool:

            logger.info(
                "Closing PostgreSQL Pool"
            )

            await self._connection_pool.close()

            logger.info(
                "PostgreSQL Pool Closed"
            )

        else:

            logger.warning(
                "PostgreSQL Pool is not "
                "initialized"
            )

    @property
    def pool(
        self,
    ):
        return self._connection_pool