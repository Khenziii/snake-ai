import pygame
from typing import TypedDict, Tuple, List
from enum import Enum


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class SquareConfig(TypedDict):
    size: int
    location_x: int
    location_y: int
    color: Tuple[int, int, int]
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


class Position(TypedDict):
    x: int
    y: int
    square: Square


class SquaresType(Position):
    snake: bool


class GameConfig(TypedDict):
    window_size_px: int
    window_title: str
    game_speed: int
    game_grid_size: int
    game_snake_start_length: int


class Game:
    def __init__(self, config: GameConfig):
        self.window_size_px = config["window_size_px"]
        self.window_title = config["window_title"]
        self.game_speed = config["game_speed"]
        self.game_grid_size = config["game_grid_size"]
        self.game_snake_start_length = config["game_snake_start_length"]

        self.tiles: List[SquaresType] = []
        self.snake_tiles: List[Position] = []
        self.snake_direction: Direction = Direction.RIGHT

        self.__run()

    def __run(self):
        pygame.init()

        self.display = pygame.display.set_mode((self.window_size_px, self.window_size_px))
        pygame.display.set_caption(self.window_title)

        self.__create_board()
        self.__create_snake()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.__render_board()
            self.__move_snake()
            pygame.display.flip()  # .flip() updates the display
            pygame.time.Clock().tick(self.game_speed)  # FPS cap

        pygame.display.quit()
        pygame.quit()

    def __create_board(self):
        size = int(self.window_size_px / self.game_grid_size)

        for y in range(self.game_grid_size):
            for x in range(self.game_grid_size):
                square_config: SquareConfig = {
                    "size": size,
                    "location_x": x * size,
                    "location_y": y * size,
                    "color": (0, 0, 0),
                    "display": self.display
                }
                square = Square(config=square_config)

                square_type: SquaresType = {
                    "x": x,
                    "y": y,
                    "snake": False,
                    "square": square,
                }
                self.tiles.append(square_type)

    def __create_snake(self):
        for i in range(self.game_snake_start_length):
            square: SquaresType = self.tiles[i]
            self.__set_square_as_snake(square)

    def __set_square_as_snake(self, square: SquaresType) -> SquaresType:
        square.update({"snake": True})
        square["square"].change_color((255, 255, 255))
        self.snake_tiles.append(square)

        return square

    def __unset_square_as_snake(self, square: SquaresType):
        square.update({"snake": False})
        square["square"].change_color((0, 0, 0))

        if square in self.snake_tiles:
            self.snake_tiles.remove(square)
        else:
            print("WARNING: Tried to un-snake a square that's not a snake, something's probably wrong with the logic")

    def __get_square_by_x_and_y(self, x: int, y: int) -> SquaresType:
        results = [d for d in self.tiles if d.get("x") == x and d.get("y") == y]
        return results[0]

    def __render_board(self):
        for tile in self.tiles:
            tile["square"].rerender()

    def __move_snake(self):
        head: Position = self.snake_tiles[-1]
        tail: Position = self.snake_tiles[0]

        square_to_remove = self.__get_square_by_x_and_y(tail["x"], tail["y"])
        self.__unset_square_as_snake(square_to_remove)

        match self.snake_direction:
            case Direction.UP:
                if head["y"] + 1 >= self.game_grid_size:
                    square_to_add = self.__get_square_by_x_and_y(head["x"], 0)
                else:
                    square_to_add = self.__get_square_by_x_and_y(head["x"], head["y"] + 1)

                self.__set_square_as_snake(square_to_add)
            case Direction.DOWN:
                if head["y"] - 1 <= self.game_grid_size:
                    square_to_add = self.__get_square_by_x_and_y(head["x"], self.game_grid_size)
                else:
                    square_to_add = self.__get_square_by_x_and_y(head["x"], head["y"] - 1)

                self.__set_square_as_snake(square_to_add)
            case Direction.RIGHT:
                if head["x"] + 1 >= self.game_grid_size:
                    square_to_add = self.__get_square_by_x_and_y(0, head["y"])
                else:
                    square_to_add = self.__get_square_by_x_and_y(head["x"] + 1, head["y"])

                self.__set_square_as_snake(square_to_add)
            case Direction.LEFT:
                if head["x"] - 1 <= self.game_grid_size:
                    square_to_add = self.__get_square_by_x_and_y(self.game_grid_size, head["y"])
                else:
                    square_to_add = self.__get_square_by_x_and_y(head["x"] - 1, head["y"])

                self.__set_square_as_snake(square_to_add)


gameConfig: GameConfig = {
    "window_size_px": 1000,
    "window_title": "Snake Game",
    "game_speed": 10,
    "game_grid_size": 20,
    "game_snake_start_length": 5,
}
game = Game(config=gameConfig)
