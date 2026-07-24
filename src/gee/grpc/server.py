import asyncio
import logging
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


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(name)s "
        "%(message)s"
    ),
)

logger = logging.getLogger(__name__)


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
        settings,
    )

    execution_engine = ExecutionEngine(
        database_service
    )

    grpc_server = grpc.aio.server()

    (
        execution_engine_pb2_grpc
        .add_ExecutionEngineServicer_to_server(
            ExecutionEngineService(
                execution_engine,
                settings,
            ),
            grpc_server,
        )
    )

    grpc_server.add_insecure_port(
        f"{settings.grpc.host}:"
        f"{settings.grpc.port}"
    )

    await grpc_server.start()

    logger.info(
        "GEE Server Started"
    )

    logger.info(
        "Profile=%s",
        settings.profile_name,
    )

    logger.info(
        "Postgres=%s:%s",
        settings.postgres.host,
        settings.postgres.port,
    )

    logger.info(
        "Database=%s",
        settings.postgres.database,
    )

    logger.info(
        "BatchSize=%s",
        settings.streaming.batch_size,
    )

    logger.info(
        "gRPC=%s:%s",
        settings.grpc.host,
        settings.grpc.port,
    )

    try:

        await grpc_server.wait_for_termination()

    finally:

        logger.info(
            "Closing PostgreSQL pool"
        )

        await postgres_pool.close()


if __name__ == "__main__":

    asyncio.run(
        serve()
    )