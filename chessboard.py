from dataclasses import dataclass

from queen import NoGoodCandidatesException, Queen


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
        solutions = set[frozenset[Queen]]()
        all_rows_and_columns = set(range(0, self.size))

        for row in entrypoints:
            for column in entrypoints:
                queen = Queen(
                    row,
                    column,
                    available_rows=all_rows_and_columns - {row},
                    available_columns=all_rows_and_columns - {column},
                )

                try:
                    queen.search()
                    solutions.update(queen.get_solution())

                except NoGoodCandidatesException:
                    pass

        return solutions

                
