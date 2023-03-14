from copy import copy
from itertools import cycle
from dataclasses import dataclass, field
from typing import Generator, Iterator

from queen import Queen
from knight_movements import KnightMovements, KnightMovementsMember


@dataclass
class KnightMover:
    queen: Queen
    last_movement: Queen = field(init=False)
    current_direction: KnightMovementsMember = field(init=False)
    movement_directions: Iterator[KnightMovementsMember] = field(init=False)

    def __post_init__(self):
        movement_directions = [
            KnightMovements.right_up.value,
            KnightMovements.up_right.value,
            KnightMovements.up_left.value,
            KnightMovements.left_up.value,
            KnightMovements.left_down.value,
            KnightMovements.down_left.value,
            KnightMovements.down_right.value,
            KnightMovements.right_down.value,
        ]

        self.current_direction = movement_directions[0]
        self.movement_directions = cycle(movement_directions)

    def move(self):
        self.last_movement = copy(self.queen)
        self.current_direction(self.queen)

    def rollback(self):
        self.queen = self.last_movement

    def rotate(self):
        self.current_direction = next(self.movement_directions)
