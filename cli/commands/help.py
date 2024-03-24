from cli.command import CommandConfig, Command, Context


class HelpCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if context is None:
            print("ERROR: Context is required for help command!")
            return

        print(context)
