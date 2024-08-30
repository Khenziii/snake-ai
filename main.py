import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "true"

from config.config import ConfigConfig, Config
from cli.cli import CliConfig, Cli
from cli.command_list import command_list


def main():
    # Use global config ("~/.config/snake-ai/config.json"), if not running
    # in dev env. On Windows, always use local config ("config.json").
    running_in_dev_env = os.getenv("SNAKE_AI_ENV") == "dev"
    running_on_unix = os.name == "posix"
    config_path = (
        "config.json"
        if running_in_dev_env or not running_on_unix
        else os.path.expanduser("~/.config/snake-ai/config.json")
    )

    configConfig: ConfigConfig = {
        "config_file_path": config_path,
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
