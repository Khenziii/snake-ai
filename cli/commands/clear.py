from cli.command import CommandConfig, Command, Context
import os


class ClearCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
