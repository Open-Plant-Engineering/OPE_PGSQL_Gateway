from pydantic import BaseModel


class FunctionCommand(BaseModel):
    schema: str
    function_name: str
    parameters: list = []