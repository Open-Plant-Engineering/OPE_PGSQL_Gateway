import uuid


class TempTableLoader:

    @staticmethod
    def create_table_name():
        return (
            "tmp_" +
            uuid.uuid4().hex
        )