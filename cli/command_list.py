from typing import List
from cli.commands import help, exit, clear
from cli.command import Command


command_list: List[Command] = [
    help.HelpCommand({
        "name": "help",
        "description": "Lists available commands",
        "args": [],
        "args_description": None,
        "context_required": True,
    }),
    exit.ExitCommand({
        "name": "exit",
        "description": "Exits CLI",
        "args": [],
        "args_description": None,
        "context_required": True,
    }),
    clear.ClearCommand({
        "name": "clear",
        "description": "Clears the command line",
        "args": [],
        "args_description": None,
        "context_required": False,
    }),
]
