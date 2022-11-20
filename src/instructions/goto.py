from src.instructions.base import BaseInstruction


class GotoInstruction(BaseInstruction):
    def __init__(self, next_state: str):
        super().__init__("Goto")
        self.__next_state = next_state

    def __str__(self):
        return f"Goto({self.__next_state})"

    def get_next_state_name(self) -> str:
        return self.__next_state

    def compute(self, machine) -> None:
        if machine.exists_state(self.__next_state):
            machine.set_state(self.__next_state)
        else:
            raise KeyError("State `%s` does not exists." % self.__next_state)

    def get_compile_instruction_name(self) -> str:
        return 'instruction_goto'
