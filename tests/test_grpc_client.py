import asyncio
import grpc
import pyarrow.ipc as ipc
import io

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)


async def main():

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
                request_id="1",
                type=execution_engine_pb2.SQL,
                command="select * from generate_series(1,5) as id",
            )
        )

        response_stream = stub.Execute(request)

        async for response in response_stream:

            print("Success:", response.success)
            print("Message:", response.message)

            source = io.BytesIO(response.payload)

            table = (
                ipc.open_stream(source)
                .read_all()
            )

            print(table)
            print(table.to_pydict())


if __name__ == "__main__":
    asyncio.run(main())