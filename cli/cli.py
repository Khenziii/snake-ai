from typing import TypedDict, List, Any
from colorama import Fore, Style
from threading import Thread
from copy import deepcopy
from cli.command import Command, Context
from config.config import Config
from game.game import GameConfig, Game
from game.square import SquareColor
from ai.wrapper import WrapperConfig, Wrapper


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
        self.game: Game | Wrapper | None = None

        self.context: Context
        self.__set_context()

        if self.display_init_message:
            print(f"{Fore.BLUE}TIP: Type `help` to list available commands!{Style.RESET_ALL}")

        self.__handle_input()

    def __start_game(self, human_or_ai: str):
        if self.game is not None:
            print("An instance of game is already running!")
            print("Use the `stop` command to stop it.")
            return

        if human_or_ai not in ["human", "ai"]:
            print("ERROR: passed invalid string to Cli.__start_game()")
            return

        human: bool = human_or_ai == "human"
        if human:
            config: GameConfig = self.config_manager.get_game_config(
                game_auto_handle_loop=True,
                game_finish_print=False,
                game_auto_run=False
            )
            self.game = Game(config)
        else:
            config: WrapperConfig = self.config_manager.get_wrapper_config(
                auto_run=False,
                finish_print=False
            )
            self.game = Wrapper(config)

        game_thread = Thread(target=self.game.run)
        game_thread.start()

    def __stop_game(self):
        if self.game is None:
            print("No games are currently running!")
            print("Use the `start` command to start one.")
            return

        self.game.running = False
        self.game = None

    def __exit(self):
        if self.game is not None:
            self.__stop_game()

        self.running = False

    def __set_game_speed(self, speed: int):
        if self.game is not None:
            self.game.game_speed = speed

        config = self.config_manager.config
        config["game"]["speed"] = speed
        self.config_manager.change_config(config)

    def __set_game_color(self, target: str, color: SquareColor):
        if target not in ["snake", "apple", "background"]:
            print("ERROR: passed invalid string to Cli.__set_game_color()")
            return

        config = self.config_manager.config
        match target:
            case "snake":
                config["game"]["snake_color"] = color
            case "apple":
                config["game"]["apple_color"] = color
            case "background":
                config["game"]["background_color"] = color
        self.config_manager.change_config(config)

        if self.game is None:
            return
        match target:
            case "snake":
                self.game.game_snake_color = color
            case "apple":
                self.game.game_apple_color = color
            case "background":
                self.game.game_background_color = color
        self.game.rerender_board()

    def __pause_game(self):
        if self.game is None:
            print("No games are currently running!")
            print("Use the `start` command to start one.")
            return

        if self.game.paused:
            print("The game is already paused!")
            return

        self.game.paused = True

    def __unpause_game(self):
        if self.game is None:
            print("No games are currently running!")
            print("Use the `start` command to start one.")
            return

        if not self.game.paused:
            print("The game is not paused!")
            return

        self.game.paused = False

    def __set_apple_count(self, count: int):
        config = self.config_manager.config
        config["game"]["apple_start_count"] = count
        self.config_manager.change_config(config)

        if self.game is None:
            print("Success!")
        else:
            print("Success! Restart the game, to apply changes.")

    def __set_grid_size(self, size: int):
        config = self.config_manager.config
        config["game"]["grid_size"] = size
        self.config_manager.change_config(config)

        if self.game is None:
            print("Success!")
        else:
            print("Success! Restart the game, to apply changes.")

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
            "set_game_speed_function": self.__set_game_speed,
            "set_game_color_function": self.__set_game_color,
            "pause_game_function": self.__pause_game,
            "unpause_game_function": self.__unpause_game,
            "set_game_apple_count_function": self.__set_apple_count,
            "set_game_grid_size_function": self.__set_grid_size,
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
                # We need to create a copy of command, to
                # not override default args permanently
                command_copy = deepcopy(command)
                if len(entered_command.split()) > 1:
                    command_copy.args = entered_command.split()[1:]

                context = None
                if command_copy.context_required:
                    context = self.context

                command_copy(context)
