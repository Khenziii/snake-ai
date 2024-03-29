from typing import TypedDict, Callable
from threading import Thread, current_thread


class ThreadWrapperConfig(TypedDict):
    name: str
    target: Callable
    daemon: bool


class ThreadWrapper(Thread):
    def __init__(self, config: ThreadWrapperConfig):
        super().__init__(
            target=config["target"],
            name=config["name"],
            daemon=config["daemon"]
        )

        self.target = config["target"]
        self.name = config["name"]
        self.parent = current_thread()
