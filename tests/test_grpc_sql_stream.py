import io

import grpc
import pytest
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_grpc_sql_stream(grpc_stub):

    request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="select * from generate_series(1,10000) as id",
        )
    )

    async def request_stream():
        yield request

    batch_count = 0
    total_rows = 0

    async for response in grpc_stub.Execute(request_stream()):
    
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