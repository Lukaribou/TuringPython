import src.State
from src.instructions.base import BaseInstruction
from src.instructions.left import LeftInstruction
from src.instructions.right import RightInstruction
from src.instructions.write import WriteInstruction
from src.instructions.goto import GotoInstruction


def make_instruction(string_instruction: str) -> BaseInstruction:
    orders = src.State.strip_list(string_instruction.lower().split(' '))

    if orders[0] == 'left':
        instr = LeftInstruction()
    elif orders[0] == 'right':
        instr = RightInstruction()
    else:
        if len(orders) != 2:
            raise ValueError('Missing value for WRITE or GOTO')
        else:
            if orders[0] == 'write':
                instr = WriteInstruction(orders[1])
            elif orders[0] == 'goto':
                instr = GotoInstruction(orders[1])
            else:
                raise ValueError('Unknown instruction `%s`' % orders[0])

    return instr
