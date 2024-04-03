from cli.command import CommandConfig, Command, Context


class LoadCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        load_model_func = context["load_model_function"]
        args_zero = self.args[0]

        load_model_func(args_zero)
