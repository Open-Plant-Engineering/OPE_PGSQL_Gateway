import asyncio

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService


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
        "add_numbers",
        10,
        20,
    )

    assert len(rows) == 1

    result = rows[0]["add_numbers"]

    assert result == 30

    print(f"SUCCESS: 10 + 20 = {result}")


asyncio.run(main())