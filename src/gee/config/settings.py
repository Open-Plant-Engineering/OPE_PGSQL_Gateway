from pydantic import BaseModel

from gee.config.postgres_settings import (
    PostgresSettings,
)

from gee.config.grpc_settings import (
    GrpcSettings,
)


class Settings(BaseModel):

    profile_name: str

    postgres: PostgresSettings

    grpc: GrpcSettings
