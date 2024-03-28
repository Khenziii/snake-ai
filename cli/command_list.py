from typing import List
from cli.command import Command
from cli.commands import help, exit, clear, start, stop, speed


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
    start.StartCommand({
        "name": "start",
        "description": "Starts the game",
        "args": ["human"],
        "args_description": "First argument should be set to either `human` or `ai`",
        "context_required": True,
    }),
    stop.StopCommand({
        "name": "stop",
        "description": "Stops the game",
        "args": [],
        "args_description": None,
        "context_required": True,
    }),
    speed.SpeedCommand({
        "name": "speed",
        "description": "Sets game's FPS (more -> snake moves faster)",
        "args": [10],
        "args_description": "First argument should be a valid integer. Default: 10.",
        "context_required": True,
    })
]
