import numpy as np
import math
import xlrd
from PyOptimizer import CGradDecent
from PyNeuronNetwork import CDense
from PyNeuronNetwork import CNeuronNetworkModel

def sigmoid(x):
    return 1./(1 + math.exp(-x))

def Relu(x):
    return np.maximum(x,0)

def BatchNormalize(x):
    avg = np.average(x)
    std = np.std(x)

    X = []
    for i in range(len(x)):
        X.append((x[i] - avg) / std)

    return np.array(X)

Data_file = 'fire_theft.xls'
book = xlrd.open_workbook(Data_file, encoding_override='utf-8')
sheet = book.sheet_by_index(0)
data = np.asarray([sheet.row_values(i) for i in range(1, sheet.nrows)])

X1 = data[:,0].reshape(42,1)
X2 = data[:,1].reshape(42,1)
X1Nor = BatchNormalize(X1)
X2Nor = BatchNormalize(X2)
dataNor = np.concatenate((X1Nor, X2Nor), axis=1)
z = np.linspace(1,42,num=42).reshape(42,1) / 42.

# Model = CNeuronNetworkModel()
# Model.add(CDense(  2, 128, activation=np.tanh))
# Model.add(CDense(128,  64, activation=np.tanh))
# Model.add(CDense( 64,  16, activation=np.tanh))
# Model.add(CDense( 16,   8, activation=np.tanh))
# Model.add(CDense(  8,   4, activation=np.tanh))
# Model.add(CDense(  4,   1, activation=np.tanh))
# Model.summary()
# X0 = Model.get_weights()
# layers = Model.layer

layers = []
layers.append(CDense(2, 128, activation=np.tanh))
layers.append(CDense(128, 64, activation=np.tanh))
layers.append(CDense(64, 16, activation=np.tanh))
layers.append(CDense(16, 8, activation=np.tanh))
layers.append(CDense(8, 4, activation=np.tanh))
layers.append(CDense(4, 1, activation=np.tanh))

X0 = []
for i in range(len(layers)):
    w_size = layers[i].weights.size
    b_size = layers[i].bias.size
    
    for j in range(w_size):
        X0.append(layers[i].weights.reshape(1,w_size)[0][j])

    for k in range(b_size):
        X0.append(layers[i].bias.reshape(1, b_size)[0][k])
    

def predict(data):
    output = 0
    for i in range(len(layers)):
        activation = layers[i].activation
        if (i == 0):
            output = activation(np.add(np.dot(data.reshape(1,2), layers[i].weights), layers[i].bias))
        else:
            output = activation(np.add(np.dot(output, layers[i].weights), layers[i].bias))
    
    return output

def MSE(x,index):
    loss = 0
    index_start = 0
    for i in range(len(layers)):
        w_size = layers[i].weights.size
        b_size = layers[i].bias.size
        
        layers[i].weights = x[index_start:index_start + w_size]
        
        index_start = index_start + w_size
        
        layers[i].bias = x[index_start:index_start + b_size]

        index_start = index_start + b_size
        
    # for i in range(len(data)):
    #     yp = predict(data[i].reshape(1,2))
    #     # print('Predict' ,yp, 'Design', z[i])
    #     loss = loss + (z[i] - yp)**2

    # loss = loss / len(data)

    yp = predict(data[index].reshape(1,2))
    # print('Predict' ,yp, 'Design', z[i])
    loss = (z[i] - yp)**2
    
    return loss

def PredictNN():
    for i in range(len(data)):
        yp = predict(data[i].reshape(1,2))
        print('Predict' ,yp, 'Design', z[i])
        
    return

