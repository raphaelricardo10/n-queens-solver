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
        entrypoints = range(0, self.middle)
        all_solutions = set[frozenset[Queen]]()
        all_rows_and_columns = set(range(0, self.size))
        processes = []
        starting_queens = []

        for row in entrypoints:
            for column in entrypoints:
                queen = Queen(
                    row,
                    column,
                    available_rows=all_rows_and_columns - {row},
                    available_columns=all_rows_and_columns - {column},
                )
                starting_queens.append(queen)

                p = multiprocessing.Process(target=queen.search)
                p.start()
                processes.append(p)

        for p in processes:
            p.join()

        for queen in starting_queens:
            all_solutions.update(queen.solutions)

        return all_solutions

                
