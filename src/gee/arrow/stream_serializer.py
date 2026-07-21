import io

import pyarrow as pa
import pyarrow.ipc as ipc


class ArrowStreamSerializer:

    @staticmethod
    def serialize_batch(rows):

        if not rows:
            return b""

        columns = {}

        for column_name in rows[0].keys():
            columns[column_name] = [
                row[column_name]
                for row in rows
            ]

        table = pa.table(columns)

        sink = io.BytesIO()

        with ipc.new_stream(
            sink,
            table.schema
        ) as writer:
            writer.write_table(table)

        return sink.getvalue()