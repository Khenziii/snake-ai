from ai.ai_game import GameConfig, AIGame
from ai.model import NetConfig, Net
from ai.agent import AgentConfig, Agent
from ai.trainer import TrainerConfig, Trainer

# gameConfig: GameConfig = {
#     "window_size_px": 1000,
#     "window_title": "Snake Game",
#     "game_speed": 10,
#     "game_grid_size": 10,
#     "game_snake_start_length": 3,
#     "game_apple_start_count": 2,
#     "game_snake_color": (255, 255, 255),
#     "game_apple_color": (255, 0, 0),
#     "game_background_color": (0, 0, 0),
#     "game_auto_handle_loop": True
# }
# game = Game(config=gameConfig)

gameConfig: GameConfig = {
    "window_size_px": 1000,
    "window_title": "Snake Game",
    "game_speed": 20,
    "game_grid_size": 10,
    "game_snake_start_length": 3,
    "game_apple_start_count": 2,
    "game_snake_color": (255, 255, 255),
    "game_apple_color": (255, 0, 0),
    "game_background_color": (0, 0, 0),
    "game_auto_handle_loop": False
}
env = AIGame(config=gameConfig)
netConfig: NetConfig = {
    "input_nodes": 400,
    "hidden_nodes": 256,
    "output_nodes": 4,
}
net = Net(config=netConfig)
agentConfig: AgentConfig = {
    "model": net,
    "env": env,
}
agent = Agent(config=agentConfig)
trainerConfig: TrainerConfig = {
    "model": net,
    "memory_size": 10_000,
    "batch_size": 64,
    "gamma": 0.99,
    "epsilon_start": 1.0,
    "epsilon_end": 0.01,
    "epsilon_decay": 0.995,
}
trainer = Trainer(config=trainerConfig)

# Training loop
for epoch in range(1000):  # Number of epochs
    state_old, _ = agent.get_state()
    action = agent.get_action()
    reward = env.handle_action(action)
    state, is_game_over = agent.get_state()
    trainer.remember(state_old, action, reward, state, is_game_over)
    trainer.train()
