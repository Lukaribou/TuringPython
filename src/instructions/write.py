from src.instructions.base import BaseInstruction


class WriteInstruction(BaseInstruction):
    def __init__(self):
        super().__init__("Write")
