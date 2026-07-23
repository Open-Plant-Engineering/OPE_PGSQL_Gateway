from pydantic import BaseModel


class StreamingSettings(BaseModel):

    batch_size: int = 1000