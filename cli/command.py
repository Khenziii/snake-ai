from typing import TypedDict, List, Any, Callable


class CommandConfig(TypedDict):
    name: str
    description: str
    args: List[Any]
    args_description: str | None
    context_required: bool


class Context(TypedDict):
    other_commands: List[CommandConfig]
    exit_function: Callable[[], None]
    start_game_function: Callable[[str], None]
    stop_game_function: Callable[[], None]
    set_game_speed_function: Callable[[int], None]
    set_game_color_function: Callable[[str, tuple[int, int, int]], None]
    set_game_apple_count_function: Callable[[int], None]
    set_game_grid_size_function: Callable[[int], None]
    pause_game_function: Callable[[], None]
    unpause_game_function: Callable[[], None]
    save_model_function: Callable[[str], None]
    load_model_function: Callable[[str], None]


class Command:
    def __init__(self, config: CommandConfig):
        self.name = config["name"]
        self.description = config["description"]
        self.args = config["args"]
        self.args_description = config["args_description"]
        self.context_required = config["context_required"]

    def __call__(self, context: Context | None):
        if context is None and self.context_required:
            print(f"ERROR: Context is required for {self.name} command!")
            return True

        return False
