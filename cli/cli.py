from typing import TypedDict, List, Any
from colorama import Fore, Style
from cli.command import Command, CommandConfig, Context


class CliConfig(TypedDict):
    display_init_message: bool
    commands: List[Command]


class Cli:
    def __init__(self, config: CliConfig):
        self.display_init_message = config["display_init_message"]
        self.commands = config["commands"]
        self.running = True

        self.context: Context
        self.__set_context()

        if self.display_init_message:
            print(f"{Fore.BLUE}TIP: Type `help` to list available commands!{Style.RESET_ALL}")

        self.__handle_input()

    def __set_context(self):
        formatted_commands: List[dict[str, Any]] = []
        for command in self.commands:
            formatted_commands.append({
                "name": command.name,
                "description": command.description,
                "args": command.args_description,
            })

        self.context: Context = {
            "other_commands": formatted_commands
        }

    def __get_command_by_name(self, command_name: str) -> Command | None:
        for command in self.commands:
            if command.name == command_name:
                return command

        return None

    def __handle_input(self):
        while self.running:
            command_name = input("> ")
            command = self.__get_command_by_name(command_name)

            if command is None:
                print(f"{command_name}: command not found!")
            else:
                context = None
                if command.context_required:
                    context = self.context

                command(context)
