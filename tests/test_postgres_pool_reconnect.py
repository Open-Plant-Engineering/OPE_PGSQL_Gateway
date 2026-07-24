import pytest

from gee.postgres.pool import (
    PostgresPool,
)


@pytest.mark.asyncio
async def test_postgres_pool_reconnect(
    settings,
):

    pool = PostgresPool(
        settings
    )

    await pool.connect()

    assert (
        pool.pool
        is not None
    )

    await pool.close()

    await pool.connect()

    assert (
        pool.pool
        is not None
    )

    await pool.close()