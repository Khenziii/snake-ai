from cli.command import CommandConfig, Command, Context


class SaveCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        save_model_func = context["save_model_function"]
        args_zero = self.args[0]

        save_model_func(args_zero)
