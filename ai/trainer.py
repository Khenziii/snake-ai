from typing import TypedDict
from ai.model import Net
from collections import deque
from torch import nn, optim
from torch import max as torch_max
from random import sample


class TrainerConfig(TypedDict):
    model: Net
    memory_size: int  # each item in this list will take up about 250 bytes.
    batch_size: int
    gamma: float


class Trainer:
    def __init__(self, config: TrainerConfig):
        self.model = config["model"]
        self.memory = deque(maxlen=config["memory_size"])
        self.batch_size = config["batch_size"]
        self.gamma = config["gamma"]
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()

        self.model.train()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def __train(self, state, action, reward, next_state, done):
        prediction = self.model(state)
        target = prediction.clone()

        new_q = reward
        if not done:
            new_prediction = self.model(next_state)
            new_q = reward + self.gamma * torch_max(new_prediction).item()

        target[action] = new_q

        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()
        self.optimizer.step()

    def train_short_memory(self):
        latest_memory = self.memory[-1]
        state, action, reward, next_state, done = latest_memory

        self.__train(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > self.batch_size:
            batch = sample(self.memory, self.batch_size)
        else:
            batch = self.memory

        states, actions, rewards, next_states, dones = zip(*batch)

        for index, _ in enumerate(states):
            state = states[index]
            action = actions[index]
            reward = rewards[index]
            next_state = next_states[index]
            done = dones[index]

            self.__train(state, action, reward, next_state, done)
