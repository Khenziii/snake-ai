from typing import TypedDict, List, Any


class CommandConfig(TypedDict):
    name: str
    description: str
    args: List[Any]
    args_description: str | None
    context_required: bool


class Context(TypedDict):
    other_commands: List[CommandConfig]


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