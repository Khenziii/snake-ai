from typing import TypedDict
import json


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

    def change_config(self, new_config: dict):
        self.config = new_config

        json_string = json.dumps(new_config, ident=4)
        with open(self.config_file_path, 'w') as file:
            file.write(json_string)