def ChicagoNNModel(x):
    activation = math.tanh

    #random_index = np.random.randint(low=0,high=41,size=10).tolist()
    #print('random_index: ', random_index)
    cost = 0
    for i in range(0, len(X1Nor)):
        h1 = activation(x[0] * X1Nor[i] + x[1] * X2Nor[i] + x[2])
        
        h2 = activation(x[3] * X1Nor[i] + x[4] * X2Nor[i] + x[5])

        h3 = activation(x[6] * X1Nor[i] + x[7] * X2Nor[i] + x[8])

        h4 = activation(x[9] * X1Nor[i] + x[10] * X2Nor[i] + x[11])

        h5 = activation(x[12] * h1 + x[13] * h2 + x[14] * h3 + x[15] * h4 + x[16]) 

        h6 = activation(x[17] * h1 + x[18] * h2 + x[19] * h3 + x[20] * h4 + x[21])

        h7 = activation(x[22] * h1 + x[23] * h2 + x[24] * h3 + x[25] * h4 + x[26])

        h8 = activation(x[27] * h1 + x[28] * h2 + x[29] * h3 + x[30] * h4 + x[31])

        y = activation(x[32] * h5 + x[33] * h6 + x[34] * h7 + x[35] * h8 + x[37]) 

        MSE = (z[i] - y)**2 /2
        cost = cost + MSE

    return cost

def ChicagoNNPrediction(x):
    activation = math.tanh
    for i in range(0, len(X1Nor)):
        h1 = activation(x[0] * X1Nor[i] + x[1] * X2Nor[i] + x[2])
        
        h2 = activation(x[3] * X1Nor[i] + x[4] * X2Nor[i] + x[5])

        h3 = activation(x[6] * X1Nor[i] + x[7] * X2Nor[i] + x[8])

        h4 = activation(x[9] * X1Nor[i] + x[10] * X2Nor[i] + x[11])

        h5 = activation(x[12] * h1 + x[13] * h2 + x[14] * h3 + x[15] * h4 + x[16]) 

        h6 = activation(x[17] * h1 + x[18] * h2 + x[19] * h3 + x[20] * h4 + x[21])

        h7 = activation(x[22] * h1 + x[23] * h2 + x[24] * h3 + x[25] * h4 + x[26])

        h8 = activation(x[27] * h1 + x[28] * h2 + x[29] * h3 + x[30] * h4 + x[31])

        y = activation(x[32] * h5 + x[33] * h6 + x[34] * h7 + x[35] * h8 + x[37])
        print('Yp: ', y, 'Y: ', z[i])

    return

def XORCostFunction(x):
    # x =[w11, w12, b1, w21, w22, b2, w31, w32, b3]
    x1 = [0., 1., 0., 1.]
    x2 = [0., 0., 1., 1.]
    yd = [0., 1., 1., 0.]

    activation = sigmoid

    cost = 0
    for i in range(0, len(x1)):
        z1 = activation(x[0] * x1[i] + x[1] * x2[i] + x[2])
        z2 = activation(x[3] * x1[i] + x[4] * x2[i] + x[5])
        y  = activation(x[6] * z1    + x[7] * z2    + x[8])
        MSE = (yd[i] - y)**2
        cost = cost + MSE

    return cost

def XORPrediction(x):
    x1 = [0., 1., 0., 1.]
    x2 = [0., 0., 1., 1.]

    activation = sigmoid
    print('XOR Prediection')
    for i in range(0, len(x1)):
        z1 = activation(x[0] * x1[i] + x[1] * x2[i] + x[2])
        z2 = activation(x[3] * x1[i] + x[4] * x2[i] + x[5])
        y  = activation(x[6] * z1    + x[7] * z2    + x[8])
        print('x: ', [x1[i], x2[i]], 'y: ', y)

def DetermineMin():
    #X0 = [0.1, 0.2, -0.3, 0.4, 0.5, 0.6, 0.7, -0.8, \
    #      0.9, 0.5, -0.4, 0.1, 0.2, 0.5, -0.3, 0.8, \
    #      0.7]
    # X0 = np.random.randn(1,38) * np.sqrt(2/38)
    # X0 = X0.tolist()[0]
    
    # yp = y_predict.predict(np.array([1, 2]))
    # print(yp.shape)
    Optimizer = CGradDecent(MSE, X0, len(X0), Gradient='Backward', LineSearch='GSS', MinNorm=0.001, MaxIter=100)
    X = Optimizer.RunOptimize()
    # print('X0', X0)
    print('X ', X)
    PredictNN()
    # ChicagoNNPrediction(X)
    

if __name__ == "__main__":
    DetermineMin()