import pygame
from typing import TypedDict, Tuple, List


class Position(TypedDict):
    x: int
    y: int


class SquaresType(Position):
    snake: bool


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

        self.change_color(self.color)

    def change_color(self, color: Tuple[int, int, int]):
        pygame.draw.rect(self.display, color, (self.location_x, self.location_y, self.size, self.size))


class GameConfig(TypedDict):
    window_size_px: int
    window_title: str
    game_speed: int
    game_grid_size: int
    game_snake_length: int


class Game:
    def __init__(self, config: GameConfig):
        self.window_size_px = config["window_size_px"]
        self.window_title = config["window_title"]
        self.game_speed = config["game_speed"]
        self.game_grid_size = config["game_grid_size"]
        self.game_snake_length = config["game_snake_length"]

        self.tiles: List[SquaresType] = []
        self.snake_tiles: List[Position] = []

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
                Square(config=square_config)

                square: SquaresType = {
                    "x": x,
                    "y": y,
                    "snake": False
                }
                self.tiles.append(square)

    def __create_snake(self):
        pass


gameConfig: GameConfig = {
    "window_size_px": 1000,
    "window_title": "Snake Game",
    "game_speed": 60,
    "game_grid_size": 5,
    "game_snake_length": 5,
}
game = Game(config=gameConfig)
