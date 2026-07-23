import pytest

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_grpc_sql_error(
    grpc_stub,
):

    request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT *
            FROM table_that_does_not_exist
            """,
        )
    )

    async def request_stream():

        yield request

    responses = []

    async for response in grpc_stub.Execute(
        request_stream()
    ):

        responses.append(
            response
        )

    assert len(responses) == 1

    assert responses[0].success is False

    assert responses[0].message != ""