import json
import os
from typing import TypedDict
from copy import deepcopy
from utils.hex_rgb_convert import hex_string_to_rgb_tuple, rgb_tuple_to_hex_string
from game.game import GameConfig
from ai.ai_game import AIGame
from ai.model import NetConfig, Net
from ai.agent import AgentConfig, Agent
from ai.trainer import TrainerConfig, Trainer
from ai.wrapper import WrapperConfig
from plotter.plotter import PlotterConfig, Plotter


default_config = {
    "window": {
        "size_px": 1000,
        "title": "Snake Game"
    },
    "game": {
        "speed": 5,
        "grid_size": 10,
        "snake_start_length": 3,
        "apple_start_count": 5,
        "snake_head_color": "#cccccc",
        "snake_body_color": "#ffffff",
        "apple_color": "#ff0000",
        "background_color": "#000000"
    },
    "trainer": {
        "memory_size": 1000000,
        "batch_size": 500,
        "gamma": 0.99,
        "epsilon_start": 1.0,
        "epsilon_end": 0.01,
        "epsilon_decay": 0.995
    },
    "plot": {
        "title": "Score Graph",
        "x_axis_label": "Retries",
        "y_axis_label": "Scores"
    }
}

class ConfigConfig(TypedDict):
    config_file_path: str


class Config:
    def __init__(self, config: ConfigConfig):
        self.config_file_path = config["config_file_path"]
        self.config = None

        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file_path):
            os.makedirs(os.path.dirname(self.config_file_path))

            json_string = json.dumps(default_config, indent=4)
            with open(self.config_file_path, 'w') as file:
                file.write(json_string)

        with open(self.config_file_path, 'r') as file:
            self.config = json.load(file)

        self.config["game"]["snake_head_color"] = hex_string_to_rgb_tuple(self.config["game"]["snake_head_color"])
        self.config["game"]["snake_body_color"] = hex_string_to_rgb_tuple(self.config["game"]["snake_body_color"])
        self.config["game"]["apple_color"] = hex_string_to_rgb_tuple(self.config["game"]["apple_color"])
        self.config["game"]["background_color"] = hex_string_to_rgb_tuple(self.config["game"]["background_color"])

    def change_config(self, new_config: dict):
        self.config = deepcopy(new_config)

        new_config["game"]["snake_head_color"] = rgb_tuple_to_hex_string(new_config["game"]["snake_head_color"])
        new_config["game"]["snake_body_color"] = rgb_tuple_to_hex_string(new_config["game"]["snake_body_color"])
        new_config["game"]["apple_color"] = rgb_tuple_to_hex_string(new_config["game"]["apple_color"])
        new_config["game"]["background_color"] = rgb_tuple_to_hex_string(new_config["game"]["background_color"])

        json_string = json.dumps(new_config, indent=4)
        with open(self.config_file_path, 'w') as file:
            file.write(json_string)

    def get_plotter_config(self) -> PlotterConfig:
        return {
            "window_title": self.config["plot"]["title"],
            "x_axis_label": self.config["plot"]["x_axis_label"],
            "y_axis_label": self.config["plot"]["y_axis_label"],
        }

    def get_game_config(self, game_auto_handle_loop: bool, game_auto_run: bool) -> GameConfig:
        plotter_config = self.get_plotter_config()
        plotter = Plotter(plotter_config)

        return {
            "window_size_px": self.config["window"]["size_px"],
            "window_title": self.config["window"]["title"],
            "game_speed": self.config["game"]["speed"],
            "game_grid_size": self.config["game"]["grid_size"],
            "game_snake_start_length": self.config["game"]["snake_start_length"],
            "game_apple_start_count": self.config["game"]["apple_start_count"],
            "game_snake_head_color": self.config["game"]["snake_head_color"],
            "game_snake_body_color": self.config["game"]["snake_body_color"],
            "game_apple_color": self.config["game"]["apple_color"],
            "game_background_color": self.config["game"]["background_color"],
            "game_auto_handle_loop": game_auto_handle_loop,
            "game_auto_run": game_auto_run,
            "plotter": plotter,
        }

    def get_net_config(self) -> NetConfig:
        return {
            "input_nodes": 10,
            "hidden_nodes": 128,
            "output_nodes": 4,
        }

    def get_agent_config(self, model: Net, env: AIGame) -> AgentConfig:
        return {
            "model": model,
            "env": env,
            "epsilon_start": self.config["trainer"]["epsilon_start"],
            "epsilon_end": self.config["trainer"]["epsilon_end"],
            "epsilon_decay": self.config["trainer"]["epsilon_decay"],
        }

    def get_trainer_config(self, model: Net) -> TrainerConfig:
        return {
            "memory_size": self.config["trainer"]["memory_size"],
            "batch_size": self.config["trainer"]["batch_size"],
            "gamma": self.config["trainer"]["gamma"],
            "model": model,
        }

    def get_wrapper_config(self, auto_run: bool) -> WrapperConfig:
        game_config = self.get_game_config(
            game_auto_handle_loop=False,
            game_auto_run=True,
        )
        env = AIGame(game_config)
        net_config = self.get_net_config()
        model = Net(net_config)
        agent_config = self.get_agent_config(
            env=env,
            model=model
        )
        agent = Agent(agent_config)
        trainer_config = self.get_trainer_config(
            model=model
        )
        trainer = Trainer(trainer_config)

        return {
            "auto_run": auto_run,
            "env": env,
            "model": model,
            "agent": agent,
            "trainer": trainer,
        }
