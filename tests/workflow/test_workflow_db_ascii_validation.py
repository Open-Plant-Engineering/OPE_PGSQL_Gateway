import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService


@pytest.mark.asyncio
async def test_workflow_db_ascii_validation():
    """
    Workflow:

        Execute Procedure
              ↓
        Read Random 100 Rows
              ↓
        Validate Word
              ↓
        Validate Sum
    """

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

    #
    # Execute procedure before validation
    #
    await db.procedure.execute(
        "public",
        "calculate_ascii_metadata",
    )

    rows = await db.sql.execute(
        """
        SELECT *
        FROM workflow_ascii
        ORDER BY random()
        LIMIT 100;
        """
    )

    assert len(rows) == 100

    for row in rows:

        expected_word = (
            chr(row["ascii1"]) +
            chr(row["ascii2"]) +
            chr(row["ascii3"])
        )

        expected_sum = (
            row["ascii1"] +
            row["ascii2"] +
            row["ascii3"]
        )

        assert row["word"] == expected_word
        assert row["sum"] == expected_sum