from typing import TypedDict
from random import randint
from torch import argmax
from utils.flatten_game_state import flatten_game_state
from ai.ai_game import AIGame
from ai.model import Net
from game.types import SquaresType


class AgentConfig(TypedDict):
    env: AIGame
    model: Net


class Agent:
    def __init__(self, config: AgentConfig):
        self.env = config["env"]
        self.model = config["model"]
        self.epsilon = None

        self.all_tiles = []
        self.snake_tiles = []
        self.snake_head = None

    def __check_if_danger(self, square: SquaresType) -> bool:
        if square["snake"]:
            return True

        if square["x"] in [0, self.env.game_grid_size - 1]:
            return True

        if square["y"] in [0, self.env.game_grid_size - 1]:
            return True

        return False

    def __amount_of_tiles_to_danger(self, direction: str, change_by: int):
        if direction not in ["x", "y"]:
            raise ValueError("Invalid direction passed to agent.__amount_of_tiles_to_danger()!")

        distance = 0
        while True:
            distance += change_by

            if direction == "x":
                square = self.env.get_square_by_x_and_y(
                    min(
                        max(self.snake_head["x"] + distance, 0),
                        self.env.game_grid_size - 1
                    ),
                    self.snake_head["y"]
                )
            else:
                square = self.env.get_square_by_x_and_y(
                    self.snake_head["x"],
                    min(
                        max(self.snake_head["y"] + distance, 0),
                        self.env.game_grid_size - 1
                    ),
                )

            if self.__check_if_danger(square):
                break

        if distance < 1:
            distance = -distance

        return distance

    def get_state(self):
        current_tiles, _, _ = self.env.get_state()

        self.all_tiles = current_tiles[0]
        self.snake_tiles = current_tiles[1]
        self.snake_head = self.snake_tiles[-1]

        current_state = {
            "danger_up": self.__amount_of_tiles_to_danger("y", -1),
            "danger_down": self.__amount_of_tiles_to_danger("y", 1),
            "danger_left": self.__amount_of_tiles_to_danger("x", -1),
            "danger_right": self.__amount_of_tiles_to_danger("x", 1),
        }
        current_state_tensor = flatten_game_state(current_state)
        return current_state_tensor

    def get_action(self, state) -> int:
        moves = self.model(state)

        # exploring vs. exploiting
        # TODO: work on this condition:
        self.epsilon = 80 - self.env.current_try
        if randint(0, 200) < self.epsilon:
            # random move
            random_index = randint(0, len(moves) - 1)
            moves[random_index] = 1

        return argmax(moves).item()
