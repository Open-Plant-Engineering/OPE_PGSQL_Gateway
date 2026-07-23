from pydantic import BaseModel


class GrpcSettings(BaseModel):

    host: str = "0.0.0.0"
    port: int
