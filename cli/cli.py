from typing import TypedDict, List, Any, Literal
from colorama import Fore, Style
from cli.command import Command, Context
from config.config import Config
from game.game import GameConfig, Game
from ai.ai_game import AIGame


class CliConfig(TypedDict):
    display_init_message: bool
    commands: List[Command]
    config_manager: Config


class Cli:
    def __init__(self, config: CliConfig):
        self.display_init_message = config["display_init_message"]
        self.commands = config["commands"]
        self.config_manager = config["config_manager"]
        self.running = True
        self.game = None

        self.context: Context
        self.__set_context()

        if self.display_init_message:
            print(f"{Fore.BLUE}TIP: Type `help` to list available commands!{Style.RESET_ALL}")

        self.__handle_input()

    def __start_game(self, human_or_ai: str):
        if self.game is not None:
            print("A instance of game is already running!")
            print("Use the `stop` command to stop it.")

        if human_or_ai not in ["human", "ai"]:
            print("ERROR: passed invalid string to Cli.__start_game()")
            return

        human: bool = human_or_ai == "human"
        if human:
            config: GameConfig = self.config_manager.get_game_config(
                game_auto_handle_loop=True,
                game_finish_print=True
            )
            self.game = Game(config)
        else:
            # config: GameConfig = self.config_manager.get_game_config(
            #     game_auto_handle_loop=False,
            #     game_finish_print=True
            # )
            # self.game = AIGame(config)
            print("This argument is going to get implemented later!")
            return

    def __stop_game(self):
        self.game.running = False
        self.game = None

    def __exit(self):
        self.running = False

    def __set_context(self):
        formatted_commands: List[dict[str, Any]] = []
        for command in self.commands:
            formatted_commands.append({
                "name": command.name,
                "description": command.description,
                "args": command.args_description,
            })

        self.context: Context = {
            "other_commands": formatted_commands,
            "exit_function": self.__exit,
            "start_game_function": self.__start_game,
            "stop_game_function": self.__stop_game,
        }

    def __get_command_by_name(self, command_name: str) -> Command | None:
        for command in self.commands:
            if command.name == command_name:
                return command

        return None

    def __handle_input(self):
        while self.running:
            entered_command = input("> ")
            if entered_command.strip() == "":
                continue

            command_name = entered_command.split()[0]
            command = self.__get_command_by_name(command_name)

            if command is None:
                print(f"{command_name}: command not found!")
            else:
                if len(entered_command.split()) > 1:
                    command.args = entered_command.split()[1:]

                context = None
                if command.context_required:
                    context = self.context

                command(context)
