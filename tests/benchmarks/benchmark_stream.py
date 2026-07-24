import asyncio
import io
import time

import grpc
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)


async def request_stream():

    yield (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT *
            FROM generate_series(
                1,
                100000
            ) AS id
            """,
        )
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

        rows = 0
        batches = 0

        start = time.perf_counter()

        async for response in stub.Execute(
            request_stream()
        ):

            table = (
                ipc.open_stream(
                    io.BytesIO(
                        response.payload
                    )
                ).read_all()
            )

            rows += table.num_rows

            batches += 1

        elapsed = (
            time.perf_counter()
            - start
        )

        print(
            f"Rows      : {rows}"
        )

        print(
            f"Batches   : {batches}"
        )

        print(
            f"Elapsed   : {elapsed:.2f}"
        )

        print(
            f"Rows/Sec  : "
            f"{rows / elapsed:.2f}"
        )


if __name__ == "__main__":

    asyncio.run(
        main()
    )