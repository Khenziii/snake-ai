from cli.command import CommandConfig, Command, Context


class UnpauseCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        unpause_game_func = context["unpause_game_function"]
        unpause_game_func()
