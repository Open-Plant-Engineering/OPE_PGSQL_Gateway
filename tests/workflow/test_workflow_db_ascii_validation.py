import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_workflow_db_ascii_validation(database_service):
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
    #
    # Execute procedure before validation
    #
    await database_service.procedure.execute(
        "public",
        "calculate_ascii_metadata",
    )

    rows = await database_service.sql.execute(
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