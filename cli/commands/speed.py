from cli.command import CommandConfig, Command, Context


class SpeedCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        set_game_speed_func = context["set_game_speed_function"]
        args_zero = self.args[0]

        try:
            args_zero_int = int(args_zero)
        except ValueError:
            print("First argument must be a valid int! See `help speed` for more examples.")
            return

        set_game_speed_func(args_zero_int)
