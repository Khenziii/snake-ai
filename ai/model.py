from torch import nn
from torch import save as torch_save
from torch import load as torch_load
from typing import TypedDict
from os import path, getcwd


class NetConfig(TypedDict):
    input_nodes: int
    hidden_nodes: int
    output_nodes: int


class Net(nn.Module):
    def __init__(self, config: NetConfig):
        super(Net, self).__init__()

        self.input_nodes = config["input_nodes"]
        self.hidden_nodes = config["hidden_nodes"]
        self.output_nodes = config["output_nodes"]

        # fc - fully connected layer
        self.fc1 = nn.Linear(self.input_nodes, self.hidden_nodes)
        self.fc2 = nn.Linear(self.hidden_nodes, self.output_nodes)

    def forward(self, x):
        x = self.fc1(x)
        x = nn.functional.relu(x)
        x = self.fc2(x)

        return x

    def save(self, filename: str = "model.pth"):
        torch_save(self.state_dict(), filename)

    def load(self, filename: str = "model.pth"):
        if not path.exists(filename):
            raise FileNotFoundError(f"No file called {filename} in {getcwd()}")

        old_model = torch_load(filename)
        self.load_state_dict(old_model)
