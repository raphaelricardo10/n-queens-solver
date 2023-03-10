from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Queen:
    row: int
    column: int
    previous: Optional[Queen] = None
    available_rows: Optional[set[int]] = None
    available_columns: Optional[set[int]] = None
    solutions: set[frozenset[Queen]] = field(init=False)

    @property
    def _key(self):
        return (self.row, self.column)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Queen):
            return False

        return self._key == other._key

    def __hash__(self) -> int:
        return hash(self._key)

    def __post_init__(self):
        self.solutions = set()

        if self.previous:
            assert self.previous.available_rows
            assert self.previous.available_columns

            self.available_rows = self.previous.available_rows - {self.row}
            self.available_columns = self.previous.available_columns - {self.column}

    def is_diagonal_with(self, other_queen: Queen) -> bool:
        rise = abs(self.row - other_queen.row)
        run = abs(self.column - other_queen.column)

        return rise == run

    def is_diagonal_with_any_queen(self, new_queen: Queen) -> bool:
        if self.is_diagonal_with(new_queen):
            return True

        if self.previous is None:
            return False

        return self.previous.is_diagonal_with_any_queen(new_queen)

    def can_add_queen(self, new_queen: Queen) -> bool:
        if self.is_diagonal_with_any_queen(new_queen):
            return False

        return True

    def is_leaf(self) -> bool:
        if self.available_rows is None:
            return False

        return len(self.available_rows) == 0

    def is_root(self) -> bool:
        return self.previous is None

    def generate_solutions(self, _partial_solution: list[Queen] = []):
        _partial_solution.append(self)

        if self.is_root():
            self.solutions.add(frozenset(_partial_solution))
            return

        self.previous.generate_solutions(_partial_solution)

    def search(self):
        assert self.available_rows is not None
        assert self.available_columns is not None

        if self.is_leaf():
            self.generate_solutions([])
            return

        for row in self.available_rows:
            for column in self.available_columns:
                new_queen = Queen(
                    row,
                    column,
                    self,
                )

                if not self.can_add_queen(new_queen):
                    continue

                new_queen.search()