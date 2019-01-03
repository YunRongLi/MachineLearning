import numpy as np
import math
import xlrd
from PyOptimizer import CGradDecent

Data_file = 'fire_theft.xls'
book = xlrd.open_workbook(Data_file, encoding_override='utf-8')
sheet = book.sheet_by_index(0)
data = np.asarray([sheet.row_values(i) for i in range(1, sheet.nrows)])

def BatchNormalize(x):
    avg = np.average(x)
    #print('Avg',avg)
    std = np.std(x)
    #print('std', std)

    X = []
    for i in range(len(x)):
        X.append((x[i] - avg) / std)

    return np.array(X)

X1 = data[:,0].reshape(42,1)
X1Nor = BatchNormalize(X1)
X2 = data[:,1].reshape(42,1)
X2Nor = BatchNormalize(X2)
z = np.linspace(1,42,num=42).reshape(42,1) / 42.

def Test2VarFun1(x):
    return x[0] - x[1] + 2*(x[0]**2) + 2 * x[0] * x[1] + x[1]**2

def sigmoid(x):
    return 1./(1 + math.exp(-x))

def Relu(x):
    return np.maximum(x,0)

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
    func = ChicagoNNModel
    #X0 = [0.1, 0.2, -0.3, 0.4, 0.5, 0.6, 0.7, -0.8, \
    #      0.9, 0.5, -0.4, 0.1, 0.2, 0.5, -0.3, 0.8, \
    #      0.7]

    X0 = np.random.randn(1,38) * np.sqrt(2/38)
    X0 = X0.tolist()[0]

    Optimizer = CGradDecent(func, X0, 38, Gradient='Forward', LineSearch='GSS', MinNorm=0.0001, MaxIter=1000)
    X = Optimizer.RunOptimize()
    print('X0', X0)
    print('X ', X)
    ChicagoNNPrediction(X)
    

if __name__ == "__main__":
    DetermineMin()