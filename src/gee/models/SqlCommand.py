from pydantic import BaseModel


class SqlCommand(BaseModel):
    sql: str
    parameters: list = []