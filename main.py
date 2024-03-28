import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "true"

from config.config import ConfigConfig, Config
from cli.cli import CliConfig, Cli
from cli.command_list import command_list

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

# configConfig: ConfigConfig = {
#     "config_file_path": "config.json",
# }
# configManager = Config(configConfig)
# gameConfig: GameConfig = configManager.get_game_config(
#     game_auto_handle_loop=False,
#     game_finish_print=True
# )
# env = AIGame(config=gameConfig)
# netConfig: NetConfig = configManager.get_net_config()
# net = Net(config=netConfig)
# agentConfig: AgentConfig = configManager.get_agent_config(
#     model=net,
#     env=env,
# )
# agent = Agent(config=agentConfig)
# trainerConfig: TrainerConfig = configManager.get_trainer_config(
#     model=net
# )
# trainer = Trainer(config=trainerConfig)
#
# scores = []
# rewards = []
#
# # Training loop
# for epoch in range(1_000_000_000):  # Number of epochs
#     state = agent.get_state()
#     action = agent.get_action(state)
#     reward, is_game_over = env.handle_action(action)
#     new_state = agent.get_state()
#     trainer.remember(state, action, reward, new_state, is_game_over)
#     trainer.train()
#
#     score = env.get_score()
#     scores.append(score)
#     rewards.append(reward)
#     if epoch % 100 == 0:
#         print(f"score: {score}")
#         print(f"average score: {sum(scores) / len(scores)}")
#         print(f"reward: {reward}")
#         print(f"average reward: {sum(rewards) / len(rewards)}")

configConfig: ConfigConfig = {
    "config_file_path": "config.json",
}
configManager = Config(configConfig)

cliConfig: CliConfig = {
    "display_init_message": True,
    "commands": command_list,
    "config_manager": configManager,
}
cli = Cli(config=cliConfig)
