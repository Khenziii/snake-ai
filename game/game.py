import pygame
from typing import TypedDict, List
from game.square import Square, SquareConfig, SquareColor
from game.types import Direction, Position, SquaresType
from random import randint


class GameConfig(TypedDict):
    window_size_px: int
    window_title: str
    game_speed: int
    game_grid_size: int
    game_snake_start_length: int
    game_apple_start_count: int
    game_snake_color: SquareColor
    game_apple_color: SquareColor
    game_background_color: SquareColor


class Game:
    def __init__(self, config: GameConfig):
        self.window_size_px = config["window_size_px"]
        self.window_title = config["window_title"]
        self.game_speed = config["game_speed"]
        self.game_grid_size = config["game_grid_size"]
        self.game_snake_start_length = config["game_snake_start_length"]
        self.game_apple_start_count = config["game_apple_start_count"]
        self.game_snake_color = config["game_snake_color"]
        self.game_apple_color = config["game_apple_color"]
        self.game_background_color = config["game_background_color"]

        self.tiles: List[SquaresType] = []
        self.snake_tiles: List[Position] = []
        self.snake_direction: Direction = Direction.RIGHT
        self.apple_tiles: List[Position] = []

        self.__run()

    def __run(self):
        pygame.init()

        self.display = pygame.display.set_mode((self.window_size_px, self.window_size_px))
        pygame.display.set_caption(self.window_title)

        self.__create_board()
        self.__create_snake()
        self.__create_apples()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    match event.unicode:
                        case "w":
                            self.snake_direction = Direction.UP
                        case "s":
                            self.snake_direction = Direction.DOWN
                        case "a":
                            self.snake_direction = Direction.LEFT
                        case "d":
                            self.snake_direction = Direction.RIGHT

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
                    "color": self.game_background_color,
                    "display": self.display
                }
                square = Square(config=square_config)

                square_type: SquaresType = {
                    "x": x,
                    "y": y,
                    "snake": False,
                    "apple": False,
                    "square": square,
                }
                self.tiles.append(square_type)

    def __create_snake(self):
        for i in range(self.game_snake_start_length):
            square: SquaresType = self.tiles[i]
            self.__set_square_as_snake(square)

    def __set_square_as_snake(self, square: SquaresType) -> SquaresType:
        square.update({"snake": True})
        square["square"].change_color(self.game_snake_color)
        self.snake_tiles.append(square)

        return square

    def __unset_square_as_snake(self, square: SquaresType):
        square.update({"snake": False})
        square["square"].change_color(self.game_background_color)

        if square in self.snake_tiles:
            self.snake_tiles.remove(square)
        else:
            print("WARNING: Tried to un-snake a square that's not a snake, something's probably wrong with the logic")

    def __set_square_as_apple(self, square: SquaresType) -> SquaresType:
        square.update({"apple": True})
        square["square"].change_color(self.game_apple_color)
        self.apple_tiles.append(square)

        return square

    def __unset_square_as_apple(self, square: SquaresType):
        square.update({"apple": False})
        square["square"].change_color(self.game_snake_color)

        if square in self.apple_tiles:
            self.apple_tiles.remove(square)
        else:
            print("WARNING: Tried to un-apple a square that's not an apple, something's probably wrong with the logic")

        self.__generate_apple()

    def __get_square_by_x_and_y(self, x: int, y: int) -> SquaresType:
        results = [d for d in self.tiles if d.get("x") == x and d.get("y") == y]
        if len(results) == 0:
            raise ValueError(f"Couldn't find any tiles for: x: {x} & y: {y}")

        return results[0]

    def __render_board(self):
        for tile in self.tiles:
            tile["square"].rerender()

    def __move_snake(self):
        head: Position = self.snake_tiles[-1]
        tail: Position = self.snake_tiles[0]

        eaten_an_apple = False
        for apple in self.apple_tiles:
            if head == apple:
                square = self.__get_square_by_x_and_y(head["x"], head["y"])
                self.__unset_square_as_apple(square)
                eaten_an_apple = True

        square_to_remove = self.__get_square_by_x_and_y(tail["x"], tail["y"])
        if not eaten_an_apple:
            self.__unset_square_as_snake(square_to_remove)

        # !!!IMPORTANT!!!
        # The Y axis is reversed for some reason, this is going to be looked into soon
        match self.snake_direction:
            case Direction.UP:
                if head["y"] <= 0:
                    square_to_add = self.__get_square_by_x_and_y(head["x"], self.game_grid_size - 1)
                else:
                    square_to_add = self.__get_square_by_x_and_y(head["x"], head["y"] - 1)

                self.__set_square_as_snake(square_to_add)
            case Direction.DOWN:
                if head["y"] + 1 >= self.game_grid_size:
                    square_to_add = self.__get_square_by_x_and_y(head["x"], 0)
                else:
                    square_to_add = self.__get_square_by_x_and_y(head["x"], head["y"] + 1)

                self.__set_square_as_snake(square_to_add)
            case Direction.RIGHT:
                if head["x"] + 1 >= self.game_grid_size:
                    square_to_add = self.__get_square_by_x_and_y(0, head["y"])
                else:
                    square_to_add = self.__get_square_by_x_and_y(head["x"] + 1, head["y"])

                self.__set_square_as_snake(square_to_add)
            case Direction.LEFT:
                if head["x"] <= 0:
                    square_to_add = self.__get_square_by_x_and_y(self.game_grid_size - 1, head["y"])
                else:
                    square_to_add = self.__get_square_by_x_and_y(head["x"] - 1, head["y"])

                self.__set_square_as_snake(square_to_add)

    def __generate_apple(self):
        random_index = randint(0, len(self.tiles))

        # check, if the tile is a snake or an apple
        square = self.tiles[random_index]
        if square["snake"] or square["apple"]:
            return self.__generate_apple()

        self.__set_square_as_apple(square)

    def __create_apples(self):
        for i in range(self.game_apple_start_count):
            self.__generate_apple()
