from typing import List
from game.types import SquaresType
from torch import tensor, float32


def flatten_game_state(game_state: List[SquaresType]):
    flatten = []
    for square in game_state:
        flatten.extend([
            square["x"],
            square["y"],
            int(square["apple"]),
            int(square["snake"])
        ])

    tensor_flatten = tensor(flatten, dtype=float32)
    return tensor_flatten
