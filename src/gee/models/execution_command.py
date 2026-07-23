from pydantic import BaseModel
from pydantic import Field

from gee.models.command_type import CommandType


class Command(BaseModel):

    type: CommandType

    command: str

    parameters: list = Field(
        default_factory=list
    )