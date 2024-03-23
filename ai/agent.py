from typing import TypedDict
from utils.flatten_game_state import flatten_game_state
from ai.ai_game import AIGame
from ai.model import Net
from random import randint
from torch import argmax


class AgentConfig(TypedDict):
    env: AIGame
    model: Net


class Agent:
    def __init__(self, config: AgentConfig):
        self.env = config["env"]
        self.model = config["model"]
        self.epsilon = None

    def get_state(self):
        current_tiles, reward, is_game_over = self.env.get_state()
        current_state_tensor = flatten_game_state(current_tiles)

        return current_state_tensor, is_game_over

    def get_action(self) -> int:
        state, _ = self.get_state()
        moves = self.model(state)

        # exploring vs. exploiting
        # TODO: work on this condition:
        if randint(0, 30) > self.env.current_generation:
            # random move
            random_index = randint(0, len(moves) - 1)
            moves[random_index] = 1

        return argmax(moves).item()
