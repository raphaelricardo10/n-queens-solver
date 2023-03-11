from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field

from queen import Queen


@dataclass
class Chessboard:
    size: int
    available_rows: set[int] = field(init=False)
    available_columns: set[int] = field(init=False)
    _queens: set[Queen] = field(init=False, default_factory=set)

    def __post_init__(self):
        self.available_rows = set(range(0, self.size))
        self.available_columns = set(range(0, self.size))

    @property
    def queens(self):
        return self._queens

    @property
    def middle(self) -> int:
        return self.static_middle(self.size)

    @staticmethod
    def static_middle(size: int) -> int:
        if size % 2 == 0:
            return int(size / 2)

        return int((size + 1) / 2)

    @staticmethod
    def is_in_diagonal(queen1: Queen, queen2: Queen) -> bool:
        rise = abs(queen1.row - queen2.row)
        run = abs(queen1.column - queen2.column)

        return rise == run

    def is_in_diagonal_with_any_queen(self, new_queen: Queen) -> bool:
        for queen in self.queens:
            if self.is_in_diagonal(queen, new_queen):
                return True

        return False

    def can_add_queen(self, new_queen: Queen) -> bool:
        if self.is_in_diagonal_with_any_queen(new_queen):
            return False

        return True
    
    def add_queen(self, new_queen: Queen):
        self.queens.add(new_queen)
        self.available_rows.remove(new_queen.row)
        self.available_columns.remove(new_queen.column)

    def remove_queen(self, queen: Queen):
        self.queens.remove(queen)
        self.available_rows.add(queen.row)
        self.available_columns.add(queen.column)

    def rotate(self) -> Chessboard:
        rotated_queens: set[Queen] = set()

        for queen in self.queens:
            rotated_queen = Queen(row=self.size - queen.column - 1, column=queen.row)
            rotated_queens.add(rotated_queen)

        resulting_chessboard = deepcopy(self)
        resulting_chessboard._queens = rotated_queens

        return resulting_chessboard

    def reflect_horizontal(self) -> Chessboard:
        rotated_queens: set[Queen] = set()

        for queen in self.queens:
            rotated_queen = Queen(row=self.size - queen.row - 1, column=queen.column)
            rotated_queens.add(rotated_queen)

        resulting_chessboard = deepcopy(self)
        resulting_chessboard._queens = rotated_queens

        return resulting_chessboard