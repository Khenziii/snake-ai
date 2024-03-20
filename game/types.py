from typing import TypedDict
from enum import Enum
from game.square import Square


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Position(TypedDict):
    x: int
    y: int
    square: Square


class SquaresType(Position):
    snake: bool
    apple: bool
