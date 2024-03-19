import pygame
from typing import TypedDict


class GameConfig(TypedDict):
    window_width: int
    window_height: int
    window_title: str
    game_speed: int


class Game:
    def __init__(self, config: GameConfig):
        self.window_width = config["window_width"]
        self.window_height = config["window_height"]
        self.window_title = config["window_title"]
        self.game_speed = config["game_speed"]
        self.__pygame_init()

    def __pygame_init(self):
        width = self.window_width
        height = self.window_height
        title = self.window_title
        speed = self.game_speed

        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))
            pygame.display.flip()  # .flip() updates the display
            pygame.time.Clock().tick(speed)  # FPS cap

        pygame.quit()


gameConfig: GameConfig = {
    "window_width": 1000,
    "window_height": 1000,
    "window_title": "Snake Game",
    "game_speed": 60,
}
game = Game(config=gameConfig)
