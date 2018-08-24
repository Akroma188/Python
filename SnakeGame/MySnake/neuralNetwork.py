import numpy as np
from scipy.stats import truncnorm


# make neural network with bias and 2 hidden layers
# use sigmoid as activation funtion
@np.vectorize
def activation_function(x):
    return 1 / (np.e ** -x)

def truncated_normal(mean, sd, low, upp):
    return truncnorm((low - mean)/sd, (upp - mean)/sd, mean, sd)

class NeuralNetwork:
    def __init__(self, num_input, num_first_hidden, num_sec_hidden, num_output):
        self.num_input = num_input
        self.num_first_hidden = num_first_hidden
        self.num_sec_hidden = num_sec_hidden
        self.num_output = num_output
        self.bias = 1

    def create_weight_matrices(self):
        # generate random distribution for weights between input and 1st hidden layer
        rad = 1 / np.sqrt(self.num_input + self.bias)
        X = truncated_normal(0, 1, -rad, rad)
        self.wih = X.rvs((self.num_first_hidden, self.num_input + self.bias))

        # generate random distribution for weights between 1st hidden layer and 2nd hidden layer
        rad = 1 / np.sqrt(self.num_first_hidden + self.bias)
        X = truncated_normal(0, 1, -rad, rad)
        self.whh = X.rvs((self.num_sec_hidden, self.num_first_hidden + self.bias))

        # generate random distribution for weights between 2nd hidden layer and output layer
        rad = 1 / np.sqrt(self.num_sec_hidden + self.bias)
        X = truncated_normal(0, 1, -rad, rad) 
        self.who = X.rvs((self.num_output, self.num_sec_hidden + self.bias))   

neural = NeuralNetwork(5,5,5,5)
neural.create_weight_matrices()
print(neural.who)