from game.game import GameConfig, Game

gameConfig: GameConfig = {
    "window_size_px": 1000,
    "window_title": "Snake Game",
    "game_speed": 10,
    "game_grid_size": 50,
    "game_snake_start_length": 1,
    "game_apple_start_count": 5,
}
game = Game(config=gameConfig)
