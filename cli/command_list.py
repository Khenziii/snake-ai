from typing import List
from cli.command import Command
from cli.commands import (
    help,
    exit,
    clear,
    start,
    stop,
    speed,
    color,
    pause,
    unpause,
    apple,
    grid_size,
    threads,
    save,
    load,
)

command_list: List[Command] = [
    help.HelpCommand({
        "name": "help",
        "description": "Lists available commands",
        "args": [None],
        "args_description": "First argument should be set to either:\n- name of the command that you'd like to learn "
                            "more about\n- nothing (in this case, the command will display a list of all commands)",
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
        "args_description": "First argument should be set to either `human` or `ai`. Default: `human`.",
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
        "args": [5],
        "args_description": "First argument should be a valid integer. Default: 5.",
        "context_required": True,
    }),
    color.ColorCommand({
        "name": "color",
        "description": "Sets game's colors",
        "args": ["snake_body", "(255,255,255)"],
        "args_description": "First argument should be set to either: `snake_body`, `snake_head`, `apple` or "
                            "`background`.\nSecond argument should be a valid RGB color.\nDefault: 'snake_body' & '("
                            "255,255,255)'",
        "context_required": True,
    }),
    pause.PauseCommand({
        "name": "pause",
        "description": "Pauses the game",
        "args": [],
        "args_description": None,
        "context_required": True,
    }),
    unpause.UnpauseCommand({
        "name": "unpause",
        "description": "Unpauses the game",
        "args": [],
        "args_description": None,
        "context_required": True,
    }),
    apple.AppleCommand({
        "name": "apple",
        "description": "Sets the amount of apples that are present at once",
        "args": [],
        "args_description": "First argument needs to be a valid int.",
        "context_required": True,
    }),
    grid_size.GridSizeCommand({
        "name": "grid_size",
        "description": "Sets the size of game's grid",
        "args": [],
        "args_description": "First argument needs to be a valid int.",
        "context_required": True,
    }),
    threads.ThreadsCommand({
        "name": "threads",
        "description": "Shows a tree of current threads. Useful for development",
        "args": [],
        "args_description": None,
        "context_required": False,
    }),
    save.SaveCommand({
        "name": "save",
        "description": "Saves current model's state into a file",
        "args": ["model.pth"],
        "args_description": "First argument is expected to be the target file to which model should be saved. "
                            "Default: model.pth",
        "context_required": True,
    }),
    load.LoadCommand({
        "name": "load",
        "description": "Loads old model's state from a file",
        "args": ["model.pth"],
        "args_description": "First argument is expected to be the target file from which model should be loaded. "
                            "Default: model.pth",
        "context_required": True,
    }),
]
