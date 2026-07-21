from pydantic import BaseModel


class Settings(BaseModel):
    grpc_host: str = "0.0.0.0"
    grpc_port: int = 50051

    pg_host: str = "localhost"
    pg_port: int = 5433
    pg_database: str = "ope"
    pg_user: str = "postgres"
    pg_password: str = "postgres"