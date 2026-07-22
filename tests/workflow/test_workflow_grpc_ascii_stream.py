import io

import grpc
import pytest
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)


@pytest.mark.asyncio
async def test_workflow_grpc_ascii_stream():
    """
    Stream all 50,000 rows through gRPC.
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
                SELECT *
                FROM workflow_ascii
                ORDER BY id
                """
            )
        )

        batch_count = 0
        total_rows = 0

        async for response in stub.Execute(request):

            assert response.success is True

            table = (
                ipc.open_stream(
                    io.BytesIO(response.payload)
                ).read_all()
            )

            batch_count += 1
            total_rows += table.num_rows

        assert total_rows == 50000
        assert batch_count == 50