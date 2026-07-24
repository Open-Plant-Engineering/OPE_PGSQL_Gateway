from pydantic import BaseModel
from pydantic import Field


class ExecutionSettings(
    BaseModel,
):

    timeout_seconds: int = Field(
        default=300,
        gt=0,
    )