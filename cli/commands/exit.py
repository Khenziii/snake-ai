from cli.command import CommandConfig, Command, Context


class ExitCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        exit_func = context["exit_function"]
        exit_func()
