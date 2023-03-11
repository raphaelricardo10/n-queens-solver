from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Queen:
    row: int
    column: int

    @property
    def _key(self):
        return (self.row, self.column)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Queen):
            return False

        return self._key == other._key

    def __hash__(self) -> int:
        return hash(self._key)
