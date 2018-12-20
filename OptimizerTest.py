import math
from PyOptimizer import CGradDecent

def Test2VarFun1(x):
    return x[0] - x[1] + 2*(x[0]**2) + 2 * x[0] * x[1] + x[1]**2

def sigmoid(x):
    return 1./(1+math.exp(-x))

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

    # print('loss: ', cost)
    # print('Prediction')
    # print('X:', x)
    #XORPrediction(x)

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
    func = XORCostFunction
    X0 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    Optimizer = CGradDecent(func, X0, 9, Gradient='Backward', LineSearch='FiS')
    X = Optimizer.RunOptimize(learn_rate=1e-5)
    XORPrediction(X)
    

if __name__ == "__main__":
    DetermineMin()