import asyncio

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService

from gee.arrow.serializer import ArrowSerializer
from gee.arrow.deserializer import ArrowDeserializer


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

    rows = await db.function.execute(
        "public",
        "get_numbers"
    )

    payload = ArrowSerializer.serialize(rows)

    print(f"Payload Size: {len(payload)} bytes")

    table = ArrowDeserializer.deserialize(payload)

    print(table)

    print(table.to_pydict())


asyncio.run(main())