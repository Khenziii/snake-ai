from typing import TypedDict
from random import randint
from numpy.random import random
from torch import argmax
from utils.flatten_game_state import flatten_game_state
from ai.ai_game import AIGame
from ai.model import Net
from game.types import SquaresType


class AgentConfig(TypedDict):
    env: AIGame
    model: Net
    epsilon_start: float
    epsilon_end: float
    epsilon_decay: float


class Agent:
    def __init__(self, config: AgentConfig):
        self.env = config["env"]
        self.model = config["model"]

        self.epsilon_start = config["epsilon_start"]
        self.epsilon_end = config["epsilon_end"]
        self.epsilon_decay = config["epsilon_decay"]
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

    # if axis == "x", returns 0 for right part of screen, 1 for left & 2 for both sides.
    # if axis == "y", returns 0 for bottom part of screen, 1 for top & 2 for both sides.
    def __check_where_apple(self, axis: str):
        if axis not in ["x", "y"]:
            raise ValueError("Invalid direction passed to agent.__check_where_apple()!")

        apple_present_left_or_top = False
        apple_present_right_or_bottom = False
        apple_present_on_both_sides = False

        for apple in self.env.apple_tiles:
            if apple[axis] < self.env.snake_tiles[-1][axis]:
                apple_present_left_or_top = True
            elif apple[axis] > self.env.snake_tiles[-1][axis]:
                apple_present_right_or_bottom = True

        if apple_present_left_or_top and apple_present_right_or_bottom:
            apple_present_on_both_sides = True

        if apple_present_on_both_sides:
            return 2
        if apple_present_left_or_top:
            return 1

        return 0

    def __amount_of_tiles_to_danger_or_apple(self, direction: str, square_type: str, change_by: int):
        if direction not in ["x", "y"]:
            raise ValueError("Invalid direction passed to agent.__amount_of_tiles_to_danger_or_apple()!")

        if square_type not in ["danger", "apple"]:
            raise ValueError("Invalid square_type passed to agent.__amount_of_tiles_to_danger_or_apple()!")

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
                if distance < 1:
                    distance = -distance

                # no apple's here
                if square_type == "apple":
                    distance = -1

                break

            if square["apple"]:
                break

        return distance

    def get_state(self):
        current_tiles, _, _ = self.env.get_state()

        self.all_tiles = current_tiles[0]
        self.snake_tiles = current_tiles[1]
        self.snake_head = self.snake_tiles[-1]

        current_state = {
            "danger_up": self.__amount_of_tiles_to_danger_or_apple(square_type="danger", direction="y", change_by=-1),
            "danger_down": self.__amount_of_tiles_to_danger_or_apple(square_type="danger", direction="y", change_by=1),
            "danger_left": self.__amount_of_tiles_to_danger_or_apple(square_type="danger", direction="x", change_by=-1),
            "danger_right": self.__amount_of_tiles_to_danger_or_apple(square_type="danger", direction="x", change_by=1),
            "apple_up": self.__amount_of_tiles_to_danger_or_apple(square_type="apple", direction="y", change_by=-1),
            "apple_down": self.__amount_of_tiles_to_danger_or_apple(square_type="apple", direction="y", change_by=1),
            "apple_left": self.__amount_of_tiles_to_danger_or_apple(square_type="apple", direction="x", change_by=-1),
            "apple_right": self.__amount_of_tiles_to_danger_or_apple(square_type="apple", direction="x", change_by=1),
            "apple_location_x": self.__check_where_apple(axis="x"),
            "apple_location_y": self.__check_where_apple(axis="y"),
        }
        current_state_tensor = flatten_game_state(current_state)
        return current_state_tensor

    def get_action(self, state) -> int:
        moves = self.model(state)

        # exploring vs. exploiting
        self.epsilon = self.epsilon_start * self.epsilon_decay ** (self.env.current_try / self.epsilon_decay)
        if random() < self.epsilon:
            # random move
            random_index = randint(0, len(moves) - 1)
            moves[random_index] = 1

        return argmax(moves).item()
