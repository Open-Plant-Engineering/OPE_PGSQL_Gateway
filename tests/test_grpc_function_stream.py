import io

import grpc
import pytest
import pyarrow.ipc as ipc

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)


@pytest.mark.asyncio
async def test_grpc_function_stream():

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
        CREATE OR REPLACE FUNCTION public.generate_numbers(
            max_value integer
        )
        RETURNS TABLE(id integer)
        AS $$
        BEGIN
            RETURN QUERY
            SELECT *
            FROM generate_series(1, max_value);
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    async with grpc.aio.insecure_channel(
        "localhost:50051"
    ) as channel:

        stub = (
            execution_engine_pb2_grpc.ExecutionEngineStub(
                channel
            )
        )

        request = execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.FUNCTION,
            command="execute_function",
        )

        request.parameters.extend([
            execution_engine_pb2.Parameter(
                name="schema",
                string_value="public",
            ),
            execution_engine_pb2.Parameter(
                name="function",
                string_value="generate_numbers",
            ),
            execution_engine_pb2.Parameter(
                name="max_value",
                int_value=10000,
            ),
        ])

        response_stream = stub.Execute(request)

        batch_count = 0
        total_rows = 0

        async for response in response_stream:

            assert response.success is True

            batch_count += 1

            table = (
                ipc.open_stream(
                    io.BytesIO(response.payload)
                ).read_all()
            )

            total_rows += table.num_rows

        assert batch_count == 10
        assert total_rows == 10000