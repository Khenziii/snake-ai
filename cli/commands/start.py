from cli.command import CommandConfig, Command, Context


class StartCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        start_game_func = context["start_game_function"]
        args_zero = self.args[0]

        if args_zero not in ["human", "ai"]:
            print("First argument of `start` command must be set to either `human` or `ai`")
            return

        start_game_func(args_zero)
