import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService

from gee.execution.execution_engine import ExecutionEngine

from gee.models.execution_command import Command
from gee.models.command_type import CommandType


@pytest.mark.asyncio
async def test_execution_engine_function(database_service):

    await database_service.sql.execute(
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

    engine = ExecutionEngine(database_service)

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