from game.game import Game, GameConfig


class AIGame(Game):
    def __init__(self, config: GameConfig):
        super().__init__(config)
        self.current_generation = 0

    def _restart_game(self):
        super()._restart_game()
        self.current_generation += 1
