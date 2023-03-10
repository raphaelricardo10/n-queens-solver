import multiprocessing
from dataclasses import dataclass

from queen import Queen


@dataclass
class Chessboard:
    size: int

    @property
    def middle(self) -> int:
        if self.size % 2 == 0:
            return int(self.size / 2)

        return int((self.size + 1) / 2)

    @staticmethod
    def combine_solutions():
        pass

    def search_for_n_queens(self) -> set[frozenset[Queen]]:
        all_solutions = set[frozenset[Queen]]()
        all_rows_and_columns = set(range(0, self.size))
        processes: list[multiprocessing.Process] = []
        starting_queens: list[Queen] = []

        for column in range(0, self.size):
            queen = Queen(
                0,
                column,
                available_rows=all_rows_and_columns - {0},
                available_columns=all_rows_and_columns - {column},
            )
            # queen.search()
            # all_solutions.update(queen.solutions)

            starting_queens.append(queen)
            p = multiprocessing.Process(target=queen.search)
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        for queen in starting_queens:
            all_solutions.update(queen.solutions)

        return all_solutions

