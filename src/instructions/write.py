from src.instructions.base import BaseInstruction


class WriteInstruction(BaseInstruction):
    def __init__(self, to_write):
        super().__init__("Write")
        self.__to_write = to_write

    def __str__(self):
        return f"Write({self.__to_write})"

    def compute(self, machine) -> None:
        machine.set_bride_piece(self.__to_write)

    @staticmethod
    def compile() -> str:
        raise NotImplementedError