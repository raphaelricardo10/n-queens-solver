from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Queen:
    row: int
    column: int
    available_rows: set[int]
    available_columns: set[int]
    root: Optional[Queen] = None
    previous: Optional[Queen] = field(init=False)
    partial_solution: list[Queen] = field(default_factory=list)
    solutions: set[frozenset[Queen]] = field(init=False, default_factory=set)

    @property
    def _key(self):
        return (self.row, self.column)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Queen):
            return False

        return self._key == other._key

    def __hash__(self) -> int:
        return hash(self._key)

    def is_diagonal_with(self, other_queen: Queen) -> bool:
        rise = abs(self.row - other_queen.row)
        run = abs(self.column - other_queen.column)

        return rise == run

    def is_diagonal_with_any_queen(self, new_queen: Queen) -> bool:
        for queen in self.partial_solution:
            if queen.is_diagonal_with(new_queen):
                return True
            
        return False

    def is_too_deep_in_tree(self) -> bool:
        assert self.root is not None
        return len(self.partial_solution) > (len(self.root.available_rows) + 1)/2
    
    def exists_a_similar_solution(self) -> bool:
        assert self.root

        if self.is_too_deep_in_tree():
            for solution in self.root.solutions:
                if frozenset(self.partial_solution).issubset(solution):
                    return True

        return False

    def can_add_queen(self, new_queen: Queen) -> bool:
        if self.is_diagonal_with(new_queen):
            return False

        if self.is_diagonal_with_any_queen(new_queen):
            return False

        if new_queen.is_too_deep_in_tree():
            if new_queen.exists_a_similar_solution():
                return False

        return True

    def is_leaf(self) -> bool:
        return len(self.available_rows) == 0

    def is_root(self) -> bool:
        return self.root is None

    def search(self):
        self.partial_solution.append(self)

        if self.is_leaf():
            assert self.root is not None
            self.root.solutions.add(frozenset(self.partial_solution))
            return

        for row in self.available_rows:
            for column in self.available_columns:
                new_queen = Queen(
                    row,
                    column,
                    available_rows=self.available_rows - {row},
                    available_columns=self.available_columns - {column},
                    root=self if self.is_root() else self.root,
                    partial_solution=self.partial_solution.copy()
                )

                if not self.can_add_queen(new_queen):
                    continue

                new_queen.search()