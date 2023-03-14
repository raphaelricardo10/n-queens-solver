from copy import copy
from typing import TypeAlias
from dataclasses import dataclass

from queen import Queen
from chessboard import Chessboard
from knight_mover import KnightMover
from knight_movements import KnightMovements

Solutions: TypeAlias = set[frozenset[Queen]]


@dataclass
class GreedySolver:
    size: int

    @staticmethod
    def can_add_queen(queen: Queen, chessboard: Chessboard) -> bool:
        if not chessboard.is_under_limits(queen):
            return False

        if not chessboard.can_add_queen(queen):
            return False

        return True

    def run_greedy(self, starting_queen: Queen) -> set[Queen]:
        chessboard = Chessboard(self.size)
        knight_mover = KnightMover(starting_queen)
        max_tries = len(KnightMovements)
        current_try = 0

        chessboard.add_queen(copy(starting_queen))

        while chessboard.available_rows and chessboard.available_columns:
            if len(chessboard.available_rows) == 1:
                try:
                    row = next(iter(chessboard.available_rows))
                    column = next(iter(chessboard.available_columns))
                    chessboard.can_add_queen(Queen(row, column))

                except KeyError:
                    break

            knight_mover.move()

            if self.can_add_queen(knight_mover.queen, chessboard):
                try:
                    chessboard.add_queen(copy(knight_mover.queen))
                    current_try = 0
                    continue

                except KeyError:
                    pass

            knight_mover.rollback()

            if current_try > max_tries:
                if knight_mover.queen.row > self.size:
                    break

                knight_mover.queen.row += 1
                current_try = 0
                continue

            knight_mover.rotate()
            current_try += 1

        return chessboard.queens

    def search_n_queens(self) -> Solutions:
        all_solutions = Solutions()

        for column in range(0, self.size):
            solution = self.run_greedy(Queen(0, column))

            if len(solution) == self.size:
                all_solutions.add(frozenset(solution))

        return all_solutions
