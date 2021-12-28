from __future__ import annotations

from typing import List, Dict

from src.utils import Statements


class Options:
    def __init__(self, debug=False):
        self.parsed = False
        self.debug = debug
        self.opts: Dict[str, str] = {}

    def parse(self, file_content: str):
        for index, line in enumerate(file_content.splitlines()):
            line = line.strip()  # retire tous les espaces devant et derrière
            if line.startswith(Statements.COMMENT.value) and not line.startswith('##'):
                if ('=' not in line) and self.debug:  # si pas d'assignation dans la ligne
                    raise ValueError("La valeur de l'option ligne `%d` est introuvable." % (index + 1))
                line = line.replace('#', '')  # retire les #
                params: List[str] = list(map(lambda s: s.strip(), line.split('=')))  # prend les valeurs et les trim
                self.set(params[0], params[1])
        self.parsed = True

    def set(self, name: str, value: str) -> Options:
        self.opts[name] = value
        if self.debug:
            print('Paramètre `%s` chargé avec pour valeur `%s`.' % (name, value))
        return self

    def get(self, name: str) -> str:
        return self.opts.get(name)

    def has(self, name: str) -> bool:
        return self.get(name) is not None
