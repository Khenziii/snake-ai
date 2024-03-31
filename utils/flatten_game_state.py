from typing import TypedDict
from torch import tensor, float32


class gameState(TypedDict):
    danger_up: int
    danger_down: int
    danger_left: int
    danger_right: int


def flatten_game_state(game_state: gameState):
    game_state_array = []
    game_state_array.extend(game_state.values())

    tensor_flatten = tensor(game_state_array, dtype=float32)
    return tensor_flatten
