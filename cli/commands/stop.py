from cli.command import CommandConfig, Command, Context


class StopCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        stop_game_func = context["stop_game_function"]
        stop_game_func()
