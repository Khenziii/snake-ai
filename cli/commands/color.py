from cli.command import CommandConfig, Command, Context
from utils.hex_rgb_convert import rgb_string_to_rgb_tuple


class ColorCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        set_color_func = context["set_game_color_function"]

        if len(self.args) < 2:
            print("This command requires at least 2 arguments. Checkout `help color`.")
            return
        args_zero = self.args[0]
        args_one = self.args[1]

        if args_zero not in ["snake", "apple", "background"]:
            print("First argument must be either `snake`, `apple` or `background`. See `help color` for examples.")
            return

        try:
            args_one_tuple = rgb_string_to_rgb_tuple(args_one)
        except ValueError:
            print(
                "Second argument is invalid! Please make sure, to enter a valid RGB color. Use this syntax: `(R,G,B)`"
            )
            return

        set_color_func(args_zero, args_one_tuple)
