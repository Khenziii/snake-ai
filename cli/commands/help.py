from typing import List
from cli.command import CommandConfig, Command, Context


def show_info_about_command(command: CommandConfig, index: int | None = None):
    if index is None:
        print(command['name'])
    else:
        print(f"{index}. {command['name']}")

    print(command['description'])

    if command['args'] is not None:
        print(f"args: {command['args']}")


class HelpCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        available_commands: List[CommandConfig] = context["other_commands"]

        args_zero = self.args[0]
        if args_zero is not None:
            for command in available_commands:
                if command['name'] == args_zero:
                    show_info_about_command(command)
                    return

            print(f"Couldn't find command: {args_zero}! See `help` for a list of all commands.")
            return

        for index, command in enumerate(available_commands, start=1):
            show_info_about_command(command, index)

            # don't end line, if last iteration
            if index == len(available_commands):
                continue

            print()
