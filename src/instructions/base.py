class BaseInstruction:
    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return f"Instr.{self.__name}"

    def __repr__(self):
        return self.__str__()

    def compute(self, machine) -> None:
        raise NotImplementedError

    def get_compile_instruction_name(self) -> str:
        raise NotImplementedError
