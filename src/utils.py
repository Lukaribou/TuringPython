from enum import Enum


class Statements(Enum):
    COMMENT = '#'
    NEXT_INSTRUCTION = '=>'
    RIGHT_SHIFT = 'right'
    LEFT_SHIFT = 'left'
    WRITE = 'write'
    GOTO = 'goto'

    @classmethod
    def has_value(cls, value: str):
        return value.upper() in cls._value2member_map_
