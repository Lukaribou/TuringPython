from src.instructions.base import BaseInstruction


class LeftInstruction(BaseInstruction):
    def __init__(self):
        super().__init__("Left")

    def compute(self, machine) -> None:
        machine.decrease_ptr_bride()
        if machine.get_ptr_bride() == -1:
            machine.insert_front_bride()
            machine.set_ptr_bride(0)

    def get_compile_instruction_name(self) -> str:
        return 'instruction_left'
