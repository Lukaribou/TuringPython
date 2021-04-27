from __future__ import annotations

from typing import Dict, List, Any

from TuringOptions import TuringOptions
import re


class Turing:
    def __init__(self, program: str, bride='', debug=False, auto_parse=True):
        self.bride: List[str] = list(bride.replace(' ', 'b'))  # ruban des valeurs
        self.ptr_bride = 0  # 0 = MSB
        self.file_content = program
        self.debug = debug
        self.options = TuringOptions(debug)
        self.states: Dict[str, Dict[str, List[str]]] = {}
        self.record: List[Dict[str, Any]] = []

        if auto_parse:
            self.parse()

    def parse(self, parse_options=True) -> None:
        if parse_options:
            self.options.parse(self.file_content)

        # modif en fonction des options
        if self.options.get("START") == "RIGHT":
            self.ptr_bride = len(self.bride) - 1  # => MSB

        # parse les instructions

        lines = re.compile("\n+(\w+)+:").split(self.file_content)  # https://regex101.com/r/urESAl/1
        lines = [s.strip() for s in '\n'.join(lines).splitlines()]  #
        lines = list(filter(lambda s: not s.startswith('#') and s != '', lines))  # enlève les options et les vides

        fn = {"name": None, "val_used": [], "qF": False}
        for instruction in lines:
            instruction = instruction.lower()

            if '=>' in instruction:
                if fn['name'] is None:
                    raise ValueError("L'instruction `%s` n'appartient à aucun état." % instruction)

                elif not instruction.startswith(('0', '1', 'b')):  # ne commence pas par un des trois
                    raise ValueError('Les valeurs autres que `0`, `1` et `b` ne sont pas acceptées. (Vérifier '
                                     'instruction `%s` dans l\'état `%s`)' % (instruction, fn['name']))

                elif instruction[0] in fn['val_used']:  # instructions val = x déjà définies
                    raise ValueError('L\'instruction en cas de valeur égale à `%s` dans `%s` existe déjà.'
                                     % (instruction[0], fn["name"]))

                # pas de problème
                self.states[fn['name']][instruction[0]] = [s.strip() for s in instruction.split('=>')[1:]]
                fn['val_used'].append(instruction[0])  # instructions pour valeur x définies

                if 'goto qf' in instruction:
                    fn['qF'] = True  # l'état final semble être atteignable
            else:
                fn['name'] = instruction  # change l'état en définition
                fn['val_used'] = []  # réinitialise les valeurs implémantées
                self.states[instruction] = {}  # ajoute l'état dans la liste

        if not fn['qF']:
            raise ValueError("L'état `qF` (état final) n'est jamais atteint.")

    def run(self, record_mvt=False) -> str:
        current_state = self.states[list(self.states.keys())[0]]  # premier état défini
        qF_reached = False
        count = 0

        def log(op: str):
            print('Opération: %s\t| Ruban: `%s`\t| Pointeur ruban: %d'
                  % (op, self.p_bride(), self.ptr_bride))

        while not qF_reached:
            for instr in current_state[self.bride[self.ptr_bride]]:  # valeur pointée par le curseur
                if instr == 'right':
                    self.ptr_bride += 1
                    if self.ptr_bride == len(self.bride):
                        self.bride.append('b')
                elif instr == 'left':
                    self.ptr_bride -= 1
                    if self.ptr_bride == -1:
                        self.bride.insert(0, 'b')
                        self.ptr_bride = 0
                elif instr.startswith('write'):
                    to_write = instr.split(' ')[1]
                    if to_write not in ['0', '1', 'b']:
                        raise ValueError('Valeur à écrire incorrect: `%s`' % to_write)

                    self.bride[self.ptr_bride] = to_write
                elif instr.startswith('goto'):
                    to_go = instr.split(' ')[1]
                    if to_go == 'qf':
                        qF_reached = True
                        break  # au cas où il y ait des instructions derrière le GOTO qF
                    elif to_go in self.states.keys():
                        current_state = self.states[to_go]
                    else:
                        raise KeyError("L'état `%s` n'existe pas." % to_go)
                else:
                    raise ValueError("L'instruction `%s` n'est pas valide." % instr)

                if self.debug:
                    log(instr)

                if record_mvt:
                    count += 1

                    self.record.append({
                        "count": count,
                        "instr": instr,
                        "bride": self.bride,
                        "ptr": self.ptr_bride,
                        "state": current_state
                    })

        return self.p_bride()

    def p_bride(self):
        return ''.join(self.bride).replace('b', ' ').strip()

    @staticmethod
    def from_file(file_path: str, bride='', debug=False, auto_parse=True) -> Turing:
        f = open(file_path, 'r')
        content = f.read()
        f.close()
        return Turing(content, bride, debug, auto_parse)
