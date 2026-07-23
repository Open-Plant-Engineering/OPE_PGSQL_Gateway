from pydantic import BaseModel


class PostgresSettings(BaseModel):

    host: str
    port: int
    database: str
    user: str
    password: str

    min_pool_size: int = 5
    max_pool_size: int = 20