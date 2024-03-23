from game.game import Game, GameConfig
from game.types import Direction


class AIGame(Game):
    def __init__(self, config: GameConfig):
        super().__init__(config)
        self.current_generation = 0

    def _restart_game(self):
        super()._restart_game()
        self.current_generation += 1

    def play_move(self):
        super().play_move()
        return self.get_state()

    def get_state(self):
        reward = 0
        if self.restart:
            reward = -100
        if self.collected_apple:
            reward = 10

        return self.tiles, reward, self.restart

    def handle_action(self, action: int):
        possible_directions = list(Direction)
        self.snake_direction = possible_directions[action]

        _, reward, is_game_over = self.play_move()
        return reward, is_game_over

    def get_score(self):
        return len(self.snake_tiles) + 1 - self.game_snake_start_length
