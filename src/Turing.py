from __future__ import annotations

from typing import Dict, List

from src.Options import Options
import re

from src.Recorder import Recorder
from src.utils import Statements


class Turing:
    def __init__(self, program: str, bride='', debug=False, auto_parse=True):
        self.bride: List[str] = list(bride.replace(' ', 'b'))  # ruban des valeurs
        self.ptr_bride = 0  # 0 = MSB
        self.file_content = program
        self.debug = debug
        self.options = Options(debug)
        self.states: Dict[str, Dict[str, List[str]]] = {}
        self.record = Recorder()

        if auto_parse:
            self.parse()

    def parse(self, parse_options=True) -> None:
        if parse_options:
            self.options.parse(self.file_content)

        # modif en fonction des options

        # START
        if self.options.get("START") == "RIGHT":
            self.ptr_bride = len(self.bride) - 1  # => MSB

        # FINAL_STATE
        self.options.set_dont_erase("FINAL_STATE", "qf")

        # parse les instructions

        lines = re.compile("\n+(\w+)+:").split(self.file_content)  # https://regex101.com/r/urESAl/1
        lines = [s.strip() for s in '\n'.join(lines).splitlines()]  #
        lines = list(filter(lambda s:
                            not s.startswith(Statements.COMMENT.value)
                            and not s.startswith(Statements.OPTION.value)
                            and s != '',
                            lines))  # enlève les options et les vides

        fn = {"name": None, "val_used": [], "qF": False}
        for instruction in lines:
            instruction = instruction.lower()

            if Statements.NEXT_INSTRUCTION.value in instruction:
                if fn['name'] is None:
                    raise ValueError("L'instruction `%s` n'appartient à aucun état." % instruction)
                elif instruction[0] in fn['val_used']:  # instructions val = x déjà définies
                    raise ValueError('L\'instruction en cas de valeur égale à `%s` dans `%s` existe déjà.'
                                     % (instruction[0], fn["name"]))

                # pas de problème
                self.states[fn['name']][instruction[0]] = [s.strip() for s in
                                                           instruction.split(Statements.NEXT_INSTRUCTION.value)[1:]]
                fn['val_used'].append(instruction[0])  # instructions pour valeur x définies

                if f'{Statements.GOTO.value} {self.options["FINAL_STATE"]}' in instruction:
                    fn['qF'] = True  # l'état final semble être atteignable
            else:
                fn['name'] = instruction  # change l'état en définition
                fn['val_used'] = []  # réinitialise les valeurs implémantées
                self.states[instruction] = {}  # ajoute l'état dans la liste

        if not fn['qF']:
            raise ValueError("L'état `qF` (état final) n'est jamais atteint.")

    def run(self, record_mvt=False) -> str:
        # option START_STATE
        name_current_state = self.options['START_STATE']
        if name_current_state is None:
            name_current_state = list(self.states.keys())[0]
        current_state = self.states.get(name_current_state)

        if current_state is None:
            raise ValueError("L'état de départ défini dans l'option START_STATE n'existe pas.")

        qF_reached = False

        def log(op: str):
            print('Opération: %s\t| Ruban: `%s`\t| Pointeur ruban: %d'
                  % (op, self.print_bride(), self.ptr_bride))

        while not qF_reached:
            for instr in current_state[self.bride[self.ptr_bride]]:  # valeur pointée par le curseur
                orders = instr.split(' ')

                try:
                    command = Statements(orders[0])
                except ValueError:
                    raise ValueError(f'La commande `{orders[0]}` n\'existe pas.')

                match command:
                    case Statements.RIGHT_SHIFT:
                        self.ptr_bride += 1
                        if self.ptr_bride == len(self.bride):
                            self.bride.append('b')
                    case Statements.LEFT_SHIFT:
                        self.ptr_bride -= 1
                        if self.ptr_bride == -1:
                            self.bride.insert(0, 'b')
                            self.ptr_bride = 0
                    case Statements.WRITE:
                        self.bride[self.ptr_bride] = orders[1]
                    case Statements.GOTO:
                        to_go = orders[1]
                        if to_go == self.options['FINAL_STATE']:
                            qF_reached = True
                            break  # au cas où il y ait des instructions derrière le GOTO qF
                        elif to_go in self.states.keys():
                            current_state = self.states[to_go]
                            name_current_state = to_go
                        else:
                            raise KeyError("L'état `%s` n'existe pas." % to_go)
                    case _:
                        raise ValueError('Commande `%s` mal placée.')

                if self.debug:
                    log(instr)

                if record_mvt:
                    self.record.put(command, self.bride, self.ptr_bride, name_current_state)

        return self.print_bride()

    def print_bride(self):
        return ''.join(self.bride).replace('b', ' ').strip()

    @staticmethod
    def from_file(file_path: str, bride='', debug=False, auto_parse=True) -> Turing:
        f = open(file_path, 'r')
        content = f.read()
        f.close()
        return Turing(content, bride, debug, auto_parse)
