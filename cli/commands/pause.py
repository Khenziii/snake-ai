from cli.command import CommandConfig, Command, Context


class PauseCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        pause_game_func = context["pause_game_function"]
        pause_game_func()
