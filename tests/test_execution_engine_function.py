import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService

from gee.execution.execution_engine import ExecutionEngine

from gee.models.command import Command
from gee.models.command_type import CommandType


@pytest.mark.asyncio
async def test_execution_engine_function():

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

    await db.sql.execute(
        """
        CREATE OR REPLACE FUNCTION public.add_numbers(
            a integer,
            b integer
        )
        RETURNS integer
        AS $$
        BEGIN
            RETURN a + b;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    engine = ExecutionEngine(db)

    command = Command(
        type=CommandType.FUNCTION,
        command="execute_function",
        parameters=[
            "public",
            "add_numbers",
            10,
            20,
        ],
    )

    rows = await engine.execute(command)

    assert len(rows) == 1

    result = rows[0]["add_numbers"]

    assert result == 30