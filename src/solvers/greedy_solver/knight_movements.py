from enum import Enum, member
from typing import Callable

from domain import Queen

KnightMovementsMember = Callable[[Queen], None]


class KnightMovements(Enum):
    @member
    def up_right(queen: Queen):  # type: ignore
        queen.row += 2
        queen.column += 1

    @member
    def up_left(queen: Queen):  # type: ignore
        queen.row += 2
        queen.column -= 1

    @member
    def left_up(queen: Queen):  # type: ignore
        queen.row += 1
        queen.column -= 2

    @member
    def left_down(queen: Queen):  # type: ignore
        queen.row -= 1
        queen.column -= 2

    @member
    def down_left(queen: Queen):  # type: ignore
        queen.row -= 2
        queen.column -= 1

    @member
    def down_right(queen: Queen):  # type: ignore
        queen.row -= 2
        queen.column += 1

    @member
    def right_down(queen: Queen):  # type: ignore
        queen.row -= 1
        queen.column += 2

    @member
    def right_up(queen: Queen):  # type: ignore
        queen.row += 1
        queen.column += 2
