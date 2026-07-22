import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService

from gee.execution.execution_engine import ExecutionEngine

from gee.models.command import Command
from gee.models.command_type import CommandType


@pytest.mark.asyncio
async def test_execution_engine_sql():

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

    engine = ExecutionEngine(db)

    command = Command(
        type=CommandType.SQL,
        command="select * from generate_series(1,5) as id",
        parameters=[],
    )

    rows = await engine.execute(command)

    assert len(rows) == 5

    assert rows[0]["id"] == 1
    assert rows[1]["id"] == 2
    assert rows[2]["id"] == 3
    assert rows[3]["id"] == 4
    assert rows[4]["id"] == 5