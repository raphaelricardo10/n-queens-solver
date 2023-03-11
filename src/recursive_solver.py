from copy import deepcopy
from dataclasses import dataclass, field
from typing import Generic, TypeAlias, TypeVar

from queen import Queen
from chessboard import Chessboard

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    data: T
    depth: int = 0
    is_leaf: bool = False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False

        return self.data == other.data  # type: ignore

    def __hash__(self) -> int:
        return self.data.__hash__()

    def is_root(self) -> bool:
        return self.depth == 0


Solutions: TypeAlias = set[frozenset[Queen]]


@dataclass
class RecursiveSolver:
    size: int
    solutions: Solutions = field(init=False, default_factory=set)

    @staticmethod
    def create_branch_with_queen(
        parent_node: Node[Chessboard], new_queen: Queen
    ) -> Node[Chessboard]:
        child_node = deepcopy(parent_node)
        child_node.depth += 1
        child_node.data.add_queen(new_queen)
        child_node.is_leaf = len(child_node.data.available_rows) == 0

        return child_node

    @staticmethod
    def make_rotations(chessboard: Chessboard) -> list[Chessboard]:
        last_rotation = chessboard
        solutions: list[Chessboard] = []

        for _ in range(0, 3):
            last_rotation = last_rotation.rotate()
            solutions.append(last_rotation)

        return solutions

    def update_solutions(self, chessboard: Chessboard):
        rotated_chessboards = self.make_rotations(chessboard)
        reflected_solutions = [x.reflect_horizontal() for x in rotated_chessboards]

        for symmetry_chessboard in rotated_chessboards + reflected_solutions:
            self.solutions.add(frozenset(symmetry_chessboard.queens))

        self.solutions.add(frozenset(chessboard.queens))

    def branch_and_search(self, node: Node[Chessboard]):
        if node.is_leaf:
            self.update_solutions(node.data)
            return

        for row in node.data.available_rows:
            for column in node.data.available_columns:
                queen = Queen(row, column)

                if node.data.can_add_queen(queen):
                    new_node = self.create_branch_with_queen(node, queen)
                    self.branch_and_search(new_node)

    def search_n_queens(self) -> Solutions:
        starting_row = 0
        starting_columns = range(0, Chessboard.static_middle(self.size))

        for column in starting_columns:
            queen = Queen(starting_row, column)
            chessboard = Chessboard(self.size)
            chessboard.add_queen(queen)

            node = Node(data=chessboard, is_leaf=False)
            self.branch_and_search(node)

        return self.solutions
