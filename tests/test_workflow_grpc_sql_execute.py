import io

import grpc
import pytest
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)


@pytest.mark.asyncio
async def test_workflow_grpc_sql_execute():
    """
    Workflow:
        Client
          ↓
        gRPC
          ↓
        ExecutionEngine
          ↓
        SQL Execution
          ↓
        Apache Arrow
          ↓
        Client

    Scenario:
        Execute a simple SQL statement through gRPC.

    Validation:
        - SQL executes successfully
        - Arrow payload is returned
        - Returned data matches expected values

    Workflow Type:
        SQL Execute

    Streaming:
        gRPC Streaming API      ✅
        Actual Data Streaming   ❌

    Result:
        Single SQL Result
        Single Arrow Batch
        Single gRPC Response

    """

    async with grpc.aio.insecure_channel(
        "localhost:50051"
    ) as channel:

        stub = (
            execution_engine_pb2_grpc.ExecutionEngineStub(
                channel
            )
        )

        request = (
            execution_engine_pb2.CommandRequest(
                type=execution_engine_pb2.SQL,
                command="""
                SELECT
                    10 AS id,
                    'Hello GEE' AS name
                """,
            )
        )

        response_stream = stub.Execute(request)

        rows_received = 0

        async for response in response_stream:

            assert response.success is True

            table = (
                ipc.open_stream(
                    io.BytesIO(response.payload)
                ).read_all()
            )

            data = table.to_pydict()

            assert data["id"] == [10]
            assert data["name"] == ["Hello GEE"]

            rows_received += table.num_rows

        assert rows_received == 1