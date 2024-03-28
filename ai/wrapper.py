from typing import TypedDict
from ai.ai_game import AIGame
from ai.model import Net
from ai.agent import Agent
from ai.trainer import Trainer


class WrapperConfig(TypedDict):
    auto_run: bool
    finish_print: bool
    env: AIGame
    model: Net
    agent: Agent
    trainer: Trainer


# A class, that manages training the neural network
# using ai_game, agent, model & trainer.
class Wrapper:
    def __init__(self, config: WrapperConfig):
        self.finish_print = config["finish_print"]
        self.env = config["env"]
        self.model = config["model"]
        self.agent = config["agent"]
        self.trainer = config["trainer"]

        self.running = True
        auto_run = config["auto_run"]
        if auto_run:
            self.run()

    def run(self):
        scores = []
        rewards = []
        iteration = 0

        # Training loop
        while self.running:
            state = self.agent.get_state()
            action = self.agent.get_action(state)
            reward, is_game_over = self.env.handle_action(action)
            new_state = self.agent.get_state()
            self.trainer.remember(state, action, reward, new_state, is_game_over)
            self.trainer.train()

            score = self.env.get_score()
            scores.append(score)
            rewards.append(reward)

            iteration += 1
            if not self.finish_print:
                continue
            if iteration % 100 == 0:
                print(f"score: {score}")
                print(f"average score: {sum(scores) / len(scores)}")
                print(f"reward: {reward}")
                print(f"average reward: {sum(rewards) / len(rewards)}")
