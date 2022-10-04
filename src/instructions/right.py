from src.instructions.base import BaseInstruction


class RightInstruction(BaseInstruction):
    def __init__(self):
        super().__init__("Right")

    def compute(self, machine) -> None:
        machine.increase_ptr_bride()
        if machine.is_ptr_at_end():
            machine.insert_back_bride()

    @staticmethod
    def compile() -> str:
        raise NotImplementedError