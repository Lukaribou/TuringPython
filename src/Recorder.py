from typing import List, Dict, Any

from src.utils import Statements


class Recorder:
    def __init__(self):
        self.__count: int = 0
        self.__records: List[Dict[str, Any]] = []

    def put(self, statement: Statements, bride: List[str], ptr_bride: int, current_state: str):
        self.__records.append({
            'count': self.__count,
            'stmt': statement,
            'bride': bride,
            'ptr_bride': ptr_bride,
            'current_state': current_state
        })
        self.__count += 1

    def __str__(self):
        return str(self.__records)
