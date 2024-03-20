import pygame
from typing import TypedDict, Tuple

SquareColor = Tuple[int, int, int]


class SquareConfig(TypedDict):
    size: int
    location_x: int
    location_y: int
    color: SquareColor
    display: pygame.Surface


class Square:
    def __init__(self, config: SquareConfig):
        self.size = config["size"]
        self.location_x = config["location_x"]
        self.location_y = config["location_y"]
        self.color = config["color"]
        self.display = config["display"]

        self.rerender()

    def change_color(self, color: Tuple[int, int, int]):
        self.color = color

    def rerender(self):
        pygame.draw.rect(self.display, self.color, (self.location_x, self.location_y, self.size, self.size))
