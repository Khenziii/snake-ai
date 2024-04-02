from torch import nn
from typing import TypedDict


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
