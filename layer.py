# %% IMPORTS
import numpy as np

# %% layer
class layer():

    def __init__(self, nodes):
        self.nodes = nodes # originally weights
    #

    def calcWeightedInput(self, inputs):
        # assumes...
        # len(weights[i]) = len(inputs)

        # multiply weights[i] * inputs = a single WeightedInput 
        WeightedInput = [sum(node * inputs) for node in self.nodes]

        return WeightedInput
    #

    def activation(self, inputs):

        for indx, input in enumerate(inputs):
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
inputs = np.random.random_sample(size = 5)
print(inputs)

layer1 = layer([np.random.random_sample(size = 5) for node in range(0,5)])
print(layer1.nodes)

output = layer1.calcWeightedInput(inputs)
print(output)

final = layer1.activation(output)
print(final)