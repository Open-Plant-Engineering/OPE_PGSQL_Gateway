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
async def test_workflow_grpc_function_execute():
    """
    Workflow:
        Client
          ↓
        gRPC
          ↓
        ExecutionEngine
          ↓
        Function Execution
          ↓
        PostgreSQL Function
          ↓
        Apache Arrow
          ↓
        Client

    Scenario:
        Execute a scalar PostgreSQL function through gRPC.

    Validation:
        - Function executes successfully
        - Result is serialized using Apache Arrow
        - Result is returned through gRPC
        - Returned value matches expected output

    Notes:
        - This is a Function Execute workflow.
        - Although the gRPC API uses a streaming response,
          only a single row is returned.
        - Only one Arrow batch is produced.
        - This is NOT a function streaming workload.

    Related Streaming Test:
        test_grpc_function_stream()

    Difference:

        Function Execute:
            add_numbers(10, 20)
                ↓
            1 row
                ↓
            1 Arrow batch
                ↓
            1 gRPC response

        Function Stream:
            generate_numbers(10000)
                ↓
            10000 rows
                ↓
            Multiple Arrow batches
                ↓
            Multiple gRPC responses

    Workflow Type:
        Function Execute

    Streaming:
        gRPC Streaming API      ✅
        Arrow Serialization     ✅
        True Data Streaming     ❌

    Result:
        Single Function Call
        Single Row
        Single Arrow Batch
        Single gRPC Response

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
                string_value="add_numbers",
            ),
            execution_engine_pb2.Parameter(
                name="a",
                int_value=10,
            ),
            execution_engine_pb2.Parameter(
                name="b",
                int_value=20,
            ),
        ])

        rows_received = 0

        async for response in stub.Execute(request):

            assert response.success is True

            table = (
                ipc.open_stream(
                    io.BytesIO(response.payload)
                ).read_all()
            )

            data = table.to_pydict()

            assert data["add_numbers"] == [30]

            rows_received += table.num_rows

        assert rows_received == 1