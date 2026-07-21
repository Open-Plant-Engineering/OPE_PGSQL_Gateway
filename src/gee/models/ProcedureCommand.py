from pydantic import BaseModel


class ProcedureCommand(BaseModel):
    schema: str
    procedure_name: str
    parameters: list = []