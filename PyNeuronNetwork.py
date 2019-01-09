import numpy as np

class CDense():
    def __init__(self, input_dim=1, output_dim=1, activation=None):
        self.__tensor = np.array(np.random.randn(input_dim,output_dim) * np.sqrt(2/input_dim))
        self.__activation = activation
        self.__layertype = 'Dense'

    @property
    def tensor(self):
        return self.__tensor

    @tensor.setter
    def tensor(self, value):
        if (len(value) == self.tensor.size):
            self.__tensor = np.array(value).reshape(self.tensor.shape)
        else:
            print('Size Wrong')

    @property
    def layertype(self):
        return self.__layertype

    @property
    def activation(self):
        return self.__activation

    @activation.setter
    def activation(self, function):
        self.__activation = function

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
            print(self.layer[i].layertype,'          ', self.layer[i].tensor.shape)

        print('---------------------------')
        return

    def set_weights(self, w):
        pass

    def get_weights(self):
        w = []
        for i in range(len(self.layer)):
            shape = self.layer[i].tensor.shape
            column = 1
            if (len(shape) > 1):
                column = shape[0]
                for j in range(1, len(shape)):
                    column = column * shape[j]
            
            for j in range(column):
                w.append(self.layer[i].tensor.reshape(1, column)[0][j])

        return w

    def predict(self, x):
        layers = self.layer.copy()

        for i in range(len(layers)):
            size = layers[i].size

    def run(self, inputs, outputs, optimizer):
        pass





    