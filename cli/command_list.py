from typing import List
from cli.commands import help, exit
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
    })
]
