import grpc
import pytest
import pytest_asyncio

from gee.config.config_loader import ConfigLoader

from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService

from gee.grpc.generated import (
    execution_engine_pb2_grpc,
)


@pytest.fixture
def profile_name():
    return "ope"


@pytest.fixture
def settings(profile_name):
    return ConfigLoader.load(profile_name)


@pytest_asyncio.fixture
async def postgres_pool(settings):

    pool = PostgresPool(settings)

    await pool.connect()

    yield pool

    await pool.close()


@pytest_asyncio.fixture
async def database_service(postgres_pool, settings):

    yield DatabaseService(
        postgres_pool,
        settings,
    )


@pytest_asyncio.fixture
async def grpc_stub(settings):

    endpoint = (
        f"{settings.grpc.host}:"
        f"{settings.grpc.port}"
    )

    async with grpc.aio.insecure_channel(
        endpoint
    ) as channel:

        yield (
            execution_engine_pb2_grpc.ExecutionEngineStub(
                channel
            )
        )