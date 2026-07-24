import pytest

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_grpc_request_stream_continues_after_error(
    grpc_stub,
):

    bad_request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT *
            FROM table_that_does_not_exist
            """,
        )
    )

    good_request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT 1 AS id
            """,
        )
    )

    async def request_stream():

        yield bad_request

        yield good_request

    responses = []

    async for response in grpc_stub.Execute(
        request_stream()
    ):

        responses.append(
            response
        )

    assert len(responses) == 2

    assert responses[0].success is False

    assert responses[1].success is True


import io

import pytest
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_request_stream_continues_after_error(
    grpc_stub,
):

    bad_request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT *
            FROM table_that_does_not_exist
            """,
        )
    )

    good_request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT 1 AS id
            """,
        )
    )

    async def request_stream():

        yield bad_request

        yield good_request

    responses = []

    async for response in grpc_stub.Execute(
        request_stream()
    ):

        responses.append(
            response
        )

    assert len(responses) == 2

    assert (
        responses[0].success
        is False
    )

    assert (
        responses[1].success
        is True
    )

    table = (
        ipc.open_stream(
            io.BytesIO(
                responses[1].payload
            )
        ).read_all()
    )

    data = table.to_pydict()

    assert data["id"] == [1]