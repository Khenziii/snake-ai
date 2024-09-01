## snake-ai

snake-ai is an extensible and customizable snake game; that offers a CLI & supports training neural networks.

### Features

- CLI - A decent part of this project is its command line interface. It allows you to work more easily & gives you access to a bunch of useful perks (such as being able to change snake's color while the game is running). To list all available commands use the `help` command.

[Video Showcasing CLI](https://github.com/Khenziii/snake-ai/assets/126098761/19baf974-d959-456b-8d67-c92d886b47bb)

- Game - The snake game itself is created using pygame. It's cleanly written and open for extension.
- Plotter - [matplotlib](https://matplotlib.org/) is being used to show nice graphs of achieved scores.
- AI - You can train, save and load neural networks at almost no effort. CLI and plotter make it convenient to track progress of your models.
- Config - thanks to the [config module](https://github.com/Khenziii/snake-ai/blob/master/config/config.py), a lot of settings can be managed directly from a .json file.

### Contributing

All contributions are greatly appreciated. PRs will be reviewed.

#### Development Environment

```shell
$ poetry install
$ SNAKE_AI_ENV=dev poetry run python3 main.py
```

If you're using NixOS, you can run those commands instead:

```shell
$ nix develop
$ python3 main.py
```

