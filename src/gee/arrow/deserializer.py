import io

import pyarrow.ipc as ipc


class ArrowDeserializer:

    @staticmethod
    def deserialize(payload: bytes):
        source = io.BytesIO(payload)

        reader = ipc.open_stream(source)

        return reader.read_all()