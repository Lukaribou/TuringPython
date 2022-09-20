from __future__ import annotations

from typing import Dict, List

from src.Options import Options
import re

from src.Recorder import Recorder
from src.State import State
from src.utils import Statements, ACCEPTED_FILES_EXTENSIONS


class Turing:
    def __init__(self, program: str, bride='', debug=False, auto_parse=True):
        self.__bride: List[str] = list(bride.replace(' ', 'b'))  # ruban des valeurs
        self.__ptr_bride = 0  # 0 = MSB
        self.__file_content = program
        self.__debug = debug
        self.__options = Options(debug)
        self.__states: Dict[str, State] = {}
        self.__record = Recorder()
        self.__current_state_name = ''
        self.__current_state = None

        if auto_parse:
            self.parse()

    def get_options(self) -> Options:
        return self.__options

    def increase_ptr_bride(self) -> Turing:
        self.__ptr_bride += 1
        return self

    def decrease_ptr_bride(self) -> Turing:
        self.__ptr_bride -= 1
        return self

    def get_ptr_bride(self) -> int:
        return self.__ptr_bride

    def set_ptr_bride(self, pos: int) -> Turing:
        self.__ptr_bride = pos
        return self

    def insert_front_bride(self) -> Turing:
        self.__bride.insert(0, 'b')
        return self

    def insert_back_bride(self) -> Turing:
        self.__bride.append('b')
        return self

    def is_ptr_at_end(self) -> bool:
        return self.__ptr_bride == len(self.__bride)

    def get_bride_at_ptr(self) -> str:
        return self.__bride[self.__ptr_bride]

    def set_bride_piece(self, new_value) -> Turing:
        self.__bride[self.__ptr_bride] = new_value
        return self

    def exists_state(self, state: str) -> bool:
        return state in self.__states.keys()

    def set_state(self, new_state: str) -> Turing:
        self.__current_state = self.__states[new_state]
        self.__current_state_name = new_state
        return self

    def parse(self, parse_options=True) -> None:
        if parse_options:
            self.__options.parse(self.__file_content)

        # modif en fonction des options

        # START
        if self.__options.get("START") == "RIGHT":
            self.__ptr_bride = len(self.__bride) - 1  # => MSB

        # FINAL_STATE
        self.__options.set_dont_erase("FINAL_STATE", "qf")

        # parse les instructions

        lines = re.compile(r"(\w+ +{[\s\S]+})+").split(self.__file_content)  # https://regex101.com/r/urESAl/1
        lines = [s.strip() for s in '\n'.join(lines).splitlines()]  #
        lines = list(filter(lambda s:
                            not s.startswith(Statements.COMMENT.value)
                            and not s.startswith(Statements.OPTION.value)
                            and s != '',
                            lines))  # enlève les options et les vides

        current_state_name: str = ''
        current_state_instr: List[str] = []

        for line in lines:
            if '}' in line:
                self.__states[current_state_name] = State(current_state_name, current_state_instr)
                current_state_name = ''
            elif '{' in line:
                current_state_name = re.match(r"(\w+)", line).group(0)
            else:
                current_state_instr.append(line)

        self.run()

    def run(self, record_mvt=False) -> str:
        # option START_STATE
        self.__current_state_name = self.__options['START_STATE'] or list(self.__states.keys())[0]
        self.__current_state = self.__states.get(self.__options['START_STATE'])

        self.__current_state.execute(self)

        return self.print_bride()

    def print_bride(self):
        return ''.join(self.__bride).replace('b', ' ').strip()

    @staticmethod
    def from_file(file_path: str, bride='', debug=False, auto_parse=True) -> Turing:
        for extension in ACCEPTED_FILES_EXTENSIONS:
            if file_path.endswith(f'.{extension}'):
                break
        else:
            raise ValueError(f'Extension du fichier non valide. [{", ".join(ACCEPTED_FILES_EXTENSIONS)}] sont acceptees.')

        f = open(file_path, 'r')
        content = f.read()
        f.close()
        return Turing(content, bride, debug, auto_parse)
