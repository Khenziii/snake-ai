import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "true"

from config.config import ConfigConfig, Config
from cli.cli import CliConfig, Cli
from cli.command_list import command_list


def main():
    configConfig: ConfigConfig = {
        "config_file_path": "config.json",
    }
    configManager = Config(configConfig)

    cliConfig: CliConfig = {
        "display_init_message": True,
        "commands": command_list,
        "config_manager": configManager,
    }
    Cli(config=cliConfig)

if __name__ == "__main__":
    main()
