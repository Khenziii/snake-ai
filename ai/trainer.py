from typing import TypedDict
from ai.model import Net
from collections import deque
from torch import nn, optim, tensor, int64, stack
from random import sample


class TrainerConfig(TypedDict):
    model: Net
    memory_size: int
    batch_size: int
    gamma: float
    epsilon_start: float
    epsilon_end: float
    epsilon_decay: float


class Trainer:
    def __init__(self, config: TrainerConfig):
        self.model = config["model"]
        self.memory = deque(maxlen=config["memory_size"])
        self.batch_size = config["batch_size"]
        self.gamma = config["gamma"]
        self.epsilon_start = config["epsilon_start"]
        self.epsilon_end = config["epsilon_end"]
        self.epsilon_decay = config["epsilon_decay"]
        self.optimizer = optim.Adam(self.model.parameters())
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        if len(self.memory) < self.batch_size:
            print("not training!")
            return

        batch = sample(self.memory, self.batch_size)
        states, actions, rewards, new_states, dones = zip(*batch)

        states = stack(states)
        actions = tensor(actions, dtype=int64)
        rewards = tensor(rewards, dtype=int64)
        new_states = stack(new_states)
        dones = tensor(dones, dtype=int64)

        q_values = self.model(states)

        next_q_values = self.model(new_states).max(1)[0]
        target_q_values = rewards + (1 - dones) * self.gamma * next_q_values

        loss = nn.functional.mse_loss(q_values.gather(1, actions.unsqueeze(1)), target_q_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon_start > self.epsilon_end:
            self.epsilon_start *= self.epsilon_decay
