from pydantic import BaseModel
from pydantic import Field

class StreamingSettings(BaseModel):

    batch_size: int = Field(default=1000, gt=0)