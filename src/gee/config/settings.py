from pydantic import BaseModel

from gee.config.postgres_settings import (
    PostgresSettings,
)

from gee.config.grpc_settings import (
    GrpcSettings,
)

from gee.config.streaming_settings import (
    StreamingSettings,
)

from gee.config.execution_settings import (
    ExecutionSettings,
)

class Settings(BaseModel):

    profile_name: str

    postgres: PostgresSettings

    grpc: GrpcSettings

    streaming: StreamingSettings

    execution: ExecutionSettings
