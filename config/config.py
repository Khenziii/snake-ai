from typing import TypedDict
import json
from utils.hex_rgb_convert import hex_string_to_rgb_tuple, rgb_tuple_to_hex_string
from game.game import GameConfig
from ai.ai_game import AIGame
from ai.model import NetConfig, Net
from ai.agent import AgentConfig
from ai.trainer import TrainerConfig


class ConfigConfig(TypedDict):
    config_file_path: str


class Config:
    def __init__(self, config: ConfigConfig):
        self.config_file_path = config["config_file_path"]
        self.config = None

        self.load_config()

    def load_config(self):
        with open(self.config_file_path, 'r') as file:
            self.config = json.load(file)

        self.config["game"]["snake_color"] = hex_string_to_rgb_tuple(self.config["game"]["snake_color"])
        self.config["game"]["apple_color"] = hex_string_to_rgb_tuple(self.config["game"]["apple_color"])
        self.config["game"]["background_color"] = hex_string_to_rgb_tuple(self.config["game"]["background_color"])

    def change_config(self, new_config: dict):
        self.config = new_config

        new_config["game"]["snake_color"] = rgb_tuple_to_hex_string(new_config["game"]["snake_color"])
        new_config["game"]["apple_color"] = rgb_tuple_to_hex_string(new_config["game"]["apple_color"])
        new_config["game"]["background_color"] = rgb_tuple_to_hex_string(new_config["game"]["background_color"])

        json_string = json.dumps(new_config, ident=4)
        with open(self.config_file_path, 'w') as file:
            file.write(json_string)

    def get_game_config(self, game_auto_handle_loop: bool, game_finish_print: bool) -> GameConfig:
        return {
            "window_size_px": self.config["window"]["size_px"],
            "window_title": self.config["window"]["title"],
            "game_speed": self.config["game"]["speed"],
            "game_grid_size": self.config["game"]["grid_size"],
            "game_snake_start_length": self.config["game"]["snake_start_length"],
            "game_apple_start_count": self.config["game"]["apple_start_count"],
            "game_snake_color": self.config["game"]["snake_color"],
            "game_apple_color": self.config["game"]["apple_color"],
            "game_background_color": self.config["game"]["background_color"],
            "game_finish_print": game_finish_print,
            "game_auto_handle_loop": game_auto_handle_loop,
        }

    def get_net_config(self) -> NetConfig:
        return {
            "input_nodes": self.config["game"]["grid_size"] ** 2 * 4,
            "hidden_nodes": 256,
            "output_nodes": 4,
        }

    def get_agent_config(self, model: Net, env: AIGame) -> AgentConfig:
        return {
            "model": model,
            "env": env,
        }

    def get_trainer_config(self, model: Net) -> TrainerConfig:
        return {
            "memory_size": self.config["trainer"]["memory_size"],
            "batch_size": self.config["trainer"]["batch_size"],
            "gamma": self.config["trainer"]["gamma"],
            "epsilon_start": self.config["trainer"]["epsilon_start"],
            "epsilon_end": self.config["trainer"]["epsilon_end"],
            "epsilon_decay": self.config["trainer"]["epsilon_decay"],
            "model": model,
        }
