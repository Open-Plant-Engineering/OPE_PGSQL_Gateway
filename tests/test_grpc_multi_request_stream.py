import io

import pytest
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_grpc_multi_request_stream(
    grpc_stub,
):

    request_1 = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT 1 AS id
            """,
        )
    )

    request_2 = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT 2 AS id
            """,
        )
    )

    request_3 = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT 3 AS id
            """,
        )
    )

    async def request_stream():

        yield request_1

        yield request_2

        yield request_3

    results = []

    async for response in grpc_stub.Execute(
        request_stream()
    ):

        assert response.success is True

        table = (
            ipc.open_stream(
                io.BytesIO(
                    response.payload
                )
            ).read_all()
        )

        results.append(
            table.to_pydict()["id"][0]
        )

    assert results == [
        1,
        2,
        3,
    ]