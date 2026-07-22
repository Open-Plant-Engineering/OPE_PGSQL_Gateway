import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService

from gee.arrow.stream_serializer import (
    ArrowStreamSerializer,
)


@pytest.mark.asyncio
async def test_sql_stream():

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

    total_rows = 0
    total_batches = 0

    async for batch in db.sql.stream(
        "select * from generate_series(1,5000) id"
    ):

        payload = (
            ArrowStreamSerializer.serialize_batch(
                batch
            )
        )

        assert payload is not None
        assert len(payload) > 0

        total_batches += 1
        total_rows += len(batch)

    assert total_batches == 5
    assert total_rows == 5000