from enum import Enum

ACCEPTED_FILES_EXTENSIONS = ['txt', 'turing']


class Statements(Enum):
    COMMENT = '#'
    OPTION = '--'
    OPTION_ASSIGN = '='
    NEXT_INSTRUCTION = '=>'
    RIGHT_SHIFT = 'right'
    LEFT_SHIFT = 'left'
    WRITE = 'write'
    GOTO = 'goto'

    @classmethod
    def has_value(cls, value: str):
        return value.lower() in cls._value2member_map_
