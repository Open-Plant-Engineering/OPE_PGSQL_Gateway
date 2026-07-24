import logging

import pytest


@pytest.mark.asyncio
async def test_pool_logging(
    settings,
    caplog,
):

    from gee.postgres.pool import (
        PostgresPool,
    )

    with caplog.at_level(
        logging.INFO
    ):

        pool = PostgresPool(
            settings
        )

        await pool.connect()

        await pool.close()

    assert (
        "PostgreSQL Connected"
        in caplog.text
    )

    assert (
        "Closing PostgreSQL Pool"
        in caplog.text
    )

    assert (
        "PostgreSQL Pool Closed"
        in caplog.text
    )