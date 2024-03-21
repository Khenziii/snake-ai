from game.game import GameConfig, Game

gameConfig: GameConfig = {
    "window_size_px": 1000,
    "window_title": "Snake Game",
    "game_speed": 10,
    "game_grid_size": 10,
    "game_snake_start_length": 3,
    "game_apple_start_count": 2,
    "game_snake_color": (255, 255, 255),
    "game_apple_color": (255, 0, 0),
    "game_background_color": (0, 0, 0),
    "game_auto_handle_loop": True
}
game = Game(config=gameConfig)
