from src.instructions.base import BaseInstruction


class GotoInstruction(BaseInstruction):
    def __init__(self):
        super().__init__("Goto")
