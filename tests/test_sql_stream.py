import asyncio

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService

from gee.arrow.stream_serializer import (
    ArrowStreamSerializer,
)


async def main():

    settings = Settings()

    pool = PostgresPool()

    await pool.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        database=settings.pg_database,
        user=settings.pg_user,
        password=settings.pg_password,
    )

    db = DatabaseService(pool)

    async for batch in db.sql.stream(
        "select * from generate_series(1,5000) id"
    ):

        payload = (
            ArrowStreamSerializer.serialize_batch(
                batch
            )
        )

        print(
            f"Rows={len(batch)} "
            f"Bytes={len(payload)}"
        )


asyncio.run(main())