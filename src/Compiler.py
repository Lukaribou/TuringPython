from typing import Dict

from src.State import State
from src.instructions.base import BaseInstruction
from src.instructions.goto import GotoInstruction
from src.instructions.write import WriteInstruction


def base_code() -> str:
    return """
    module main

    struct Machine {
    mut:
        ptr_bride u64
        bride	  []string
    }
    
    fn init_machine() Machine {
        return Machine{0, []}
    }
    
    fn instruction_left(mut m &Machine) {
        if m.ptr_bride == 0 {
            m.bride.prepend('b')
            m.ptr_bride = 1
        }
        m.ptr_bride -= 1
    }
    
    fn instruction_right(mut m &Machine) {
        m.ptr_bride += 1
        m.bride << 'b'
    }
    
    fn instruction_write(mut m &Machine, to_write string) {
        m.bride[m.ptr_bride] = to_write
    }
    
    """


def get_instruction_written(instr: BaseInstruction) -> str:
    as_string = 'return ' if isinstance(instr, GotoInstruction) else ''

    as_string += f'{instr.get_compile_instruction_name()}(mut m'

    if isinstance(instr, (WriteInstruction, GotoInstruction)):
        as_string += f', "{instr.get_right_part()}"'

    as_string += ')'

    return as_string


def state_make_function(state: State) -> str:
    s = "fn state_" + state.get_name() + "(mut m &Machine) {\n"

    if_count = 0
    for cond_value, instrs in state.get_instructions().items():
        cond_string = ""

        # "else if"
        if if_count > 0:
            cond_string += 'else '

        cond_string += 'if m.bride[m.ptr_bride] == "' + cond_value + '" {\n'
        cond_string += '\n'.join(map(get_instruction_written, instrs))
        cond_string += '\n}'

        s += cond_string + "\n"
        if_count += 1

    return s + "}"


class Compiler:
    def __init__(self, instructions: Dict[str, State], file_name='turing.exe'):
        self.__states = instructions

    def make(self, delete_v_file=True) -> bool:
        total_str = ""
        for state in self.__states.values():
            total_str += state_make_function(state) + "\n"

        if delete_v_file:
            self.delete_v()

        return True

    # delete v file
    def delete_v(self) -> bool:
        pass


if __name__ == '__main__':
    print(state_make_function(State('test', ['0 => WRITE 1 => LEFT', '1 => LEFT => LEFT', '2 => LEFT => GOTO eq1'])))
