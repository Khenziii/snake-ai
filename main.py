from ai.ai_game import GameConfig, AIGame
from ai.model import Net, NetConfig
from ai.agent import AgentConfig, Agent
from torch import nn, optim

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
    "game_speed": 1,
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

# Define the loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)

# Training loop
for epoch in range(1000):  # Number of epochs
    action = agent.get_action()
    reward = env.handle_action(action)

    # # Calculate the loss
    # loss = criterion(action, reward)
    #
    # # Backpropagate and optimize
    # optimizer.zero_grad()
    # loss.backward()
    # optimizer.step()
    #
    # # Print the loss every 100 epochs
    # if epoch % 100 == 0:
    #     print(f'Epoch {epoch}, Loss: {loss.item()}')
