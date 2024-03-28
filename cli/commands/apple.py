from cli.command import CommandConfig, Command, Context


class AppleCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        if len(self.args) < 1:
            print("This command requires exactly one argument (a valid int).")
            return
        args_zero = self.args[0]

        try:
            args_zero_int = int(args_zero)
        except ValueError:
            print("First argument has to be a valid int.")
            return

        set_game_apple_count_func = context["set_game_apple_count_function"]
        set_game_apple_count_func(args_zero_int)
