from typing import List
from cli.command import CommandConfig, Command, Context


class HelpCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        available_commands: List[CommandConfig] = context["other_commands"]
        for index, command in enumerate(available_commands, start=1):
            print(f"{index}. {command['name']}")
            print(command['description'])

            if command['args'] is not None:
                print(f"args: {command['args']}")

            # don't end line, if last iteration
            if index == len(available_commands):
                return

            print()
