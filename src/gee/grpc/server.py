import asyncio
import sys

import grpc

from gee.grpc.generated import (
    execution_engine_pb2_grpc,
)

from gee.config.config_loader import (
    ConfigLoader,
)

from gee.grpc.service import (
    ExecutionEngineService,
)

from gee.postgres.pool import (
    PostgresPool,
)

from gee.postgres.database_service import (
    DatabaseService,
)

from gee.execution.execution_engine import (
    ExecutionEngine,
)


async def serve():

    if len(sys.argv) != 2:

        raise ValueError(
            "Usage: "
            "python -m gee.grpc.server "
            "<profile_name>"
        )

    profile_name = sys.argv[1]

    settings = ConfigLoader.load(
        profile_name
    )

    postgres_pool = PostgresPool(
        settings
    )

    await postgres_pool.connect()

    database_service = DatabaseService(
        postgres_pool,
        settings
    )

    execution_engine = ExecutionEngine(
        database_service
    )

    grpc_server = grpc.aio.server()

    (
        execution_engine_pb2_grpc
        .add_ExecutionEngineServicer_to_server(
            ExecutionEngineService(
                execution_engine
            ),
            grpc_server,
        )
    )

    grpc_server.add_insecure_port(
        f"{settings.grpc.host}:"
        f"{settings.grpc.port}"
    )

    await grpc_server.start()

    print()
    print("GEE Server Started")
    print("-" * 50)
    print(
        f"Profile : "
        f"{settings.profile_name}"
    )
    print(
        f"Postgres: "
        f"{settings.postgres.host}:"
        f"{settings.postgres.port}"
    )
    print(
        f"Database: "
        f"{settings.postgres.database}"
    )
    print(
        f"gRPC    : "
        f"{settings.grpc.host}:"
        f"{settings.grpc.port}"
    )
    print("-" * 50)
    print()

    await grpc_server.wait_for_termination()


if __name__ == "__main__":

    asyncio.run(
        serve()
    )