# %% IMPORTS
import numpy as np
import math as m

# %% layer
class layer():

    def __init__(self, nodes, weights):
        self.nodes = nodes # originally weights
        self.weights = weights
    #

    def calcWeightedInput(self, inputs):
        # assumes...
        # len(weights[i]) = len(inputs)

        # multiply weights[i] * inputs = a single WeightedInput 
        WeightedInput = [sum(weight * inputs) for weight in self.weights]

        return WeightedInput
    #

    def activation(self, inputs):

        for indx, input in enumerate(inputs):
            inputs[indx] = 1 / (1 + m.exp(-input))

            if(input < 1):
                inputs[indx] = 0
            else:
                inputs[indx] = 1
            #
        #

        return inputs
    #

# layer

# %% 
# inputs = np.random.random_sample(size = 5)

# layer1 = layer(np.zeros((5), dtype = float), [np.random.random_sample(size = 5) for node in range(0,5)])
# print(layer1.weights)
# print(layer1.nodes)

# output = layer1.calcWeightedInput(inputs)
# print(output)

# final = layer1.activation(output)
# print(final)