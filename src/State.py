from __future__ import annotations

from typing import List, Dict

from src.instructions.instructions import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Turing import Turing


def strip_list(my_list: List[str]) -> List[str]:
    return list(map(lambda l: l.strip(), my_list))


class State:
    def __init__(self, name: str, instructions: List[str]):
        self.__name = name
        self.__instructions: Dict[str, List[BaseInstruction]] = {}

        for line in instructions:
            instr: List[str] = strip_list(line.split('=>'))
            if len(instr) >= 2:
                self.__instructions[instr[0]] = list(map(make_instruction, instr[1:]))

    def __contains__(self, item):
        return item in self.__instructions.keys()

    def __str__(self):
        return f"State({self.__name})"

    def execute(self, machine: Turing) -> bool:
        if machine.get_bride_at_ptr() not in self:
            raise ValueError(f"No instructions for bride's value `{machine.get_bride_at_ptr()}` in state `{self.__name}`")
        else:
            for instruction in self.__instructions[machine.get_bride_at_ptr()]:
                instruction.compute(machine)
                if isinstance(instruction, GotoInstruction):
                    return True
        return False
