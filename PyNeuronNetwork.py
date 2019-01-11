import numpy as np

class CDense():
    def __init__(self, input_dim=1, output_dim=1, activation=None):
        weights = np.array(np.random.randn(input_dim,output_dim) * np.sqrt(2/input_dim))
        bias = np.array(np.random.randn(1,output_dim) * np.sqrt(2))
        self.__weights = weights
        self.__bias = bias
        self.__activation = activation
        self.__layertype = 'Dense'

    @property
    def layertype(self):
        return self.__layertype

    @property
    def activation(self):
        return self.__activation

    @activation.setter
    def activation(self, function):
        self.__activation = function

    @property
    def weights(self):
        return self.__weights

    @weights.setter
    def weights(self, value):
        if (len(value) == self.weights.size):
            self.__weights = np.array(value).reshape(self.weights.shape)
        else:
            print('Weight Size Wrong')

    @property
    def bias(self):
        return self.__bias

    @bias.setter
    def bias(self, value):
        if (len(value) == self.bias.size):
            self.__bias = np.array(value).reshape(self.bias.shape)
        else:
            print('Bias Size Wrong')

class CNeuronNetworkModel():
    def __init__(self):
        self.__layer = []

    @property
    def layer(self):
        return self.__layer

    def add(self, layer):
        self.__layer.append(layer)

    def summary(self):
        print('---------------------------')
        print('Layer(type)    Output Shape')
        
        for i in range(len(self.__layer)):
            print(self.layer[i].layertype,'          ', self.layer[i].dim)

        print('---------------------------')
        return

    def set_weights(self, w):
        pass

    def get_weights(self):
        w = []
        for i in range(len(self.layer)):
            shape = self.layer[i].dim
            column = 1
            if (len(shape) > 1):
                column = shape[0]
                for j in range(1, len(shape)):
                    column = column * shape[j]
            
            for j in range(column):
                w.append(self.layer[i].tensor['weight'].reshape(1, column)[0][j])
                w.append(self.layer[i].tensor['bias'][0])

        return w

    def run(self, inputs, outputs, optimizer):
        pass





    