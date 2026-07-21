from pydantic import BaseModel

from gee.models.command_type import CommandType


class Command(BaseModel):
    type: CommandType

    command: str

    parameters: list = []