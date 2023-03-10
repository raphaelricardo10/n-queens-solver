from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


class NoGoodCandidatesException(Exception):
    pass


@dataclass
class Queen:
    row: int
    column: int
    previous: Optional[Queen] = None
    available_rows: Optional[set[int]] = None
    available_columns: Optional[set[int]] = None
    good_candidates: set[Queen] = field(init=False)

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
        self.good_candidates = set()

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

    def have_no_good_candidates(self):
        return len(self.good_candidates) == 0

    def is_root(self) -> bool:
        if self.available_rows is None:
            return False

        return len(self.available_rows) == 0

    def search(self):
        assert self.available_rows is not None
        assert self.available_columns is not None

        if self.is_root():
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

                try:
                    new_queen.search()
                    self.good_candidates.add(new_queen)

                except NoGoodCandidatesException:
                    pass

        if self.have_no_good_candidates():
            raise NoGoodCandidatesException

    def get_solution(self, _last_insertions: list[Queen] = []) -> set[frozenset[Queen]]:
        _last_insertions.append(self)

        assert self.available_rows is not None
        if len(self.available_rows) == 0:
            return {frozenset(_last_insertions)}

        solution = set[frozenset[Queen]]()
        for candidate in self.good_candidates:
            partial_solution = candidate.get_solution(_last_insertions.copy())
            solution.update(partial_solution)

        return solution
