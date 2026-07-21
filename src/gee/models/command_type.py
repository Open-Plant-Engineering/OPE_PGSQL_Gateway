from enum import Enum


class CommandType(str, Enum):
    SQL = "SQL"
    FUNCTION = "FUNCTION"
    PROCEDURE = "PROCEDURE"