from torch import nn, relu


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        # take a look at this:
        # https://i.imgur.com/jXFKmyj.png
        # as you can see, a neural network consist of:
        # input layer, hidden layer/s, output layer
        # there actually can be a lot of hidden layers, but
        # for our use case, just one should be sufficient

        # the number of input nodes is determined by the number of
        # actions that the network can take in scenario given by the environment
        # in our case, that's 4 (move: up / down / right / left)
        number_of_input_nodes = 4

        # getting the number of hidden nodes is a little bit more tricky
        # some people say that it's more like art than science
        # finding the actual correct / perfect number of hidden nodes can involve
        # a lot of effort, so I'll just use a few rules of thumb to get the number somewhat right,
        # here are the rules:
        # 1. There should be less hidden nodes than input and output nodes
        # 2. The number of hidden nodes should be around 2/3 of input nodes
        # + output_nodes
        # 3. The number of hidden nodes should be less than 2 * input nodes
        number_of_hidden_nodes = 4

        # number of output nodes is just the number of outputs that we want.
        # if we were to calculate the probability of each possible move, then we'd
        # set this to four. For our use case, this is going to be one, as we want to
        # find the best move (there should be only one best move).
        number_of_output_nodes = 1

        # fc - fully connected layer
        self.fc1 = nn.Linear(number_of_input_nodes, number_of_hidden_nodes)
        self.fc2 = nn.Linear(number_of_hidden_nodes, number_of_output_nodes)

    def forward(self, x):
        x = self.fc1(x)
        x = relu(x)
        x = self.fc2(x)

        return x
